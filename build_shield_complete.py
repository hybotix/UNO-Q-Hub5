#!/usr/bin/env python3
"""
UNO Q HUB75 Shield Schematic Generator
Generates all 8 shield schematics with complete component lists from BOM
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from kicad10_builder import Schematic, RootSchematic, Component, HierarchicalLabel

# Shield root UUID (stable across regenerations)
SHIELD_ROOT_UUID = "bc84562d-846a-4607-81a1-500b7991d137"

# Sheet UUIDs (stable)
SHEET_UUIDS = {
    "power": "efaa96f4-7a06-4df5-bf2b-8bbb82a448c8",
    "esp32s3": "02ac644c-33d8-477e-a8a6-71ca0780d582",
    "hub75": "1f2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e",
    "audio": "2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d",
    "display": "3b4c5d6e-7f8a-9b0c-1d2e-3f4a5b6c7d8e",
    "uno_if": "4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f",
    "connect": "5d6e7f8a-9b0c-1d2e-3f4a-5b6c7d8e9f0a",
}

def build_power_sheet():
    """Build shield power.kicad_sch with LDO, caps, indicators."""
    sch = Schematic("power.kicad_sch", "Power", SHEET_UUIDS["power"])
    
    # Barrel jack input
    sch.add_component(Component("J4", "HybotixParts:BarrelJack_5V", "DC +5V IN", 10, 20,
                                footprint="Connector_BarrelJack:BarrelJack_CUI_PJ-102AH_Horizontal"))
    
    # Input bulk caps
    sch.add_component(Component("C1", "Device:C", "100µF", 20, 20,
                                footprint="Capacitor_SMD:C_1206_3216Metric"))
    sch.add_component(Component("C2", "Device:C", "100nF", 25, 20,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # AMS1117-3.3 LDO
    sch.add_component(Component("U4", "HybotixParts:AMS1117-3.3", "AMS1117-3.3", 35, 20,
                                footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2"))
    
    # Output caps
    sch.add_component(Component("C3", "Device:C", "10µF", 45, 20,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C4", "Device:C", "10µF", 50, 20,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C5", "Device:C", "100nF", 55, 20,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # EN and GPIO0 pullups
    sch.add_component(Component("R10", "Device:R", "10kΩ", 60, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R11", "Device:R", "10kΩ", 60, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # LED indicators
    sch.add_component(Component("D1", "Device:LED", "Green LED", 70, 15,
                                footprint="LED_SMD:LED_0402_1005Metric"))
    sch.add_component(Component("R1", "Device:R", "620Ω", 75, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("D2", "Device:LED", "Green LED", 70, 25,
                                footprint="LED_SMD:LED_0402_1005Metric"))
    sch.add_component(Component("R2", "Device:R", "270Ω", 75, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Outputs
    sch.add_label(HierarchicalLabel("+5V_EXT", "output", 85, 20))
    sch.add_label(HierarchicalLabel("+5V_EXT_HUB75", "output", 85, 25))
    sch.add_label(HierarchicalLabel("+3V3", "output", 85, 30))
    sch.add_label(HierarchicalLabel("DGND", "output", 85, 35))
    sch.add_label(HierarchicalLabel("AGND", "output", 85, 40))
    sch.add_label(HierarchicalLabel("AVDD", "output", 85, 45))
    
    return sch

def build_esp32s3_sheet():
    """Build shield esp32s3.kicad_sch with WROOM-1 module, USB, pullups."""
    sch = Schematic("esp32s3.kicad_sch", "ESP32-S3", SHEET_UUIDS["esp32s3"])
    
    # ESP32-S3-WROOM-1-N16R8 module
    sch.add_component(Component("U1", "HybotixParts:ESP32-S3-WROOM-1-N16R8", 
                                "ESP32-S3-WROOM-1-N16R8", 30, 30,
                                footprint="Package_BGA:ESP32-S3-WROOM-1_18x25.5mm_P0.5mm"))
    
    # Decoupling caps
    sch.add_component(Component("C10", "Device:C", "100nF", 20, 30,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    sch.add_component(Component("C11", "Device:C", "10µF", 25, 30,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    
    # USB-C connector
    sch.add_component(Component("J5", "HybotixParts:USB_C_Receptacle", "USB-C Debug", 60, 30,
                                footprint="Connector_USB:USB_C_Receptacle_GCT_USB4135-GF-A_Horizontal"))
    
    # Pullups
    sch.add_component(Component("R12", "Device:R", "5.1kΩ", 65, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R13", "Device:R", "5.1kΩ", 65, 35,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Inputs
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 30))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 35))
    
    # Outputs to other sheets
    sch.add_label(HierarchicalLabel("SPI_MOSI", "output", 50, 15))
    sch.add_label(HierarchicalLabel("SPI_MISO", "output", 50, 20))
    sch.add_label(HierarchicalLabel("SPI_SCK", "output", 50, 25))
    sch.add_label(HierarchicalLabel("CS_S3_MCU", "output", 50, 30))
    
    return sch

def build_hub75_driver_sheet():
    """Build shield hub75_driver.kicad_sch with SN74HCT245 level shifters."""
    sch = Schematic("hub75_driver.kicad_sch", "HUB75 Driver", SHEET_UUIDS["hub75"])
    
    # Level shifter U2 (RGB + CLK/LAT)
    sch.add_component(Component("U2", "HybotixParts:SN74HCT245PW", "SN74HCT245", 30, 25,
                                footprint="Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"))
    
    # Level shifter U3 (ADDR_A-E)
    sch.add_component(Component("U3", "HybotixParts:SN74HCT245PW", "SN74HCT245", 30, 45,
                                footprint="Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"))
    
    # Decoupling caps
    sch.add_component(Component("C16", "Device:C", "100nF", 20, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    sch.add_component(Component("C17", "Device:C", "100nF", 20, 45,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # HUB75 IDC connector
    sch.add_component(Component("J1", "HybotixParts:HUB75_2x8_IDC", "HUB75 Panel", 60, 35,
                                footprint="Connector_IDC:IDC-Header_2x08_P2.54mm_Vertical"))
    
    # Input/Output
    sch.add_label(HierarchicalLabel("+5V_EXT_HUB75", "input", 10, 30))
    sch.add_label(HierarchicalLabel("HUB75_RGB", "input", 10, 40))
    sch.add_label(HierarchicalLabel("HUB75_CTRL", "input", 10, 50))
    
    return sch

def build_audio_codec_sheet():
    """Build shield audio_codec.kicad_sch with ES8388."""
    sch = Schematic("audio_codec.kicad_sch", "Audio Codec", SHEET_UUIDS["audio"])
    
    # ES8388 codec
    sch.add_component(Component("U5", "HybotixParts:ES8388", "ES8388", 30, 30,
                                footprint="Package_QFP:LQFP-48_7x7mm_P0.5mm"))
    
    # AGND star point (note: actual star via implemented in PCB layout)
    
    # AVDD filtering (ferrite + caps)
    sch.add_component(Component("FB1", "Device:R", "BLM15AX601SN1D", 15, 20,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("C6", "Device:C", "10µF", 20, 20,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C7", "Device:C", "100nF", 25, 20,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # DVDD
    sch.add_component(Component("C8", "Device:C", "10µF", 20, 30,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C9", "Device:C", "100nF", 25, 30,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # I2C pullups
    sch.add_component(Component("R3", "Device:R", "1kΩ", 50, 30,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R4", "Device:R", "1kΩ", 55, 30,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Audio outputs
    sch.add_component(Component("C12", "Device:C", "10µF", 60, 20,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C13", "Device:C", "10µF", 65, 20,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("J_OUT", "Connector:Conn_1x04_Pin", "LINE OUT", 75, 20,
                                footprint="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"))
    sch.add_component(Component("J_MIC", "Connector:Conn_1x04_Pin", "MIC IN", 75, 30,
                                footprint="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"))
    
    # Inputs
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("AGND", "input", 10, 35))
    sch.add_label(HierarchicalLabel("I2S_BCLK", "input", 10, 40))
    sch.add_label(HierarchicalLabel("I2S_LRCLK", "input", 10, 45))
    sch.add_label(HierarchicalLabel("I2S_DOUT", "input", 10, 50))
    sch.add_label(HierarchicalLabel("I2C_SDA", "input", 10, 55))
    sch.add_label(HierarchicalLabel("I2C_SCL", "input", 10, 60))
    
    return sch

def build_display_sheet():
    """Build shield display.kicad_sch with FPC connector and GT911 touch."""
    sch = Schematic("display.kicad_sch", "Display", SHEET_UUIDS["display"])
    
    # FPC connector for display
    sch.add_component(Component("J6", "HybotixParts:FPC_22pin_0.5mm", "FPC 22-pin", 30, 30,
                                footprint="Connector_FPC:Molex_503480-2200_22pin_P0.5mm_Vertical"))
    
    # GT911 pullups
    sch.add_component(Component("R20", "Device:R", "4.7kΩ", 50, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R21", "Device:R", "4.7kΩ", 55, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # SPI mode select jumper
    sch.add_component(Component("JP1", "Device:R", "0Ω", 60, 30,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Inputs
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("+5V_BL", "input", 10, 30))
    sch.add_label(HierarchicalLabel("LCD_CLK", "input", 10, 35))
    sch.add_label(HierarchicalLabel("LCD_MOSI", "input", 10, 40))
    sch.add_label(HierarchicalLabel("LCD_CS", "input", 10, 45))
    sch.add_label(HierarchicalLabel("LCD_DC", "input", 10, 50))
    sch.add_label(HierarchicalLabel("LCD_RST", "input", 10, 55))
    sch.add_label(HierarchicalLabel("LCD_BL_PWM", "input", 10, 60))
    sch.add_label(HierarchicalLabel("I2C_SDA", "input", 10, 65))
    sch.add_label(HierarchicalLabel("I2C_SCL", "input", 10, 70))
    sch.add_label(HierarchicalLabel("TOUCH_INT", "input", 10, 75))
    
    return sch

def build_uno_q_interface_sheet():
    """Build shield uno_q_interface.kicad_sch with SPI3 and UART debug."""
    sch = Schematic("uno_q_interface.kicad_sch", "UNO Q Interface", SHEET_UUIDS["uno_if"])
    
    # SPI3 header
    sch.add_component(Component("J2", "Connector:Conn_1x06_Pin", "SPI3", 30, 25,
                                footprint="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical"))
    
    # UART debug header
    sch.add_component(Component("J3", "Connector:Conn_1x02_Pin", "UART", 50, 25,
                                footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"))
    
    # Inputs (from UNO Q side)
    sch.add_label(HierarchicalLabel("SPI_MOSI", "input", 10, 20))
    sch.add_label(HierarchicalLabel("SPI_MISO", "input", 10, 25))
    sch.add_label(HierarchicalLabel("SPI_SCK", "input", 10, 30))
    sch.add_label(HierarchicalLabel("CS_S3_MCU", "input", 10, 35))
    sch.add_label(HierarchicalLabel("GPIO47", "input", 10, 40))
    
    return sch

def build_connectivity_sheet():
    """Build shield connectivity.kicad_sch with Qwiic and Grove."""
    sch = Schematic("connectivity.kicad_sch", "Connectivity", SHEET_UUIDS["connect"])
    
    # Qwiic connectors
    sch.add_component(Component("J8", "HybotixParts:Qwiic_JST_SH_4", "Qwiic", 30, 20,
                                footprint="Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.0mm_Vertical"))
    sch.add_component(Component("J9", "HybotixParts:Qwiic_JST_SH_4", "Qwiic", 40, 20,
                                footprint="Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.0mm_Vertical"))
    
    # Qwiic pullups
    sch.add_component(Component("R5", "Device:R", "4.7kΩ", 50, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R6", "Device:R", "4.7kΩ", 55, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Grove connectors
    sch.add_component(Component("J10", "HybotixParts:Grove_4pin", "Grove", 30, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J11", "HybotixParts:Grove_4pin", "Grove", 40, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J12", "HybotixParts:Grove_4pin", "Grove", 50, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J13", "HybotixParts:Grove_4pin", "Grove", 60, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J14", "HybotixParts:Grove_4pin", "Grove", 70, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    
    # I2C bus
    sch.add_label(HierarchicalLabel("I2C_SDA", "input", 10, 20))
    sch.add_label(HierarchicalLabel("I2C_SCL", "input", 10, 25))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 30))
    
    return sch

def build_shield_root():
    """Build root schematic linking all 8 shield sub-sheets."""
    root = RootSchematic("uno_q_hub75_shield.kicad_sch", "UNO Q HUB75 Shield",
                         SHIELD_ROOT_UUID, "uno_q_hub75_shield")
    
    root.add_sheet("Power", "sheets/power.kicad_sch", SHEET_UUIDS["power"],
                   {"+5V_EXT": "power_out", "+5V_EXT_HUB75": "power_out", "+3V3": "power_out",
                    "DGND": "power_out", "AGND": "power_out", "AVDD": "power_out"})
    
    root.add_sheet("ESP32-S3", "sheets/esp32s3.kicad_sch", SHEET_UUIDS["esp32s3"],
                   {"+3V3": "power_in", "DGND": "power_in", "SPI_MOSI": "output",
                    "SPI_MISO": "output", "SPI_SCK": "output", "CS_S3_MCU": "output"})
    
    root.add_sheet("HUB75 Driver", "sheets/hub75_driver.kicad_sch", SHEET_UUIDS["hub75"],
                   {"+5V_EXT_HUB75": "power_in", "HUB75_RGB": "input", "HUB75_CTRL": "input"})
    
    root.add_sheet("Audio Codec", "sheets/audio_codec.kicad_sch", SHEET_UUIDS["audio"],
                   {"+3V3": "power_in", "AGND": "power_out", "I2S_BCLK": "input",
                    "I2S_LRCLK": "input", "I2S_DOUT": "input", "I2C_SDA": "bidirectional",
                    "I2C_SCL": "bidirectional"})
    
    root.add_sheet("Display", "sheets/display.kicad_sch", SHEET_UUIDS["display"],
                   {"+3V3": "power_in", "+5V_BL": "power_in", "LCD_CLK": "input",
                    "LCD_MOSI": "input", "LCD_CS": "input", "LCD_DC": "input",
                    "LCD_RST": "input", "LCD_BL_PWM": "input", "I2C_SDA": "bidirectional",
                    "I2C_SCL": "bidirectional", "TOUCH_INT": "input"})
    
    root.add_sheet("UNO Q Interface", "sheets/uno_q_interface.kicad_sch", SHEET_UUIDS["uno_if"],
                   {"SPI_MOSI": "input", "SPI_MISO": "input", "SPI_SCK": "input",
                    "CS_S3_MCU": "input", "GPIO47": "input"})
    
    root.add_sheet("Connectivity", "sheets/connectivity.kicad_sch", SHEET_UUIDS["connect"],
                   {"I2C_SDA": "bidirectional", "I2C_SCL": "bidirectional", "+3V3": "power_in"})
    
    return root

def main():
    """Generate all shield schematics."""
    basedir = Path("/home/claude/UNO-Q-Hub5/KiCad/shield")
    basedir.mkdir(parents=True, exist_ok=True)
    (basedir / "sheets").mkdir(exist_ok=True)
    
    print("Building UNO Q HUB75 Shield Schematics")
    print("=" * 50)
    
    # Build sub-sheets
    print("\nSub-sheets:")
    build_power_sheet().save(str(basedir / "sheets/power.kicad_sch"))
    build_esp32s3_sheet().save(str(basedir / "sheets/esp32s3.kicad_sch"))
    build_hub75_driver_sheet().save(str(basedir / "sheets/hub75_driver.kicad_sch"))
    build_audio_codec_sheet().save(str(basedir / "sheets/audio_codec.kicad_sch"))
    build_display_sheet().save(str(basedir / "sheets/display.kicad_sch"))
    build_uno_q_interface_sheet().save(str(basedir / "sheets/uno_q_interface.kicad_sch"))
    build_connectivity_sheet().save(str(basedir / "sheets/connectivity.kicad_sch"))
    
    # Build root
    print("\nRoot schematic:")
    build_shield_root().save(str(basedir / "uno_q_hub75_shield.kicad_sch"))
    
    print("\n✓ Shield schematics complete")

if __name__ == "__main__":
    main()
