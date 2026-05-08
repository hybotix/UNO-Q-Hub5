# UNO-Q-Hub5

**Hybrid RobotiX** — UNO Q HUB75 Shield and Carrier Board
Dale Weber | Part of the **My Chairiet** distributed computing platform

---

## Overview

UNO-Q-Hub5 is a hardware project producing two complementary boards that enable
HUB75 RGB LED matrix panel driving and ecosystem expansion for the Arduino UNO Q:

| Board | Form Factor | Connects Via |
|-------|-------------|-------------|
| **UNO Q HUB75 Shield** | Arduino UNO shield | Top headers (JDIGITAL/JANALOG/JSPI) + JMISC pass-through |
| **UNO Q HUB75 Carrier** | Carrier board | Bottom connectors (JMISC B1 + JMEDIA B2) |

Both boards share a common ESP32-S3 co-processor architecture for HUB75 driving.

---

## Common Features (Both Boards)

- **ESP32-S3-MINI-1** HUB75 co-processor — DMA-driven via ESP32-HUB75-MatrixPanel-DMA
- **Dual SPI master control** — STM32U585 MCU (sketch side) and QRB2210 MPU (Linux side) via independent CS lines
- **2x 74HCT245** level shifters — 3.3V ESP32-S3 to 5V HUB75 panel signals
- **HUB75 2x8 IDC connector** — 64x32 panel and compatible
- **External 5V power** for HUB75 panel (barrel jack)
- **AMS1117-3.3 LDO** — 3.3V for ESP32-S3 from external 5V rail
- **Audio** — analog PMIC audio from JMISC to 3.5mm jacks (headphone/mic combo, line out)
- **2x Qwiic** JST-SH 4-pin connectors (daisy-chain)
- **5x Grove connectors** — I2C, UART, SPI, Digital, Analog
- **Power indicator LED**

---

## UNO Q HUB75 Shield

Standard Arduino UNO form-factor shield. Mounts on UNO Q top headers.
Includes a Samtec FTSH-130-01 pass-through connector on the underside for
JMISC audio signal access.

**Shield-specific features:**
- JMISC pass-through (Samtec FTSH-130-01 2x30 1.27mm) for audio access
- 3.5mm combo jack (headphone + mic)
- 3.5mm line out jack
- All standard UNO Q top header pins passed through

---

## UNO Q HUB75 Carrier Board

Full carrier board. UNO Q mounts on top via JMISC and JMEDIA connectors.
Provides the complete high-speed peripheral ecosystem plus RPi 5 compatible
interfaces.

**Carrier-specific features:**
- **MIPI DSI** — 22-pin 0.5mm FPC, RPi 5 compatible
- **MIPI CSI0 + CSI1** — 22-pin 0.5mm FPC x2, RPi 5 compatible
- **40-pin GPIO header** — RPi 5 electrically compatible (GPIO, SPI, I2C, UART, PWM)
- **HAT ID EEPROM** on pins 27/28 for RPi HAT compliance
- **1.8V to 3.3V level shifting** (TXS0108E) for MPU GPIO bank
- **Carrier VIN input** — barrel jack + screw terminal (7-24V)
- **HUB75 power** — separate barrel jack + screw terminal (5V)
- **Audio** — headphone/mic combo, line out, earpiece (3x 3.5mm jacks)
- **PSSI breakout** — 2.54mm + JST (STM32U585 parallel interface)
- **I2C4 breakout** — 2.54mm + JST
- **OpAmp breakout** — 2.54mm
- **MPU GPIO breakout** — 2.54mm + JST (1.8V — clearly labeled)
- **Buck converter** — onboard 5V/3A from VIN rail

> WARNING: No PCIe — The QRB2210 SoC has no PCIe root complex. NVMe HATs and
> PCIe HATs will not function. See docs/RPi_COMPATIBILITY.md.

---

## Repository Structure

```
UNO-Q-Hub5/
├── KiCad/
│   ├── shield/                 Shield KiCad v9 project
│   └── carrier/                Carrier KiCad v9 project
├── firmware/
│   ├── shield/                 ESP32-S3 PlatformIO firmware (shield)
│   └── carrier/                ESP32-S3 PlatformIO firmware (carrier)
├── docs/
│   ├── DESIGN_SPEC.md          Full design specification
│   ├── PIN_MAPPING.md          Detailed signal mapping tables
│   └── RPi_COMPATIBILITY.md    RPi 5 HAT compatibility notes
├── LICENSE
└── README.md
```

---

## Hardware Status

| Item | Shield | Carrier |
|------|--------|---------|
| Design spec | Done | Done |
| Schematic | In progress | In progress |
| PCB layout | Not started | Not started |
| ESP32-S3 firmware | Not started | Not started |
| UNO Q sketch integration | Not started | Not started |
| UNO Q Linux/MQTT integration | Not started | Not started |

---

## References

- Arduino UNO Q Documentation: https://docs.arduino.cc/hardware/uno-q/
- QRB2210 Datasheet: https://docs.qualcomm.com/bundle/publicresource/80-30843-1
- ESP32-HUB75-MatrixPanel-DMA: https://github.com/mrfaptastic/ESP32-HUB75-MatrixPanel-DMA
- RPi HAT Specification: https://github.com/raspberrypi/hats
- Samtec FTSH-130-01-L-DV: https://www.samtec.com/products/ftsh
- Molex 0545821522 FPC: https://www.molex.com

---

## Project

**Hybrid RobotiX** — Dale Weber
Part of the **My Chairiet** distributed computing platform.
"I. WILL. NEVER. GIVE. UP. OR. SURRENDER."
