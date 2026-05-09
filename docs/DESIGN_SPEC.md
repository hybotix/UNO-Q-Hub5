# UNO Q HUB75 Project — Design Specification

**Hybrid RobotiX** — Dale Weber
**Revision:** 0.3
**Date:** 2026-05-08
**Status:** APPROVED

---

## Project Overview

Two hardware products for HUB75 RGB LED matrix driving, QSPI display,
and I2S audio on the Arduino UNO Q platform:

| Board | Description | Build Order |
|-------|-------------|-------------|
| **UNO Q HUB75 Shield** | Arduino UNO form-factor shield | First |
| **UNO Q Super Carrier** | Full development carrier | Second |

---

## ESP32-S3 — Co-Processor Role (No Wireless)

**The ESP32-S3 is a dedicated co-processor. It has no wireless role.**

All wireless (WiFi 6, BLE 5, Thread, Matter, Zigbee) is handled exclusively
by the ESP32-C6. The S3's onboard PCB antenna is non-functional by design.
The C6 antenna keepout is the only one requiring strict PCB enforcement.

### S3 Co-Processor Functions

| Function | Interface | Notes |
|----------|-----------|-------|
| HUB75 LED panel driver | 13 GPIO → 74HCT245 ×2 → IDC | DMA via ESP32-HUB75-MatrixPanel-DMA |
| 5" TFT display driver | 4-wire SPI (SPI2/LCD_CAM) | 80MHz, LVGL partial rendering |
| I2S audio processor | 4 GPIO → ES8388 | I2S master |
| SPI slave to UNO Q | SPI3, 1–2 CS lines | STM32U585 and/or QRB2210 masters |
| I2C master | GPIO8/9 shared bus | ES8388 control + GT911 touch |
| USB debug | GPIO19/20 | CDC/JTAG — replaces UART0 |

---

## Module: ESP32-S3-WROOM-1-N16R8

### Selection Rationale

| Candidate | Verdict | Reason |
|-----------|---------|--------|
| ESP32-S3-MINI-1 | ❌ Rejected | No PSRAM — cannot buffer 5" display |
| ESP32-S3-WROOM-1-N8R8 | ⚠️ Marginal | 8MB flash too small for full firmware stack |
| **ESP32-S3-WROOM-1-N16R8** | ✅ **Selected** | 16MB flash, 8MB PSRAM, VDD_SPI=3.3V |
| ESP32-S3-WROOM-1-N16R16V | ❌ Rejected | VDD_SPI=1.8V — GPIO47/48 incompatible with 3.3V HUB75 |
| ESP32-S3-WROOM-2-N32R16V | ❌ Rejected | Same VDD_SPI=1.8V issue on GPIO47/48 |

### Module Specifications

| Parameter | Value |
|-----------|-------|
| Part number | ESP32-S3-WROOM-1-N16R8 |
| Flash | 16MB Quad SPI |
| PSRAM | 8MB Octal SPI (in-package, ESP32-S3R8) |
| Internal SRAM | 512KB |
| Castellated pads | 36 |
| Usable GPIO | **33** (GPIO35/36/37 consumed by PSRAM internally) |
| VDD_SPI | 3.3V — GPIO47/48 safe at 3.3V |
| Dimensions | 18.0 × 25.5 × 3.1mm |
| Antenna | PCB trace — **non-functional, C6 handles all RF** |
| Alternate PN | ESP32-S3-WROOM-1U-N16R8 (U.FL) — drop-in substitute |

### PSRAM Constraint — Critical Design Note

The ESP32-S3R8 chip uses octal SPI for its in-package PSRAM.
**GPIO35, GPIO36, and GPIO37 are hardwired to the PSRAM internally.**
They appear as castellated pads on the module edge but cannot be used
as general-purpose GPIO. Treat as NC on the carrier PCB.

### PSRAM Memory Budget

| Use | Size |
|-----|------|
| Full 800×480 16bpp frame buffer | 768KB |
| LVGL heap (partial rendering) | 512KB |
| Audio DMA ring buffers | 64KB |
| Application heap | ~6.7MB remaining |

---

## GPIO Allocation — Shield (Verified: 32 used, 1 spare)

OE on both 74HCT245s is tied permanently LOW in hardware (0Ω to GND
at pin 19). No GPIO required for OE.

UART0 (GPIO43/44 default) is superseded by USB CDC on GPIO19/20.
GPIO43/44 are reassigned to the display SPI bus.

| GPIO | Signal | Direction | Peripheral |
|------|--------|-----------|------------|
| 0 | — | — | **NC on shield** (used on carrier for CS_S3_MPU) |
| 1 | HUB75_R1 | OUT | 74HCT245 U2 |
| 2 | HUB75_G1 | OUT | 74HCT245 U2 |
| 3 | HUB75_B1 | OUT | 74HCT245 U2 |
| 4 | HUB75_R2 | OUT | 74HCT245 U2 |
| 5 | I2S_BCLK | OUT | ES8388 |
| 6 | I2S_LRCLK | OUT | ES8388 |
| 7 | I2S_DOUT | OUT | ES8388 DAC |
| 8 | I2C_SDA | BIDIR | ES8388 + GT911 (shared) |
| 9 | I2C_SCL | OUT | ES8388 + GT911 (shared) |
| 10 | CS_S3_MCU | IN | SPI3 slave — STM32U585 CS |
| 11 | LCD_CS | OUT | SPI2 display |
| 12 | SPI_MISO | OUT | SPI3 slave |
| 13 | SPI_MOSI | IN | SPI3 slave |
| 14 | SPI_SCK | IN | SPI3 slave |
| 15 | I2S_DIN | IN | ES8388 ADC |
| 16 | LCD_DC | OUT | SPI2 display — Data/Command |
| 17 | LCD_CLK | OUT | SPI2 display — SPI clock |
| 18 | LCD_MOSI | OUT | SPI2 display — pixel data |
| 19 | USB_D- | BIDIR | USB CDC/JTAG |
| 20 | USB_D+ | BIDIR | USB CDC/JTAG |
| 21 | HUB75_G2 | OUT | 74HCT245 U2 |
| 33 | HUB75_CLK | OUT | 74HCT245 U2 |
| 34 | HUB75_LAT | OUT | 74HCT245 U2 |
| 35 | *** NC *** | — | PSRAM internal — do not connect |
| 36 | *** NC *** | — | PSRAM internal — do not connect |
| 37 | *** NC *** | — | PSRAM internal — do not connect |
| 38 | HUB75_ADDR_A | OUT | 74HCT245 U3 |
| 39 | HUB75_ADDR_B | OUT | 74HCT245 U3 |
| 40 | HUB75_ADDR_C | OUT | 74HCT245 U3 |
| 41 | HUB75_ADDR_D | OUT | 74HCT245 U3 |
| 42 | HUB75_ADDR_E | OUT | 74HCT245 U3 |
| 43 | LCD_RST / TOUCH_RST | OUT | Display + GT911 (shared reset) |
| 44 | TOUCH_INT | IN | GT911 (input-only GPIO) |
| 45 | HUB75_B2 | OUT | 74HCT245 U2 |
| 46 | LCD_BL_PWM | OUT | Backlight — LEDC peripheral |
| 47 | UART_DEBUG_TX | OUT | **Spare — 2-pin debug header on shield** |
| 48 | — | — | **Spare — available** |

### GPIO Count Verification

| Function | Count | GPIOs |
|----------|-------|-------|
| HUB75 RGB data (R1,G1,B1,R2,G2,B2) | 6 | 1,2,3,4,21,45 |
| HUB75 timing (CLK,LAT) | 2 | 33,34 |
| HUB75 address (ADDR_A–E) | 5 | 38,39,40,41,42 |
| HUB75 OE | 0 | **Tied LOW at 74HCT245** |
| I2S audio (BCLK,LRCLK,DOUT,DIN) | 4 | 5,6,7,15 |
| I2C shared bus (SDA,SCL) | 2 | 8,9 |
| SPI3 slave (MOSI,MISO,SCK,CS_MCU) | 4 | 10,12,13,14 |
| USB CDC/JTAG (D+,D-) | 2 | 19,20 |
| SPI2 display (CLK,MOSI,CS,DC) | 4 | 11,16,17,18 |
| Display+Touch RST (shared) | 1 | 43 |
| Touch INT | 1 | 44 |
| Backlight PWM | 1 | 46 |
| **Total required** | **32** | |
| **Usable on WROOM-1-N16R8** | **33** | |
| **Spare** | **1** | GPIO47 (debug TX) |
| **Available** | **1** | GPIO48 |

---

## GPIO Allocation — Super Carrier Additions

The carrier adds CS_S3_MPU (QRB2210 chip select) and the S3↔C6 direct
UART link. These use GPIO0 and the two spare GPIOs from the shield map.

### Boot Constraint on GPIO0
GPIO0 is a strapping pin. It must be HIGH at boot for normal operation.
CS_S3_MPU is active-LOW and pulled HIGH by a 10kΩ resistor to +3V3.
At power-on, CS_S3_MPU is deasserted (HIGH), satisfying the GPIO0
strapping requirement. This is safe and a well-established pattern.

| GPIO | Signal | Direction | Notes |
|------|--------|-----------|-------|
| 0 | CS_S3_MPU | IN | SPI3 slave — QRB2210 CS. 10kΩ pullup to +3V3. Boot-safe. |
| 47 | S3_C6_TX | OUT | Direct UART to ESP32-C6 RX (GPIO4) |
| 48 | S3_C6_RX | IN | Direct UART from ESP32-C6 TX (GPIO5) |

**Carrier total: 35 GPIOs used (32 base + GPIO0 + GPIO47 + GPIO48).**
**Carrier usable: 33 + GPIO0 = 34. Over by 1.**

### Carrier Resolution

On the carrier, the S3↔C6 UART is bidirectional — both TX and RX are
needed. That requires GPIO47 + GPIO48 = 2 GPIOs. Plus CS_S3_MPU on
GPIO0. Total carrier demand = 35. Available = 34 (33 + GPIO0).

**Resolution: Drop S3_C6_RX on the carrier.**

The S3 sends data TO the C6 (display events, sensor triggers).
The C6 sends data TO the S3 (WiFi status, MQTT payloads to display).
The return path (C6→S3) is already covered by the SPI slave bus —
the C6 can assert CS_C6 to drive the S3's SPI3 slave directly.

**S3↔C6 communication model:**
- S3→C6: UART TX (GPIO47) — fast unidirectional push
- C6→S3: SPI slave CS_C6_MCU line (QRB2210 or STM32U585 mediates)

This eliminates the need for GPIO48 on the carrier as a UART RX line.
GPIO48 remains spare on both shield and carrier.

**Final carrier GPIO count: 34 used, 0 spare on WROOM-1-N16R8+GPIO0.**

---

## Display Interface — 5" TFT with Capacitive Touch

### Interface Specification

| Parameter | Value |
|-----------|-------|
| Bus | 4-wire SPI via SPI2 (LCD_CAM peripheral) |
| Max clock | 80MHz |
| Throughput | ~10MB/s |
| Frame rate | ~13fps full frame; smooth UI with LVGL partial rendering |
| Connector | 22-pin 0.5mm FPC (Molex 503480-2200 family) |
| Touch controller | GT911 (5-point capacitive, I2C, 100Hz) |
| Touch bus | Shared I2C (GPIO8/9) + INT (GPIO44) |
| Touch RST | Shared with LCD_RST on GPIO43 |
| Backlight | PWM via GPIO46 (LEDC), power from +5V_EXT |

### Target Display Modules

Any 5" 800×480 SPI TFT with GT911 capacitive touch and 22-pin FPC.
Primary target: Waveshare 5" SPI LCD 800×480 + GT911 cap touch.
Secondary target: BuyDisplay ER-TFTM050 series with SPI interface.

### Display Connector Pinout (22-pin 0.5mm FPC)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | GND | |
| 2 | +3V3 | Display logic supply |
| 3 | LCD_CLK | SPI2 clock (GPIO17) |
| 4 | LCD_MOSI | SPI2 data (GPIO18) |
| 5 | LCD_CS | SPI2 chip select (GPIO11) |
| 6 | LCD_DC | Data/Command (GPIO16) |
| 7 | LCD_RST | Shared with TOUCH_RST (GPIO43) |
| 8 | LCD_BL_PWM | Backlight PWM (GPIO46) |
| 9 | TOUCH_INT | GT911 interrupt (GPIO44, input-only) |
| 10 | I2C_SDA | GT911 touch data (GPIO8, shared) |
| 11 | I2C_SCL | GT911 touch clock (GPIO9, shared) |
| 12 | GND | |
| 13 | +5V_BL | Backlight LED supply (from +5V_EXT) |
| 14 | GND | |
| 15–22 | NC | Reserved |

### Jumper Select (JP1/JP2)

Two 0Ω resistor footprints (2.54mm pads, jumper-compatible) on the
SPI data path allow future QSPI upgrade if GPIO budget permits:

| Jumper | Position | Mode |
|--------|----------|------|
| JP1 | Closed (default) | 4-wire SPI |
| JP2 | Open (default) | QSPI D1/D2 path — DNP |

---

## Audio Interface — ES8388

| Parameter | Value |
|-----------|-------|
| Codec | ES8388 (24-bit stereo I2S) |
| S3 role | I2S master |
| Sample rate | Up to 96kHz |
| Control | I2C (GPIO8/9, shared with GT911) |
| Output | Stereo line-level, 1×4 2.54mm header |
| Input | PDM/I2S digital mic, 1×4 2.54mm header |
| AVDD | Filtered from +3V3 via FB1 (600Ω@100MHz ferrite) |
| AGND | Star point at U5 — separate pour from DGND |

---

## HUB75 Driver

```
ESP32-S3 (3.3V GPIO) → 74HCT245 ×2 (3.3V→5V) → HUB75 2×8 IDC → Panel
```

| IC | Function | Signals |
|----|----------|---------|
| U2 (SN74HCT245PW) | RGB + timing | R1,G1,B1,R2,G2,B2,CLK,LAT |
| U3 (SN74HCT245PW) | Address | ADDR_A,ADDR_B,ADDR_C,ADDR_D,ADDR_E + 3 NC |

Both ICs: DIR tied LOW (A→B), ~OE tied LOW (always enabled) via 0Ω to GND.
VCC = +5V_EXT_HUB75. No GPIO consumed for OE or DIR.

---

## SPI Bus Architecture

| CS Signal | GPIO | Active On | SPI Controller |
|-----------|------|-----------|----------------|
| CS_S3_MCU | GPIO10 | Shield + Carrier | SPI3 |
| CS_S3_MPU | GPIO0 | Carrier only | SPI3 |
| CS_C6_MCU | — | Carrier only | C6 SPI slave |
| CS_C6_MPU | — | Carrier only | C6 SPI slave |

---

## Wireless Architecture

| Capability | Owner | Notes |
|-----------|-------|-------|
| WiFi 6 (802.11ax) | ESP32-C6 | Carrier only |
| BLE 5.0 | ESP32-C6 | Carrier only |
| Thread (802.15.4) | ESP32-C6 | Carrier only |
| Matter | ESP32-C6 | Carrier only |
| Zigbee | ESP32-C6 | Carrier only |
| **S3 WiFi/BLE** | **Unused** | Module present, antenna non-functional by design |

---

## S3 ↔ C6 Direct Link (Carrier)

| Direction | Path | GPIO |
|-----------|------|------|
| S3 → C6 | UART TX (unidirectional) | S3: GPIO47, C6: GPIO4 |
| C6 → S3 | SPI3 slave (C6 asserts CS_C6 via UNO Q) | Existing SPI bus |

---

## Power Architecture

| Rail | Source | Voltage | Max Current | Used For |
|------|--------|---------|-------------|----------|
| +5V_EXT | Barrel jack J4 | 5.0V | 5A | HUB75 panel, backlight |
| +5V_EXT_HUB75 | Direct from J4 | 5.0V | 3A | 74HCT245 VCC, HUB75 IDC |
| +5V_BL | Direct from J4 | 5.0V | 200mA | Display backlight LED |
| +3V3 | AMS1117-3.3 | 3.3V | 800mA | S3, ES8388, level shifters |
| AVDD | +3V3 via FB1 | 3.3V | 50mA | ES8388 analog supply |
| DGND | GND plane (L2) | 0V | — | All digital returns |
| AGND | Separate pour | 0V | — | ES8388 analog only, star at U5 |

---

## Qwiic + Grove (both boards)

| Connector | Count | Interface | Source | Pullups |
|-----------|-------|-----------|--------|---------|
| Qwiic (JST-SH 1.0mm) | 2 | I2C | STM32U585 | 4.7kΩ to +3V3 |
| Grove I2C (2.0mm) | 1 | I2C | STM32U585 | — |
| Grove UART (2.0mm) | 1 | UART | STM32U585 | — |
| Grove SPI (2.0mm) | 1 | SPI | STM32U585 | — |
| Grove Digital (2.0mm) | 1 | GPIO | STM32U585 | — |
| Grove Analog (2.0mm) | 1 | ADC | STM32U585 | — |

---

## Revision History

| Rev | Date | Notes |
|-----|------|-------|
| 0.1 | 2026-05-08 | Initial |
| 0.2 | 2026-05-08 | ES8388 codec, ESP32-C6 carrier-only, S3↔C6 UART, hierarchical schematics |
| 0.3 | 2026-05-08 | **Major update.** Module: MINI-1 → WROOM-1-N16R8 (8MB PSRAM). S3 defined as pure co-processor — no wireless role. GPIO35/36/37 consumed by PSRAM — full GPIO remapping. 74HCT245 OE tied LOW in hardware (no GPIO). USB CDC replaces UART0. Display: 4-wire SPI via SPI2/LCD_CAM, 80MHz, GT911 cap touch on shared I2C, 22-pin FPC. GPIO0 on carrier for CS_S3_MPU (boot-safe with 10kΩ pullup). S3→C6 UART TX on GPIO47 (unidirectional). Final verified: shield 32 GPIO used / 1 spare; carrier 34 GPIO used / 0 spare. |
