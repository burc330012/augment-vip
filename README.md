# Augment VIP

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

A utility toolkit for Augment VIP users, providing tools to manage and clean VS Code databases. Now with Python-based cross-platform compatibility!

Tested on Mac Os Vscode
Status : Working
Last Tested : 4 June 2025 1:50PM GMT8+

## 🚀 Features

- **Database Cleaning**: Remove Augment-related entries from VS Code databases
- **Telemetry ID Modification**: Generate random telemetry IDs for VS Code to enhance privacy
- **Multi-Installation Support**: Automatically detects and supports multiple VS Code variants:
  - Standard VS Code
  - VS Code Insiders
  - VS Code Server (Remote Development)
  - VS Code Server Insiders
  - VSCodium
  - Code-OSS
- **Smart Path Detection**: Priority-based detection finds the first available VS Code installation
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Python-Based**: Uses Python for better cross-platform compatibility
- **Virtual Environment**: Isolates dependencies to avoid conflicts
- **Safe Operations**: Creates backups before making any changes
- **User-Friendly**: Clear, color-coded output and detailed status messages

## 📋 Requirements

- Python 3.6 or higher
- No external system dependencies required (all managed through Python)

## 💻 Installation

### One-Line Install

You can install with a single command using curl:

```bash
curl -fsSL https://raw.githubusercontent.com/azrilaiman2003/augment-vip/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

This will:
1. Download the installation script
2. Make it executable
3. Check for Python 3.6 or higher
4. Create a new `augment-vip` directory in your current location
5. Download the Python installer and package files
6. Set up a Python virtual environment
7. Install the package in the virtual environment
8. Prompt you if you want to run the database cleaning and telemetry ID modification tools
9. Run the selected tools automatically

### Installation Options

You can also run the installation script with options to automatically run the cleaning and ID modification tools:

```bash
# Install and run database cleaning
curl -fsSL https://raw.githubusercontent.com/azrilaiman2003/augment-vip/python/install.sh -o install.sh && chmod +x install.sh && ./install.sh --clean

# Install and modify telemetry IDs
curl -fsSL https://raw.githubusercontent.com/azrilaiman2003/augment-vip/python/install.sh -o install.sh && chmod +x install.sh && ./install.sh --modify-ids

# Install and run all tools
curl -fsSL https://raw.githubusercontent.com/azrilaiman2003/augment-vip/python/install.sh -o install.sh && chmod +x install.sh && ./install.sh --all

# Show help
curl -fsSL https://raw.githubusercontent.com/azrilaiman2003/augment-vip/python/install.sh -o install.sh && chmod +x install.sh && ./install.sh --help
```

### Repository Install

If you prefer to clone the entire repository:

```bash
git clone https://github.com/azrilaiman2003/augment-vip.git
cd augment-vip
python install.py
```

### Manual Installation

If you prefer to set up manually:

```bash
# Clone the repository
git clone https://github.com/azrilaiman2003/augment-vip.git
cd augment-vip

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install the package
pip install -e .
```

## 🔧 Usage

### Clean VS Code Databases

To remove Augment-related entries from VS Code databases:

```bash
# If using the virtual environment (recommended)
.venv/bin/augment-vip clean  # macOS/Linux
.venv\Scripts\augment-vip clean  # Windows

# If installed globally
augment-vip clean
```

This will:
- Detect your operating system
- Find VS Code database files
- Create backups of each database
- Remove entries containing "augment" from the databases
- Report the results

### Modify VS Code Telemetry IDs

To change the telemetry IDs in VS Code's storage.json file:

```bash
# If using the virtual environment (recommended)
.venv/bin/augment-vip modify-ids  # macOS/Linux
.venv\Scripts\augment-vip modify-ids  # Windows

# If installed globally
augment-vip modify-ids
```

This will:
- Locate the VS Code storage.json file
- Generate a random 64-character hex string for machineId
- Generate a random UUID v4 for devDeviceId
- Create a backup of the original file
- Update the file with the new random values

### List VS Code Installations

To see all detected VS Code installations:

```bash
# If using the virtual environment (recommended)
.venv/bin/augment-vip list-installations  # macOS/Linux
.venv\Scripts\augment-vip list-installations  # Windows

# If installed globally
augment-vip list-installations
```

This will show:
- All detected VS Code installations and their types
- File paths for storage.json and state.vscdb
- Whether the required files exist

### Run All Tools

To run both tools at once:

```bash
# If using the virtual environment (recommended)
.venv/bin/augment-vip all  # macOS/Linux
.venv\Scripts\augment-vip all  # Windows

# If installed globally
augment-vip all
```

## 📁 Project Structure

```
augment-vip/
├── .venv/                  # Virtual environment (created during installation)
├── augment_vip/            # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── db_cleaner.py       # Database cleaning functionality
│   ├── id_modifier.py      # Telemetry ID modification functionality
│   └── utils.py            # Utility functions
├── install.py              # Python installation script
├── install.sh              # Bash wrapper for Python installer
├── README.md               # This file
├── requirements.txt        # Package dependencies
└── setup.py                # Package setup script
```

## 🔍 How It Works

The tool works by:

1. **Multi-Installation Detection**: Scans for VS Code installations in priority order:
   - **Windows**: `%APPDATA%\Code\`, `%APPDATA%\Code - Insiders\`, `%USERPROFILE%\.vscode-server\`, etc.
   - **macOS**: `~/Library/Application Support/Code/`, `~/.vscode-server/`, etc.
   - **Linux**: `~/.config/Code/`, `~/.vscode-server/`, `~/.vscode-server-insiders/`, etc.

2. **Smart Path Selection**: Uses the first available installation found, with standard VS Code taking priority over server installations.

3. **Creating Backups**: Before making any changes, the tool creates a backup of each file.

4. **Database Cleaning**: Uses SQLite commands to remove entries containing "augment" from the databases.

5. **Telemetry ID Modification**: Updates machineId and devDeviceId in storage.json with random values.

6. **Reporting Results**: Provides detailed feedback about which installation was processed and the operations performed.

## 🛠️ Troubleshooting

### Common Issues

**Python Not Found**
```
[ERROR] Python 3 is not installed or not in PATH
```
Install Python 3.6 or higher:
- Windows: Download from https://www.python.org/downloads/
- macOS: `brew install python3` or download from https://www.python.org/downloads/
- Ubuntu/Debian: `sudo apt install python3 python3-venv`
- Fedora/RHEL: `sudo dnf install python3 python3-venv`

**Permission Denied**
```
[ERROR] Permission denied
```
Make sure the scripts are executable:
```bash
chmod +x install.sh
```

**No Databases Found**
```
[WARNING] No database files found
```
This may occur if you haven't used VS Code on your system, or if it's installed in non-standard locations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Azril Aiman - me@azrilaiman.my

Project Link: [https://github.com/azrilaiman2003/augment-vip](https://github.com/azrilaiman2003/augment-vip)

---

Made with ❤️ by [Azril Aiman](https://github.com/azrilaiman2003)
