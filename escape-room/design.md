# Design

## 1. Hardware architecture

### Main controller

**ESP32 DevKit-C** (or any ESP32 board). Reasons:

- Native BLE (classic and BLE 4.x advertising + GATT)
- Plenty of GPIO, two ADCs, hardware I2C
- Arduino-IDE friendly so prototyping is fast
- Cheap enough to keep a spare on the bench

NFC handled by a **PN532** module on I2C (set DIP switches to I2C mode).
It reads/writes NDEF tags and can emulate a tag, so both directions of
NFC interaction are covered with one part.

### Peripheral map

| Function           | Part                              | Bus / pins                    |
|--------------------|-----------------------------------|-------------------------------|
| LCD                | 20×4 char LCD with PCF8574 I2C    | I2C @ 0x27 (or 0x3F)          |
| NFC reader/writer  | PN532                             | I2C @ 0x24, IRQ on GPIO 4     |
| GPIO expander      | MCP23017 (for button array)       | I2C @ 0x20, INT on GPIO 5     |
| 7-seg display      | TM1637 4-digit                    | CLK GPIO 18, DIO GPIO 19      |
| RGB / status LEDs  | 74HC595 shift register            | DATA 23, CLK 22-ish, LATCH 21 |
| Keypad             | 4×4 matrix                        | direct GPIO (8 pins) or PCF8574 |
| Rotary encoder     | EC11 with push                    | GPIO 32, 33; button GPIO 25   |
| Potentiometers     | 2× 10 kΩ linear                   | ADC1_CH0 (36), ADC1_CH3 (39)  |
| Big red flip switch| Toggle SPDT with safety cover     | GPIO 13                       |
| Buzzer             | Passive piezo                     | GPIO 16 (LEDC PWM)            |
| Servo lock         | SG90 9 g servo                    | GPIO 27 (LEDC PWM, 50 Hz)     |
| Patch panel        | 6× banana jack pairs + ID resistors| ADC2 channels (see below)    |

> The I2C addresses above don't collide. If you swap the LCD backpack
> and it lands on 0x20 too, change the MCP23017 address by jumpering A0.

### Patch panel — quick design note

Banana jacks are tempting but fragile. Cheaper option: six 4 mm test
points in two rows of three, with **identifier resistors** baked into
each plug end (different value per plug, e.g. 1 kΩ, 2.2 kΩ, 4.7 kΩ,
10 kΩ, 22 kΩ, 47 kΩ). The firmware reads each input through a
fixed-value pull-up divider and identifies *which* plug landed *where*
by the divider ratio. That lets you score the wiring puzzle in
software with no per-plug switches.

### Power

5 V wall adapter → buck/boost to 5 V rail for servo, LCD backlight,
TM1637. ESP32 fed via its 5 V → AMS1117 onboard. **Decouple the servo
rail** with a 470 µF cap close to the SG90; the inrush spikes will
brown the ESP out otherwise.

Optional: 18650 + TP4056 + protection if you want it battery-powered
during the game. Not required for v1.

## 2. Puzzle stages

Six stages, designed so the **output of each is one or more digits of
the final unlock code**. Stages 1–5 can be largely independent so the
player can attack them in any order once they realize that; stage 6 is
gated on everything else.

### Stage 1 — Authenticate (NFC handshake)

- LCD: `AUTHENTICATE / SCAN BADGE`
- Behind the front panel, an NFC sticker is embedded under a marked
  spot. It carries an NDEF URL or text record with a 4-character
  callsign (e.g. `NJ-7B`).
- The case's PN532 is also live. The player must read the badge with
  their phone, *then* present their phone to the case's NFC area. The
  PN532 in target mode reads the NDEF record the phone shares back —
  or, simpler v1: phone reads the embedded tag, gets the callsign,
  player keys it into the keypad.
- **Yields**: digit 1 of the master code (mapped from callsign).

> Cross-platform note: iPhones read NDEF since iOS 14; Android reads
> and writes. Sticking to read-only on the phone side keeps both
> platforms working.

### Stage 2 — Tune the carrier (zero-beat with pots + buzzer)

- Buzzer plays a fixed reference tone (say 880 Hz).
- Two pots control two oscillators in firmware whose sum is also
  emitted on the buzzer. Player turns the pots until the beat
  frequency goes to zero (the ear hears the warble slow and stop).
- LCD shows a level meter so they know they're close.
- **Yields**: digit 2. The exact pot positions at zero-beat encode it
  (e.g. higher pot value mod 10).

This is the "scope replacement" — uses ears instead of eyes, so no
test equipment needed.

### Stage 3 — Patch the signal path (jumper panel)

- LCD shows a routing requirement, e.g. `A→3, B→1, C→6`.
- Player wires the six numbered jacks into the three labeled inputs
  using the identifier-resistor plugs. Firmware reads ADC values to
  determine which plug is in which jack.
- **Yields**: digit 3.

### Stage 4 — Decommissioned beacon (BLE scan)

- ESP32 starts BLE advertising with name `NJ-BEACON-XXXX` where `XXXX`
  is the current 4-hex code. The advertisement also carries
  manufacturer-data with extra bytes that hint at the format.
- Player uses **any** BLE scanner app (nRF Connect, LightBlue, even
  iOS/Android Bluetooth settings — the device name is visible).
- To raise the difficulty: rotate the code through a Caesar shift
  every 30 s, with the shift driven by a value visible on the 7-seg
  display. Player must invert the shift mentally.
- **Yields**: digit 4.

### Stage 5 — The combination (button array + Simon-ish)

- A 3×3 array of momentary buttons with LEDs behind each.
- LCD shows a sequence requirement derived from clues found in
  earlier stages (e.g. "Press in the order of the resistor colors
  from stage 3").
- Wrong sequence → buzzer raspberry, restart. Three failures locks
  the stage for 30 s (anti-brute-force).
- **Yields**: digits 5 and 6.

### Stage 6 — Arm and launch

- LCD: `ENTER MASTER CODE`. Player keys the 6-digit code on the
  keypad.
- Correct code: LCD says `ARM`. Player lifts the safety cover and
  flips the big red switch. LCD counts down 5 → 0. Player must press
  a "LAUNCH" button at exactly zero (±200 ms window).
- Servo retracts the latch. Lid pops. 7-seg shows total elapsed time.
  Buzzer plays a fanfare. LEDs do a victory chase.

If they flip the red switch *before* the code is right: buzzer
alarm, LCD `INTRUSION DETECTED`, 10 s cooldown. Adds tension.

## 3. State machine

```
BOOT  ─►  IDLE  ─►  STAGE_1  ─►  STAGE_2  ─►  STAGE_3
                          │         │           │
                          └─────────┴───────────┴───►  ARM_READY  ─►  LAUNCH  ─►  WIN
                                                          ▲                       │
                                                          │                       │
                                                       STAGE_4, STAGE_5 ──────────┘
```

Stages 1–5 set bits in a `stages_solved` bitmask. `ARM_READY` is
entered when the bitmask is full. `LAUNCH` requires the correct
sequence in stage 6.

States also have side-effects:

- `BOOT`: self-test (LCD test pattern, LED chase, buzzer chirp, NFC
  presence check, servo seat-to-locked). Useful for debugging on the
  bench.
- `IDLE`: shows narrative intro on LCD, slow pulse on status LED.
  First keypad press → `STAGE_1`.
- `FAIL_LOCKOUT`: optional, after N wrong master-code attempts.

## 4. Master code derivation

| Stage | Output                            | Digit slot |
|-------|-----------------------------------|------------|
| 1     | NFC callsign → digit              | 1          |
| 2     | Zero-beat pot position → digit    | 2          |
| 3     | Patch-panel correct → digit       | 3          |
| 4     | BLE-revealed value → digit        | 4          |
| 5     | Simon sequence → 2 digits         | 5, 6       |

Keep the mapping in firmware in one constants table so you can rotate
codes between play sessions without rebuilding the puzzles.

## 5. Hint system

Long-press `*` on the keypad → LCD shows a stage-appropriate hint
from a table. Three levels per stage:

- Level 1: gentle nudge ("listen, don't look")
- Level 2: technique hint ("zero-beat is a thing")
- Level 3: near-spoiler ("turn the left pot down until the warble
  stops")

Hint level resets per session. Optional: log hint usage to flash for
post-game gloating.

## 6. Failure modes you'll want to guard against

- **Player powers it off mid-game** — persist `stages_solved` to NVS
  every state change so a power blip doesn't reset progress.
- **Servo brown-out on first boot** — drive servo only after a 200 ms
  delay post-boot, use a separate 5 V rail with bulk cap.
- **NFC field interferes with the LCD** — keep the PN532 antenna at
  least 30 mm from the LCD module; both run at ~13 MHz harmonics-ish.
- **Friend reverse-engineers the firmware** — don't put the master
  code in a string literal. Compute it from the stage outputs every
  boot, or store it XORed with the chip ID.
