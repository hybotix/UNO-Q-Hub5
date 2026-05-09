# UNO Q HUB75 Shield — PCB Layout Documentation

**Hybrid RobotiX** — Dale Weber  
**Revision:** 1.0  
**Date:** 2026-05-08  
**Tool:** KiCad 10  
**Standards:** IPC-2221B, IPC-2152, IPC-7351C Level B, IEEE 315  

This document provides complete layout intent for the UNO Q HUB75 Shield. A PCB layout
contractor or the KiCad operator should be able to produce a DRC-clean, PCBWay-ready
layout from this document alone, without needing to interpret the schematics.

---

## 1. Board Specification

| Parameter | Value |
|-----------|-------|
| Form factor | Arduino UNO shield |
| Board outline | 68.58 × 53.34mm (2.70 × 2.10 inches) |
| Board origin | Lower-left corner of outline at (0, 0) |
| Layer stackup | 4-layer |
| Board thickness | 1.6mm |
| Copper weight outer | 1oz (35µm) |
| Copper weight inner | 0.5oz (17.5µm) |
| Min trace width | 0.15mm signal, 0.50mm power, 1.50mm high-current |
| Min clearance | 0.20mm general, 0.15mm differential pairs |
| Min drill (PTH) | 0.30mm |
| Min drill (NPTH) | 0.80mm (mounting holes: 3.20mm) |
| Min annular ring | 0.15mm |
| Via standard | 0.80mm pad / 0.40mm drill |
| Via thermal relief | Spokes on power planes, solid on GND plane |
| Surface finish | ENIG (electroless nickel / immersion gold) |
| Solder mask | Green LPI, both sides |
| Silkscreen | White, both sides |
| Controlled impedance | No (no differential pairs on shield) |
| Assembly side | Top only |

---

## 2. Layer Stack

| Layer | KiCad Name | Function |
|-------|-----------|----------|
| 1 | F.Cu | Signal + power routing, SMD pads |
| 2 | In1.Cu | GND plane — unbroken except under ESP32-S3 antenna |
| 3 | In2.Cu | Power plane — +3V3 pour, +5V_EXT_HUB75 pour, split |
| 4 | B.Cu | Signal + miscellaneous routing |

### Layer assignment rules

- **All SMD component pads:** F.Cu only (top-side assembly)
- **GND plane (In1.Cu):** Solid pour, no splits. Single exception: keepout under
  ESP32-S3-WROOM-1 antenna region (see §5.1). Stitching vias every 5mm around
  the board perimeter, every 8mm across the interior.
- **Power plane (In2.Cu):** Split into two zones:
  - +3V3 zone: covers ~65% of board (logic area)
  - +5V_EXT_HUB75 zone: covers HUB75 driver region (U2, U3, J1 area)
  - The two zones must be separated by a minimum 0.50mm split gap.
  - +5V_EXT main rail (from J4 to C1) routes on F.Cu as a 1.5mm trace — does not
    need a power plane zone since it feeds only the LDO and HUB75.
- **Signal routing preference:** F.Cu first. Use B.Cu for jumpers and traces that
  cannot route on F.Cu without crossing. Minimize layer changes.
- **Never route signals on In1.Cu or In2.Cu.** These are plane layers only.

---

## 3. Board Outline and Mechanical

### 3.1 Arduino UNO Shield Outline

The UNO shield outline is NOT a simple rectangle. It has a notch cut from the
upper-right corner to clear the USB-A port on the UNO Q board below.

**Outline coordinates (mm, origin at lower-left):**

```
(0, 0) → (68.58, 0)           bottom edge
(68.58, 0) → (68.58, 35.56)   right edge lower
(68.58, 35.56) → (64.52, 35.56) USB notch bottom
(64.52, 35.56) → (64.52, 53.34) USB notch right
(64.52, 53.34) → (0, 53.34)   top edge
(0, 53.34) → (0, 0)           left edge
```

The 4.06mm wide × 17.78mm tall notch at upper-right clears the UNO Q USB port.
All edges on Edge.Cuts layer, 0.05mm line width.

### 3.2 UNO Q Header Positions (fixed — do not move)

These are the standard Arduino UNO female header positions. All headers are SMD
or through-hole on the BOTTOM of the shield (facing the UNO Q). They define the
mechanical mating position.

The shield mounts above the UNO Q. Headers are on the bottom face, reaching
down to the UNO Q pins. All component placement above refers to the TOP face.

| Header | Position | Pins | Pitch |
|--------|----------|------|-------|
| J_POWER (POWER header) | Left edge, Y=2.54 to Y=15.24 from bottom | 6-pin | 2.54mm |
| J_ANALOG (ANALOG IN header) | Left edge, Y=20.32 to Y=35.56 from bottom | 6-pin | 2.54mm |
| J_DIGITAL_LOW (D0–D7) | Top edge, X=11.43 to X=30.23 | 8-pin | 2.54mm |
| J_DIGITAL_HIGH (D8–D13+) | Top edge, X=32.00 to X=50.80 | 10-pin | 2.54mm |

**Important:** Verify exact XY positions from the KiCad Arduino UNO shield template
(`Shield_Arduino_UNO.kicad_mod` or equivalent) before layout. The positions above
are nominal — manufacturing tolerances exist between UNO variants.

### 3.3 Mounting Holes

Four M3 mounting holes (3.20mm drill, NPTH or PTH with GND connection):

| Hole | Position |
|------|----------|
| MH1 | (2.54, 2.54) |
| MH2 | (66.04, 2.54) |
| MH3 | (2.54, 50.80) |
| MH4 | (66.04, 50.80) — omit if conflicts with USB notch |

Copper keepout radius 1.5mm from hole center on all layers.
Silkscreen circle 4.0mm diameter around each hole.

### 3.4 Fiducials

Three fiducials (1.0mm Cu dot, 3.0mm solder mask opening, no silkscreen):

| Fiducial | Position | Notes |
|----------|----------|-------|
| FID1 | (5.00, 5.00) | Top-left reference |
| FID2 | (63.58, 5.00) | Top-right reference |
| FID3 | (5.00, 48.34) | Bottom-left reference |

---

## 4. Functional Zones

The shield divides into four functional zones. Understanding zone boundaries
is critical for signal integrity and AGND/DGND isolation.

```
┌─────────────────────────────────────────────────────┐
│  POWER ZONE          │  DIGITAL/MODULE ZONE          │
│  J4 barrel jack      │  U1 ESP32-S3 module           │
│  C1/C2 bulk caps     │  U2/U3 74HCT245               │
│  U4 AMS1117          │  J1 HUB75 IDC                 │
│  D1/D2 LEDs          │  J5 USB-C                     │
├──────────────────────┤  J6 FPC display               │
│  AUDIO ZONE          │                               │
│  U5 ES8388           ├───────────────────────────────┤
│  FB1 ferrite         │  CONNECTIVITY ZONE            │
│  C6-C9 audio bypass  │  J8/J9 Qwiic                  │
│  C12-C15 DC-block    │  J10-J14 Grove                │
│  J_OUT, J_MIC        │  J2/J3 UNO Q interface        │
│  R3/R4 pullups       │  R5/R6 pullups                │
└─────────────────────────────────────────────────────┘
LEFT EDGE                                   RIGHT EDGE
```

Zone boundaries are conceptual — there is no physical boundary on the PCB.
The GND plane (In1.Cu) is continuous across all zones. The AGND pour on F.Cu
is confined to the audio zone (see §7.3).

---

## 5. Component Placement

Place components in the order listed. Each group is placed before moving to
the next. Respect minimum courtyard clearance: 0.25mm between courtyards.

### 5.1 U1 — ESP32-S3-WROOM-1-N16R8 (18.0 × 25.5mm module)

**Position:** Center-right of board, top surface.  
**Suggested centroid:** X=46, Y=28 (adjust to keep antenna past board edge keepout).  
**Rotation:** 0° (castellations facing left/toward board center, antenna end pointing toward right edge).

**Antenna keepout (CRITICAL):**
The WROOM-1 module has a PCB trace antenna on the right end of the module
(the end without pads). Although the S3 radio is unused (C6 handles all RF),
the keepout must still be respected:
- No copper on ANY layer within 3mm beyond the antenna end of the module.
- This means the antenna end should be within 3mm of or overhanging the right
  board edge. Adjust X position so the antenna region hangs at or past X=65.58.
- If full overhang is not possible, minimize copper in that region and apply a
  copper keepout zone on all layers.

**Pad connections:**
- Castellated pads on left side: SPI3, I2C, I2S, power — route on F.Cu toward
  U4, U2/U3, U5.
- Castellated pads on right side: HUB75 signals (R1,G1,B1,R2,G2,B2,CLK,LAT,
  ADDR_A-E) — route rightward toward U2/U3.
- GPIO35/36/37 pads: No Connect markers in KiCad. Do not route. Apply NC pad
  designation in Gerber notes.

**Decoupling (place first, before U1):**
- C10 (100nF 0402): within 2mm of U1 VCC pin (pin 2 on castellations)
- C11 (10µF 0805): within 4mm of U1 VCC

**EN pullup:**
- R10 (10kΩ 0402): EN pin to +3V3. Can share +3V3 via with C10/C11.

**GPIO0 pullup:**
- R11 (10kΩ 0402): GPIO0 pin to +3V3. Place close to module edge.

### 5.2 U4 — AMS1117-3.3 (SOT-223-3)

**Position:** Left-center area, between J4 barrel jack and U1.  
**Suggested centroid:** X=12, Y=30.  
**Rotation:** Tab (pin 2, +3V3 output) facing toward board interior (away from edge).

**Critical layout rules:**
- Tab is electrically OUTPUT (+3V3). Connect tab to +3V3 polygon pour.
- Thermal via array under tab: minimum 4 vias (0.8mm/0.4mm) in a 2×2 grid,
  connected to In2.Cu +3V3 plane. This is the primary thermal path.
- Input cap C3 (10µF 0805): within 3mm of IN pin (pin 3).
- Output cap C4 (10µF 0805): within 3mm of OUT pin (pin 2/tab).
- HF bypass C5 (100nF 0402): directly adjacent to C4, same side.
- Keep at least 5mm from U5 ES8388 analog section.

### 5.3 J4 — Barrel Jack (CUI PJ-102AH)

**Position:** Left edge, lower half. Connector body extends to or past left board edge.  
**Suggested centroid:** X=5, Y=15.  
**Rotation:** Jack opening faces left (outward from board).

**Layout:**
- Tip pin (+5V_EXT): 1.5mm trace to C1 (100µF 1206 bulk cap). C1 as close to
  J4 as possible, max 5mm.
- C2 (100nF 0402): parallel with C1, same net.
- From C1/C2 junction: 1.5mm trace to U4 IN pin, and separate 1.5mm trace to
  In2.Cu +5V_EXT_HUB75 zone via.
- GND pin: direct via to In1.Cu GND plane. No trace needed — just via.
- Switch pin (barrel jack detect): NC or tie to GND via 100kΩ (not in BOM —
  leave NC unless auto-power-off is desired).

### 5.4 U2 — SN74HCT245PW (TSSOP-20, RGB+CLK+LAT signals)

**Position:** Right-center area, between U1 and J1.  
**Suggested centroid:** X=56, Y=22.  
**Rotation:** A-side pins (inputs from U1) facing left, B-side pins (outputs to J1) facing right.

**Layout:**
- VCC (pin 20): to +5V_EXT_HUB75 zone on In2.Cu via 0.5mm trace.
- C16 (100nF 0402): within 2mm of VCC pin. Connect between VCC and GND plane.
- DIR (pin 1): 0Ω resistor R_DIR_U2 to GND. Place resistor within 3mm of pin.
  If no resistor in schematic, use a direct 0.20mm trace to nearest GND via.
- ~OE (pin 19): 0Ω resistor R_OE_U2 to GND. Same placement rule.
- A-side inputs: traces from U1 castellations. Length <30mm. F.Cu preferred.
- B-side outputs: traces to J1 HUB75 IDC. Keep parallel, even spacing.
  Length matching not required but avoid large disparities (keep within 10mm
  of each other).

### 5.5 U3 — SN74HCT245PW (TSSOP-20, ADDR_A–E signals)

**Position:** Adjacent to U2, slightly lower (toward board bottom).  
**Suggested centroid:** X=56, Y=34.  
**Rotation:** Same as U2 — A-side facing left, B-side facing right.

**Layout:** Identical rules to U2. C17 (100nF 0402) within 2mm of VCC.
ADDR_A–E from U1 castellations → U3 A-side inputs → U3 B-side outputs → J1.
Three A-side pins (A6, A7, A8) are unused — NC.

### 5.6 J1 — HUB75 IDC Connector (2×8, 2.54mm)

**Position:** Right edge or upper-right area, body parallel to right board edge.  
**Suggested centroid:** X=62, Y=28.  
**Orientation:** Pin 1 toward top of board. IDC opening faces right (toward edge),
allowing cable to exit without bending over components.

**Layout:**
- Pin 4, 8, 14, 16, 18 (GND pins): direct vias to In1.Cu GND plane. Short as possible.
- VCC (pin 5V_HUB75, if present): to +5V_EXT_HUB75 pour via 0.5mm trace.
- Signal pins from U2/U3 B-side: short direct traces. Max 10mm from 245 to IDC.
- No termination resistors required at these frequencies (<20MHz effective).
- Place J1 so the cable can run horizontally out the right edge or upward
  off the top edge without conflicting with the display FPC cable.

### 5.7 U5 — ES8388 (LQFP-48, 7×7mm, 0.5mm pitch)

**Position:** Lower-left quadrant, audio zone.  
**Suggested centroid:** X=20, Y=20.  
**Rotation:** 0° (pin 1 at upper-left, standard LQFP orientation).

**This is the most layout-critical component on the board.**

**AGND/DGND star point:**
- The ES8388 AGND pins (2, 29) and DGND pins (16, 40) must meet at a single
  star point beneath U5.
- Implementation: Create a small (~3×3mm) isolated AGND copper pour on F.Cu,
  covering only the AGND pins side of U5. Connect this pour to the In1.Cu GND
  plane via exactly ONE via (the star point). This via is at the center of the
  AGND pour, under U5. The DGND pins connect directly to In1.Cu GND via nearby
  vias as usual. This implements NT1 (net tie) from the schematic.
- Label this via in documentation: "AGND STAR POINT — SINGLE CONNECTION TO GND PLANE."
- No other AGND connection to In1.Cu exists anywhere on the board.

**AVDD filtering (FB1):**
- FB1 (BLM15AX601SN1D, 0402 ferrite): place within 5mm of U5 AVDD pins (1, 28).
- Route: +3V3 pour via → FB1 → small AVDD copper island (F.Cu).
- C6 (10µF 0805) + C7 (100nF 0402): on the AVDD island, within 3mm of U5 pins.
- The AVDD island is electrically isolated from +3V3. It is a separate net fed
  through FB1. Do not connect AVDD to +3V3 pour anywhere except through FB1.

**DVDD decoupling:**
- C8 (10µF 0805) + C9 (100nF 0402): within 3mm of U5 DVDD pins (15, 39).
- Connected to In2.Cu +3V3 zone.

**VMID and VREF:**
- C34 (2.2µF 0402) on VMID pin (pin 3): place close, connect to AGND island.
- C35 (2.2µF 0402) on VREF pin (pin 4): place close, connect to AGND island.

**DAC output path:**
- LOUT1 (pin 44) → C12 (10µF 0805 DC-block) → R30 (10kΩ load) → J_OUT pin 1
- ROUT1 (pin 46) → C13 (10µF 0805 DC-block) → R31 (10kΩ load) → J_OUT pin 2
- All audio output traces on F.Cu, over AGND pour only (not over +3V3 or HUB75 area).
- Keep audio traces away from I2S clock traces (minimum 2mm separation).
- C12/C13 polarity: positive terminal toward U5 output. Mark orientation in silkscreen.

**ADC input path:**
- J_MIC pin 3 (DATA) → U5 LINPUT1 (pin 34): short direct trace.
- J_MIC pin 4 (CLK): from U5 (if U5 provides PDM clock) or MCU GPIO. Short.
- C14 (10µF) on LINPUT1 path: if needed for bias isolation.

**I2C control:**
- SDA (pin 6) and SCL (pin 5): route toward U1 I2C bus.
- ADDR/CSB (pin 7): 0Ω resistor R3 to GND. Place within 3mm of pin.
- R3/R4 (1kΩ I2C pullups): on I2C bus, near U5. Can share with GT911 pullup
  network since same bus.

**I2S signals:**
- BCLK (pin 8), LRCK (pin 9), ADCDAT (pin 10), DACDAT (pin 11):
  Route directly toward U1. Length <30mm. Route on F.Cu over GND plane (In1.Cu).
  Keep at least 3mm away from HUB75 signal traces.

**Keep the following away from U5 (min 5mm):**
- U2/U3 74HCT245 VCC pins and 5V output traces (switching noise)
- J1 HUB75 IDC connector
- U4 AMS1117 tab (thermal source)

### 5.8 J5 — USB-C Receptacle (GCT USB4135-GF-A)

**Position:** Rear edge (top of board), right side.  
**Suggested centroid:** X=58, Y=52.  
**Orientation:** USB opening facing outward (upward, toward top edge).

**Layout:**
- D- (A7) → U1 GPIO19: short direct trace, 0.20mm.
- D+ (A6) → U1 GPIO20: short direct trace, 0.20mm.
- Keep D+/D- traces parallel, same length (±1mm), 0.20mm width, 0.20mm gap.
  This is a USB 2.0 pair — not strict differential impedance control needed at
  FS/HS speeds on a 50mm board, but symmetry helps.
- CC1 (A5) → R12 (5.1kΩ) → GND.
- CC2 (B5) → R13 (5.1kΩ) → GND.
- VBUS (A4): NC (not connected to board power — debug only, no power draw from USB).
- GND pins + shell: direct to In1.Cu GND plane, multiple vias.
- Shell ground: connect to GND via a 1nF capacitor + 1MΩ resistor in parallel
  (chassis ground ESD per USB spec). Not in BOM — add or document as optional.

### 5.9 J6 — FPC Connector (Molex 503480-2200, 22-pin 0.5mm)

**Position:** Upper-center area, FPC cable exiting toward top edge.  
**Suggested centroid:** X=36, Y=46.  
**Orientation:** Bottom-contact FPC. Cable exits toward the top of the board.
The display module sits above the shield — the FPC cable folds back over the
top edge and connects to the display module mounted above.

**This is the most mechanically critical connector on the board.**

**Pad layout requirements (IPC-7351C Level B):**
- 0.5mm pitch, 22 pads. ENIG finish required — do not use HASL here.
- Stencil aperture: reduce 10% from pad size to control paste volume on fine pitch.
- Solder mask: openings exactly at pad edges, no expansion (mask-defined pads).
- Courtyard: 0.5mm beyond connector body on all sides.

**Signal routing from J6 to U1:**
- LCD_CLK (pin 3) → U1 GPIO17: 0.15mm trace, F.Cu.
- LCD_MOSI (pin 4) → U1 GPIO18: 0.15mm trace, F.Cu.
- LCD_CS (pin 5) → U1 GPIO11: 0.15mm trace, F.Cu.
- LCD_DC (pin 6) → U1 GPIO16: 0.15mm trace, F.Cu.
- LCD_RST/TOUCH_RST (pin 7) → U1 GPIO43: 0.15mm trace, F.Cu.
- TOUCH_INT (pin 9) → U1 GPIO44: 0.15mm trace, F.Cu.
- LCD_BL_PWM (pin 8) → U1 GPIO46: 0.15mm trace, F.Cu.
- I2C_SDA (pin 10) → shared I2C bus (also connects to U5 SDA).
- I2C_SCL (pin 11) → shared I2C bus (also connects to U5 SCL).
- +3V3 (pin 2): from +3V3 pour, 0.30mm trace. Bypass C20 (100nF) within 5mm.
- +5V_BL (pin 13): from +5V_EXT rail, 0.50mm trace. Bulk cap C21 (10µF) within 5mm.
- GND (pins 1, 12, 14): direct vias to In1.Cu.
- NC (pins 15–22): no copper, no via. Confirm in solder mask that these are open.

**GT911 pullups:** R20 and R21 (4.7kΩ) on I2C bus between J6 and U5.
Place between J6 and the bus merge point. Connected to +3V3.

**JP1 (0Ω SPI mode select):** In series with LCD_CLK trace. Place between J6
pin 3 and the trace toward U1. Footprint: 0402.

### 5.10 J8 / J9 — Qwiic Connectors (JST SM04B-SRSS-TB, 1.0mm 4-pin)

**Position:** Upper-left corner.  
**J8 centroid:** X=8, Y=50.  
**J9 centroid:** X=16, Y=50.  
**Orientation:** Right-angle SMD, connector opening toward top edge.

**Layout:**
- Both connectors share the same SDA/SCL/+3V3/GND nets (daisy-chain).
- R5 (4.7kΩ, SDA pullup) + R6 (4.7kΩ, SCL pullup): on the shared bus, between
  J8/J9 and U1. Place within 10mm of J8.
- +3V3 and GND traces: 0.30mm.
- SDA/SCL: 0.20mm traces to U1 (GPIO8, GPIO9 via UNO Q headers).

### 5.11 J10–J14 — Grove Connectors (4-pin 2.0mm)

**Position:** Top edge, evenly spaced between J8/J9 and J1 HUB75.  
**Spacing:** 12mm center-to-center along top edge.  
**J10 centroid:** X=28, Y=51.  
**J11 centroid:** X=40, Y=51.  
**J12 centroid:** X=52, Y=51.  
**Orientation:** 2.0mm pitch, connector openings toward top edge.

J13 and J14 may need to move toward right edge or be dropped to fit — verify
after J1 HUB75 IDC and J5 USB-C are placed.

**Signals from UNO Q headers:** SDA/SCL, UART TX/RX, SPI, GPIO, ADC — route
as individual 0.20mm traces to appropriate UNO Q header pins. These are slow
signals, no length or impedance requirements.

### 5.12 J2 — UNO Q SPI Interface (1×6 2.54mm pin header)

**Position:** Along lower-right area, accessible as a breakout header.  
**Suggested centroid:** X=55, Y=8.  
**Orientation:** Vertical, pins accessible from top.

SPI signals (MOSI/MISO/SCK/CS) route from UNO Q digital header J_DIGITAL_HIGH
to this breakout, then continue to U1. The routing passes through this header.

### 5.13 J3 — UART Debug Header (1×2 2.54mm)

**Position:** Near J2, lower-right area.  
**Suggested centroid:** X=62, Y=8.

GPIO47 (UART TX) from U1 → J3 pin 1. GND → J3 pin 2.
0.15mm trace. No length requirement.

### 5.14 D1, D2 — Power Indicator LEDs (0402)

**D1 (+5V indicator):** Near J4 barrel jack. X=8, Y=10.  
**D2 (+3V3 indicator):** Near U4 AMS1117. X=16, Y=10.

**Layout:**
- D1: Anode → +5V_EXT via R1 (620Ω) → cathode → GND.
- D2: Anode → +3V3 via R2 (270Ω) → cathode → GND.
- LED polarity: cathode toward GND (verify footprint orientation — mark K on silkscreen).
- Visible from above when shield is assembled. Place near board edge.

### 5.15 J_OUT / J_MIC — Audio Headers (1×4 2.54mm)

**J_OUT:** Near U5, lower-left.  X=8, Y=30.  
**J_MIC:** Below J_OUT. X=8, Y=24.  
**Orientation:** Vertical, pin 1 toward board bottom.

Both headers in the AGND audio zone. All traces to/from U5 stay within the
audio zone, over the AGND pour.

---

## 6. Net Classes and Trace Widths

Define the following net classes in KiCad before routing:

| Net Class | Width | Clearance | Nets Included |
|-----------|-------|-----------|---------------|
| Default | 0.20mm | 0.20mm | All signal nets not listed below |
| Power_Low | 0.50mm | 0.25mm | +3V3, AVDD, +5V_BL |
| Power_High | 1.50mm | 0.30mm | +5V_EXT, +5V_EXT_HUB75, GND main traces |
| Audio | 0.20mm | 0.30mm | LOUT1, ROUT1, LINPUT1, RINPUT1, AVDD_NET |
| USB_DP_DM | 0.20mm | 0.20mm | D+, D- |
| HUB75_5V | 1.00mm | 0.30mm | +5V_EXT_HUB75 traces to U2/U3 VCC and J1 |

All trace widths are minimums. Widen wherever space allows, especially GND
connection traces from vias to pads.

---

## 7. Copper Pours and Planes

### 7.1 In1.Cu — GND Plane

- Full board fill.
- Clearance from pads: 0.20mm.
- Thermal relief on through-hole pads: 4 spokes, 0.30mm spoke width, 0.25mm gap.
- Solid fill under SMD GND pads (no thermal relief for SMD — direct connection).
- **Exception:** Apply copper keepout zone under ESP32-S3 antenna (see §5.1).
- **AGND star point via** passes through In1.Cu and IS connected to the GND plane.
  The star point via IS the single connection of the AGND island to GND.

### 7.2 In2.Cu — Power Plane (split)

**Zone A: +3V3**
- Area: approximately X=0 to X=55, full Y extent.
- Fill net: +3V3.
- Priority: lower (zone B can overlap at boundaries, zone A yields).

**Zone B: +5V_EXT_HUB75**
- Area: approximately X=48 to X=68.58, Y=10 to Y=45 (HUB75 driver area).
- Fill net: +5V_EXT_HUB75.
- Priority: higher (this zone is smaller and more specific).

**Split gap:** Minimum 0.50mm between zone A and zone B fills.

**Note:** +5V_EXT (from J4, before LDO) does NOT get a power plane zone.
It is a routed trace only (1.5mm width), not a plane. Only the regulated
+3V3 and the HUB75 5V rail have plane zones.

### 7.3 F.Cu — AGND Audio Island

A small isolated copper pour on F.Cu in the audio zone:

- **Extent:** Approximately 12mm × 12mm centered on U5 ES8388.
- **Net:** AGND (separate from GND for pour/DRC purposes — use net tie in schematic).
- **Contents:** U5 AGND pins, C6, C7 (AVDD side caps), C12, C13, C14, C15 (audio
  signal caps), R30, R31 (load resistors), J_OUT, J_MIC.
- **Single via to GND plane:** At AGND star point, under U5 center.
  This via is 0.80mm/0.40mm standard, on the AGND net.
- **No other vias on AGND island to GND plane.** This is enforced by DRC —
  the AGND net must have exactly one via connection to GND.
- **Isolation:** 0.30mm gap between AGND pour and all other F.Cu copper.

### 7.4 F.Cu — +3V3 Local Fill

A local +3V3 fill on F.Cu covering the logic area (U1, U4, U5 DVDD section)
to reduce the need for long +3V3 traces. Connected to In2.Cu +3V3 zone via
multiple stitching vias (every 8mm).

### 7.5 F.Cu — +5V_EXT_HUB75 Local Fill

A local 5V fill on F.Cu in the HUB75 driver area (U2, U3, J1). Connected to
In2.Cu +5V_EXT_HUB75 zone. Width of the fill matches the high-current
requirement — this fill carries up to 3A to the HUB75 panel.

---

## 8. Via Strategy

### 8.1 Standard Signal Vias

- Size: 0.80mm pad / 0.40mm drill.
- Use for layer transitions on signal traces.
- Minimize via count. Each via is a potential impedance discontinuity and
  manufacturing defect. Route on F.Cu wherever possible.

### 8.2 Power Vias (access to planes)

- Size: 0.80mm / 0.40mm (same as signal — adequate for local decoupling).
- For high-current connections (+5V_EXT, +5V_EXT_HUB75 feeding large currents):
  use 2–3 vias in parallel at each connection point.

### 8.3 GND Stitching Vias

- Size: 0.80mm / 0.40mm.
- Pattern: 5mm from board edge all around, then 8mm grid across interior.
- Purpose: maintain continuous GND reference plane, reduce loop area.
- Do not stitch in AGND island area (AGND isolation zone).

### 8.4 AMS1117 Thermal Vias

- Size: 0.60mm / 0.30mm (smaller for tighter array under small SOT-223 tab).
- Count: minimum 4, arranged in 2×2 grid under the tab.
- Connect: F.Cu tab pad → through hole → In2.Cu +3V3 plane (thermal mass).

---

## 9. Routing Order and Rules

Route in this sequence to minimize conflicts:

### Pass 1 — Critical short traces (before any other routing)

Route these first because changing them later disrupts everything around them:

1. U5 ES8388 decoupling: AVDD to FB1 to C6/C7. DVDD to C8/C9.
   All within 5mm of U5. On F.Cu, over AGND island or local GND.

2. U4 AMS1117: +5V_EXT to U4 IN via C3. U4 OUT (+3V3) to C4/C5.
   Thermal via array under U4 tab.

3. U1 ESP32-S3 decoupling: C10/C11 to VCC pins. Within 2mm.

4. U2/U3 SN74HCT245: C16/C17 to VCC pins. Within 2mm.

5. AGND star point via: single via from AGND pour to GND plane.

### Pass 2 — Power distribution

6. J4 tip (+5V_EXT) → C1/C2 → U4 IN: 1.5mm trace on F.Cu.
7. U4 OUT (+3V3) → +3V3 F.Cu pour → In2.Cu zone via stitching vias.
8. +5V_EXT_HUB75 → U2 VCC (pin 20), U3 VCC (pin 20), J1 power pins:
   1.0mm trace from +5V_EXT rail tap (after C1) → In2.Cu HUB75 zone.

### Pass 3 — HUB75 signal path

9. U1 GPIO1–4, GPIO21, GPIO45 (RGB data) → U2 A-side inputs.
10. U1 GPIO33, GPIO34 (CLK, LAT) → U2 A-side.
11. U2 B-side → J1 corresponding pins.
12. U1 GPIO38–42 (ADDR A–E) → U3 A-side inputs.
13. U3 B-side → J1 address pins.
14. DIR and ~OE 0Ω ties to GND on both U2 and U3.

All HUB75 signal traces: 0.20mm width, F.Cu. Length target <25mm for RGB/CLK,
<35mm for ADDR. No length matching required.

### Pass 4 — SPI display and touch

15. U1 GPIO17/18/11/16 (SPI2 display) → JP1 → J6 FPC pins 3–6.
16. U1 GPIO43 (LCD_RST) → J6 pin 7.
17. U1 GPIO44 (TOUCH_INT) → J6 pin 9. (Input-only — single 0.15mm trace.)
18. U1 GPIO46 (LCD_BL_PWM) → J6 pin 8.
19. R20/R21 pullups on SDA/SCL side of J6 (pins 10/11) to +3V3.

All display traces: 0.15mm, F.Cu. Keep SPI traces parallel with <0.3mm spacing
for the segment from U1 to J6 (aesthetics and EMI, not strict requirement).

### Pass 5 — I2S audio

20. U1 GPIO5 (BCLK) → U5 pin 8.
21. U1 GPIO6 (LRCLK) → U5 pin 9.
22. U1 GPIO7 (I2S_DOUT) → U5 pin 10 (ADCDAT input on ES8388 side).
23. U1 GPIO15 (I2S_DIN) → U5 pin 11 (DACDAT output from ES8388).

All I2S traces: 0.20mm, F.Cu, length <30mm. Route over GND plane (avoid
routing over +5V_EXT_HUB75 plane section).

### Pass 6 — I2C shared bus

24. U1 GPIO8 (SDA) → shared bus → U5 pin 6 (SDA) → J6 pin 10 → J8/J9 SDA.
    Pullup R3 (1kΩ codec) and R20 (4.7kΩ display) both on this bus.
    Resultant parallel resistance: ~820Ω — acceptable at 400kHz I2C.
25. U1 GPIO9 (SCL) → shared bus → U5 pin 5 (SCL) → J6 pin 11 → J8/J9 SCL.
    Pullup R4 (1kΩ codec) and R21 (4.7kΩ display) on SCL.
26. R5/R6 (4.7kΩ Qwiic pullups) also on SDA/SCL — but these are in parallel
    with R3/R4. Total pullup ~510Ω. Verify at 400kHz — may need to remove R3/R4
    or increase values. Leave in for now, adjust after bring-up if needed.

### Pass 7 — SPI3 slave interface

27. U1 GPIO13 (SPI_MOSI) → J2 pin 1.
28. U1 GPIO12 (SPI_MISO) → J2 pin 2.
29. U1 GPIO14 (SPI_SCK) → J2 pin 3.
30. U1 GPIO10 (CS_S3_MCU) → J2 pin 4.
31. J2 traces also connect onward to UNO Q headers.

These are slow signals (max 40MHz SPI). 0.20mm traces, no length matching.

### Pass 8 — USB-C

32. U1 GPIO19/20 (D-/D+) → J5 A7/A6. 0.20mm matched-length traces.
33. R12/R13 (5.1kΩ) from J5 CC1/CC2 to GND.

### Pass 9 — Power indicators

34. +5V_EXT → R1 → D1 anode, D1 cathode → GND.
35. +3V3 → R2 → D2 anode, D2 cathode → GND.

### Pass 10 — Connectivity headers

36. J8/J9 (Qwiic): +3V3, GND, SDA, SCL from shared bus.
37. J10–J14 (Grove): signals from UNO Q headers. 0.20mm traces.
38. J3: GPIO47 (UART TX) → J3 pin 1. GND → pin 2.
39. GPIO0 → R11 → +3V3 (pullup).
40. EN → R10 → +3V3 (pullup).

### Pass 11 — Audio outputs

41. U5 LOUT1 (pin 44) → C12 positive → C12 negative → R30 → GND,
    and C12 negative → J_OUT pin 1.
42. U5 ROUT1 (pin 46) → C13 positive → C13 negative → R31 → GND,
    and C13 negative → J_OUT pin 2.
43. J_MIC +3V3 (pin 1) → +3V3 pour. Bypass C36 (10µF) + C37 (100nF) near J_MIC.
44. J_MIC DATA (pin 3) → U5 LINPUT1 (pin 34). Route within audio zone.
45. J_MIC GND (pin 2) → AGND island.

### Pass 12 — Ground fills and cleanup

46. Flood fill In1.Cu GND plane.
47. Flood fill In2.Cu +3V3 and +5V_EXT_HUB75 zones.
48. Flood fill F.Cu AGND island (verify single via connection).
49. Local F.Cu +3V3 and +5V_EXT_HUB75 fills.
50. Add GND stitching vias.
51. Run DRC. Fix all violations.

---

## 10. DRC Rule Settings

Configure these rules in KiCad Board Setup before routing:

```
Minimum clearance:         0.20mm
Minimum trace width:       0.15mm
Minimum via diameter:      0.80mm
Minimum via drill:         0.40mm
Minimum hole-to-hole:      0.25mm
Courtyard clearance:       0.25mm
Solder mask expansion:     0.05mm
Solder mask min width:     0.10mm
Paste margin:              -0.05mm (reduce paste for fine-pitch)
Paste margin ratio:        0
```

**Net-specific DRC rules (add as custom rules in KiCad):**

```python
# High-current power traces
(rule "High_Current_Power"
  (constraint min_track_width (min 1.5mm))
  (condition "A.NetName == '+5V_EXT' || A.NetName == '+5V_EXT_HUB75'"))

# Audio signal protection
(rule "Audio_Clearance"  
  (constraint clearance (min 0.30mm))
  (condition "A.NetName =~ 'LOUT.*' || A.NetName =~ 'ROUT.*' || A.NetName =~ 'LINPUT.*'"))

# AGND star point enforcement  
(rule "AGND_Via_Count"
  (constraint max_via_count (max 1))
  (condition "A.NetName == 'AGND'"))
```

---

## 11. Silkscreen Requirements

### Top silkscreen (F.Silkscreen)
- **All SMD component references:** visible, not over pads or vias.
- **J4 barrel jack:** "DC +5V IN" label. Arrow indicating tip polarity (+).
- **J5 USB-C:** "S3 DEBUG" label.
- **J6 FPC:** "DISPLAY" label. Arrow indicating pin 1.
  "BOTTOM CONTACT — ZIF LOCK BEFORE CABLE" text nearby.
- **J1 HUB75 IDC:** "HUB75 PANEL" label. Pin 1 indicator.
- **J8/J9 Qwiic:** "QWIIC" label. Pin 1 (GND, black wire) indicator.
- **J_OUT:** "LINE OUT L R GND AGND" pin labels.
- **J_MIC:** "MIC VCC GND DATA CLK" pin labels.
- **U1 module:** "ESP32-S3" label. "NO RF — C6 HANDLES WIRELESS" note.
- **AGND star point:** Small "★AGND" marker over the star via location.
- **Hybrid RobotiX logo** and board name "UNO Q HUB75 SHIELD" in upper-right.
- **Revision and date:** "Rev 0.3 / 2026-05-08" in lower-right.
- **Dale Weber / N7PKT** in lower-left (optional, space permitting).

### Bottom silkscreen (B.Silkscreen)
- UNO Q header pin labels where space allows.
- "HYBRID ROBOTIX" company name.
- Fiducial labels (FID1, FID2, FID3).

---

## 12. Solder Mask Notes

- **J6 FPC connector pads (0.5mm pitch):** Use mask-defined pads.
  Solder mask opening = pad size exactly (no expansion). Critical for fine pitch.
- **U5 ES8388 pads (0.5mm pitch LQFP):** Same — mask-defined, no expansion.
- **AMS1117 U4 tab:** Full solder mask opening over tab. Stencil aperture 80%
  of pad area with a grid of 4 openings to allow outgassing.
- **All 0402 pads:** Standard 0.05mm expansion.
- **LED cathodes:** Mark with a small triangle or "K" in silkscreen layer —
  the 0402 LED footprint should have polarity marking.
- **Via tenting:** Tent all vias on both sides (solder mask over via).
  Exception: AGND star via — leave untented as a test point.

---

## 13. Stencil Notes (for PCBWay)

- Stencil material: stainless steel, laser cut.
- Stencil thickness: 0.12mm.
- Aperture adjustments from nominal pad size:
  - J6 FPC 0.5mm pitch: reduce aperture width by 10% (paste control).
  - U5 ES8388 0.5mm pitch: reduce aperture width by 10%.
  - U4 AMS1117 tab: grid of 4 apertures, each 40% of tab area, 0.5mm gap between.
  - All 0402 passives: standard aperture (100% of pad).
  - All 0805 caps: standard aperture.

---

## 14. Fabrication Notes for PCBWay

Include these notes in the Gerber package README or order notes:

```
Project: UNO Q HUB75 Shield
Revision: 0.3
Designer: Dale Weber / Hybrid RobotiX

FABRICATION REQUIREMENTS:
- 4-layer board (Signal / GND / Power / Signal)
- Board size: 68.58 x 53.34mm
- Board thickness: 1.6mm
- Copper: 1oz outer, 0.5oz inner
- Min trace/space: 0.15/0.15mm
- Min drill: 0.30mm PTH
- Surface finish: ENIG (REQUIRED — FPC connector on board)
- Solder mask: Green LPI, both sides
- Silkscreen: White, both sides
- Controlled impedance: NO (no differential pairs)
- IPC Class: 2

SPECIAL NOTES:
1. J6 (FPC connector): 0.5mm pitch, 22 pads. ENIG mandatory.
   Mask-defined pads. Zero solder mask expansion on these pads.
2. U5 (ES8388): 0.5mm pitch LQFP-48. Standard process, fine pitch.
3. AGND net: isolated island with single via connection to GND plane.
   This is intentional. Do not connect AGND to GND plane anywhere
   else. See layout notes for AGND star point location.
4. GPIO35/36/37 pads on U1: NC (no connect). No trace. No via.
5. Board outline includes non-rectangular notch at upper-right corner
   (USB clearance notch). See Edge.Cuts layer.
```

---

## 15. Assembly Notes for PCBWay (if ordering PCBA)

```
ASSEMBLY: TOP SIDE ONLY

SPECIAL ATTENTION COMPONENTS:
1. U5 ES8388 (LQFP-48, 0.5mm pitch):
   - Pin 1 marker toward board upper-left when board oriented with
     J4 barrel jack at left edge.
   - X-ray or AOI inspection required.
   - Stencil aperture reduction 10% on all U5 pads.

2. J6 FPC Connector (Molex 503480-2200):
   - BOTTOM CONTACT type. Verify before placement.
   - Cable lock lever must be in OPEN position for cable insertion.
   - Do not apply pressure to lock lever during reflow.
   - Pin 1 toward board left edge.

3. U1 ESP32-S3-WROOM-1-N16R8:
   - Castellated module. Requires paste on castellated pads.
   - Confirm module orientation: antenna end toward right board edge.
   - GPIO35/36/37 pads: no solder. NC.

4. D1, D2 LEDs (0402):
   - Polarity critical. Cathode (K) toward GND trace.
   - Verify orientation from silkscreen triangle marker.

5. C12, C13 (10µF DC-blocking caps, 0805):
   - Polarity critical (electrolytic-equivalent in X5R).
   - Positive terminal toward U5 output pin (away from J_OUT).
   - Mark "+" terminal on silkscreen if not already on footprint.

CONSIGNED PARTS (supply yourself — not stocked at PCBWay):
- U1: ESP32-S3-WROOM-1-N16R8 (confirm module, not bare chip)
- J6: Molex 503480-2200 (22-pin 0.5mm FPC, bottom-contact)
- J8, J9: JST SM04B-SRSS-TB(LF)(SN)

STANDARD PARTS (PCBWay can source):
- U2, U3: SN74HCT245PWR (TI, DigiKey/Mouser stocked)
- U4: AMS1117-3.3 (any standard vendor)
- U5: ES8388 (LCSC C109698 — source from LCSC, not elsewhere)
- All 0402/0805 passives: standard
```

---

## 16. Bring-Up Sequence

After first boards arrive, test in this order to isolate faults:

1. **Visual inspection:** Check for solder bridges on U5 (0.5mm pitch) and J6.
   Use magnification. Pay attention to U5 corner pins.

2. **Power-on test (no U1 installed):**
   - Apply 5V to J4.
   - Verify D1 (green, 5V indicator) lights.
   - Measure +3V3 at U4 output: should be 3.28–3.32V.
   - Verify D2 (green, 3V3 indicator) lights.
   - Measure current draw: should be <50mA at this stage.

3. **Install U1 (ESP32-S3 module):**
   - Verify +3V3 present at U1 VCC pins before installing.
   - After install, apply 5V. Module should boot. Connect USB-C to J5.
   - Verify COM port appears on host PC (USB CDC).
   - Flash basic blink firmware. Confirm GPIO toggling on oscilloscope.

4. **I2C bus scan:**
   - Run I2C scanner firmware on U1.
   - Should find: 0x10 (ES8388 at ADDR=GND), 0x5D (GT911 if display connected).
   - If ES8388 not found: check R3/R4 pullups, U5 AVDD power, U5 orientation.

5. **HUB75 test:**
   - Connect HUB75 panel via J1.
   - Apply separate 5V to +5V_EXT_HUB75 (if not already from J4).
   - Flash ESP32-HUB75-MatrixPanel-DMA example firmware.
   - Verify panel displays test pattern.
   - If no display: check U2/U3 VCC = 5V, check DIR/~OE tied to GND,
     check GPIO assignments match firmware config.

6. **Display test:**
   - Connect 5" TFT display via J6 FPC (bottom-contact, lock lever closed).
   - Flash LVGL test firmware.
   - Verify display shows image. Touch input (GT911) should respond.

7. **Audio test:**
   - Connect powered speaker to J_OUT.
   - Flash I2S tone generator firmware (440Hz sine wave).
   - Verify audio output on both L and R channels.
   - Check AVDD = 3.3V at U5 pins 1/28. Check AGND star via resistance
     to GND (should be <1Ω direct, not open).

---

## 17. Known Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| U5 ES8388 solder bridge at 0.5mm pitch | Medium | X-ray or AOI inspection, stencil aperture reduction, visual inspect |
| AGND star point accidentally double-connected | Low | Custom DRC rule §10, verify single via in AGND pour during layout |
| J6 FPC wrong contact direction (top vs bottom) | Medium | Verify Molex 503480-2200 is bottom-contact before ordering |
| ESP32-S3 module GPIO35/36/37 connected | Low | NC markers in KiCad, fab note to leave unpopulated |
| I2C bus overloaded (multiple pullups in parallel) | Low | Measure at 400kHz during bring-up, remove R3/R4 if needed |
| HUB75 panel draws more than 5A at full white | Low | Use external 5V supply for panel, not J4 |
| AMS1117 thermal — 400mA through SOT-223 | Low | 4 thermal vias under tab, adequate margin at expected load |
| USB-C D+/D- length mismatch causing signal integrity | Low | Route matched length during layout, FS/HS speeds tolerant |

---

*Document end. Generated 2026-05-08. Rev 1.0.*  
*Hybrid RobotiX — hybridrobotix.io — Dale Weber / N7PKT*
