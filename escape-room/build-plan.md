# Build plan

Eight milestones from bench prototype to sealed case. Each one ends in
something testable so you can stop and pick up later without holding
state in your head.

## M1 — Inventory and finalize BOM

- [ ] Tick the `Have?` column in `bom.md`
- [ ] Decide servo vs solenoid
- [ ] Decide banana jacks vs PCB-header patch panel
- [ ] Order the missing parts in one batch

**Done when**: the only blockers are shipping times.

## M2 — Controller + display + keypad on the bench

- [ ] ESP32 boots, prints to serial
- [ ] LCD over I2C scans and shows `HELLO NIGHTJAR`
- [ ] 4×4 keypad reads to serial
- [ ] Buzzer chirps on keypress

**Done when**: you can type into the keypad and see characters on the
LCD with a confirmation beep.

## M3 — NFC reader proof of life

- [ ] PN532 detected on I2C scan
- [ ] Read NDEF text record from an NTAG215 sticker
- [ ] Write a known callsign to a fresh tag (for the embedded badge)
- [ ] Demonstrate phone-side read (Android: NFC Tools; iOS: Shortcuts
      or built-in tag reader)

**Done when**: a sticker programmed by the case is readable by both
phones, and the case can re-read it.

## M4 — BLE advertising

- [ ] ESP32 starts BLE with a custom name including a code
- [ ] Code rotates every 30 s with a Caesar shift driven by a counter
- [ ] 7-seg shows the current shift
- [ ] Verified visible in nRF Connect and in iOS/Android BT settings

**Done when**: phone-side scan shows the rotating name.

## M5 — Analog puzzles (pots + buzzer beat)

- [ ] Pots read steadily on ADC, smoothed
- [ ] Two oscillators in firmware mix to the buzzer
- [ ] Zero-beat condition detected within ±2 Hz
- [ ] LCD shows a level/tuning meter

**Done when**: turning the pots produces an audible warble that
disappears at the target and the firmware fires a "TUNED" event.

## M6 — Patch panel

- [ ] Six jacks wired through dividers to ADC inputs
- [ ] Firmware identifies which plug is in which jack from ADC value
- [ ] LCD shows current routing and required routing
- [ ] Wrong wiring buzzes, correct wiring chimes

**Done when**: you can wire the panel and the case knows what you did.

## M7 — Glue it all into the state machine

- [ ] All five gameplay stages registered and gateable
- [ ] `stages_solved` bitmask persisted to NVS
- [ ] Hint system on long-press `*` (3 levels per stage)
- [ ] Master-code computation pulls from per-stage outputs
- [ ] Big red switch + LAUNCH button drive the servo
- [ ] Full no-skip dry run in front of one volunteer

**Done when**: a friend who *doesn't* know the design can solve it
with a phone in hand.

## M8 — Move from breadboard to case

- [ ] Lay out the front panel on paper, then in CAD
- [ ] Cut/drill the panel (acrylic for prototyping is forgiving)
- [ ] Solder modules to perfboard or a small custom PCB
- [ ] Mount servo and verify it can actually pop the lid under load
- [ ] Cable management; nothing that can rattle loose
- [ ] Power-on smoke test, then a sealed-case dry run

**Done when**: the lid is closed, only the front panel is visible,
and it still solves cleanly.

## Stretch goals (post-v1)

- Battery + USB-C charging
- Web dashboard for the host (over WiFi, hidden SSID) showing stage
  state and elapsed time
- Multi-session leaderboard stored in flash
- Per-session randomization of codes so the same friend can't replay
  from memory
