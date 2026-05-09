# UNO Q HUB75 Shield — Bill of Materials

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.3
**Date:** 2026-05-08
**Applies to:** UNO Q HUB75 Shield (first board to fab)

---

## Co-Processor Module

| Ref | Part | Description | Source |
|-----|------|-------------|--------|
| U1 | **ESP32-S3-WROOM-1-N16R8** | 16MB flash, 8MB octal PSRAM, PCB antenna, 18×25.5mm | [Mouser](https://www.mouser.com) / [LCSC C2913202](https://lcsc.com) |
| U1 alt | ESP32-S3-WROOM-1U-N16R8 | Same spec, U.FL external antenna — drop-in substitute | Mouser / DigiKey |

**Note:** GPIO35/36/37 are NC (consumed by PSRAM internally). GPIO0 has 10kΩ pullup (boot-safe). S3 radio unused — C6 handles all wireless on the Super Carrier.

---

## ICs

| Ref | Part | Package | Function | Source |
|-----|------|---------|----------|--------|
| U2 | SN74HCT245PW**R** | TSSOP-20 | Level shifter: R1,G1,B1,R2,G2,B2,CLK,LAT (3.3V→5V) | [TI](https://www.ti.com/product/SN74HCT245) / Mouser |
| U3 | SN74HCT245PW**R** | TSSOP-20 | Level shifter: ADDR_A–E + 3 NC (3.3V→5V) | TI / Mouser |
| U4 | AMS1117-3.3 | SOT-223-3 | 3.3V LDO, 800mA — logic supply | Mouser / DigiKey |
| U5 | ES8388 | LQFP-48 | 24-bit stereo I2S audio codec (DAC + ADC) | [LCSC C109698](https://lcsc.com) |

**74HCT245 notes:** VCC = +5V_EXT_HUB75 (not +3V3). DIR pin 1 = GND (0Ω). ~OE pin 19 = GND (0Ω). Both tied in hardware — no GPIO needed.

---

## Discrete Semiconductors

| Ref | Part | Package | Function |
|-----|------|---------|----------|
| D1 | LED green | 0402 | +5V_EXT power indicator |
| D2 | LED green | 0402 | +3V3 power indicator |

---

## Resistors (all 0402 1% unless noted)

| Ref | Value | Function |
|-----|-------|----------|
| R1 | 620Ω | D1 LED current limit (5V rail: (5–2)/0.005 = 600Ω → 620Ω std) |
| R2 | 270Ω | D2 LED current limit (3.3V rail: (3.3–2)/0.005 = 260Ω → 270Ω std) |
| R3 | 1kΩ | ES8388 I2C_SDA pullup (codec control) |
| R4 | 1kΩ | ES8388 I2C_SCL pullup (codec control) |
| R5 | 4.7kΩ | Qwiic I2C SDA pullup |
| R6 | 4.7kΩ | Qwiic I2C SCL pullup |
| R10 | 10kΩ | ESP32-S3 EN pullup (required — do not omit) |
| R11 | 10kΩ | GPIO0 pullup — boot-safe; CS_S3_MPU on carrier |
| R12 | 5.1kΩ | USB-C CC1 pulldown (device identification) |
| R13 | 5.1kΩ | USB-C CC2 pulldown (device identification) |
| R20 | 4.7kΩ | GT911 I2C SDA pullup (display side of FPC) |
| R21 | 4.7kΩ | GT911 I2C SCL pullup (display side of FPC) |
| JP1 | 0Ω | SPI mode select — CLOSED (populated, default SPI) |
| JP2 | DNP | QSPI upgrade path — NOT POPULATED |
| 2× | 0Ω | 74HCT245 DIR tie to GND (U2 pin 1, U3 pin 1) |
| 2× | 0Ω | 74HCT245 ~OE tie to GND (U2 pin 19, U3 pin 19) |

---

## Capacitors (all X7R unless noted)

| Ref | Value | Voltage | Package | Function |
|-----|-------|---------|---------|----------|
| C1 | 100µF | 10V | 1206 electrolytic | +5V_EXT input bulk — barrel jack entry |
| C2 | 100nF | 10V | 0402 | +5V_EXT HF bypass |
| C3 | 10µF | 10V | 0805 X5R | AMS1117 VIN input |
| C4 | 10µF | 10V | 0805 X5R | AMS1117 VOUT output (min 10µF for stability) |
| C5 | 100nF | 10V | 0402 | AMS1117 VOUT HF bypass |
| C6 | 10µF | 10V | 0805 X5R | ES8388 AVDD bulk (after FB1 ferrite) |
| C7 | 100nF | 10V | 0402 | ES8388 AVDD HF bypass |
| C8 | 10µF | 10V | 0805 X5R | ES8388 DVDD bulk |
| C9 | 100nF | 10V | 0402 | ES8388 DVDD HF bypass |
| C10 | 100nF | 10V | 0402 | ESP32-S3 +3V3 HF bypass (within 2mm of VCC pin) |
| C11 | 10µF | 10V | 0805 X5R | ESP32-S3 +3V3 bulk |
| C12/C13 | 10µF | 10V | 0805 X5R | ES8388 LOUT/ROUT DC-blocking caps |
| C14/C15 | 10µF | 10V | 0805 X5R | ES8388 LINPUT/RINPUT DC-blocking caps |
| C16 | 100nF | 10V | 0402 | 74HCT245 U2 VCC bypass |
| C17 | 100nF | 10V | 0402 | 74HCT245 U3 VCC bypass |
| C20 | 100nF | 10V | 0402 | +3V3 bypass at FPC connector |
| C21 | 10µF | 10V | 0805 X5R | +5V_BL bulk at FPC connector |

---

## Inductors / Ferrite Beads

| Ref | Part | Value | Function |
|-----|------|-------|----------|
| FB1 | Murata BLM15AX601SN1D | 600Ω @ 100MHz, 0402 | ES8388 AVDD filter — isolates analog from digital +3V3 |

---

## Connectors

### Power
| Ref | Part | Function |
|-----|------|----------|
| J4 | CUI PJ-102AH barrel jack 5.5/2.1mm | +5V_EXT input — HUB75 + logic |

### HUB75
| Ref | Part | Function |
|-----|------|----------|
| J1 | 2×8 IDC 2.54mm vertical | HUB75 panel connector |

### Display
| Ref | Part | Function |
|-----|------|----------|
| J6 | Molex 503480-2200 (22-pin 0.5mm FPC, bottom-contact) | 5" TFT + GT911 touch |

### Audio
| Ref | Part | Function |
|-----|------|----------|
| J_OUT | 1×4 2.54mm pin header | Stereo line out: L, R, GND, AGND |
| J_MIC | 1×4 2.54mm pin header | PDM/I2S mic in: VCC, GND, DATA, CLK |

### USB
| Ref | Part | Function |
|-----|------|----------|
| J5 | GCT USB4135-GF-A (USB-C receptacle) | ESP32-S3 debug CDC/JTAG |

### UNO Q Interface
| Ref | Part | Function |
|-----|------|----------|
| J2 | 1×6 2.54mm pin header | SPI3 + CS_S3_MCU (mates with UNO Q JSPI) |
| J3 | 1×2 2.54mm pin header | UART debug TX (GPIO47) + GND |

### Connectivity
| Ref | Part | Function |
|-----|------|----------|
| J8 | JST SM04B-SRSS-TB (Qwiic, 1.0mm 4-pin) | Qwiic 1 |
| J9 | JST SM04B-SRSS-TB (Qwiic, 1.0mm 4-pin) | Qwiic 2 |
| J10 | Grove 4-pin 2.0mm | Grove I2C |
| J11 | Grove 4-pin 2.0mm | Grove UART |
| J12 | Grove 4-pin 2.0mm | Grove SPI |
| J13 | Grove 4-pin 2.0mm | Grove Digital |
| J14 | Grove 4-pin 2.0mm | Grove Analog |

---

## Target Display Module (not on shield BOM — purchased separately)

| Item | Specification |
|------|--------------|
| Size | 5.0" |
| Resolution | 800×480 |
| Interface | 4-wire SPI |
| Touch | GT911 5-point capacitive, I2C |
| Connector | 22-pin 0.5mm FPC (compatible with J6) |
| Primary source | Waveshare 5inch LCD SPI + GT911 |
| Secondary source | BuyDisplay ER-TFTM050 series (SPI variant) |

---

## Fabrication Requirements

| Spec | Value |
|------|-------|
| Layers | 4 |
| Stackup | Signal / GND plane / Power plane / Signal |
| Copper weight | 1oz (35µm) outer, 0.5oz inner |
| Min trace/space | 0.15/0.15mm |
| Min drill | 0.3mm |
| Surface finish | **ENIG** (required for 0.5mm FPC pads on J6) |
| Solder mask | Both sides, LPI |
| Silkscreen | Top + bottom |
| Board thickness | 1.6mm |
| Board outline | Arduino UNO shield: 68.6 × 53.3mm |

---

## Component Count Summary

| Category | Count |
|----------|-------|
| ICs (module + discrete) | 5 |
| LEDs | 2 |
| Resistors (incl. 0Ω ties) | ~18 |
| Capacitors | ~20 |
| Ferrite beads | 1 |
| Connectors | ~16 |
| **Total line items** | **~62** |

---

## Key Sourcing Notes

1. **ES8388** — Order from LCSC (C109698). Sporadic availability elsewhere.
2. **Molex 503480-2200** — 22-pin 0.5mm FPC. Order from DigiKey or Molex direct. Verify bottom-contact orientation — top-contact variants exist and will not mate with standard flat cables.
3. **SN74HCT245PWR** — Note the R suffix (tape-and-reel). Equivalent in tube packaging is SN74HCT245PW (no R). Both are identical electrically.
4. **AMS1117-3.3 SOT-223** — Tab pin (pin 2) is output. Tab connects to +3V3 trace and thermal via array. Do not confuse with TO-92 variant.
5. **JST SM04B-SRSS-TB** — Qwiic-compatible 1.0mm 4-pin SMD right-angle. Verify LF/SN suffix for RoHS compliance.

---

## Revision History

| Rev | Date | Notes |
|-----|------|-------|
| 0.1 | 2026-05-08 | Initial |
| 0.2 | 2026-05-08 | Full dual-board BOM |
| 0.3 | 2026-05-08 | Shield-only BOM. Module upgraded to ESP32-S3-WROOM-1-N16R8 (8MB PSRAM). Added display BOM items: Molex 503480-2200 FPC (J6), JP1/JP2 mode select, GT911 I2C pullups R20/R21, USB-C CC resistors R12/R13, GPIO0/EN pullups R10/R11, +5V_BL bulk C21. Resistor values calculated per IPC-2152 LED current limits. |
