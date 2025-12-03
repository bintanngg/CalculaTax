# CalculaTax v2.0 - Indonesian Tax Calculator

CalculaTax is a simple desktop application built with Python and Tkinter to help calculate various types of taxes applicable in Indonesia, now with a redesigned interface.

---

## Description

This application provides an easy-to-use graphical user interface for calculating Income Tax (PPh 23), Value Added Tax (PPN), and Luxury Goods Sales Tax (PPnBM). Users can select the tax type, category, NPWP (taxpayer identification number) status (if relevant), and enter the nominal amount to get calculation details.

## Features

- **Graphical User Interface (GUI):** Built with Tkinter for ease of use.
- **Supports 3 Tax Types:**
    - PPh 23 (with different rates for NPWP and non-NPWP holders)
    - PPN (Value Added Tax)
    - PPnBM (Luxury Goods Sales Tax)
- **Dynamic Categories:** Category options change automatically based on the selected tax type.
- **Clean Code Structure:** Business logic (calculations) is separated from the display logic (UI) for easy maintenance.
- **External Configuration:** Tax rates are stored in the `rates.json` file, making them easy to update without changing the code.
- **Executable Ready:** Can be easily compiled into a single `.exe` file using PyInstaller.

## Upcoming Features

- **PPh 21 Calculation:** The next update will include a feature to calculate PPh 21 (Employee Income Tax).

## Requirements

- **Python 3.6+** 
- No external libraries are required (only uses standard Python libraries).

## How to Run

1. Make sure you have Python 3 installed.
2. Clone or download this repository.
3. Ensure the following files are in the same directory:
    - `app.py` 
    - `ui.py`
    - `tax_logic.py`
    - `rates.json`
4. Open a terminal or command prompt in that directory, then run the command:
   ```sh
   python app.py
   ```
5. The application will open.

## How to Compile (into an .exe)

You can compile this application into a single executable file (`.exe`) using PyInstaller.

1.  Install PyInstaller: `pip install pyinstaller`
2.  Navigate to the project directory via the terminal.
3.  Run the following command:
    ```sh
    pyinstaller --onefile --windowed --add-data "rates.json;." --name CalculaTax_v2.0 app.py
    ```
4.  The `CalculaTax_v2.0.exe` file will be available in the `dist` folder.

## Project Structure

The project consists of several main files:

- **`app.py`**: The main file and entry point for running the application.
- **`ui.py`**: A module containing all the code for the graphical user interface (GUI). This file is responsible for displaying windows, buttons, and all visual elements.
- **`tax_logic.py`**: A module containing all the business logic and functions for performing tax calculations.
- **`rates.json`**: A configuration file in JSON format that stores all tax rates. If there are changes to government rates, you only need to update this file.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.