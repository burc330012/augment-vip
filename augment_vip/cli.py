"""
Command-line interface for Augment VIP
"""

import os
import sys
import click
from pathlib import Path

from . import __version__
from .utils import info, success, error, warning, list_all_vscode_installations
from .db_cleaner import clean_vscode_db
from .id_modifier import modify_telemetry_ids

@click.group()
@click.version_option(version=__version__)
def cli():
    """Augment VIP - Tools for managing VS Code settings"""
    pass

@cli.command()
def clean():
    """Clean VS Code databases by removing Augment-related entries"""
    if clean_vscode_db():
        success("Database cleaning completed successfully")
    else:
        error("Database cleaning failed")
        sys.exit(1)

@cli.command()
def modify_ids():
    """Modify VS Code telemetry IDs"""
    if modify_telemetry_ids():
        success("Telemetry ID modification completed successfully")
    else:
        error("Telemetry ID modification failed")
        sys.exit(1)

@cli.command()
def all():
    """Run all tools (clean and modify IDs)"""
    info("Running all tools...")
    
    clean_result = clean_vscode_db()
    modify_result = modify_telemetry_ids()
    
    if clean_result and modify_result:
        success("All operations completed successfully")
    else:
        error("Some operations failed")
        sys.exit(1)

@cli.command()
def list_installations():
    """List all detected VS Code installations"""
    info("Scanning for VS Code installations...")

    installations = list_all_vscode_installations()

    if not installations:
        warning("No VS Code installations found")
        return

    success(f"Found {len(installations)} VS Code installation(s):")

    for i, installation in enumerate(installations, 1):
        info(f"\n{i}. {installation['name']}")
        info(f"   Path: {installation['path']}")
        info(f"   Pattern: {installation['pattern_used']}")
        info(f"   Storage JSON: {'✓' if installation['storage_json_exists'] else '✗'} {installation['storage_json_path']}")
        info(f"   State DB: {'✓' if installation['state_db_exists'] else '✗'} {installation['state_db_path']}")

@cli.command()
def install():
    """Install Augment VIP"""
    info("Installing Augment VIP...")

    # This is a placeholder for any installation steps
    # In Python, most of the installation is handled by pip/setup.py

    success("Augment VIP installed successfully")
    info("You can now use the following commands:")
    info("  - augment-vip clean: Clean VS Code databases")
    info("  - augment-vip modify-ids: Modify telemetry IDs")
    info("  - augment-vip all: Run all tools")
    info("  - augment-vip list-installations: List all VS Code installations")

def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
