# tax_logic.py
'''
Tax Logic Module for CalculaTax
This module handles all business logic and tax calculations.
'''

import json

class TaxLogic:
    def __init__(self, rates_filepath="rates.json"):
        """
        Initializes the TaxLogic class by loading tax rates from a JSON file.
        
        :param rates_filepath: Path to the JSON file containing tax rates.
        :raises FileNotFoundError: If the rates file cannot be found.
        :raises json.JSONDecodeError: If the rates file is not a valid JSON.
        """
        try:
            with open(rates_filepath, 'r') as f:
                self.rates = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Tax rates file not found at '{rates_filepath}'")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Error: Could not decode the tax rates file. Please check for valid JSON format.", "", 0)

    def get_categories(self, tax_type):
        """Returns a list of categories for a given tax type."""
        if tax_type == 'PPN':
            return list(self.rates['ppn_rates'].keys())
        elif tax_type == 'PPnBM':
            return list(self.rates['ppnbm_rates'].keys())
        elif tax_type == 'PPh 23':
            return list(self.rates['pph23_rates'].keys()) + list(self.rates['fintech_rates'].keys())
        return []

    def calculate_ppn(self, amount, category):
        """Calculates PPN."""
        rate = self.rates['ppn_rates'][category]
        tax = amount * rate
        final_amount = amount + tax
        return {
            "dpp": amount,
            "rate": rate,
            "tax": tax,
            "final_amount": final_amount
        }

    def calculate_ppnbm(self, amount, category):
        """Calculates PPnBM and its corresponding PPN."""
        rate = self.rates['ppnbm_rates'][category]
        ppnbm = amount * rate
        # PPN for PPnBM is calculated on the amount after deducting PPnBM
        ppn_rate = self.rates['ppn_rates']['Barang mewah (12%)'] 
        ppn = ppn_rate * amount
        final_amount = amount + ppn + ppnbm
        return {
            "dpp": amount,
            "ppn_rate": ppn_rate,
            "ppn": ppn,
            "ppnbm_rate": rate,
            "ppnbm": ppnbm,
            "final_amount": final_amount
        }

    def calculate_pph23(self, amount, category, has_npwp):
        """Calculates PPh 23."""
        if category in self.rates['fintech_rates']:
            rate = self.rates['fintech_rates'][category]
        else:
            rates = self.rates['pph23_rates'][category]
            rate = rates[0] if has_npwp else rates[1]
        
        tax = amount * rate
        final_amount = amount - tax
        return {
            "dpp": amount,
            "rate": rate,
            "tax": tax,
            "final_amount": final_amount
        }
