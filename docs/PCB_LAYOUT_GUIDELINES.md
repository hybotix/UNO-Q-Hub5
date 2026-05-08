# UNO Q HUB75 Project — PCB Layout Guidelines

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.2
**Date:** 2026-05-08

Guidelines for KiCad v9 PCB layout. Carrier is the priority — lay it out first.

---

## General Rules (both boards)

- 4-layer stackup: Top Cu / GND plane / Power plane / Bottom Cu
- Min trace: 0.15mm signal, 0.5mm power, 1.0mm high-current (VIN, +5V, HUB75_5V)
- Min via: 0.8mm diameter / 0.4mm drill standard; 0.4mm/0.2mm microvia for MIPI pairs (carrier)
- Min clearance: 0.2mm general; 0.15mm MIPI diff pairs
- Board outline: 0.05mm line on Edge.Cuts layer
- Silkscreen: reference designators on all SMD parts; value optional
- Courtyard: all components must have non-overlapping courtyards
- Mounting holes: M3, 3.2mm drill, copper-free keepout 1.5mm radius
- DRC must pass before Gerber export

---

## Shield — Form Factor

- **Size:** 68.6mm × 53.3mm (standard Arduino UNO shield)
- **Connectors facing outward:** UNO Q header rows on PCB edge
- **Top-side assembly only** (shield sits above UNO Q)
- Barrel jack J4: right or rear edge
- USB-C J5: rear or right edge (accessible when shield is mounted)
- HUB75 IDC J1: rear edge, centered
- Qwiic J8/J9: front-left corner
- Grove J10–J14: front edge, evenly spaced

### Shield Component Placement Priority

1. UNO Q headers — fixed by shield standard
2. ESP32-S3-MINI-1 (U1) — center-right, antenna toward board edge (no copper under antenna)
3. ES8388 (U5) — near U1 I2S pins, away from HUB75 switching noise
4. 74HCT245 U2/U3 — between U1 and J1 HUB75 connector
5. AMS1117 U4 — near barrel jack J4
6. Audio headers J6/J7 — near ES8388
7. USB-C J5 — board edge

---

## Carrier — Form Factor

- **Size:** TBD — minimum to fit all connectors; estimate 100mm × 80mm
- **UNO Q mounts on top** via B1 (JMISC) and B2 (JMEDIA)
- B1 and B2 placement must match UNO Q board connector positions exactly
  - Verify exact UNO Q JMISC/JMEDIA XY positions from Arduino documentation before layout
- **Bottom of carrier:** SMD components (ICs, passives)
- **Top of carrier:** Through-hole connectors, FPC connectors, UNO Q mounting connectors

### Carrier Component Placement Priority

1. **B1 (JMISC) and B2 (JMEDIA)** — FIRST. All other placement radiates from these.
2. **RPi 5 FPC connectors J1/J2/J3** — Must route cleanly from B2 JMEDIA MIPI lanes. Short, direct, impedance controlled.
3. **RPi 5 40-pin J4** — Adjacent to B1/B2, signals route from JMISC directly.
4. **TPS54331 (U7) buck converter** — Corner placement, away from MIPI/audio. L1 and D2 close to U7.
5. **ESP32-S3 (U1)** — Antenna toward board edge. I2S traces short to ES8388.
6. **ESP32-C6 (U6)** — Antenna toward board edge, opposite side or corner from S3. Short UART traces to S3.
7. **ES8388 (U5)** — Near S3 I2S pins. Audio output headers J11/J12 adjacent.
8. **74HCT245 U2/U3** — Between S3 and HUB75 connector J5.
9. **TXS0108E U8/U9** — Between B1 JMISC MPU GPIO pins and RPi 40-pin J4 / J24 MPU GPIO header.
10. **24C32 U10** — Near RPi 40-pin J4 pins 27/28.
11. **HUB75 J5** — Rear or side edge.
12. **Power connectors J6/J7/J8/J9** — Same edge, separated (5V panel vs VIN carrier).

---

## Critical Layout Rules by Signal Type

### HUB75 Signals
- 3.3V side: ESP32-S3 → 74HCT245 inputs. Keep traces short (<20mm).
- 5V side: 74HCT245 outputs → J1/J5 HUB75 IDC. Parallel traces, even length not required.
- DIR and ~OE pins on both 245s: tie to GND plane via 0Ω resistor or direct pour.
- 100nF bypass cap on each 245 VCC pin, as close as possible.

### I2S Audio (ES8388)
- BCLK, LRCLK, DOUT, DIN: keep traces <30mm, away from HUB75 switching signals.
- AVDD separate from DVDD on ES8388: use 10µF + 100nF on each, star ground at ES8388.
- Audio output traces (LOUT, ROUT) to DC-block caps to J6/J11 headers: short, no via if possible.
- Mic input traces short, away from switching regulators.
- I2C codec control (SDA/SCL): can share via with main I2C bus — 1kΩ pullups to 3V3 close to ES8388.

### SPI Bus (S3 and C6)
- MOSI/MISO/SCK: route as matched-length group on same layer.
- CS lines: individual traces direct to each chip. No length matching required.
- Termination not required at 80MHz or below on board-length traces.

### S3 ↔ C6 UART Link
- Short direct traces, max 50mm. No special impedance requirement.
- Route on inner layer if crossing under other components.

### MIPI Diff Pairs (Carrier only)
- **Impedance:** 100Ω differential (adjust trace width/spacing for stackup).
- **Length matching:** Within each lane ±0.5mm P-N skew; between lanes ±5mm.
- **Route on inner layer** where possible — avoid vias in diff pair runs.
- **No copper fill within 3× trace width of diff pair** on adjacent layers.
- **Ref to ground plane** — never route over power plane splits.
- Separate FPC connectors J1/J2/J3 with 3mm minimum between them.

### 1.8V MPU GPIO (Carrier only)
- TXS0108E A-side (1.8V): connect to B1 JMISC MPU GPIO directly, <10mm traces.
- TXS0108E B-side (3.3V): to RPi 40-pin J4 and J24 breakout header.
- OE pin: tie to 3V3 via 10kΩ pullup.
- 100nF bypass on each VCCA and VCCB.
- Silkscreen warning on J24: "⚠️ 1.8V — Do not apply 3.3V or 5V"

### Buck Converter TPS54331 (Carrier only)
- VIN input: two 100µF bulk caps close to pin 1, short traces.
- PH node (switching node): minimize copper area to reduce EMI. L1 close to PH pin.
- D2 (SS34): anode to GND, cathode to PH — within 5mm of PH pin.
- Output caps (100µF): close to output rail, before L1.
- PGND and AGND: star ground at IC, single via to GND plane.
- Keep switching node away from MIPI traces and audio.
- Thermal via array under exposed pad if IC has one.

### Power Distribution
- +5V rail (from TPS54331): 1.0mm trace minimum, polygon pour preferred.
- +3V3 rail (from AMS1117): 0.5mm trace minimum.
- VIN: 1.0mm+ trace from barrel jack/screw terminal to TPS54331 VIN.
- HUB75 5V: dedicated path from J6/J7 to J5 IDC pin 4/8/14/18 (all GND pins) and power pins. Separate from logic ground.
- GND plane: Layer 2 (continuous). No splits except under HUB75 5V section.

---

## Mounting Holes

| Board | Qty | Diameter | Notes |
|---|---|---|---|
| Shield | 4 | M3 (3.2mm) | Match UNO shield standard positions |
| Carrier | 4+ | M3 (3.2mm) | At corners; align with UNO Q board holes |

---

## Fabrication Targets

| Spec | Shield | Carrier |
|---|---|---|
| Layers | 4 | 4 |
| Min trace/space | 0.15/0.15mm | 0.15/0.15mm |
| Min drill | 0.3mm | 0.2mm (microvia) |
| Surface finish | HASL or ENIG | ENIG (required for FPC connectors) |
| Solder mask | Both sides | Both sides |
| Silkscreen | Top | Top + Bottom |
| Board thickness | 1.6mm | 1.6mm |

**ENIG is required on the carrier** for reliable soldering of the 0.5mm FPC connectors and Samtec 1.27mm pitch connectors.

---

## Gerber Export Checklist

- [ ] Edge.Cuts (board outline)
- [ ] F.Cu, In1.Cu (GND), In2.Cu (Power), B.Cu
- [ ] F.Mask, B.Mask
- [ ] F.Silkscreen, B.Silkscreen
- [ ] F.Courtyard, B.Courtyard (for review, not sent to fab)
- [ ] Drill file (excellon, separate PTH/NPTH)
- [ ] BOM + CPL for SMD assembly

---

## Revision History

| Rev | Date | Notes |
|---|---|---|
| 0.1 | 2026-05-08 | Initial layout guidelines |
| 0.2 | 2026-05-08 | Final approved. Added MIPI impedance notes, TPS54331 switching node rules, ES8388 AVDD/DVDD star ground, S3↔C6 UART routing. |
