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

def get_vscode_paths() -> Dict[str, Path]:
    """
    Get VS Code paths based on the operating system.
    Checks multiple VS Code installation locations in priority order.

    Returns:
        Dict with paths to VS Code directories and files
    """
    system = platform.system()
    paths = {}

    # Define possible VS Code installation paths in priority order
    possible_paths = []

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        userprofile = os.environ.get("USERPROFILE")
        if not appdata:
            error("APPDATA environment variable not found")
            sys.exit(1)

        # Windows paths in priority order
        possible_paths = [
            Path(appdata) / "Code" / "User",                    # Standard VS Code
            Path(appdata) / "Code - Insiders" / "User",         # VS Code Insiders
            Path(userprofile) / ".vscode-server" / "data" / "User" if userprofile else None,  # Remote VS Code
            Path(userprofile) / ".vscode-server-insiders" / "data" / "User" if userprofile else None,  # Remote Insiders
            Path(appdata) / "VSCodium" / "User",                # VSCodium
            Path(appdata) / "Code - OSS" / "User",              # Code-OSS
        ]
        # Filter out None values
        possible_paths = [p for p in possible_paths if p is not None]

    elif system == "Darwin":  # macOS
        app_support = Path.home() / "Library" / "Application Support"
        possible_paths = [
            app_support / "Code" / "User",                      # Standard VS Code
            app_support / "Code - Insiders" / "User",           # VS Code Insiders
            Path.home() / ".vscode-server" / "data" / "User",   # Remote VS Code
            Path.home() / ".vscode-server-insiders" / "data" / "User",  # Remote Insiders
            app_support / "VSCodium" / "User",                  # VSCodium
            app_support / "Code - OSS" / "User",                # Code-OSS
        ]

    elif system == "Linux":
        config_dir = Path.home() / ".config"
        possible_paths = [
            config_dir / "Code" / "User",                       # Standard VS Code
            config_dir / "Code - Insiders" / "User",            # VS Code Insiders
            Path.home() / ".vscode-server" / "data" / "User",   # Remote VS Code
            Path.home() / ".vscode-server-insiders" / "data" / "User",  # Remote Insiders
            config_dir / "VSCodium" / "User",                   # VSCodium
            config_dir / "Code - OSS" / "User",                 # Code-OSS
        ]

    else:
        error(f"Unsupported operating system: {system}")
        sys.exit(1)

    # Find the first existing VS Code installation
    base_dir = None
    installation_type = None

    for path in possible_paths:
        if path.exists():
            base_dir = path
            # Determine installation type for logging
            if "Code - Insiders" in str(path):
                installation_type = "VS Code Insiders"
            elif "vscode-server-insiders" in str(path):
                installation_type = "VS Code Server (Insiders)"
            elif "vscode-server" in str(path):
                installation_type = "VS Code Server"
            elif "VSCodium" in str(path):
                installation_type = "VSCodium"
            elif "Code - OSS" in str(path):
                installation_type = "Code-OSS"
            else:
                installation_type = "VS Code"
            break

    if base_dir is None:
        error("No VS Code installation found. Checked the following locations:")
        for path in possible_paths:
            error(f"  - {path}")
        sys.exit(1)

    info(f"Found {installation_type} installation at: {base_dir}")

    # Common paths
    paths["base_dir"] = base_dir
    paths["installation_type"] = installation_type
    paths["storage_json"] = base_dir / "globalStorage" / "storage.json"
    paths["state_db"] = base_dir / "globalStorage" / "state.vscdb"

    return paths

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
    List all available VS Code installations on the system

    Returns:
        List of dictionaries containing installation info
    """
    system = platform.system()
    installations = []

    # Define possible VS Code installation paths
    possible_paths = []

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        userprofile = os.environ.get("USERPROFILE")
        if appdata:
            possible_paths = [
                (Path(appdata) / "Code" / "User", "VS Code"),
                (Path(appdata) / "Code - Insiders" / "User", "VS Code Insiders"),
                (Path(userprofile) / ".vscode-server" / "data" / "User" if userprofile else None, "VS Code Server"),
                (Path(userprofile) / ".vscode-server-insiders" / "data" / "User" if userprofile else None, "VS Code Server (Insiders)"),
                (Path(appdata) / "VSCodium" / "User", "VSCodium"),
                (Path(appdata) / "Code - OSS" / "User", "Code-OSS"),
            ]

    elif system == "Darwin":  # macOS
        app_support = Path.home() / "Library" / "Application Support"
        possible_paths = [
            (app_support / "Code" / "User", "VS Code"),
            (app_support / "Code - Insiders" / "User", "VS Code Insiders"),
            (Path.home() / ".vscode-server" / "data" / "User", "VS Code Server"),
            (Path.home() / ".vscode-server-insiders" / "data" / "User", "VS Code Server (Insiders)"),
            (app_support / "VSCodium" / "User", "VSCodium"),
            (app_support / "Code - OSS" / "User", "Code-OSS"),
        ]

    elif system == "Linux":
        config_dir = Path.home() / ".config"
        possible_paths = [
            (config_dir / "Code" / "User", "VS Code"),
            (config_dir / "Code - Insiders" / "User", "VS Code Insiders"),
            (Path.home() / ".vscode-server" / "data" / "User", "VS Code Server"),
            (Path.home() / ".vscode-server-insiders" / "data" / "User", "VS Code Server (Insiders)"),
            (config_dir / "VSCodium" / "User", "VSCodium"),
            (config_dir / "Code - OSS" / "User", "Code-OSS"),
        ]

    # Filter out None values and check which installations exist
    for path_info in possible_paths:
        if path_info[0] is not None and path_info[0].exists():
            path, name = path_info
            # Check if the required files exist
            storage_json = path / "globalStorage" / "storage.json"
            state_db = path / "globalStorage" / "state.vscdb"

            installations.append({
                "name": name,
                "path": path,
                "storage_json_exists": storage_json.exists(),
                "state_db_exists": state_db.exists(),
                "storage_json_path": storage_json,
                "state_db_path": state_db
            })

    return installations
