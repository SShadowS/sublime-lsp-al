# Bill of materials

Mark the `Have?` column as you inventory what's already in your parts
bins. Quantities are minimums; double small consumables (LEDs,
resistors) so a blown part doesn't stall the build.

## Controller and comms

| # | Part                              | Qty | Have? | Notes |
|---|-----------------------------------|-----|-------|-------|
| 1 | ESP32 DevKit-C (30-pin)           |  1  |       | Spare strongly recommended. |
| 2 | PN532 NFC module                  |  1  |       | Set DIP switches to **I2C** mode. |
| 3 | NTAG215 stickers / cards          |  3  |       | One for the embedded badge, two spares. |
| 4 | MCP23017 GPIO expander            |  1  |       | DIP or SOIC + breakout. Optional if you wire keypad directly. |

## Display and feedback

| # | Part                              | Qty | Have? | Notes |
|---|-----------------------------------|-----|-------|-------|
| 5 | 20×4 character LCD with I2C bp.   |  1  |       | 16×2 works but 20×4 reads better. |
| 6 | TM1637 4-digit 7-segment          |  1  |       | Big red one is dramatic. |
| 7 | 74HC595 shift register            |  1  |       | For LED bar. Skip if driving LEDs from MCP23017. |
| 8 | 5 mm LEDs assorted                | 12  |       | At least one red, one green; rest decorative. |
| 9 | Passive piezo buzzer              |  1  |       | Passive = you control frequency via PWM. |

## Inputs

| #  | Part                             | Qty | Have? | Notes |
|----|----------------------------------|-----|-------|-------|
| 10 | 4×4 matrix keypad                |  1  |       | Membrane or PCB. PCB feels nicer. |
| 11 | EC11 rotary encoder w/ button    |  1  |       | Knurled knob looks the part. |
| 12 | 10 kΩ linear potentiometer       |  2  |       | Panel-mount with knobs. |
| 13 | 12 mm momentary push buttons     |  9  |       | For the Simon-ish button array. |
| 14 | Big red SPST toggle + safety cover|  1 |       | The "jet missile" switch. Source: aliexpress "missile switch", ~€3. |
| 15 | 1 × LAUNCH button (illuminated)  |  1  |       | Arcade-style, 24 mm. |

## Patch panel

| #  | Part                             | Qty | Have? | Notes |
|----|----------------------------------|-----|-------|-------|
| 16 | 4 mm panel jacks                 |  9  |       | Or PCB headers + custom plugs. |
| 17 | ID resistors (1k/2k2/4k7/10k/22k/47k)| 6 |       | One per plug end. 1 % preferred. |
| 18 | Short patch cables               |  6  |       | Banana-banana or matching to your jack choice. |

## Mechanical / lock

| #  | Part                             | Qty | Have? | Notes |
|----|----------------------------------|-----|-------|-------|
| 19 | SG90 9 g servo                   |  1  |       | Or MG90S metal-gear for durability. |
| 20 | 12 V solenoid latch (alternative)|  1  |       | If you prefer solenoid; needs a MOSFET driver and 12 V rail. |
| 21 | Latch mechanism / catch          |  1  |       | 3D print or repurpose a cabinet latch. |

## Power

| #  | Part                             | Qty | Have? | Notes |
|----|----------------------------------|-----|-------|-------|
| 22 | 5 V 2 A wall adapter w/ DC jack  |  1  |       | Servo + LCD backlight = surprisingly hungry. |
| 23 | Panel-mount DC jack              |  1  |       | 5.5 × 2.1 mm. |
| 24 | 470 µF electrolytic              |  2  |       | Bulk cap for servo rail. |
| 25 | 100 nF ceramic                   | 10  |       | Decoupling on every IC. |

## Case and assembly

| #  | Part                             | Qty | Have? | Notes |
|----|----------------------------------|-----|-------|-------|
| 26 | Aluminum briefcase / ammo can    |  1  |       | A4 footprint, ~80 mm deep. |
| 27 | 3 mm acrylic for front panel     |  1  |       | Laser-cut or hand-drilled. |
| 28 | M3 standoffs + screws assortment |  1  |       | For mounting the ESP and modules. |
| 29 | Dupont and silicone wire         |     |       | Already in your bench, presumably. |
| 30 | Heat-shrink, kapton, double-sided foam| | |       | The usual. |

## What you almost certainly already have

Resistors (220 Ω, 1 k, 10 k pull-ups), breadboard, jumper wires, USB
cable, common 5 mm LEDs. Skip purchasing these — pull from the parts
bin.

## Open shopping decisions

- **Servo vs solenoid**: servo is simpler (one PWM line, no flyback
  diode, runs from 5 V). Solenoid is more dramatic (loud *clack*) but
  needs 12 V and a MOSFET. Pick after you've handled the case.
- **Banana jacks vs PCB headers** for the patch panel: banana jacks
  feel right but are €1–2 each × 6 = budget-relevant. Headers + a
  custom plug strip is half the price and lets the resistor IDs be
  hidden inside the plug.
