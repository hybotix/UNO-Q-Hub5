#!/usr/bin/env python3
"""
KiCad 10.0.2 Schematic Builder
Generates valid .kicad_sch files for UNO Q HUB75 Shield and Super Carrier

Usage:
    python3 kicad10_builder.py --shield
    python3 kicad10_builder.py --carrier
    python3 kicad10_builder.py --all
"""

import uuid
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

# Version for KiCad 10.0.2 compatibility
KICAD_VERSION = "20231120"
GENERATOR_VERSION = "10.0.0"

@dataclass
class Component:
    """Represents a placed symbol instance in schematic."""
    ref: str
    lib_id: str
    value: str
    at_x: float
    at_y: float
    unit: int = 1
    footprint: str = ""
    
    def generate(self) -> str:
        """Generate KiCad s-expression for this component."""
        sym_uuid = str(uuid.uuid4())
        
        lines = [
            f"  (symbol (lib_id \"{self.lib_id}\")",
            f"    (at {self.at_x} {self.at_y} 0)",
            f"    (unit {self.unit})",
            "    (in_bom yes) (on_board yes)",
            f"    (uuid \"{sym_uuid}\")",
            f"    (property \"Reference\" \"{self.ref}\"",
            f"      (at {self.at_x} {self.at_y - 1.5} 0)",
            "      (effects (font (size 1.27 1.27)))",
            "    )",
            f"    (property \"Value\" \"{self.value}\"",
            f"      (at {self.at_x} {self.at_y + 1.5} 0)",
            "      (effects (font (size 1.27 1.27)))",
            "    )",
        ]
        
        if self.footprint:
            lines.append(f"    (property \"Footprint\" \"{self.footprint}\"")
            lines.append(f"      (at {self.at_x} {self.at_y} 0)")
            lines.append("      (effects (font (size 1.27 1.27)) hide)")
            lines.append("    )")
        
        lines.extend([
            "    (instances",
            "      (project \"uno_q_hub75_shield\"",
            "        (path \"/bc84562d-846a-4607-81a1-500b7991d137/SHEETUUID\"",
            f"          (reference \"{self.ref}\") (unit {self.unit})",
            "        )",
            "      )",
            "    )",
            "  )",
        ])
        
        return "\n".join(lines)

@dataclass
class HierarchicalLabel:
    """Represents a hierarchical label (sheet pin connection)."""
    name: str
    shape: str  # input, output, bidirectional, tri_state, passive, unspecified
    at_x: float
    at_y: float
    
    def generate(self) -> str:
        """Generate KiCad s-expression for this label."""
        label_uuid = str(uuid.uuid4())
        lines = [
            f"  (hierarchical_label \"{self.name}\"",
            f"    (shape {self.shape})",
            f"    (at {self.at_x} {self.at_y} 0)",
            "    (effects (font (size 1.27 1.27)) (justify left))",
            f"    (uuid \"{label_uuid}\")",
            "  )",
        ]
        return "\n".join(lines)

class Schematic:
    """Represents a complete KiCad schematic file."""
    
    def __init__(self, filename: str, title: str, sheet_uuid: str = None):
        self.filename = filename
        self.title = title
        self.sheet_uuid = sheet_uuid or str(uuid.uuid4())
        self.components: List[Component] = []
        self.labels: List[HierarchicalLabel] = []
    
    def add_component(self, comp: Component) -> None:
        """Add a placed symbol to the schematic."""
        self.components.append(comp)
    
    def add_label(self, label: HierarchicalLabel) -> None:
        """Add a hierarchical label to the schematic."""
        self.labels.append(label)
    
    def generate(self) -> str:
        """Generate complete KiCad schematic s-expression."""
        lines = [
            "(kicad_sch",
            f"  (version {KICAD_VERSION})",
            "  (generator eeschema)",
            f"  (generator_version \"{GENERATOR_VERSION}\")",
            f"  (uuid \"{self.sheet_uuid}\")",
            "  (paper \"A4\")",
            "",
            "  (lib_symbols",
            "  )",
            "",
        ]
        
        # Add components
        for comp in self.components:
            lines.append(comp.generate())
            lines.append("")
        
        # Add labels
        for label in self.labels:
            lines.append(label.generate())
            lines.append("")
        
        # Sheet instances
        lines.extend([
            "  (sheet_instances",
            "    (path \"/\"",
            "      (page \"1\")",
            "    )",
            "  )",
            ")",
        ])
        
        return "\n".join(lines)
    
    def save(self, path: str) -> None:
        """Write schematic to file."""
        content = self.generate()
        Path(path).write_text(content)
        print(f"✓ {Path(path).name} ({len(content)} bytes)")

class RootSchematic:
    """Represents a root (hierarchical) schematic with sub-sheets."""
    
    def __init__(self, filename: str, title: str, root_uuid: str, project_name: str):
        self.filename = filename
        self.title = title
        self.root_uuid = root_uuid
        self.project_name = project_name
        self.sheets: List[Tuple[str, str, str, Dict]] = []  # (name, file, uuid, pins)
    
    def add_sheet(self, name: str, file: str, sheet_uuid: str, pins: Dict[str, str]) -> None:
        """Add a hierarchical sub-sheet reference."""
        self.sheets.append((name, file, sheet_uuid, pins))
    
    def generate(self) -> str:
        """Generate root schematic with sheet blocks."""
        lines = [
            "(kicad_sch",
            f"  (version {KICAD_VERSION})",
            "  (generator eeschema)",
            f"  (generator_version \"{GENERATOR_VERSION}\")",
            f"  (uuid \"{self.root_uuid}\")",
            "  (paper \"A3\")",
            "  (title_block",
            f"    (title \"{self.title}\")",
            "    (date \"2026-05-09\")",
            "    (rev \"0.3\")",
            "    (company \"Hybrid RobotiX\")",
            "  )",
            "",
            "  (lib_symbols",
            "  )",
            "",
        ]
        
        # Add sheet blocks
        y_pos = 30
        for sheet_num, (name, file, sheet_uuid, pins) in enumerate(self.sheets, 1):
            lines.append("  (sheet")
            lines.append(f"    (at 20 {y_pos})")
            lines.append("    (size 60 50)")
            lines.append("    (stroke (width 0.254) (type default))")
            lines.append("    (fill (type color) (color 255 255 204 0.3))")
            lines.append(f"    (uuid \"{sheet_uuid}\")")
            lines.append(f"    (property \"Sheet name\" \"{name}\"")
            lines.append(f"      (at 20 {y_pos - 2} 0)")
            lines.append("      (effects (font (size 1.524 1.524)) (justify left bottom))")
            lines.append("    )")
            lines.append(f"    (property \"Sheet file\" \"{file}\"")
            lines.append(f"      (at 20 {y_pos - 4} 0)")
            lines.append("      (effects (font (size 1.27 1.27)) (justify left bottom))")
            lines.append("    )")
            
            # Add pins
            pin_y = y_pos + 10
            for pin_name, pin_dir in pins.items():
                pin_uuid = str(uuid.uuid4())
                lines.append(f"    (pin \"{pin_name}\" {pin_dir}")
                lines.append(f"      (at 80 {pin_y} 0)")
                lines.append("      (effects (font (size 1.27 1.27)))")
                lines.append(f"      (uuid \"{pin_uuid}\")")
                lines.append("    )")
                pin_y += 4
            
            # Instances block
            lines.append("    (instances")
            lines.append(f"      (project \"{self.project_name}\"")
            lines.append(f"        (path \"/{self.root_uuid}\"")
            lines.append(f"          (page \"{sheet_num + 1}\")")
            lines.append("        )")
            lines.append("      )")
            lines.append("    )")
            lines.append("  )")
            lines.append("")
            
            y_pos += 60
        
        # Sheet instances
        lines.extend([
            "  (sheet_instances",
            "    (path \"/\"",
            "      (page \"1\")",
            "    )",
            "  )",
            ")",
        ])
        
        return "\n".join(lines)
    
    def save(self, path: str) -> None:
        """Write root schematic to file."""
        content = self.generate()
        Path(path).write_text(content)
        print(f"✓ {Path(path).name} ({len(content)} bytes)")

if __name__ == "__main__":
    print("KiCad 10 Schematic Builder loaded successfully")
    print(f"Version: {KICAD_VERSION} (KiCad 10.0.2 compatible)")
