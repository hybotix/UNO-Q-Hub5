# RPi 5 HAT Compatibility Notes

**Hybrid RobotiX** — UNO Q HUB75 Carrier Board  
**Revision:** 0.1 | **Date:** 2026-05-08

---

## Overview

The UNO Q HUB75 Carrier exposes a 40-pin GPIO header that is electrically and
physically compatible with the Raspberry Pi 5 for the majority of HAT categories.
This document describes what works, what doesn't, and why.

---

## Compatible Interfaces

| Interface | RPi 5 Pins | UNO Q Source | Status |
|-----------|-----------|--------------|--------|
| GPIO (3.3V) | Various | STM32U585 + QRB2210 (level shifted) | ✅ Compatible |
| SPI0 | 19, 21, 23, 24, 26 | STM32U585 SPI | ✅ Compatible |
| I2C1 | 3, 5 | STM32U585 I2C | ✅ Compatible |
| UART0 | 8, 10 | STM32U585 UART | ✅ Compatible |
| PWM | 12, 33 | STM32U585 PWM | ✅ Compatible |
| 5V power | 2, 4 | Carrier 5V rail | ✅ Compatible |
| 3.3V power | 1, 17 | Carrier 3.3V rail | ✅ Compatible |
| GND | 6, 9, 14, 20, 25, 30, 34, 39 | Carrier GND | ✅ Compatible |
| HAT ID I2C | 27, 28 | Dedicated EEPROM | ✅ Compatible |
| MIPI DSI | 22-pin FPC | QRB2210 DSI | ✅ Compatible |
| MIPI CSI0 | 22-pin FPC | QRB2210 CSI0 | ✅ Compatible |
| MIPI CSI1 | 22-pin FPC | QRB2210 CSI1 | ✅ Compatible |

---

## Incompatible Interfaces

### PCIe — NOT SUPPORTED

The Raspberry Pi 5 exposes a PCIe 2.0 ×1 interface via the FPC connector and
optionally via the 40-pin header on some HATs.

**The QRB2210 SoC has no PCIe root complex.** This is a hard silicon limitation.
No bridge chip can add PCIe root complex capability to a processor that does not
have one. USB-to-PCIe bridges exist but present as USB host controllers, not
native PCIe, and HATs expecting a native PCIe root complex will not enumerate.

**Affected HAT categories:**
- NVMe SSD HATs (M.2 HATs)
- PCIe GPIO expander HATs
- Any HAT explicitly requiring PCIe

**Workaround:** None possible at the hardware level.

---

## HAT Categories — Compatibility Summary

| HAT Category | Compatible | Notes |
|---|---|---|
| Sensor HATs (I2C/SPI) | ✅ Yes | Full compatibility |
| Display HATs (SPI/I2C) | ✅ Yes | Full compatibility |
| Motor/servo HATs (PWM/I2C) | ✅ Yes | Full compatibility |
| Audio HATs (I2S) | ⚠️ Partial | I2S not exposed — analog audio available via jacks |
| Camera HATs | ✅ Yes | Via 22-pin FPC CSI connectors |
| Relay HATs (GPIO) | ✅ Yes | Full compatibility |
| LED HATs (SPI/I2C) | ✅ Yes | Full compatibility |
| NVMe/SSD HATs | ❌ No | Requires PCIe — not available |
| USB HATs | ⚠️ Partial | USB available via UNO Q USB-C, not 40-pin header |

---

## Voltage Levels

The RPi 5 40-pin header operates at 3.3V logic. The UNO Q carrier meets this:

- STM32U585 GPIO: native 3.3V — direct connection
- QRB2210 MPU GPIO: 1.8V native → level shifted to 3.3V via TXS0108E

**Do not apply 5V logic to any 40-pin header GPIO pin.**

---

## HAT ID EEPROM

Full RPi HAT specification compliance requires a 24C32 or compatible I2C EEPROM
on pins 27 (ID_SD) and 28 (ID_SC) with 4.7kΩ pullups to 3.3V.

The carrier includes this EEPROM. HAT identification will function correctly for
HATs that query the ID bus.

---

## References

- Raspberry Pi HAT specification: https://github.com/raspberrypi/hats
- Raspberry Pi 5 GPIO pinout: https://pinout.xyz
- QRB2210 datasheet: https://docs.qualcomm.com/bundle/publicresource/80-30843-1
