'''
CalculaTax v.1.2
This is a python script for calculating Tax based on regulations in Indonesia
Made by Bintang
'''

import tkinter as tk
from tkinter import ttk, messagebox

class TaxCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalculaTax v1.2 | Made by Bintang")
        self.resizable(False, False)
        self.setup_tax_rates()
        self.create_widgets()
        self.bind_events()

    def setup_tax_rates(self):
        self.ppn_rates = {'barang tidak mewah (11%)': 0.11, 'barang mewah (12%)': 0.12}
        self.ppnbm_rates = {
            'hunian mewah (20%)': 0.20, 'balon udara (40%)': 0.40, 'pesawat udara (40%)': 0.40,
            'peluru dan senjata api (40%)': 0.40, 'helikopter (50%)': 0.50, 'pesawat udara lainnya (50%)': 0.50,
            'senjata peledak (50%)': 0.50, 'kapal pesiar (75%)': 0.75, 'yacht (75%)': 0.75
        }
        self.pph23_rates = {
            'jasa': (0.02, 0.04), 'dividen': (0.15, 0.30), 'bunga': (0.15, 0.30),
            'royalti': (0.15, 0.30), 'hadiah': (0.15, 0.50), 'sewa': (0.02, 0.02)
        }

    def create_widgets(self):
        tk.Label(self, text="Kalkulator Pajak Indonesia", font=("Arial", 16, "bold")).pack(pady=10)
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Pilih Jenis Pajak:").grid(row=0, column=0, sticky="w")
        self.tax_type = ttk.Combobox(frame, values=['PPh 23', 'PPN', 'PPnBM'], state="readonly")
        self.tax_type.grid(row=0, column=1, padx=10)
        self.tax_type.set('PPh 23')

        tk.Label(frame, text="Pilih Kategori:").grid(row=1, column=0, sticky="w")
        self.category = ttk.Combobox(frame, values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech Dalam Negeri', 'Fintech Luar Negeri'], state="readonly")
        self.category.grid(row=1, column=1, padx=10)
        self.category.set('Jasa')

        tk.Label(frame, text="Status NPWP:").grid(row=2, column=0, sticky="w")
        self.npwp = ttk.Combobox(frame, values=['Memiliki NPWP', 'Tidak Memiliki NPWP'], state="readonly")
        self.npwp.grid(row=2, column=1, padx=10)
        self.npwp.set('Memiliki NPWP')

        tk.Label(frame, text="Nominal (IDR):").grid(row=3, column=0, sticky="w")
        self.amount = tk.Entry(frame)
        self.amount.grid(row=3, column=1, padx=10)
        self.amount_var = tk.StringVar()
        self.amount.config(textvariable=self.amount_var)
        self.amount_var.trace_add("write", self.format_amount)

        tk.Button(self, text="Hitung Pajak", command=self.calculate, font=("Arial", 12)).pack(pady=10)
        tk.Label(self, text="Hasil Perhitungan:", font=("Arial", 12, "bold")).pack(pady=5)
        self.result = tk.Text(self, height=6, width=50, wrap=tk.WORD)
        self.result.pack(pady=5)

    def bind_events(self):
        self.tax_type.bind("<<ComboboxSelected>>", self.on_tax_change)
        self.category.bind("<<ComboboxSelected>>", self.on_category_change)

    def format_amount(self, *args):
        value = self.amount_var.get()
        clean = value.replace(',', '')
        if clean.isdigit() and clean:
            self.amount_var.set(f"{int(clean):,}")
        else:
            self.amount_var.set(''.join(c for c in value if c.isdigit()))

    def on_tax_change(self, event):
        tax = self.tax_type.get()
        if tax == 'PPN':
            self.category.config(values=list(self.ppn_rates.keys()), state="readonly")
            self.category.set(list(self.ppn_rates.keys())[0])
            self.npwp.config(state="disabled")
        elif tax == 'PPnBM':
            self.category.config(values=list(self.ppnbm_rates.keys()), state="readonly")
            self.category.set(list(self.ppnbm_rates.keys())[0])
            self.npwp.config(state="disabled")
        else:
            self.category.config(values=list(self.pph23_rates.keys()) + ['Fintech Dalam Negeri', 'Fintech Luar Negeri'], state="readonly")
            self.category.set(list(self.pph23_rates.keys())[0])
            self.npwp.config(state="readonly")

    def on_category_change(self, event):
        cat = self.category.get()
        if cat in ['Fintech Dalam Negeri', 'Fintech Luar Negeri']:
            self.npwp.config(state="disabled")
        else:
            self.npwp.config(state="readonly")

    def calculate(self):
        try:
            tax_type = self.tax_type.get()
            amount = float(self.amount_var.get().replace(',', ''))
            category = self.category.get().lower()
            self.result.delete(1.0, tk.END)

            if tax_type == 'PPN': #PPN
                rate = self.ppn_rates[category]
                tax = amount * rate
                final = amount + tax
                rate_pct = f"{int(rate*100)}%"
                output = f"Jenis Pajak: {tax_type}\nKategori: {self.category.get()}\nNilai DPP: Rp{amount:,.0f}\nPPN ({rate_pct}): Rp{tax:,.0f}\nNilai Akhir: Rp{final:,.0f}\n"
            elif tax_type == 'PPnBM': #PPnBM
                rate = self.ppnbm_rates[category]
                ppnbm = amount * rate
                ppn = 0.12 * (amount - ppnbm)
                final = amount + ppn + ppnbm
                rate_pct = f"{int(rate*100)}%"
                output = f"Jenis Pajak: {tax_type}\nKategori: {self.category.get()}\nNilai DPP: Rp{amount:,.0f}\nPPN (12%): Rp{ppn:,.0f}\nPPnBM ({rate_pct}): Rp{ppnbm:,.0f}\nNilai Akhir: Rp{final:,.0f}\n"
            else:  # PPh 23
                if category == 'fintech dalam negeri':
                    tax, rate = amount * 0.15, 0.15
                elif category == 'fintech luar negeri':
                    tax, rate = amount * 0.20, 0.20
                else:
                    npwp = self.npwp.get() == 'Memiliki NPWP'
                    rates = self.pph23_rates[category]
                    rate = rates[0] if npwp else rates[1]
                    tax = amount * rate
                final = amount - tax
                rate_pct = f"{int(rate*100)}%"
                output = f"Jenis Pajak: {tax_type}\nKategori: {self.category.get().capitalize()}\nNilai DPP: Rp{amount:,.0f}\nPPh 23 ({rate_pct}%): Rp{tax:,.0f}\nNilai Akhir: Rp{final:,.0f}\n"
            self.result.insert(tk.END, output)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Input tidak valid: {e}")

if __name__ == "__main__":
    app = TaxCalculatorApp()
    app.mainloop()
