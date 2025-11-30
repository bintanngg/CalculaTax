# CalculaTax - Indonesian Tax Calculator

CalculaTax is a simple desktop application created with Python and Tkinter to help calculate various types of taxes applicable in Indonesia.

---

## Description

This application provides an easy-to-use graphical user interface to calculate income tax (PPh 23), Value Added Tax (PPN), and Sales Tax on Luxury Goods (PPnBM). Users can select the tax type, category, NPWP status (if relevant), and enter the nominal amount to get the calculation details.

## Features

- **Graphical User Interface (GUI):** Built using Tkinter for ease of use.
- **Supports 3 Tax Types:**
    - PPh 23 (with different rates for NPWP and non-NPWP holders)
    - PPN (Value Added Tax)
    - PPnBM (Sales Tax on Luxury Goods)
- **Dynamic Categories:** Category options change automatically according to the selected tax type.
- **Clean Code Structure:** Business logic (calculations) is separated from the display logic (UI) for ease of maintenance.
- **External Configuration:** Tax rates are stored in a `rates.json` file, making them easy to update without changing the code.

## Upcoming Features

- **PPh 21 Calculation:** The next update will include a feature to calculate PPh 21 (Employee Income Tax).

## Requirements

- **Python 3.6+** 
- No external libraries are required (only uses standard Python libraries).

## How to Run

1. Make sure you have Python 3 installed.
2. Clone or download this repository.
3. Ensure the following three files are in the same directory:
    - `Calculatax_v1.2.2.py`
    - `tax_logic.py`
    - `rates.json`
4. Open a terminal or command prompt in that directory, then run the command:
   ```sh
   python Calculatax_v1.2.2.py
   ```
5. The application will open.

## Project Structure

This project consists of three main files:

- **`Calculatax_v1.2.2.py`**: The main file containing the code for the user interface (GUI). This file is responsible for displaying the window, buttons, and all visual elements.
- **`tax_logic.py`**: The module containing all business logic and functions for performing tax calculations.
- **`rates.json`**: A configuration file in JSON format that stores all tax rates. If there are rate changes from the government, you just need to update this file.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.