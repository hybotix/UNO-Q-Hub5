# UNO-Q-Hub5

**Hybrid RobotiX** — UNO Q Shield for HUB75 LED Panels

---

## Overview

UNO-Q-Hub5 is a custom Arduino UNO Q shield that drives HUB75 RGB LED matrix panels via an onboard ESP32-S3 co-processor. The ESP32-S3 owns the HUB75 interface entirely, offloading all panel refresh timing from the UNO Q's STM32U585 MCU.

The shield is designed for use with the **My Chairiet** platform and the **Hybrid RobotiX Standardized Sensor Platform (HSP)**, but functions as a general-purpose HUB75 display shield for any UNO Q project.

---

## Architecture

### Dual-Brain SPI Control

The UNO Q has two independent processors, and either can command the shield:

| Master | Interface | Connection |
|--------|-----------|------------|
| STM32U585 (MCU / sketch side) | SPI via shield headers | J2 — CS_MCU |
| QRB2210 (MPU / Linux side) | SPI via shield headers | J3 — CS_MPU |

MOSI, MISO, and SCK are shared. Each master has its own dedicated CS line. The ESP32-S3 is a pure SPI slave — it processes commands and data without caring which master is active. Software on the UNO Q must ensure only one master drives the bus at a time.

### HUB75 Signal Path

```
ESP32-S3 (3.3V) → 74HCT245 (U2/U3) (level shift to 5V) → HUB75 IDC Connector (J1) → Panel
```

Two 74HCT245 octal bus transceivers handle level shifting:
- **U2** — RGB data lines (R1, G1, B1, R2, G2, B2) + CLK + LAT
- **U3** — Address lines (A, B, C, D, E) + OE

### Power

External 5V power is **required** for the HUB75 panel. The barrel jack (J4) feeds the panel directly. The AMS1117-3.3 LDO (U4) derives 3.3V from the external 5V rail to power the ESP32-S3. The UNO Q shield headers carry logic signals only — panel power does not flow through the shield headers.

> ⚠️ A 64×32 HUB75 panel can draw 3–4A at 5V under full brightness. Use an adequately rated 5V supply.

---

## Hardware

### Bill of Materials

| Ref | Value | Description |
|-----|-------|-------------|
| U1 | ESP32-S3-MINI-1 | HUB75 co-processor, SPI slave |
| U2 | 74HCT245 | Octal bus transceiver, RGB + CLK + LAT |
| U3 | 74HCT245 | Octal bus transceiver, address + OE |
| U4 | AMS1117-3.3 | 3.3V LDO regulator |
| J1 | HUB75 2×8 IDC | Panel connector |
| J2 | 1×6 pin header | UNO Q SPI + CS_MCU |
| J3 | 1×3 pin header | UNO Q MPU CS_MPU |
| J4 | Barrel jack | External 5V panel power input |
| C1, C2 | 10µF | LDO input/output bulk caps |
| C3 | 100nF | ESP32-S3 3.3V decoupling |
| C4 | 10µF | ESP32-S3 3.3V bulk decoupling |
| C5, C6 | 100nF | 74HCT245 VCC decoupling |
| R1 | 10kΩ | ESP32-S3 EN pullup |
| R2 | 330Ω | Power LED current limit |
| D1 | LED | Power indicator |

### Supported Panels

- 64×32 HUB75 RGB LED matrix (primary target)
- Other HUB75-compatible panels supported by [ESP32-HUB75-MatrixPanel-DMA](https://github.com/mrfaptastic/ESP32-HUB75-MatrixPanel-DMA)

---

## Firmware

The ESP32-S3 firmware uses the **ESP32-HUB75-MatrixPanel-DMA** library for DMA-driven panel refresh. The SPI slave interface receives display commands and frame data from whichever UNO Q brain is active.

Firmware source will be located in the `firmware/` directory (in development).

---

## KiCad Project

The schematic is located in `KiCad/`:

```
KiCad/
├── uno_q_hub75_shield.kicad_pro   KiCad v9 project file
└── uno_q_hub75_shield.kicad_sch   Schematic (KiCad v9 S-expression format)
```

Open `uno_q_hub75_shield.kicad_pro` in KiCad 9 to load the project.

---

## Repository Structure

```
UNO-Q-Hub5/
├── KiCad/          KiCad v9 schematic and PCB files
├── firmware/       ESP32-S3 PlatformIO firmware (in development)
├── docs/           Design notes, pin assignments, architecture diagrams
├── LICENSE
└── README.md
```

---

## Status

| Item | Status |
|------|--------|
| Schematic | 🟡 Initial draft |
| PCB layout | 🔴 Not started |
| ESP32-S3 firmware | 🔴 Not started |
| UNO Q sketch integration | 🔴 Not started |
| UNO Q Python/MQTT integration | 🔴 Not started |

---

## Project

**Hybrid RobotiX** — Dale Weber  
Part of the **My Chairiet** distributed computing platform.
UNO Q Shield for Hub5 Compatible LED Panels
