# UNO Q HUB75 Project — Design Standards Reference

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.2
**Date:** 2026-05-08

This document defines the applicable design standards and their specific
requirements for this project. All schematics and PCB layouts must comply.

---

## Applicable Standards

| Standard | Scope | Application |
|---|---|---|
| IEEE 315 / ANSI Y32.2 | Schematic symbols and drawing conventions | All schematics |
| IPC-2221B | Generic PCB design (geometry, clearances, materials) | PCB layout |
| IPC-2152 | Current-carrying capacity (supersedes IPC-2221B Appendix B charts) | Trace sizing |
| IPC-7351C | Land pattern (footprint) dimensions and tolerances | All footprints |
| IPC-A-600 | Acceptability of printed boards | Fabrication inspection |
| IPC-J-STD-001 | Soldering requirements | Assembly |

---

## IEEE 315 — Schematic Conventions

### Signal Flow
- Left-to-right signal flow on every sheet
- Inputs on the left side of component symbols
- Outputs on the right side of component symbols
- Power pins at the top of symbols
- Ground pins at the bottom of symbols

### Power and Ground
- Dedicated power symbols: `+5V_EXT`, `+5V_EXT_HUB75`, `+3V3`
- Dedicated ground symbols: `DGND` (digital ground), `AGND` (analog ground)
- `PWR_FLAG` placed on every power and ground net — required for ERC pass
- Power flows downward on the sheet; return (ground) at sheet bottom

### Hierarchical Sheets
- Each functional block is a separate sheet
- Hierarchical pins typed correctly: `power_in`, `power_out`, `input`, `output`, `bidirectional`
- Sheet borders color-coded by function:
  - Yellow: Power distribution
  - Blue: Processing (ESP32-S3, ESP32-C6)
  - Orange: HUB75 driver
  - Purple: Audio
  - Green: Interface/headers
  - Pink: Connectivity (Qwiic/Grove)

### Symbols
- All component symbols use IEC-style rectangular body
- Pin names on inside of symbol body
- Pin numbers per component datasheet
- No-connect markers `X` on all unused pins
- Reference designators follow standard scheme:
  - U = IC
  - R = Resistor
  - C = Capacitor
  - L = Inductor
  - FB = Ferrite bead
  - D = Diode/LED
  - J = Connector
  - B = Board-to-board connector
  - NT = Net tie
  - #PWR = Power symbol (hidden)

### Component Properties (required on every component)
- `Reference` — unique designator
- `Value` — part value or MPN
- `Footprint` — full KiCad library path
- `Datasheet` — URL or filename
- `MPN` — manufacturer part number (for BOM)

---

## IPC-2221B — PCB Design

### Layer Stackup (4-layer)
| Layer | Name | Function |
|---|---|---|
| 1 | F.Cu | Signal, component side |
| 2 | In1.Cu | GND plane (solid, unbroken) |
| 3 | In2.Cu | Power plane (split by voltage domain) |
| 4 | B.Cu | Signal, secondary |

**GND plane (Layer 2) rules:**
- Solid copper, no routing through it
- No anti-pads except required clearances
- Via stitching every 5mm along power domain boundaries
- Splits only to accommodate keepouts under RF antenna areas

**Power plane (Layer 3) splits:**
- `+3V3` domain: Logic section
- `+5V_EXT_HUB75` domain: HUB75 level shifter section
- `AGND` domain: ES8388 analog audio section (separate pour on Layer 2 also)
- Physical moat (gap) between domains: 0.5mm minimum
- No signal traces cross a power domain moat

### Clearances
| Net Class | Trace-to-Trace | Trace-to-Plane | Trace-to-Edge |
|---|---|---|---|
| Signal (default) | 0.20mm | 0.20mm | 0.30mm |
| Power (+5V, +3V3) | 0.30mm | 0.25mm | 0.50mm |
| HV/High current | 0.50mm | 0.40mm | 0.75mm |
| MIPI diff (carrier) | 0.15mm | 0.15mm | 0.30mm |

### Via Rules
| Via Type | Drill | Annular Ring | Total Diameter |
|---|---|---|---|
| Standard signal | 0.4mm | 0.2mm | 0.8mm |
| Power/GND stitching | 0.6mm | 0.2mm | 1.0mm |
| Thermal relief (TQFP, SOT-223) | 0.4mm | 0.15mm | 0.7mm |
| Microvia (MIPI only, carrier) | 0.1mm | 0.15mm | 0.4mm |

### Mounting Holes
- M3 drill: 3.2mm
- Copper-free keepout: 1.5mm radius from hole edge
- Non-plated through-hole (NPTH): use for mechanical mounting

### Thermal Management
- AMS1117-3.3 (SOT-223): Tab pin tied to `+3V3` plane via 4 thermal vias
- TPS54331 (SOIC-8, carrier): No exposed pad — ensure SOT-223 tab rule does not apply
- 74HCT245 (TSSOP-20): Standard thermal relief on GND pin; no special handling required
- ES8388 (LQFP-48): Exposed pad (if present) to AGND star point

---

## IPC-2152 — Current-Carrying Capacity

These trace widths are calculated for **1oz copper (35µm), outer layer, 10°C temperature rise** above ambient.
For inner layers, derate by approximately 50% (use wider traces or copper pours).

| Net | Max Current | Min Trace Width (outer) | Min Trace Width (inner) | Preferred |
|---|---|---|---|---|
| VIN input (carrier only) | 3A | 1.5mm | 3.0mm | Polygon pour |
| +5V_EXT to LDO | 1A | 0.8mm | 1.6mm | 1.0mm trace |
| +5V_EXT_HUB75 to J1/J5 | 5A (panel) | 2.5mm | 5.0mm | Polygon pour, both layers |
| +3V3 rail | 500mA | 0.5mm | 1.0mm | Polygon pour on power plane |
| ESP32-S3 VCC | 500mA | 0.5mm | — | 0.5mm direct from LDO |
| ES8388 AVDD | 50mA | 0.25mm | — | 0.3mm after ferrite bead |
| Signal traces (SPI, I2S, GPIO) | 50mA | 0.2mm | — | 0.2mm standard |
| MIPI diff pairs (carrier) | 10mA | 0.15mm | — | 0.15mm matched pair |

**HUB75 panel power (5A sustained):**
The HUB75 +5V rail for panel power is the highest-current net on the board.
Use copper pour fills on both F.Cu and B.Cu, stitched with 1.0mm vias every 3mm.
This net must NOT pass through the AMS1117-3.3 — it routes directly from J4/J6 barrel jack to J1/J5 IDC.

---

## IPC-7351C — Footprint Standards

### Density Level
Use **Level B (Nominal/Median)** for all components. This is the standard
for general-purpose boards with typical assembly equipment.

### Critical Footprints

**ESP32-S3-MINI-1 / ESP32-C6-MINI-1:**
- Use Espressif reference footprint
- No solder mask over castellated edges
- Courtyard: module dimensions + 0.5mm keepout on all sides
- Antenna keepout: no copper, no pour, no vias within 3.14mm of antenna edge

**Samtec FTSH-130-01 (carrier only):**
- 1.27mm pitch, 2×30, SMD
- Use Samtec land pattern drawing
- Solder paste: 80% stencil aperture coverage
- ENIG surface finish required

**Molex 0545821522 FPC (carrier only):**
- 0.5mm pitch, 22-pin, bottom-contact
- Staggered pads per Molex drawing
- Stencil: 0.12mm aperture reduction per pad
- ENIG surface finish required

**ES8388 LQFP-48:**
- IPC-7351C SM-R nominal land pattern
- Paste mask: 80% aperture
- Exposed thermal pad to AGND pour if present in package

**SN74HCT245PW TSSOP-20:**
- IPC-7351C level B land pattern
- 0.65mm pitch

**AMS1117-3.3 SOT-223-3:**
- Tab pin (pin 2) is both GND and thermal path — connect to +3V3 plane
- 4 thermal vias under tab: 0.4mm drill, 0.7mm pad

**JST SH 1.0mm Qwiic:**
- Use JST official footprint
- Horizontal SMD mount
- Mechanical tab included in footprint

---

## Ground Design — AGND / DGND Rules

This is the most critical aspect of the audio power design.

### Star Ground Topology
```
                    ┌─────────────────────────────┐
                    │         GND PLANE (L2)       │
                    │         (digital ground)     │
                    │                              │
  U2 74HCT245 ──────┤                              │
  U3 74HCT245 ──────┤                              │
  U1 ESP32-S3 ──────┤                              │
  U4 AMS1117  ──────┤                              │
  J1 HUB75 GND ─────┤                              │
                    │         STAR POINT           │
                    │         (at U5 ES8388)       │────── AGND pour (under U5 only)
                    └─────────────────────────────┘
                                                       │
                                                   U5 ES8388
                                                   AGND pins
                                                   AVDD bypass
                                                   Audio outputs
```

### Rules
1. DGND (GND plane Layer 2): solid copper, connects all digital components
2. AGND (separate pour on Layer 2): exists only under and around U5 ES8388
3. Single connection point between AGND and DGND: one via or trace at U5's DGND/AGND pin boundary
4. No digital signal traces may route over the AGND pour region
5. FB1 ferrite bead: filters +3V3 to create AVDD — physically within 5mm of U5
6. Audio output traces (LOUT, ROUT) run over AGND pour only
7. I2C codec control traces (shared with digital domain) cross AGND boundary only at the star point

### PCB Implementation
- Define AGND as a named net in KiCad
- Create copper pour zone for AGND on Layer 2, restricted to ES8388 area
- Set zone fill priority: DGND plane fills first, AGND zone fills second
- KiCad net tie footprint (NT1) bridges AGND to DGND at single pad

---

## Return Current Path Requirements (IPC-2221B §6.2.3)

Every high-frequency signal trace must have an unbroken return current path
directly beneath it on the adjacent ground plane.

### Critical Signals and Their Return Paths

| Signal | Frequency | Required Return Path |
|---|---|---|
| HUB75 CLK (S3_HUB75_CLK) | Up to 40MHz | Continuous GND plane under entire CLK trace route |
| SPI SCK | Up to 80MHz | Continuous GND plane under MOSI/MISO/SCK traces |
| I2S BCLK | Up to 6.4MHz | Continuous GND plane or AGND pour under I2S traces |
| HUB75 RGB data | Up to 20MHz | Continuous GND plane under U2/U3 output traces to J1 |
| MIPI diff pairs (carrier) | 1–4GHz | Must stay on same layer; no layer changes; GND plane immediately adjacent |

### Via Placement Rules
- Via stitching row along +5V_EXT / +3V3 boundary: 1.0mm vias every 5mm
- Via stitching row along AGND / DGND boundary: 0.8mm vias every 3mm
- Via stitching at HUB75 connector GND pins: 0.8mm via immediately at each GND pin (4, 8, 14, 16)
- No via in the signal path between U2/U3 and J1 (keep HUB75 signals on single layer)

---

## Revision History

| Rev | Date | Notes |
|---|---|---|
| 0.1 | 2026-05-08 | Initial |
| 0.2 | 2026-05-08 | Full standards compliance doc. IPC-2152 trace tables. AGND/DGND star topology diagram. Return current path requirements. IPC-7351C footprint specs. |
