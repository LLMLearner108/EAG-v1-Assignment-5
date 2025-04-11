from typing import List

def set_units_and_mode() -> List[str]:
    """
    Sets the CNC machine to use metric units, absolute positioning,
    feed per revolution mode, and selects the XZ plane.
    """
    return [
        "G21",  # Units in mm
        "G90",  # Absolute positioning
        "G95",  # Feed per revolution
        "G18"   # XZ plane selection
    ]

def select_tool_and_start_spindle(tool_number: int, offset: int, spindle_speed: int) -> List[str]:
    """
    Selects the tool and starts the spindle at a given speed.
    
    Args:
        tool_number: Tool number (e.g., 1 for T0101)
        offset: Tool offset number
        spindle_speed: Spindle speed in RPM
    """
    return [
        f"T{tool_number:02d}{offset:02d}",  # Tool selection
        f"G97 S{spindle_speed} M03"         # Spindle on clockwise with RPM
    ]

def move_to_safe_start(x: float, z: float) -> List[str]:
    """
    Moves the tool to a safe starting position before cutting.
    
    Args:
        x: X-coordinate in mm
        z: Z-coordinate in mm
    """
    return [f"G0 X{x} Z{z}"]

def face_stock(z_face: float, feed_rate: float) -> List[str]:
    """
    Faces the end of the stock to ensure it's flat.
    
    Args:
        z_face: Final Z position to face to (usually 0)
        feed_rate: Feed rate for facing
    """
    return [
        f"G1 Z{z_face} F{feed_rate}",  # Feed to face
        "G0 Z2"                        # Retract after facing
    ]

def perform_uniform_turning(start_diameter: float, final_diameter: float, length: float, feed_rate: float) -> List[str]:
    """
    Cuts along the full length of the cylinder to reduce its diameter uniformly.
    
    Args:
        start_diameter: Initial diameter of the rod in mm
        final_diameter: Final diameter after turning in mm
        length: Length of the cut along Z-axis in mm
        feed_rate: Feed rate in mm/rev
    """
    return [
        f"G0 X{start_diameter} Z0",                # Rapid to start position
        f"G1 X{final_diameter} Z-{length} F{feed_rate}"  # Turning pass
    ]

def retract_and_end_program(retract_x: float = 100, retract_z: float = 100) -> List[str]:
    """
    Retracts the tool to a safe position and ends the program.
    
    Args:
        retract_x: X-coordinate for safe retract
        retract_z: Z-coordinate for safe retract
    """
    return [
        f"G0 X{retract_x} Z{retract_z}",  # Retract tool
        "M05",                            # Stop spindle
        "M30"                             # End of program
    ]

def generate_uniform_reduction_program(
    tool_number: int = 1,
    offset: int = 1,
    spindle_speed: int = 800,
    start_diameter: float = 50,
    final_diameter: float = 30,
    length: float = 100,
    feed_rate: float = 0.25
) -> List[str]:
    """
    Generates G-code for reducing a cylindrical rod uniformly from the starting diameter
    to the final diameter over a specified length.
    """
    gcode = ["%", "O2000 (Uniform reduction to 30 mm diameter)"]
    gcode += set_units_and_mode()
    gcode += select_tool_and_start_spindle(tool_number, offset, spindle_speed)
    gcode += move_to_safe_start(x=60, z=2)
    gcode += face_stock(z_face=0, feed_rate=0.2)
    gcode += perform_uniform_turning(start_diameter, final_diameter, length, feed_rate)
    gcode += retract_and_end_program()
    gcode.append("%")
    return gcode
