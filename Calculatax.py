'''This is python script for calculating Tax based regulation in Indonesia'''

import tkinter as tk
from tkinter import ttk, messagebox

# Code for PPN
def calculate_ppn(amount, category):
   '''
   Pengenaan PPN Berdasarkan Pasal 2 PMK No. 131/2024
   -Barang Tidak Mewah: 11%
   -Barang Mewah: 12%
   '''
   if category.lower() == 'barang tidak mewah':
       rate = 0.11
   elif category.lower() == 'barang mewah':
       rate = 0.12
   else:
       raise ValueError("Kategori PPN tidak valid. Pilih: Barang Tidak Mewah atau Barang Mewah.")
   return amount * rate

# Code for PPH 23
def calculate_pph23(amount, category, npwp=True, fintech=False, fintech_luar=False):
	"""
	Menghitung PPh 23 berdasarkan kategori penghasilan dan status NPWP/fintech.
	Kategori:
	  - 'jasa': 2% (atau 4% tanpa NPWP)
	  - 'dividen': 15% (atau 30% tanpa NPWP)
	  - 'bunga': 15% (atau 30% tanpa NPWP)
	  - 'royalti': 15% (atau 30% tanpa NPWP)
	  - 'hadiah': 15% (atau 50% tanpa NPWP)
	  - 'sewa': 2%
	  - 'fintech': 15% (dalam negeri), 20% (luar negeri)
	"""
	if fintech:
		rate = 0.2 if fintech_luar else 0.15
	else:
		rates = {
			'jasa': 0.02 if npwp else 0.04,
			'dividen': 0.15 if npwp else 0.30,
			'bunga': 0.15 if npwp else 0.30,
			'royalti': 0.15 if npwp else 0.30,
			'hadiah': 0.15 if npwp else 0.50,
			'sewa': 0.02
		}
		rate = rates.get(category.lower())
		if rate is None:
			raise ValueError("Kategori tidak valid. Pilih: jasa, dividen, bunga, royalti, hadiah, sewa, fintech.")
	return amount * rate

# Calculating Tax Code
def calculate_tax(tax_type_var, category_var, amount_var, result_text):
    try:
        tax_type = tax_type_var.get()
        amount_str = amount_var.get().replace(',', '')
        amount = float(amount_str)
        result_text.delete(1.0, tk.END)
        if tax_type == 'PPN': # PPN
            kategori = category_var.get()
            pajak_ppn = calculate_ppn(amount, kategori)
            rate_percent = "11%" if kategori.lower() == 'barang tidak mewah' else "12%"
            nilaippn = amount + pajak_ppn
            result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
            result_text.insert(tk.END, f"Kategori: {kategori}\n")
            result_text.insert(tk.END, f"Nilai DPP: Rp{amount:,.0f}\n")
            result_text.insert(tk.END, f"Pajak PPN ({rate_percent}): Rp{pajak_ppn:,.0f}\n")
            result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaippn:,.0f}\n")
        else:  # PPh 23
            kategori = category_var.get()
            fintech = kategori == 'Fintech'
            if fintech:
                pajak_dalam = calculate_pph23(amount, kategori, npwp=True, fintech=True, fintech_luar=False)
                pajak_luar = calculate_pph23(amount, kategori, npwp=True, fintech=True, fintech_luar=True)
                result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
                result_text.insert(tk.END, f"Kategori: {kategori.capitalize()}\n")
                result_text.insert(tk.END, f"Pajak PPh 23 Fintech Dalam Negeri (15%): Rp{pajak_dalam:,.0f}\n")
                result_text.insert(tk.END, f"Pajak PPh 23 Fintech Luar Negeri (20%): Rp{pajak_luar:,.0f}\n")
            else:
                pajak_npwp = calculate_pph23(amount, kategori, npwp=True, fintech=False, fintech_luar=False)
                pajak_no_npwp = calculate_pph23(amount, kategori, npwp=False, fintech=False, fintech_luar=False)
                result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
                result_text.insert(tk.END, f"Kategori: {kategori.capitalize()}\n")
                result_text.insert(tk.END, f"Pajak PPh 23 dengan NPWP: Rp{pajak_npwp:,.0f}\n")
                result_text.insert(tk.END, f"Pajak PPh 23 tanpa NPWP: Rp{pajak_no_npwp:,.0f}\n")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def on_tax_type_change(*args):
    if tax_type_var.get() == 'PPN':
        category_combo.config(values=['Barang Tidak Mewah', 'Barang Mewah'], state="readonly")
        category_var.set('Barang Tidak Mewah')
    else:
        category_combo.config(values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech'], state="readonly")
        category_var.set('Jasa')

#Code for GUI
def format_amount_input(*args):
    value = amount_var.get()
    clean = value.replace(',', '')
    if clean.isdigit() and clean:
        formatted = f"{int(clean):,}"
        if formatted != value:
            amount_var.set(formatted)
    else:
        # Remove invalid characters
        amount_var.set(''.join(c for c in value if c.isdigit()))
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kalkulator Pajak Indonesia v1.0 | Made by Bintang")
    root.resizable(False, False)  # Membuat window resizable

    # Global variables for GUI
    tax_type_var = tk.StringVar()
    category_var = tk.StringVar()
    amount_var = tk.StringVar()
    result_text = None
    category_combo = None

    # Judul
    title_label = tk.Label(root, text="Kalkulator Pajak Indonesia", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Frame untuk input
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # Jenis Pajak
    tk.Label(input_frame, text="Pilih Jenis Pajak:").grid(row=0, column=0, sticky="w")
    tax_type_combo = ttk.Combobox(input_frame, textvariable=tax_type_var, values=['PPh 23', 'PPN'], state="readonly")
    tax_type_combo.grid(row=0, column=1, padx=10)
    tax_type_combo.set('PPh 23')  # Default
    tax_type_var.trace_add("write", lambda *args: on_tax_type_change(tax_type_var, category_combo, *args))

    # Kategori
    tk.Label(input_frame, text="Pilih Kategori:").grid(row=1, column=0, sticky="w")
    category_combo = ttk.Combobox(input_frame, textvariable=category_var, values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech'], state="readonly")
    category_combo.grid(row=1, column=1, padx=10)
    category_combo.set('Jasa')  # Default

    # Nominal
    tk.Label(input_frame, text="Nominal (IDR):").grid(row=2, column=0, sticky="w")
    amount_entry = tk.Entry(input_frame, textvariable=amount_var)
    amount_entry.grid(row=2, column=1, padx=10)
    amount_var.trace_add("write", format_amount_input)

    # Tombol Hitung
    calculate_button = tk.Button(root, text="Hitung Pajak", command=lambda: calculate_tax(tax_type_var, category_var, amount_var, result_text), font=("Arial", 12))
    calculate_button.pack(pady=10)

    # Hasil
    result_label = tk.Label(root, text="Hasil Perhitungan:", font=("Arial", 12, "bold"))
    result_label.pack(pady=5)
    result_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
    result_text.pack(pady=5)

    # Update global reference
    result_text = result_text

    root.mainloop()
