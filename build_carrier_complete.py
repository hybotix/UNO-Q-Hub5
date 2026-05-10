#!/usr/bin/env python3
"""
UNO Q Super Carrier Schematic Generator
Generates all 8 carrier schematics with complete component lists from BOM
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from kicad10_builder import Schematic, RootSchematic, Component, HierarchicalLabel

# Carrier root UUID (stable across regenerations)
CARRIER_ROOT_UUID = "a7d62ed3-8e95-4e64-b6df-722c91664a1a"

# Sheet UUIDs (stable)
SHEET_UUIDS = {
    "power": "c1d2e3f4-5a6b-7c8d-9e0f-1a2b3c4d5e6f",
    "mounting": "d2e3f4a5-6b7c-8d9e-0f1a-2b3c4d5e6f7a",
    "esp32c6": "e3f4a5b6-7c8d-9e0f-1a2b-3c4d5e6f7a8b",
    "display": "f4a5b6c7-8d9e-0f1a-2b3c-4d5e6f7a8b9c",
    "rpi5": "a5b6c7d8-9e0f-1a2b-3c4d-5e6f7a8b9c0d",
    "level": "b6c7d8e9-0f1a-2b3c-4d5e-6f7a8b9c0d1e",
    "expand": "c7d8e9f0-1a2b-3c4d-5e6f-7a8b9c0d1e2f",
}

def build_carrier_power_sheet():
    """Build carrier power.kicad_sch with TPS54331 buck and dual VIN."""
    sch = Schematic("power.kicad_sch", "Power", SHEET_UUIDS["power"])
    
    # TPS54331 buck converter
    sch.add_component(Component("U7", "HybotixParts:TPS54331DR", "TPS54331DR", 30, 30,
                                footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"))
    
    # Input caps (dual VIN support)
    sch.add_component(Component("C18", "Device:C", "100µF", 15, 25,
                                footprint="Capacitor_SMD:C_1206_3216Metric"))
    sch.add_component(Component("C19", "Device:C", "100µF", 20, 25,
                                footprint="Capacitor_SMD:C_1206_3216Metric"))
    
    # Output caps
    sch.add_component(Component("C22", "Device:C", "100µF", 40, 30,
                                footprint="Capacitor_SMD:C_1206_3216Metric"))
    sch.add_component(Component("C23", "Device:C", "100nF", 45, 30,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # Feedback divider
    sch.add_component(Component("R_P1", "Device:R", "100kΩ", 50, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R_P2", "Device:R", "100kΩ", 55, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Soft-start
    sch.add_component(Component("C24", "Device:C", "4.7µF", 60, 30,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    
    # AMS1117 for low-current rail
    sch.add_component(Component("U8", "HybotixParts:AMS1117-3.3", "AMS1117-3.3", 70, 30,
                                footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2"))
    
    # LDO bypass
    sch.add_component(Component("C25", "Device:C", "10µF", 75, 25,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    sch.add_component(Component("C26", "Device:C", "100nF", 80, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # Outputs
    sch.add_label(HierarchicalLabel("VIN_7_24V", "input", 10, 20))
    sch.add_label(HierarchicalLabel("+5V", "output", 85, 30))
    sch.add_label(HierarchicalLabel("+3V3", "output", 85, 35))
    sch.add_label(HierarchicalLabel("DGND", "output", 85, 40))
    
    return sch

def build_mounting_sheet():
    """Build carrier uno_q_mounting.kicad_sch with Samtec mezzanine connectors."""
    sch = Schematic("uno_q_mounting.kicad_sch", "UNO Q Mounting", SHEET_UUIDS["mounting"])
    
    # Samtec FTSH-130-01 mezzanine connectors
    sch.add_component(Component("B1", "HybotixParts:FTSH-130-01", "JMISC", 30, 25,
                                footprint="Connector_Samtec:Samtec_FTSH-130-01-L-DV-A_2x30_P1.27mm_Vertical"))
    
    sch.add_component(Component("B2", "HybotixParts:FTSH-130-01", "JMEDIA", 50, 25,
                                footprint="Connector_Samtec:Samtec_FTSH-130-01-L-DV-A_2x30_P1.27mm_Vertical"))
    
    # Power
    sch.add_label(HierarchicalLabel("+5V", "input", 10, 20))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 30))
    
    # SPI/I2C from shield
    sch.add_label(HierarchicalLabel("CS_S3_MPU", "input", 10, 40))
    sch.add_label(HierarchicalLabel("S3_C6_TX", "output", 70, 20))
    sch.add_label(HierarchicalLabel("S3_C6_RX", "input", 70, 25))
    
    return sch

def build_esp32c6_sheet():
    """Build carrier esp32c6_radio.kicad_sch with C6 module and antenna."""
    sch = Schematic("esp32c6_radio.kicad_sch", "ESP32-C6 Radio", SHEET_UUIDS["esp32c6"])
    
    # ESP32-C6-MINI-1 module
    sch.add_component(Component("U9", "HybotixParts:ESP32-C6-MINI-1", 
                                "ESP32-C6-MINI-1", 30, 30,
                                footprint="Package_BGA:ESP32-C6-MINI-1_18x18.5mm_P0.4mm"))
    
    # Decoupling
    sch.add_component(Component("C27", "Device:C", "100nF", 20, 30,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    sch.add_component(Component("C28", "Device:C", "10µF", 25, 30,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    
    # Antenna selection resistors
    sch.add_component(Component("R_ANT_PCB", "Device:R", "0Ω", 50, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R_ANT_EXT", "Device:R", "DNP", 55, 25,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # U.FL antenna connector
    sch.add_component(Component("J_ANT", "HybotixParts:UFL_Connector", "U.FL", 60, 30,
                                footprint="Connector_Coaxial:HIROSE_UFL_2013_E"))
    
    # USB-C for C6 (optional firmware programming)
    sch.add_component(Component("J_C6_USB", "HybotixParts:USB_C_Receptacle", "C6 USB", 70, 30,
                                footprint="Connector_USB:USB_C_Receptacle_GCT_USB4135-GF-A_Horizontal"))
    
    # Power
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 35))
    
    # UART to S3
    sch.add_label(HierarchicalLabel("S3_C6_TX", "input", 10, 40))
    sch.add_label(HierarchicalLabel("S3_C6_RX", "output", 10, 45))
    
    return sch

def build_display_chain_sheet():
    """Build carrier display_chain.kicad_sch with MIPI switch and HDMI converter."""
    sch = Schematic("display_chain.kicad_sch", "Display Chain", SHEET_UUIDS["display"])
    
    # MIPI DSI to HDMI converter
    sch.add_component(Component("U10", "HybotixParts:LT8618SX", "LT8618SX", 30, 30,
                                footprint="Package_QFP:LQFP-56_10x10mm_P0.5mm"))
    
    # MIPI switch
    sch.add_component(Component("U11", "HybotixParts:CBTL04GP054", "CBTL04GP054", 55, 30,
                                footprint="Package_DFN:DFN-16_3x3mm_P0.5mm"))
    
    # Decoupling
    sch.add_component(Component("C29", "Device:C", "100nF", 20, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    sch.add_component(Component("C30", "Device:C", "10µF", 25, 25,
                                footprint="Capacitor_SMD:C_0805_2012Metric"))
    
    # HDMI output
    sch.add_component(Component("J_HDMI", "HybotixParts:HDMI_Micro_D", "Micro-HDMI", 75, 30,
                                footprint="Connector_HDMI:Molex_47151-2001_Micro-HDMI_Horizontal"))
    
    # MIPI DSI input (FPC)
    sch.add_component(Component("J_DSI", "HybotixParts:FPC_MIPI_DSI", "MIPI DSI", 75, 40,
                                footprint="Connector_FPC:Molex_503480-40_40pin_P0.5mm_Vertical"))
    
    # Power
    sch.add_label(HierarchicalLabel("+5V", "input", 10, 20))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 30))
    
    return sch

def build_rpi5_interface_sheet():
    """Build carrier rpi5_interface.kicad_sch with 40-pin GPIO and HAT EEPROM."""
    sch = Schematic("rpi5_interface.kicad_sch", "RPi5 Interface", SHEET_UUIDS["rpi5"])
    
    # 40-pin GPIO header
    sch.add_component(Component("J_GPIO", "Connector:Conn_2x20_Odd_Even", "GPIO 40-pin", 30, 30,
                                footprint="Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical"))
    
    # HAT EEPROM
    sch.add_component(Component("U12", "HybotixParts:AT24C32", "24C32", 60, 25,
                                footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"))
    
    # EEPROM bypass
    sch.add_component(Component("C31", "Device:C", "100nF", 55, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # EEPROM pullups
    sch.add_component(Component("R22", "Device:R", "4.7kΩ", 65, 20,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R23", "Device:R", "4.7kΩ", 70, 20,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # CSI connectors (camera)
    sch.add_component(Component("J_CSI0", "HybotixParts:FPC_CSI", "CSI0", 70, 35,
                                footprint="Connector_FPC:Molex_503480-30_30pin_P0.5mm_Vertical"))
    sch.add_component(Component("J_CSI1", "HybotixParts:FPC_CSI", "CSI1", 75, 35,
                                footprint="Connector_FPC:Molex_503480-30_30pin_P0.5mm_Vertical"))
    
    # Power
    sch.add_label(HierarchicalLabel("+5V", "input", 10, 20))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 25))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 30))
    
    return sch

def build_level_shift_sheet():
    """Build carrier level_shift.kicad_sch with TXS0108E level shifters."""
    sch = Schematic("level_shift.kicad_sch", "Level Shift", SHEET_UUIDS["level"])
    
    # MPU GPIO to 3.3V level shifters
    sch.add_component(Component("U_LS1", "HybotixParts:TXS0108E", "TXS0108E", 30, 25,
                                footprint="Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"))
    sch.add_component(Component("U_LS2", "HybotixParts:TXS0108E", "TXS0108E", 50, 25,
                                footprint="Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"))
    
    # Decoupling
    sch.add_component(Component("C32", "Device:C", "100nF", 20, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    sch.add_component(Component("C33", "Device:C", "100nF", 40, 25,
                                footprint="Capacitor_SMD:C_0402_1005Metric"))
    
    # Power
    sch.add_label(HierarchicalLabel("VIN_1V8_REF", "input", 10, 20))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 30))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 35))
    
    return sch

def build_expansion_sheet():
    """Build carrier expansion.kicad_sch with Qwiic, Grove, and breakouts."""
    sch = Schematic("expansion.kicad_sch", "Expansion", SHEET_UUIDS["expand"])
    
    # Qwiic connectors
    sch.add_component(Component("J15", "HybotixParts:Qwiic_JST_SH_4", "Qwiic", 30, 20,
                                footprint="Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.0mm_Vertical"))
    sch.add_component(Component("J16", "HybotixParts:Qwiic_JST_SH_4", "Qwiic", 40, 20,
                                footprint="Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.0mm_Vertical"))
    
    # Qwiic pullups
    sch.add_component(Component("R24", "Device:R", "4.7kΩ", 50, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    sch.add_component(Component("R25", "Device:R", "4.7kΩ", 55, 15,
                                footprint="Resistor_SMD:R_0402_1005Metric"))
    
    # Grove connectors
    sch.add_component(Component("J17", "HybotixParts:Grove_4pin", "Grove PSSI", 30, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J18", "HybotixParts:Grove_4pin", "Grove I2C4", 40, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J19", "HybotixParts:Grove_4pin", "Grove", 50, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J20", "HybotixParts:Grove_4pin", "Grove", 60, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    sch.add_component(Component("J21", "HybotixParts:Grove_4pin", "Grove OpAmp", 70, 40,
                                footprint="Connector_Grove:Grove_4pin_Vertical"))
    
    # Power
    sch.add_label(HierarchicalLabel("I2C_SDA", "input", 10, 20))
    sch.add_label(HierarchicalLabel("I2C_SCL", "input", 10, 25))
    sch.add_label(HierarchicalLabel("+3V3", "input", 10, 30))
    sch.add_label(HierarchicalLabel("DGND", "input", 10, 35))
    
    return sch

def build_carrier_root():
    """Build root schematic linking all 7 carrier sub-sheets."""
    root = RootSchematic("uno_q_super_carrier.kicad_sch", "UNO Q Super Carrier",
                         CARRIER_ROOT_UUID, "uno_q_super_carrier")
    
    root.add_sheet("Power", "sheets/power.kicad_sch", SHEET_UUIDS["power"],
                   {"VIN_7_24V": "input", "+5V": "power_out", "+3V3": "power_out", "DGND": "power_out"})
    
    root.add_sheet("UNO Q Mounting", "sheets/uno_q_mounting.kicad_sch", SHEET_UUIDS["mounting"],
                   {"+5V": "power_in", "+3V3": "power_in", "DGND": "power_in",
                    "CS_S3_MPU": "input", "S3_C6_TX": "output", "S3_C6_RX": "input"})
    
    root.add_sheet("ESP32-C6 Radio", "sheets/esp32c6_radio.kicad_sch", SHEET_UUIDS["esp32c6"],
                   {"+3V3": "power_in", "DGND": "power_in", "S3_C6_TX": "input", "S3_C6_RX": "output"})
    
    root.add_sheet("Display Chain", "sheets/display_chain.kicad_sch", SHEET_UUIDS["display"],
                   {"+5V": "power_in", "+3V3": "power_in", "DGND": "power_in"})
    
    root.add_sheet("RPi5 Interface", "sheets/rpi5_interface.kicad_sch", SHEET_UUIDS["rpi5"],
                   {"+5V": "power_in", "+3V3": "power_in", "DGND": "power_in"})
    
    root.add_sheet("Level Shift", "sheets/level_shift.kicad_sch", SHEET_UUIDS["level"],
                   {"VIN_1V8_REF": "input", "+3V3": "power_in", "DGND": "power_in"})
    
    root.add_sheet("Expansion", "sheets/expansion.kicad_sch", SHEET_UUIDS["expand"],
                   {"I2C_SDA": "bidirectional", "I2C_SCL": "bidirectional", "+3V3": "power_in", "DGND": "power_in"})
    
    return root

def main():
    """Generate all carrier schematics."""
    basedir = Path("/home/claude/UNO-Q-Hub5/KiCad/carrier")
    basedir.mkdir(parents=True, exist_ok=True)
    (basedir / "sheets").mkdir(exist_ok=True)
    
    print("Building UNO Q Super Carrier Schematics")
    print("=" * 50)
    
    # Build sub-sheets
    print("\nSub-sheets:")
    build_carrier_power_sheet().save(str(basedir / "sheets/power.kicad_sch"))
    build_mounting_sheet().save(str(basedir / "sheets/uno_q_mounting.kicad_sch"))
    build_esp32c6_sheet().save(str(basedir / "sheets/esp32c6_radio.kicad_sch"))
    build_display_chain_sheet().save(str(basedir / "sheets/display_chain.kicad_sch"))
    build_rpi5_interface_sheet().save(str(basedir / "sheets/rpi5_interface.kicad_sch"))
    build_level_shift_sheet().save(str(basedir / "sheets/level_shift.kicad_sch"))
    build_expansion_sheet().save(str(basedir / "sheets/expansion.kicad_sch"))
    
    # Build root
    print("\nRoot schematic:")
    build_carrier_root().save(str(basedir / "uno_q_super_carrier.kicad_sch"))
    
    print("\n✓ Carrier schematics complete")

if __name__ == "__main__":
    main()
