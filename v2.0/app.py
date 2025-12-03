# app.py
'''
Application Runner for CalculaTax
This script imports the UI and runs the application.
'''

from ui import TaxCalculatorApp

if __name__ == "__main__":
    app = TaxCalculatorApp()
    app.mainloop()
