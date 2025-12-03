# ui.py
'''
UI Module for CalculaTax
This module contains the main UI class for the tax calculator, redesigned
with a professional, banking-style UX.
'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
from tax_logic import TaxLogic

# --- Constants ---
TAX_PPH23 = 'PPh 23'
TAX_PPN = 'PPN'
TAX_PPNBM = 'PPnBM'

# --- Helper Function for PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Main Application Class (View/Controller) ---
class TaxCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        try:
            # Use the helper function to find the rates file
            rates_path = resource_path("rates.json")
            self.tax_logic = TaxLogic(rates_path)
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Initialization Error", str(e))
            self.destroy()
            return

        self._configure_styles()
        self.title("CalculaTax v2.0 | Bintang")
        self.resizable(False, False)
        
        self.main_frame = ttk.Frame(self, padding="15 15 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.bind_events()
        self.on_tax_change() # Set initial UI state

    def _configure_styles(self):
        """Configures a modern ttk theme and styles."""
        style = ttk.Style(self)
        style.theme_use('clam')

        # --- Colors ---
        self.BG_COLOR = "#f0f2f5"
        self.FG_COLOR = "#1c1c1c"  # Darker text for contrast
        self.PRIMARY_COLOR = "#e30613" # Sinarmas Red
        self.ACCENT_COLOR = "#feebee" # Light red accent

        # --- Base Style Configurations ---
        self.configure(background=self.BG_COLOR)
        style.configure('.', background=self.BG_COLOR, foreground=self.FG_COLOR, font=('Segoe UI', 10))
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('TLabel', background=self.BG_COLOR, foreground=self.FG_COLOR, padding=(0, 5, 0, 5))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('TCheckbutton', background=self.BG_COLOR)

        # --- LabelFrame Style ---
        style.configure('TLabelFrame', background=self.BG_COLOR, bordercolor=self.PRIMARY_COLOR, relief="solid", borderwidth=1)
        style.configure('TLabelFrame.Label', font=('Segoe UI', 11, 'bold'), foreground=self.PRIMARY_COLOR, background=self.BG_COLOR, padding=(10, 0, 10, 0))

        # --- Button Style ---
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), background=self.PRIMARY_COLOR, foreground='white')
        style.map('TButton', background=[('active', '#c00010')]) # Darker red for active state
        
        # --- Entry Style ---
        style.configure('TEntry', font=('Segoe UI', 10), fieldbackground='white')

    def create_widgets(self):
        """Creates and places all UI widgets using a structured layout."""
        # --- CONFIGURATION FRAME ---
        config_frame = ttk.LabelFrame(self.main_frame, text="Konfigurasi Pajak", padding="15 10")
        config_frame.pack(fill=tk.X, expand=True, pady=5)
        config_frame.grid_columnconfigure(1, weight=1)

        self._create_labeled_combobox(config_frame, "Jenis Pajak:", 0, [TAX_PPH23, TAX_PPN, TAX_PPNBM], "tax_type")
        self._create_labeled_combobox(config_frame, "Kategori:", 1, [], "category")

        # --- TRANSACTION FRAME ---
        trans_frame = ttk.LabelFrame(self.main_frame, text="Detail Transaksi", padding="15 10")
        trans_frame.pack(fill=tk.X, expand=True, pady=10)
        trans_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(trans_frame, text="Nominal (IDR):").grid(row=0, column=0, sticky="w")
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(trans_frame, textvariable=self.amount_var, width=25, justify='right')
        self.amount_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # --- Options ---
        options_frame = ttk.Frame(trans_frame)
        options_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        self.has_npwp_var = tk.BooleanVar(value=True)
        self.npwp_checkbox = ttk.Checkbutton(options_frame, text="NPWP", variable=self.has_npwp_var)
        self.npwp_checkbox.pack(side=tk.LEFT, padx=(0, 15))

        self.include_ppn_var = tk.BooleanVar()
        self.ppn_checkbox = ttk.Checkbutton(options_frame, text="PPN", variable=self.include_ppn_var)
        self.ppn_checkbox.pack(side=tk.LEFT, padx=(0, 15))
        
        self.gross_up_var = tk.BooleanVar()
        self.gross_up_checkbox = ttk.Checkbutton(options_frame, text="Gross Up PPh", variable=self.gross_up_var)
        self.gross_up_checkbox.pack(side=tk.LEFT)
        
        # --- ACTION & RESULT ---
        ttk.Button(self.main_frame, text="Hitung Pajak", command=self.calculate, style='TButton').pack(pady=10, fill=tk.X, ipady=4)
        
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Ringkasan Perhitungan", padding="15 10")
        self.result_frame.pack(fill=tk.X, expand=True)
        self.result_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(self.result_frame, text="Hasil akan ditampilkan di sini.").pack()

    def _create_labeled_combobox(self, parent, label_text, row, values, var_name):
        """Helper to create a consistent Label and Combobox pair."""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=(0, 10))
        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)
        
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", pady=5)
        setattr(self, f"{var_name}_combo", combo)
        
        if values:
            combo.set(values[0])

    def bind_events(self):
        self.tax_type_combo.bind("<<ComboboxSelected>>", self.on_tax_change)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        self.amount_var.trace_add('write', self.format_amount_input)

    def format_amount_input(self, *args):
        # A simple mechanism to prevent non-numeric input could go here,
        # but for simplicity, we'll rely on the final validation in calculate().
        pass

    def on_tax_change(self, event=None):
        tax_type = self.tax_type_var.get()
        categories = self.tax_logic.get_categories(tax_type)
        
        self.category_combo.config(values=categories)
        self.category_combo.set(categories[0] if categories else "")
        # Call update_dependent_widgets AFTER setting the new category
        # to ensure the UI state (like NPWP checkbox) is based on the correct new category.
        self.after(1, self._update_dependent_widgets)

    def on_category_change(self, event=None):
        self._update_dependent_widgets()

    def _update_dependent_widgets(self):
        tax_type = self.tax_type_var.get()
        category = self.category_var.get()

        # NPWP Checkbox
        npwp_should_be_enabled = (tax_type == TAX_PPH23 and self.tax_logic.is_npwp_required(category))
        self.npwp_checkbox.config(state="normal" if npwp_should_be_enabled else "disabled")
        if npwp_should_be_enabled:
            self.has_npwp_var.set(True) # Default to checked when enabled for PPh 23
        else:
            self.has_npwp_var.set(False) # Uncheck if disabled

        # PPN Checkbox
        ppn_should_be_enabled = (tax_type == TAX_PPH23)
        self.ppn_checkbox.config(state="normal" if ppn_should_be_enabled else "disabled")
        if not ppn_should_be_enabled: self.include_ppn_var.set(False)

        # Gross Up Checkbox
        gross_up_should_be_enabled = (tax_type == TAX_PPH23)
        self.gross_up_checkbox.config(state="normal" if gross_up_should_be_enabled else "disabled")
        if not gross_up_should_be_enabled: self.gross_up_var.set(False)

    def calculate(self):
        try:
            tax_type, category = self.tax_type_var.get(), self.category_var.get()
            amount_str = self.amount_var.get().replace(',', '')
            if not amount_str: raise ValueError("Nominal tidak boleh kosong.")
            
            amount = float(amount_str)
            has_npwp = self.has_npwp_var.get()
            include_ppn, is_gross_up = self.include_ppn_var.get(), self.gross_up_var.get()

            result_data = self.tax_logic.calculate_pph23(amount, category, has_npwp, include_ppn, is_gross_up) if tax_type == TAX_PPH23 \
                else self.tax_logic.calculate_ppn(amount, category) if tax_type == TAX_PPN \
                else self.tax_logic.calculate_ppnbm(amount, category)

            self.display_result(tax_type, result_data)

        except (ValueError, KeyError) as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"Terjadi kesalahan tak terduga: {str(e)}")

    def display_result(self, tax_type, data):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        if not data:
            ttk.Label(self.result_frame, text="Perhitungan gagal atau tidak tersedia.").pack()
            return

        row_counter = 0
        def add_row(label, value, bold=False):
            nonlocal row_counter
            font_weight = 'bold' if bold else 'normal'
            ttk.Label(self.result_frame, text=label, font=('Segoe UI', 10)).grid(row=row_counter, column=0, sticky='w', pady=2)
            ttk.Label(self.result_frame, text=f"Rp {value:,.0f}", font=('Segoe UI', 10, font_weight)).grid(row=row_counter, column=1, sticky='e', pady=2)
            row_counter += 1

        original_amount = float(self.amount_var.get().replace(',', ''))
        
        # Display logic based on tax type
        if tax_type == TAX_PPH23:
            is_gross_up = data.get('is_gross_up', False)
            dpp = data['dpp']
            
            # Special display logic for the mixed case of Gross-up + PPN
            if is_gross_up and data.get('ppn', 0) > 0:
                add_row("Nominal Awal (Nett)", original_amount)
                add_row("DPP PPh 23 (Gross-up)", data['dpp_gross_up'])
                add_row("DPP PPN", original_amount) # PPN is based on the original amount in this specific case
            elif is_gross_up:
                 add_row("Nominal Awal (Nett)", original_amount)
                 add_row("Dasar Pengenaan Pajak (DPP Gross)", dpp)
            else:
                add_row("Dasar Pengenaan Pajak (DPP)", dpp)
 
            if 'ppn' in data and data['ppn'] > 0:
                add_row(f"PPN ({data['ppn_rate']:.0%})", data['ppn'])
            
            add_row(f"PPh 23 ({data['rate']:.1%})", -data['tax']) # Show tax as negative
            
            ttk.Separator(self.result_frame, orient='horizontal').grid(row=row_counter, column=0, columnspan=2, sticky='ew', pady=8)
            row_counter += 1
            
            # Determine the correct final label based on calculation options
            if is_gross_up:
                # With the logic fix, final_amount is always the total cost in gross-up scenarios.
                add_row("Total Biaya", data['final_amount'], bold=True)
            else:
                add_row("Nominal Diterima" if not data.get('ppn', 0) > 0 else "Total Tagihan", data['final_amount'], bold=True)

        elif tax_type == TAX_PPN:
            add_row("Dasar Pengenaan Pajak (DPP)", data['dpp'])
            add_row(f"PPN ({data['rate']:.0%})", data['tax'])
            ttk.Separator(self.result_frame, orient='horizontal').grid(row=row_counter, column=0, columnspan=2, sticky='ew', pady=8)
            row_counter += 1
            add_row("Total Tagihan", data['final_amount'], bold=True)

        elif tax_type == TAX_PPNBM:
            add_row("Dasar Pengenaan Pajak (DPP)", data['dpp'])
            add_row(f"PPN ({data['ppn_rate']:.0%})", data['ppn'])
            add_row(f"PPnBM ({data['ppnbm_rate']:.0%})", data['ppnbm'])
            ttk.Separator(self.result_frame, orient='horizontal').grid(row=row_counter, column=0, columnspan=2, sticky='ew', pady=8)
            row_counter += 1
            add_row("Total Tagihan", data['final_amount'], bold=True)
