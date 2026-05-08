# UNO Q HUB75 Project — Bill of Materials

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.2
**Date:** 2026-05-08

Covers both the **Shield** and **Carrier** boards. Items marked **Carrier Only**
are not present on the shield. All SMD passives are 0402 unless noted.

---

## Integrated Circuits

| Ref (Shield) | Ref (Carrier) | Part | Package | Description | Source |
|---|---|---|---|---|---|
| U1 | U1 | ESP32-S3-MINI-1 | SMD module | HUB75 DMA + I2S audio co-processor | [Espressif](https://www.espressif.com/en/products/modules/esp32-s3) / Mouser / DigiKey |
| — | U6 | ESP32-C6-MINI-1 | SMD module | Thread/Matter/Zigbee/WiFi6/BLE5 radio co-processor (**Carrier Only**) | [Espressif](https://www.espressif.com/en/products/modules/esp32-c6) / Mouser / DigiKey |
| U2 | U2 | SN74HCT245PWR | TSSOP-20 | Level shifter: R1,G1,B1,R2,G2,B2,CLK,LAT (3.3V→5V) | [TI](https://www.ti.com/product/SN74HCT245) / Mouser |
| U3 | U3 | SN74HCT245PWR | TSSOP-20 | Level shifter: ADDR A–E, OE (3.3V→5V) | [TI](https://www.ti.com/product/SN74HCT245) / Mouser |
| U4 | U4 | AMS1117-3.3 | SOT-223-3 | 3.3V LDO regulator (800mA) | Mouser / DigiKey |
| U5 | U5 | ES8388 | LQFP-48 | 24-bit stereo I2S audio codec (DAC + ADC) | [Everest Semi](https://datasheet.lcsc.com/szlcsc/Everest-Semiconductor-ES8388_C109698.pdf) / LCSC |
| — | U7 | TPS54331DR | SOIC-8 | 28V/3A buck converter, VIN→5V (**Carrier Only**) | [TI](https://www.ti.com/product/TPS54331) / Mouser |
| — | U8 | TXS0108EPWR | TSSOP-20 | 8-bit 1.8V↔3.3V level shifter, MPU GPIO bank 1 (GPIO 0–7) (**Carrier Only**) | [TI](https://www.ti.com/product/TXS0108E) / Mouser |
| — | U9 | TXS0108EPWR | TSSOP-20 | 8-bit 1.8V↔3.3V level shifter, MPU GPIO bank 2 (GPIO 8–12) (**Carrier Only**) | [TI](https://www.ti.com/product/TXS0108E) / Mouser |
| — | U10 | 24C32WP | SOIC-8 | 32Kb I2C EEPROM — RPi HAT ID EEPROM on pins 27/28 (**Carrier Only**) | Mouser / DigiKey |

---

## Discrete Semiconductors

| Ref (Shield) | Ref (Carrier) | Part | Package | Description |
|---|---|---|---|---|
| D1 | D1 | LED (green) | 0402 | 3.3V power indicator |
| — | D3 | LED (green) | 0402 | 3.3V rail indicator (**Carrier Only**) |
| — | D2 | SS34 | SMA | Schottky diode, TPS54331 catch diode (**Carrier Only**) |

---

## Passive Components — Resistors (all 0402 1% unless noted)

| Ref (Shield) | Ref (Carrier) | Value | Purpose |
|---|---|---|---|
| R1 | R3 | 10kΩ | ESP32-S3 EN pullup |
| — | R4 | 10kΩ | ESP32-C6 EN pullup (**Carrier Only**) |
| R2 | R1 | 330Ω | PWR LED current limit |
| — | R2 | 330Ω | 3.3V PWR LED current limit (**Carrier Only**) |
| R3 | R5 | 1kΩ | ES8388 I2C_SDA pullup (codec control) |
| R4 | R6 | 1kΩ | ES8388 I2C_SCL pullup (codec control) |
| R5 | R9 | 4.7kΩ | Qwiic I2C SDA pullup |
| R6 | R10 | 4.7kΩ | Qwiic I2C SCL pullup |
| — | R7 | 4.7kΩ | HAT ID EEPROM SDA pullup (**Carrier Only**) |
| — | R8 | 4.7kΩ | HAT ID EEPROM SCL pullup (**Carrier Only**) |
| — | R11 | 100kΩ | TPS54331 RT (switching frequency) (**Carrier Only**) |
| — | R12 | 1.0kΩ | TPS54331 VSENSE divider high (**Carrier Only**) |
| — | R13 | 200kΩ | TPS54331 VSENSE divider low (**Carrier Only**) |

---

## Passive Components — Capacitors (all 0402 X7R unless noted)

| Ref (Shield) | Ref (Carrier) | Value | Voltage | Purpose |
|---|---|---|---|---|
| C1 | — | 10µF 0805 | 10V | AMS1117 input bulk |
| C2 | — | 10µF 0805 | 10V | AMS1117 output bulk |
| C3 | C4 | 100nF | 10V | ESP32-S3 VCC bypass |
| C4 | C5 | 10µF 0805 | 10V | ESP32-S3 VCC bulk |
| C5 | C11 | 100nF | 10V | 74HCT245 U2 VCC bypass |
| C6 | C12 | 100nF | 10V | 74HCT245 U3 VCC bypass |
| C9 | C8 | 100nF | 10V | ES8388 AVDD bypass |
| C10 | C9 | 10µF 0805 | 10V | ES8388 AVDD bulk |
| C11 | C10 | 10µF 0805 | 10V | ES8388 DVDD bulk |
| C12 | — | 10µF 0805 | 10V | ES8388 audio output DC-block |
| — | C1 | 100µF 1206 | 35V | TPS54331 VIN input bulk (**Carrier Only**) |
| — | C2 | 100µF 1206 | 10V | TPS54331 output bulk (**Carrier Only**) |
| — | C3 | 10µF 0805 | 10V | AMS1117 output bulk (**Carrier Only**) |
| — | C6 | 100nF | 10V | ESP32-C6 VCC bypass (**Carrier Only**) |
| — | C7 | 10µF 0805 | 10V | ESP32-C6 VCC bulk (**Carrier Only**) |
| — | C13 | 100nF | 10V | TXS0108E U8 bypass (**Carrier Only**) |
| — | C14 | 100nF | 10V | TXS0108E U9 bypass (**Carrier Only**) |
| — | C15 | 100nF | 10V | TPS54331 SS/TR softstart (**Carrier Only**) |
| — | C16 | 22pF | 50V | TPS54331 COMP compensation (**Carrier Only**) |
| — | C17 | 10µF 0805 | 10V | ES8388 audio output DC-block (**Carrier Only**) |

---

## Inductors

| Ref (Shield) | Ref (Carrier) | Value | Rating | Description |
|---|---|---|---|---|
| — | L1 | 10µH | 3A, DCR <50mΩ | TPS54331 output inductor. Bourns SRR1260A-100M or equivalent (**Carrier Only**) |

---

## Connectors — HUB75 + Power

| Ref (Shield) | Ref (Carrier) | Part | Description |
|---|---|---|---|
| J1 | J5 | 2×8 IDC 2.54mm vertical | HUB75 panel connector |
| J4 | J6 | Barrel jack 5.5/2.1mm | HUB75 external 5V input |
| — | J7 | Screw terminal 2-pin 5.0mm | HUB75 5V alternate input (**Carrier Only**) |
| — | J8 | Barrel jack 5.5/2.1mm | Carrier VIN 7–24V input (**Carrier Only**) |
| — | J9 | Screw terminal 2-pin 5.0mm | Carrier VIN alternate input (**Carrier Only**) |

---

## Connectors — USB

| Ref (Shield) | Ref (Carrier) | Part | Description |
|---|---|---|---|
| J5 | J10 | USB-C receptacle (GCT USB4135 or equiv) | ESP32-S3 flash/debug |
| — | J13 | USB-C receptacle | ESP32-C6 flash/debug (**Carrier Only**) |

---

## Connectors — Audio

| Ref (Shield) | Ref (Carrier) | Part | Description |
|---|---|---|---|
| J6 | J11 | 1×4 pin header 2.54mm | Stereo line out: L, R, GND, AGND |
| J7 | J12 | 1×4 pin header 2.54mm | PDM/I2S mic in: VCC, GND, DATA, CLK |

---

## Connectors — UNO Q Headers (Shield only)

| Ref | Part | Description |
|---|---|---|
| J2 | 1×6 pin header 2.54mm | UNO Q SPI: MOSI, MISO, SCK, CS_S3_MCU, GND, 3V3 |
| J3 | 1×3 pin header 2.54mm | UNO Q CS_S3_MPU, GND, 3V3 |

---

## Connectors — UNO Q Mounting (Carrier only)

| Ref | Part | Description |
|---|---|---|
| B1 | Samtec FTSH-130-01-L-DV-A (2×30, 1.27mm) | JMISC connector — SPI, I2C, GPIO, power |
| B2 | Samtec FTSH-130-01-L-DV-A (2×30, 1.27mm) | JMEDIA connector — MIPI DSI, CSI0, CSI1, power |

Samtec part: [FTSH-130-01-L-DV-A](https://www.samtec.com/products/ftsh)

---

## Connectors — RPi 5 Compatible (Carrier only)

| Ref | Part | Description |
|---|---|---|
| J1 | Molex 0545821522 (22-pin, 0.5mm FPC) | MIPI DSI 4-lane — RPi 5 display compatible |
| J2 | Molex 0545821522 (22-pin, 0.5mm FPC) | MIPI CSI0 4-lane — RPi 5 camera compatible |
| J3 | Molex 0545821522 (22-pin, 0.5mm FPC) | MIPI CSI1 4-lane — RPi 5 camera compatible |
| J4 | 2×20 pin header 2.54mm | RPi 5 compatible 40-pin GPIO header |

---

## Connectors — Qwiic + Grove (both boards)

| Ref (Shield) | Ref (Carrier) | Part | Description |
|---|---|---|---|
| J8 | J14 | JST SH 4-pin 1.0mm horizontal | Qwiic 1 |
| J9 | J15 | JST SH 4-pin 1.0mm horizontal | Qwiic 2 |
| J10 | J16 | Grove 4-pin 2.0mm | Grove I2C (SDA, SCL, 3V3, GND) |
| J11 | J17 | Grove 4-pin 2.0mm | Grove UART (TX, RX, 3V3, GND) |
| J12 | J18 | Grove 4-pin 2.0mm | Grove SPI (MOSI, MISO, 3V3, GND) |
| J13 | J19 | Grove 4-pin 2.0mm | Grove Digital (GPIO0, GPIO1, 3V3, GND) |
| J14 | J20 | Grove 4-pin 2.0mm | Grove Analog (ADC0, ADC1, 3V3, GND) |

---

## Connectors — Expansion Breakout (Carrier only)

| Ref | Part | Description |
|---|---|---|
| J21 | 1×12 pin header 2.54mm | PSSI: D0–D7, CLK, RDY, DE, GND |
| J22 | 1×4 pin header 2.54mm | I2C4: SDA, SCL, 3V3, GND |
| J23 | 1×4 pin header 2.54mm | OpAmp: VOUT, VINP, VINM, GND |
| J24 | 1×12 pin header 2.54mm | MPU GPIO 0–11 (**1.8V — do not connect 3.3V/5V**) |

---

## Component Count Summary

| Category | Shield | Carrier |
|---|---|---|
| ICs | 5 | 10 |
| Discrete semiconductors | 1 | 3 |
| Resistors | 6 | 13 |
| Capacitors | 10 | 17 |
| Inductors | 0 | 1 |
| Connectors | 14 | 24 |
| **Total line items** | **36** | **68** |

---

## Recommended Suppliers

| Supplier | Best for |
|---|---|
| [Mouser](https://www.mouser.com) | TI ICs, connectors, passives |
| [DigiKey](https://www.digikey.com) | Samtec, Molex FPC, ES8388 |
| [LCSC](https://www.lcsc.com) | ES8388, ESP32 modules, low-cost passives |
| [Samtec](https://www.samtec.com) | FTSH-130-01 direct |
| [Espressif Direct](https://www.espressif.com) | ESP32-S3-MINI-1, ESP32-C6-MINI-1 |

---

## Critical Sourcing Notes

1. **ES8388** — Order from LCSC (C109698). Availability can be spotty elsewhere.
2. **Samtec FTSH-130-01** — Must match UNO Q JMISC/JMEDIA pitch exactly (1.27mm, 2×30). Order direct from Samtec for guaranteed spec.
3. **Molex 0545821522** — 22-pin 0.5mm FPC bottom-contact. Verify orientation before soldering — RPi 5 cable compatibility depends on it.
4. **TPS54331** — Can substitute TPS54232 (2A) for lighter loads, or TPS563201 (3A, SOT-23-6) if board space is tight.
5. **24C32** — Any I2C EEPROM ≥32Kb at address 0x50 with SDA/SCL on 4-pin SOIC-8. Microchip 24FC32AT-I/SN works.
6. **ESP32-S3-MINI-1 vs MINI-1U** — Use MINI-1 (PCB antenna) unless you plan to add an external antenna. MINI-1U has u.FL connector instead.

---

## Revision History

| Rev | Date | Notes |
|---|---|---|
| 0.1 | 2026-05-08 | Initial BOM |
| 0.2 | 2026-05-08 | Final approved. ES8388 24-bit I2S codec. ESP32-C6 carrier-only. S3↔C6 direct UART. No analog audio from JMISC. |
