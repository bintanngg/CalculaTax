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
    rates = {
        'barang tidak mewah (11%)': 0.11,
        'barang mewah (12%)': 0.12,
    }
    rate = rates.get(category.lower())
    if rate is None:
        raise ValueError("Kategori PPN tidak valid. Pilih: Barang Tidak Mewah atau Barang Mewah.")
    return amount * rate

# Code for PPnBM
def calculate_ppnbm(amount, category):
    '''
    Pengenaan PPnBM berdasarkan PMK 15/PMK.03/2023
    -Hunian mewah: 20%
    -Balon udara, senjata api, dan peluru selain keperluan negara: 40%
    -Pesawat udara, helikopter, dan peluru/senjata peledak: 50%
    -Kendaraan air mewah, yacht, dsb: 75%
    '''
    ppnbm_mapping = {
        'hunian mewah (20%)': ('hunian_mewah', 0.20),
        'balon udara (40%)': ('balon_senjata', 0.40),
        'pesawat udara (40%)': ('balon_senjata', 0.40),
        'peluru dan senjata api (40%)': ('balon_senjata', 0.40),
        'helikopter (50%)': ('pesawat_peledak', 0.50),
        'pesawat udara lainnya (50%)': ('pesawat_peledak', 0.50),
        'senjata peledak (50%)': ('pesawat_peledak', 0.50),
        'kapal pesiar (75%)': ('yacht', 0.75),
        'yacht (75%)': ('yacht', 0.75)
    }
    internal_cat, rate = ppnbm_mapping.get(category.lower(), (None, None))
    if rate is None:
        raise ValueError(f"Kategori tidak valid. Pilih: {list(ppnbm_mapping.keys())}")
    return amount * rate, internal_cat, rate

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
        pph23_rates = {
            'jasa': (0.02, 0.04),
            'dividen': (0.15, 0.30),
            'bunga': (0.15, 0.30),
            'royalti': (0.15, 0.30),
            'hadiah': (0.15, 0.50),
            'sewa': (0.02, 0.02)
        }
        rates = pph23_rates.get(category.lower())
        if rates is None:
            raise ValueError(f"Kategori tidak valid. Pilih: {list(pph23_rates.keys())}")
        rate = rates[0] if npwp else rates[1]
    return amount * rate, rate

# Calculating Tax Code
def calculate_tax(tax_type_var, category_var, amount_var, npwp_var, result_text):
    try:
        tax_type = tax_type_var.get()
        amount_str = amount_var.get().replace(',', '')
        amount = float(amount_str)
        result_text.delete(1.0, tk.END)
        if tax_type == 'PPN':  # PPN
            kategori = category_var.get()
            pajak_ppn = calculate_ppn(amount, kategori)
            rate_percent = "11%" if 'tidak mewah' in kategori.lower() else "12%"
            nilaippn = amount + pajak_ppn
            result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
            result_text.insert(tk.END, f"Kategori: {kategori}\n")
            result_text.insert(tk.END, f"Nilai DPP: Rp{amount:,.0f}\n")
            result_text.insert(tk.END, f"PPN ({rate_percent}): Rp{pajak_ppn:,.0f}\n")
            result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaippn:,.0f}\n")
        elif tax_type == 'PPnBM':  # PPnBM
            kategori = category_var.get()
            pajak_ppnbm, internal_cat, rate = calculate_ppnbm(amount, kategori)
            rate_percent = f"{int(rate * 100)}%"
            ppn_ppnbm = 0.12 * (amount - pajak_ppnbm)
            nilaiakhir = amount + ppn_ppnbm + pajak_ppnbm
            result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
            result_text.insert(tk.END, f"Kategori: {kategori}\n")
            result_text.insert(tk.END, f"Nilai DPP: Rp{amount:,.0f}\n")
            result_text.insert(tk.END, f"PPN (12%): Rp{ppn_ppnbm:,.0f}\n")
            result_text.insert(tk.END, f"PPnBM ({rate_percent}): Rp{pajak_ppnbm:,.0f}\n")
            result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaiakhir:,.0f}\n")
        else:  # PPh 23
            kategori = category_var.get()
            fintech_dalam = kategori == 'Fintech Dalam Negeri'
            fintech_luar = kategori == 'Fintech Luar Negeri'
            result_text.insert(tk.END, f"Jenis Pajak: {tax_type}\n")
            result_text.insert(tk.END, f"Kategori: {kategori.capitalize()}\n")
            result_text.insert(tk.END, f"Nilai DPP: Rp{amount:,.0f}\n")
            if fintech_dalam:
                pajak, _ = calculate_pph23(amount, 'fintech', npwp=True, fintech=True, fintech_luar=False)
                nilaiakhir = amount - pajak
                result_text.insert(tk.END, f"PPh 23 (15%): Rp{pajak:,.0f}\n")
                result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaiakhir:,.0f}\n")
            elif fintech_luar:
                pajak, _ = calculate_pph23(amount, 'fintech', npwp=True, fintech=True, fintech_luar=True)
                nilaiakhir = amount - pajak
                result_text.insert(tk.END, f"PPh 23 (20%): Rp{pajak:,.0f}\n")
                result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaiakhir:,.0f}\n")
            else:
                npwp = npwp_var.get() == 'Memiliki NPWP'
                pajak, rate = calculate_pph23(amount, kategori, npwp=npwp, fintech=False, fintech_luar=False)
                nilaiakhir = amount - pajak
                rate_percent = int(rate * 100)
                result_text.insert(tk.END, f"PPh 23 ({rate_percent}%): Rp{pajak:,.0f}\n")
                result_text.insert(tk.END, f"Nilai Akhir: Rp{nilaiakhir:,.0f}\n")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def on_tax_type_change(tax_type_var, category_combo, npwp_combo, *args):
    tax_type = tax_type_var.get()
    if tax_type == 'PPN':
        category_combo.config(values=['Barang Tidak Mewah (11%)', 'Barang Mewah (12%)'], state="readonly")
        category_var.set('Barang Tidak Mewah (11%)')
        npwp_combo.config(state="disabled")
        npwp_var.set('')
    elif tax_type == 'PPnBM':
        category_combo.config(values=['Hunian Mewah (20%)',
                                      'Balon Udara (40%)', 'Pesawat Udara (40%)', 'Peluru dan Senjata Api (40%)',
                                      'Helikopter (50%)', 'Pesawat Udara Lainnya (50%)', 'Senjata Peledak (50%)',
                                      'Kapal Pesiar (75%)', 'Yacht (75%)'],
                              state="readonly")
        category_var.set('Hunian Mewah (20%)')
        npwp_combo.config(state="disabled")
        npwp_var.set('')
    else:  # PPh 23
        category_combo.config(values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech Dalam Negeri', 'Fintech Luar Negeri'], state="readonly")
        category_var.set('Jasa')
        npwp_combo.config(state="readonly")
        npwp_var.set('Memiliki NPWP')

def on_category_change(category_var, npwp_combo, *args):
    category = category_var.get()
    if category in ['Fintech Dalam Negeri', 'Fintech Luar Negeri']:
        npwp_combo.config(state="disabled")
        npwp_var.set('')
    else:
        npwp_combo.config(state="readonly")
        npwp_var.set('Memiliki NPWP')

# Code for GUI
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
    root.title("CalculaTax v1.1 | Made by Bintang")
    root.resizable(False, False)  # Membuat window resizable

    # Global variables for GUI
    tax_type_var = tk.StringVar()
    category_var = tk.StringVar()
    amount_var = tk.StringVar()
    npwp_var = tk.StringVar()
    result_text = None
    category_combo = None
    npwp_combo = None

    # Judul
    title_label = tk.Label(root, text="Kalkulator Pajak Indonesia", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Frame untuk input
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # Jenis Pajak
    tk.Label(input_frame, text="Pilih Jenis Pajak:").grid(row=0, column=0, sticky="w")
    tax_type_combo = ttk.Combobox(input_frame, textvariable=tax_type_var, values=['PPh 23', 'PPN', 'PPnBM'], state="readonly")
    tax_type_combo.grid(row=0, column=1, padx=10)
    tax_type_combo.set('PPh 23')  # Default

    # Kategori
    tk.Label(input_frame, text="Pilih Kategori:").grid(row=1, column=0, sticky="w")
    category_combo = ttk.Combobox(input_frame, textvariable=category_var, values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech Dalam Negeri', 'Fintech Luar Negeri'], state="readonly")
    category_combo.grid(row=1, column=1, padx=10)
    category_combo.set('Jasa')  # Default

    # NPWP
    tk.Label(input_frame, text="Status NPWP:").grid(row=2, column=0, sticky="w")
    npwp_combo = ttk.Combobox(input_frame, textvariable=npwp_var, values=['Memiliki NPWP', 'Tidak Memiliki NPWP'], state="readonly")
    npwp_combo.grid(row=2, column=1, padx=10)
    npwp_combo.set('Memiliki NPWP')  # Default

    # Nominal
    tk.Label(input_frame, text="Nominal (IDR):").grid(row=3, column=0, sticky="w")
    amount_entry = tk.Entry(input_frame, textvariable=amount_var)
    amount_entry.grid(row=3, column=1, padx=10)
    amount_var.trace_add("write", format_amount_input)

    # Add trace after category_combo is defined
    tax_type_var.trace_add("write", lambda *args: on_tax_type_change(tax_type_var, category_combo, npwp_combo, *args))
    category_var.trace_add("write", lambda *args: on_category_change(category_var, npwp_combo, *args))

    # Tombol Hitung
    calculate_button = tk.Button(root, text="Hitung Pajak", command=lambda: calculate_tax(tax_type_var, category_var, amount_var, npwp_var, result_text), font=("Arial", 12))
    calculate_button.pack(pady=10)

    # Hasil
    result_label = tk.Label(root, text="Hasil Perhitungan:", font=("Arial", 12, "bold"))
    result_label.pack(pady=5)
    result_text = tk.Text(root, height=6, width=50, wrap=tk.WORD)
    result_text.pack(pady=5)

    # Update global reference
    result_text = result_text

    root.mainloop()
