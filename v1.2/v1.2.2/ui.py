# ui.py
'''
UI Module for CalculaTax
This module contains the main UI class for the tax calculator.
'''

import tkinter as tk
from tkinter import ttk, messagebox
import os
from tax_logic import TaxLogic

# --- Constants to avoid "magic strings" ---
TAX_PPH23 = 'PPh 23'
TAX_PPN = 'PPN'
TAX_PPNBM = 'PPnBM'

NPWP_HAVE = 'Memiliki NPWP'
NPWP_NONE = 'Tidak Memiliki NPWP'

# --- Main Application Class (View/Controller) ---
class TaxCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        try:
            # Build an absolute path to the rates.json file relative to the script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            rates_path = os.path.join(script_dir, "rates.json")
            self.tax_logic = TaxLogic(rates_path)
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Initialization Error", str(e))
            self.destroy()
            return

        self.title("CalculaTax v1.2.2 | Made by Bintang")
        self.resizable(False, False)
        
        self.create_widgets()
        self.bind_events()
        self.on_tax_change() # Set initial state

    def create_widgets(self):
        """Creates and places all UI widgets."""
        tk.Label(self, text="Kalkulator Pajak Indonesia", font=("Arial", 16, "bold")).pack(pady=10)
        
        frame = tk.Frame(self)
        frame.pack(pady=10, padx=20)

        # --- Tax Type Selection ---
        tk.Label(frame, text="Pilih Jenis Pajak:").grid(row=0, column=0, sticky="w", pady=2)
        self.tax_type_var = tk.StringVar()
        self.tax_type_combo = ttk.Combobox(frame, textvariable=self.tax_type_var, 
                                           values=[TAX_PPH23, TAX_PPN, TAX_PPNBM], state="readonly")
        self.tax_type_combo.grid(row=0, column=1, padx=10, pady=2)
        self.tax_type_combo.set(TAX_PPH23)

        # --- Category Selection ---
        tk.Label(frame, text="Pilih Kategori:").grid(row=1, column=0, sticky="w", pady=2)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(frame, textvariable=self.category_var, state="readonly")
        self.category_combo.grid(row=1, column=1, padx=10, pady=2)

        # --- NPWP Status ---
        tk.Label(frame, text="Status NPWP:").grid(row=2, column=0, sticky="w", pady=2)
        self.npwp_var = tk.StringVar()
        self.npwp_combo = ttk.Combobox(frame, textvariable=self.npwp_var, 
                                       values=[NPWP_HAVE, NPWP_NONE], state="readonly")
        self.npwp_combo.grid(row=2, column=1, padx=10, pady=2)
        self.npwp_combo.set(NPWP_HAVE)

        # --- Amount Input ---
        tk.Label(frame, text="Nominal (IDR):").grid(row=3, column=0, sticky="w", pady=2)
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=2)

        # --- PPN Option ---
        self.include_ppn_var = tk.BooleanVar()
        self.ppn_checkbox = tk.Checkbutton(self, text="Sertakan PPN 11%", 
                                           variable=self.include_ppn_var)
        self.ppn_checkbox.pack(pady=5)
        
        # --- Gross Up Option ---
        self.gross_up_var = tk.BooleanVar()
        self.gross_up_checkbox = tk.Checkbutton(self, text="Gross Up PPh",
                                                variable=self.gross_up_var)
        self.gross_up_checkbox.pack(pady=5)
        
        # --- Action & Result ---
        tk.Button(self, text="Hitung Pajak", command=self.calculate, font=("Arial", 12)).pack(pady=10)
        tk.Label(self, text="Hasil Perhitungan:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result_text = tk.Text(self, height=7, width=50, wrap=tk.WORD)
        self.result_text.pack(pady=5, padx=10)

    def bind_events(self):
        """Binds UI events to handler methods."""
        self.tax_type_combo.bind("<<ComboboxSelected>>", self.on_tax_change)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)

    def on_tax_change(self, event=None):
        """Handles changes in the tax type selection."""
        tax_type = self.tax_type_var.get()
        categories = self.tax_logic.get_categories(tax_type)
        
        self.category_combo.config(values=categories)
        if categories:
            self.category_combo.set(categories[0])
        else:
            self.category_combo.set("")
        
        self._update_dependent_widgets()

    def on_category_change(self, event=None):
        """Handles changes in the category selection."""
        self._update_dependent_widgets()

    def _update_dependent_widgets(self):
        """Enables or disables dependent widgets like NPWP and PPN checkbox."""
        tax_type = self.tax_type_var.get()
        category = self.category_var.get()

        # Manage NPWP combo box state
        if tax_type == TAX_PPH23 and self.tax_logic.is_npwp_required(category):
            self.npwp_combo.config(state="readonly")
        else:
            self.npwp_combo.config(state="disabled")
            
        # Manage "Include PPN" checkbox state
        if tax_type == TAX_PPH23:
            self.ppn_checkbox.config(state="normal")
        else:
            self.ppn_checkbox.config(state="disabled")
            self.include_ppn_var.set(False)

        # Manage "Gross Up" checkbox state
        if tax_type == TAX_PPH23:
            self.gross_up_checkbox.config(state="normal")
        else:
            self.gross_up_checkbox.config(state="disabled")
            self.gross_up_var.set(False)

    def calculate(self):
        """
        Main calculation function. It gets inputs, calls the business logic,
        and formats the output.
        """
        try:
            tax_type = self.tax_type_var.get()
            category = self.category_var.get()
            amount_str = self.amount_var.get().replace(',', '')
            
            if not amount_str:
                raise ValueError("Nominal tidak boleh kosong.")
            amount = float(amount_str)

            has_npwp = self.npwp_var.get() == NPWP_HAVE
            include_ppn = self.include_ppn_var.get()
            is_gross_up = self.gross_up_var.get()

            result_data = None
            if tax_type == TAX_PPN:
                result_data = self.tax_logic.calculate_ppn(amount, category)
            elif tax_type == TAX_PPNBM:
                result_data = self.tax_logic.calculate_ppnbm(amount, category)
            elif tax_type == TAX_PPH23:
                result_data = self.tax_logic.calculate_pph23(amount, category, has_npwp, include_ppn, is_gross_up)
            
            output_string = self.format_output(tax_type, category, result_data)
            self.display_result(output_string)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except KeyError as e:
            messagebox.showerror("Configuration Error", f"Kategori '{str(e)}' tidak ditemukan dalam konfigurasi.")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"Terjadi kesalahan: {str(e)}")

    def format_output(self, tax_type, category, data):
        """Formats the result data dictionary into a display string."""
        if not data:
            return "Perhitungan tidak dapat dilakukan."
        
        # Get original amount from the entry field for clarity
        original_amount_str = self.amount_var.get()
        try:
            original_amount = float(original_amount_str.replace(',', ''))
            nominal_awal_str = f"Nominal Awal: Rp{original_amount:,.0f}"
        except ValueError:
            nominal_awal_str = "Nominal Awal: (Invalid)"

        dpp_str = f"Nilai DPP: Rp{data['dpp']:,.0f}"
        final_str = f"Nilai Akhir: Rp{data['final_amount']:,.0f}"
        
        if tax_type == TAX_PPN:
            rate_pct = f"{data['rate']:.0%}"
            tax_str = f"PPN ({rate_pct}): Rp{data['tax']:,.0f}"
            return f"Jenis Pajak: {tax_type}\nKategori: {category}\n{dpp_str}\n{tax_str}\n{final_str}"
        
        elif tax_type == TAX_PPNBM:
            ppn_rate_pct = f"{data['ppn_rate']:.0%}"
            ppnbm_rate_pct = f"{data['ppnbm_rate']:.0%}"
            ppn_str = f"PPN ({ppn_rate_pct}): Rp{data['ppn']:,.0f}"
            ppnbm_str = f"PPnBM ({ppnbm_rate_pct}): Rp{data['ppnbm']:,.0f}"
            return f"Jenis Pajak: {tax_type}\nKategori: {category}\n{dpp_str}\n{ppn_str}\n{ppnbm_str}\n{final_str}"

        elif tax_type == TAX_PPH23:
            rate_pct = f"{data['rate']:.0%}"
            tax_str = f"PPh 23 ({rate_pct}): Rp{data['tax']:,.0f}"
            
            # Check if PPN was part of the calculation
            if 'ppn' in data and data['ppn'] > 0:
                ppn_rate_pct = f"{data['ppn_rate']:.0%}"
                ppn_str = f"PPN ({ppn_rate_pct}): Rp{data['ppn']:,.0f}"
                return (f"Jenis Pajak: {tax_type}\nKategori: {category}\n"
                        f"{nominal_awal_str} (Termasuk PPN)\n"
                        f"{dpp_str}\n{ppn_str}\n{tax_str}\n{final_str}")
            else:
                return (f"Jenis Pajak: {tax_type}\nKategori: {category}\n"
                        f"{dpp_str}\n{tax_str}\n{final_str}")
            
        return "Jenis pajak tidak dikenal."

    def display_result(self, text):
        """Clears and inserts text into the result widget."""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
