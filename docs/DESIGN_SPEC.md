# UNO Q HUB75 Project — Design Specification

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.2
**Date:** 2026-05-08
**Status:** APPROVED — Proceeding to schematic

---

## Overview

This project produces two hardware designs for HUB75 RGB LED matrix panel driving
and ecosystem expansion on the Arduino UNO Q platform:

1. **UNO Q HUB75 Shield** — Arduino UNO form-factor shield (top headers)
2. **UNO Q HUB75 Carrier** — Full carrier board (JMISC B1 + JMEDIA B2 bottom connectors)

These are standalone Hybrid RobotiX products — not platform-specific to My Chairiet.

---

## Co-Processor Architecture

### ESP32-S3-MINI-1 (both boards)

| Role | Detail |
|------|--------|
| HUB75 co-processor | DMA-driven via ESP32-HUB75-MatrixPanel-DMA library |
| I2S audio processor | Master to ES8388 codec (BCLK, LRCLK, DOUT, DIN) |
| SPI interface | Slave — dual CS: CS_S3_MCU (STM32U585) + CS_S3_MPU (QRB2210) |
| C6 link | Direct UART to ESP32-C6 (carrier only) |
| USB | Native USB-OTG via USB-C for flashing/debug |

### ESP32-C6-MINI-1 (carrier only)

| Role | Detail |
|------|--------|
| Radio co-processor | Thread, Matter, Zigbee (802.15.4), WiFi 6, BLE 5 |
| Ecosystems | Home Assistant, broader IoT/Mesh networking |
| SPI interface | Slave — dual CS: CS_C6_MCU (STM32U585) + CS_C6_MPU (QRB2210) |
| S3 link | Direct UART to ESP32-S3 (independent of UNO Q) |
| USB | USB-Serial/JTAG for flashing/debug |

### S3 ↔ C6 Direct Link

S3 and C6 communicate via dedicated UART. This is independent of the UNO Q —
the C6 can push data to the S3 display, and the S3 can trigger wireless events
on the C6 without UNO Q involvement.

### SPI Bus Architecture

Four independent CS lines on the shared SPI bus:

| CS Line | Master | Target |
|---------|--------|--------|
| CS_S3_MCU | STM32U585 | ESP32-S3 |
| CS_S3_MPU | QRB2210 | ESP32-S3 |
| CS_C6_MCU | STM32U585 | ESP32-C6 (carrier only) |
| CS_C6_MPU | QRB2210 | ESP32-C6 (carrier only) |

MOSI, MISO, SCK shared across all. Software must ensure only one master
and one target active simultaneously.

---

## Audio Architecture (both boards)

### I2S Codec: ES8388

| Parameter | Value |
|-----------|-------|
| Resolution | 24-bit |
| Interface | I2S slave to ESP32-S3 |
| Output | Stereo line-level on pin headers |
| Input | Digital PDM/I2S microphone via header |
| Supply | 3.3V |
| Control | I2C from ESP32-S3 |

### Signal Chain

```
ESP32-S3 I2S DOUT → ES8388 DAC → Line Out header (stereo, line-level)
PDM/I2S Mic header → ES8388 ADC → ESP32-S3 I2S DIN
```

### Audio Connectors

| Connector | Type | Signals |
|-----------|------|---------|
| Line Out | 2.54mm pin header | L+, L-, R+, R- (differential) or L, R, GND |
| Mic In | 2.54mm pin header | VCC, GND, DATA, CLK (PDM/I2S mic compatible) |

No analog JMISC audio path on either board. No headphone amplifier.
No 3.5mm jacks (line-level headers only).

---

## HUB75 Signal Path (both boards)

```
ESP32-S3 (3.3V) → 74HCT245 x2 (3.3V→5V) → HUB75 2x8 IDC → Panel
```

| IC | Signals |
|----|---------|
| U_LS1 (74HCT245) | R1, G1, B1, R2, G2, B2, CLK, LAT |
| U_LS2 (74HCT245) | ADDR_A, ADDR_B, ADDR_C, ADDR_D, ADDR_E, OE |

DIR tied LOW (A→B), ~OE tied LOW (always enabled).
External 5V required. Panel power does not flow through UNO Q headers.

---

## Qwiic + Grove (both boards)

### Qwiic
- 2x JST-SH 4-pin (1.0mm pitch) in daisy-chain configuration
- I2C SDA/SCL from STM32U585 (3.3V)
- 4.7kΩ pullups to 3.3V

### Grove
| Connector | Interface | Signals |
|-----------|-----------|---------|
| Grove I2C | I2C | SDA, SCL |
| Grove UART | UART | TX, RX |
| Grove SPI | SPI | MOSI, MISO, SCK, CS |
| Grove Digital | GPIO | GPIO0, GPIO1 |
| Grove Analog | ADC | ADC0, ADC1 |

All Grove signals from STM32U585 at 3.3V. Standard 4-pin 2.0mm pitch connectors.

---

## UNO Q HUB75 Shield

### Form Factor
Standard Arduino UNO shield. Connects via top headers only (JDIGITAL, JANALOG,
JSPI, JCTL). Fully self-contained — no JMISC pass-through required.

### Components
| Ref | Part | Function |
|-----|------|----------|
| U1 | ESP32-S3-MINI-1 | HUB75 + I2S audio co-processor |
| U2 | SN74HCT245 | Level shifter: RGB + CLK + LAT |
| U3 | SN74HCT245 | Level shifter: ADDR A-E + OE |
| U4 | AMS1117-3.3 | 3.3V LDO from external 5V |
| U5 | ES8388 | 24-bit I2S audio codec |

### Connectors
| Ref | Type | Purpose |
|-----|------|---------|
| J1 | HUB75 2x8 IDC | Panel connector |
| J2 | 1x6 2.54mm | UNO Q SPI + CS_S3_MCU |
| J3 | 1x3 2.54mm | UNO Q CS_S3_MPU |
| J4 | Barrel jack 5.5/2.1mm | HUB75 external 5V |
| J5 | USB-C | ESP32-S3 flash/debug |
| J6 | 1x4 2.54mm | Line out (L, R, GND, AGND) |
| J7 | 1x4 2.54mm | PDM/I2S mic in (VCC, GND, DATA, CLK) |
| J8 | JST-SH 4-pin | Qwiic 1 |
| J9 | JST-SH 4-pin | Qwiic 2 |
| J10 | Grove 4-pin 2.0mm | Grove I2C |
| J11 | Grove 4-pin 2.0mm | Grove UART |
| J12 | Grove 4-pin 2.0mm | Grove SPI |
| J13 | Grove 4-pin 2.0mm | Grove Digital |
| J14 | Grove 4-pin 2.0mm | Grove Analog |

---

## UNO Q HUB75 Carrier Board

### Form Factor
Carrier board. UNO Q mounts on top via JMISC (B1) + JMEDIA (B2).
Smallest PCB to accommodate all connectors with clean signal routing.

### UNO Q Mounting
| Ref | Part | Mates With |
|-----|------|-----------|
| B1 | Samtec FTSH-130-01 2x30 1.27mm | JMISC on UNO Q underside |
| B2 | Samtec FTSH-130-01 2x30 1.27mm | JMEDIA on UNO Q underside |

### Components
| Ref | Part | Function |
|-----|------|----------|
| U1 | ESP32-S3-MINI-1 | HUB75 + I2S audio co-processor |
| U2 | SN74HCT245 | Level shifter: RGB + CLK + LAT |
| U3 | SN74HCT245 | Level shifter: ADDR A-E + OE |
| U4 | AMS1117-3.3 | 3.3V LDO for S3 |
| U5 | ES8388 | 24-bit I2S audio codec |
| U6 | ESP32-C6-MINI-1 | Thread/Matter/Zigbee/WiFi6/BLE radio |
| U7 | TPS54331 (or similar) | Buck converter 7-24V→5V, 3A |
| U8 | TXS0108E | 1.8V→3.3V level shifter bank 1 (MPU GPIO 0-7) |
| U9 | TXS0108E | 1.8V→3.3V level shifter bank 2 (MPU GPIO 8-12) |
| U10 | 24C32 EEPROM | RPi HAT ID EEPROM (pins 27/28) |

### High-Speed Interfaces (from JMEDIA)
| Ref | Connector | Interface | Compatibility |
|-----|-----------|-----------|---------------|
| J1 | Molex 0545821522 22-pin 0.5mm FPC | MIPI DSI 4-lane | RPi 5 compatible |
| J2 | Molex 0545821522 22-pin 0.5mm FPC | MIPI CSI0 4-lane | RPi 5 compatible |
| J3 | Molex 0545821522 22-pin 0.5mm FPC | MIPI CSI1 4-lane | RPi 5 compatible |

### 40-Pin GPIO Header
| Ref | Connector | Compatibility |
|-----|-----------|---------------|
| J4 | 2x20 2.54mm | RPi 5 electrically compatible |

- STM32U585 signals: 3.3V native, direct routing
- QRB2210 MPU GPIO (1.8V): TXS0108E level shifted to 3.3V
- HAT ID EEPROM on pins 27/28, 4.7kΩ pullups
- No PCIe (QRB2210 silicon limitation — documented)

### HUB75 + Power
| Ref | Type | Purpose |
|-----|------|---------|
| J5 | HUB75 2x8 IDC | Panel connector |
| J6 | Barrel jack 5.5/2.1mm | HUB75 5V input |
| J7 | Screw terminal 2-pin | HUB75 5V input (alternate) |
| J8 | Barrel jack 5.5/2.1mm | Carrier VIN 7-24V |
| J9 | Screw terminal 2-pin | Carrier VIN 7-24V (alternate) |

### Audio
| Ref | Type | Purpose |
|-----|------|---------|
| J10 | USB-C | ESP32-S3 flash/debug |
| J11 | 1x4 2.54mm | Line out (L, R, GND, AGND) |
| J12 | 1x4 2.54mm | PDM/I2S mic in (VCC, GND, DATA, CLK) |

### Radio (C6)
| Ref | Type | Purpose |
|-----|------|---------|
| J13 | USB-C | ESP32-C6 flash/debug |

### Qwiic + Grove
| Ref | Type | Purpose |
|-----|------|---------|
| J14 | JST-SH 4-pin | Qwiic 1 |
| J15 | JST-SH 4-pin | Qwiic 2 |
| J16 | Grove 4-pin 2.0mm | Grove I2C |
| J17 | Grove 4-pin 2.0mm | Grove UART |
| J18 | Grove 4-pin 2.0mm | Grove SPI |
| J19 | Grove 4-pin 2.0mm | Grove Digital |
| J20 | Grove 4-pin 2.0mm | Grove Analog |

### Expansion Breakout
| Ref | Type | Signals | Voltage |
|-----|------|---------|---------|
| J21 | 2.54mm + JST | PSSI (8 data + CLK + RDY + DE) | 3.3V |
| J22 | 2.54mm + JST | I2C4 SCL/SDA | 3.3V |
| J23 | 2.54mm | OpAmp1 VOUT/VINP/VINM | Analog |
| J24 | 2.54mm + JST | MPU GPIO 0-11 | 1.8V ⚠️ |

⚠️ J24 signals are 1.8V. Do not connect 3.3V or 5V logic directly.

### Known Limitations
- No PCIe — QRB2210 has no PCIe root complex
- No I2S digital audio from JMISC — MI2S stays internal
- MPU GPIO count: 12 available from JMISC
- Some RPi 40-pin positions populated from STM32U585 not QRB2210

---

## Revision History

| Rev | Date | Author | Notes |
|-----|------|--------|-------|
| 0.1 | 2026-05-08 | Dale Weber | Initial spec |
| 0.2 | 2026-05-08 | Dale Weber | Final approved spec — ESP32-S3 I2S audio (ES8388 24-bit), ESP32-C6 radio co-processor (carrier only), S3/C6 direct UART link, line-level headers only, PDM/I2S mic, no analog JMISC audio, no JMISC pass-through on shield |
