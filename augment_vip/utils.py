"""
Utility functions for the Augment VIP project
"""

import os
import sys
import platform
import json
import sqlite3
import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# VS Code installation patterns - each variant can have multiple possible directory structures
VSCODE_PATTERNS = {
    "VS Code": [
        ["Code", "User"],
    ],
    "VS Code Insiders": [
        ["Code - Insiders", "User"],
    ],
    "VS Code Server": [
        [".vscode-server", "data", "User"],  # Standard pattern
        [".vscode-server", "User"],          # Alternative pattern
    ],
    "VS Code Server (Insiders)": [
        [".vscode-server-insiders", "data", "User"],  # Standard pattern
        [".vscode-server-insiders", "User"],          # Alternative pattern (likely fix for Linux)
    ],
    "VSCodium": [
        ["VSCodium", "User"],
    ],
    "Code-OSS": [
        ["Code - OSS", "User"],
    ],
}

# Console colors
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama for Windows support
    
    def info(msg: str) -> None:
        """Print an info message in blue"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {msg}")
    
    def success(msg: str) -> None:
        """Print a success message in green"""
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")
    
    def warning(msg: str) -> None:
        """Print a warning message in yellow"""
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}")
    
    def error(msg: str) -> None:
        """Print an error message in red"""
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")
        
except ImportError:
    # Fallback if colorama is not installed
    def info(msg: str) -> None:
        print(f"[INFO] {msg}")
    
    def success(msg: str) -> None:
        print(f"[SUCCESS] {msg}")
    
    def warning(msg: str) -> None:
        print(f"[WARNING] {msg}")
    
    def error(msg: str) -> None:
        print(f"[ERROR] {msg}")

def get_base_directories() -> List[Path]:
    """
    Get base directories to search for VS Code installations based on OS

    Returns:
        List of base directory paths
    """
    system = platform.system()
    base_dirs = []

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        userprofile = os.environ.get("USERPROFILE")
        if not appdata:
            error("APPDATA environment variable not found")
            sys.exit(1)
        base_dirs = [Path(appdata), Path(userprofile) if userprofile else None]

    elif system == "Darwin":  # macOS
        app_support = Path.home() / "Library" / "Application Support"
        base_dirs = [app_support, Path.home()]

    elif system == "Linux":
        config_dir = Path.home() / ".config"
        base_dirs = [config_dir, Path.home()]

    else:
        error(f"Unsupported operating system: {system}")
        sys.exit(1)

    # Filter out None values
    return [base_dir for base_dir in base_dirs if base_dir is not None]

def get_vscode_paths() -> Dict[str, Path]:
    """
    Get VS Code paths using pattern-based detection.
    Checks multiple patterns for each VS Code variant to handle different directory structures.

    Returns:
        Dict with paths to VS Code directories and files
    """
    base_dirs = get_base_directories()

    # Try each VS Code variant with multiple patterns in priority order
    for variant_name, patterns in VSCODE_PATTERNS.items():
        for pattern in patterns:
            for base_dir in base_dirs:
                # Build the full path by joining pattern segments
                candidate_path = base_dir
                for segment in pattern:
                    candidate_path = candidate_path / segment

                # Check if this path exists
                if candidate_path.exists():
                    pattern_used = " / ".join(pattern)
                    info(f"Found {variant_name} installation at: {candidate_path}")
                    info(f"Using pattern: {pattern_used}")

                    # Return the found installation
                    return {
                        "base_dir": candidate_path,
                        "installation_type": variant_name,
                        "pattern_used": pattern_used,
                        "storage_json": candidate_path / "globalStorage" / "storage.json",
                        "state_db": candidate_path / "globalStorage" / "state.vscdb"
                    }

    # No installation found - show detailed error with all checked patterns
    error("No VS Code installation found. Checked the following patterns:")
    for variant_name, patterns in VSCODE_PATTERNS.items():
        error(f"  {variant_name}:")
        for pattern in patterns:
            for base_dir in base_dirs:
                candidate_path = base_dir
                for segment in pattern:
                    candidate_path = candidate_path / segment
                error(f"    - {candidate_path}")
    sys.exit(1)

def backup_file(file_path: Path) -> Path:
    """
    Create a backup of a file
    
    Args:
        file_path: Path to the file to backup
        
    Returns:
        Path to the backup file
    """
    if not file_path.exists():
        error(f"File not found: {file_path}")
        sys.exit(1)
        
    backup_path = Path(f"{file_path}.backup")
    shutil.copy2(file_path, backup_path)
    success(f"Created backup at: {backup_path}")
    
    return backup_path

def generate_machine_id() -> str:
    """Generate a random 64-character hex string for machineId"""
    return uuid.uuid4().hex + uuid.uuid4().hex

def generate_device_id() -> str:
    """Generate a random UUID v4 for devDeviceId"""
    return str(uuid.uuid4())

def list_all_vscode_installations() -> List[Dict[str, Any]]:
    """
    List all available VS Code installations using pattern-based detection

    Returns:
        List of dictionaries containing installation info
    """
    base_dirs = get_base_directories()
    installations = []
    found_variants = set()  # Track which variants we've already found

    # Check each variant with all patterns
    for variant_name, patterns in VSCODE_PATTERNS.items():
        for pattern in patterns:
            for base_dir in base_dirs:
                # Build the full path
                candidate_path = base_dir
                for segment in pattern:
                    candidate_path = candidate_path / segment

                # Check if this path exists and we haven't found this variant yet
                if candidate_path.exists() and variant_name not in found_variants:
                    storage_json = candidate_path / "globalStorage" / "storage.json"
                    state_db = candidate_path / "globalStorage" / "state.vscdb"
                    pattern_used = " / ".join(pattern)

                    installations.append({
                        "name": variant_name,
                        "path": candidate_path,
                        "pattern_used": pattern_used,
                        "storage_json_exists": storage_json.exists(),
                        "state_db_exists": state_db.exists(),
                        "storage_json_path": storage_json,
                        "state_db_path": state_db
                    })

                    found_variants.add(variant_name)
                    break  # Found this variant, don't check other patterns for it

    return installations
