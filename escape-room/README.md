# Project NIGHTJAR

A 5–6 stage electronic puzzle box for geek friends. Mid-to-high difficulty,
target solve time 45–60 minutes, solvable with only the case and a phone
(no oscilloscope or multimeter required from the player).

## Constraints

- **Solver tools**: case + phone only. NFC and BLE are the only "external"
  channels and both are native on modern Android/iPhone.
- **Builder tools**: lab supply, scope, soldering station, ESP/Arduino
  toolchain.
- **Difficulty**: mid-to-high. Hint button on the case (long-press) is
  acceptable; printed hint envelopes (open if stuck) are nicer.

## Narrative (working draft)

> "PROJECT NIGHTJAR — black-budget signal-intelligence prototype recovered
> from a dead drop. Power is intact. The original handler is gone. The
> contents of the box are yours if you can authenticate to it as he did."

Generic enough to fit whatever ends up inside (whisky, dice, USB drive,
party-favor). Replace the theme if you have something better.

## Recommended case

Aluminum briefcase or ammo can, roughly A4 footprint, 60–100 mm deep,
single hinged lid. One front panel holds every input/output. The lid is
held by a 9 g servo or 12 V solenoid latch; the final puzzle drives it.

Why not multi-compartment: each extra drawer is a mechanical project of
its own (latch, alignment, hinge) for marginal puzzle gain. A single
satisfying *clack* at the end is the better payoff.

## Repo layout

- `design.md` — hardware architecture, pin map, puzzle stages, state
  machine, code-derivation table
- `bom.md` — parts list and what's already on hand
- `build-plan.md` — milestone checklist from bench prototype to sealed
  case
- `firmware/` — ESP32 sketch (PlatformIO or Arduino IDE; empty for now)

## Status

Design phase. Nothing built yet.
