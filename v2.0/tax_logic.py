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

    def is_npwp_required(self, category):
        """Checks if a given category requires an NPWP for rate calculation."""
        # As a rule, only standard PPh23 services are affected by NPWP status.
        # Fintech and other special taxes are often final and have a fixed rate.
        return category in self.rates['pph23_rates']

    def calculate_ppn(self, amount, category):
        """Calculates PPN."""
        if amount < 0:
            raise ValueError("Input amount cannot be negative.")
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
        if amount < 0:
            raise ValueError("Input amount cannot be negative.")
        rate = self.rates['ppnbm_rates'][category]
        ppnbm = amount * rate
        # PPN for goods subject to PPnBM uses the standard PPN rate.
        ppn_rate = self.rates['standard_ppn_rate'] 
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

    def calculate_pph23(self, amount, category, has_npwp, include_ppn=False, is_gross_up=False):
        """
        Calculates PPh 23, with options for PPN inclusion and gross-up calculation.
        """
        if amount < 0:
            raise ValueError("Input amount cannot be negative.")
        # 1. Determine the tax rate first
        base_rate = 0
        if category in self.rates['fintech_rates']:
            base_rate = self.rates['fintech_rates'][category]
        else:
            base_rate = self.rates['pph23_rates'][category][0] # Base rate is the first one

        # Apply NPWP sanction if required and not present
        rate = base_rate * 2 if self.is_npwp_required(category) and not has_npwp else base_rate
            
        # 2. Determine DPP and taxes based on calculation type
        if is_gross_up and include_ppn:
            # Special handling for the combined case of "Gross Up" and "Include PPN".
            # Based on user feedback, this requires a mixed-base calculation.
            
            # PPN is based on the nominal input amount.
            dpp_for_ppn = amount
            ppn_rate = self.rates['standard_ppn_rate']
            ppn = dpp_for_ppn * ppn_rate
            
            # PPh 23 tax is based on a grossed-up value from the nominal amount.
            if rate >= 1:
                raise ValueError("Gross up cannot be calculated for a tax rate of 100% or more.")
            dpp_for_pph = amount / (1 - rate)
            tax = dpp_for_pph * rate
            
            # The final amount is the sum of the grossed-up PPh base and the PPN.
            final_amount = dpp_for_pph + ppn
            
            # For display purposes, the returned DPP is the original nominal amount.
            # We return both DPPs for clarity in the UI.
            return {
                "dpp": dpp_for_ppn, # DPP for PPN
                "dpp_gross_up": dpp_for_pph, # DPP for PPh 23
                "rate": rate, "tax": tax, "final_amount": final_amount, "ppn_rate": ppn_rate,
                "ppn": ppn, "is_gross_up": is_gross_up, "net_amount_input": amount
            }
        else:
            # Standard logic for all other cases.
            if is_gross_up:
                if rate >= 1:
                    raise ValueError("Gross up cannot be calculated for a tax rate of 100% or more.")
                dpp = amount / (1 - rate)
            else:
                dpp = amount

            tax = dpp * rate

            ppn = 0
            ppn_rate = 0
            if include_ppn:
                ppn_rate = self.rates['standard_ppn_rate']
                ppn = dpp * ppn_rate
                # If PPN is included, the final amount is the total outlay for the payer.
                final_amount = dpp + ppn
            else:
                # If gross-up, final_amount is the total cost (dpp). Otherwise, it's the net received by the payee.
                final_amount = dpp if is_gross_up else dpp - tax
        
        return {
            "dpp": dpp,
            "rate": rate,
            "tax": tax,
            "final_amount": final_amount,
            "ppn_rate": ppn_rate,
            "ppn": ppn,
            "is_gross_up": is_gross_up,
            "net_amount_input": amount if is_gross_up else None # Pass original amount for UI
        }
