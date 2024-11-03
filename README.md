# Edit 'InstallDate'

A Python application for managing and editing the installation dates of software on Windows systems.

## Features

- **View all installed software** with their installation dates.
- **Edit existing installation dates.**
- **Create a new installation date** if it doesn't exist.

## Prerequisites

- **Python 3.x** installed on your machine.
- **Administrative privileges** may be required to modify the Windows registry.

## Installation

1. **Download the script**:
   - Download the `main.py` file from the repository.

2. **Install required libraries** (if necessary):
   - This application uses the built-in libraries `tkinter` and `winreg`, so no additional installations are required.

## Usage

1. Open a command prompt or terminal.
2. Navigate to the directory where the script is located.
3. Run the application: main.py
4. The GUI will display a list of installed software. You can:
- Click the **"Edit Date"** button next to any software to modify its installation date.
- If the installation date is not set, you can enter a new date in the format **YYYYMMDD**.

## Important Notes

- **Backup the Registry**: It is recommended to back up the Windows registry before making any changes to avoid accidental data loss.
- **Data Format**: Ensure that the installation date is entered in the correct format (**YYYYMMDD**).

## License

This project is open-source. Feel free to modify and use it according to your needs.

