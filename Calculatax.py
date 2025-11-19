'''This is python script for calculating Tax based regulation in Indonesia'''

import tkinter as tk
from tkinter import ttk, messagebox

#Code for PPH 23
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

def format_amount_input(*args):
    try:
        value = amount_var.get().replace(',', '').replace('.', '')
        if value.isdigit():
            formatted = f"{int(value):,}"
            amount_var.set(formatted)
    except:
        pass

def calculate_tax():
    try:
        kategori = category_var.get()
        amount_str = amount_var.get().replace(',', '')
        amount = float(amount_str)
        fintech = kategori == 'Fintech'
        result_text.delete(1.0, tk.END)
        if fintech:
            pajak_dalam = calculate_pph23(amount, kategori, npwp=True, fintech=True, fintech_luar=False)
            pajak_luar = calculate_pph23(amount, kategori, npwp=True, fintech=True, fintech_luar=True)
            result_text.insert(tk.END, f"Kategori: {kategori.capitalize()}\n")
            result_text.insert(tk.END, f"Pajak PPh 23 Fintech Dalam Negeri (15%): IDR {pajak_dalam:,.0f}\n")
            result_text.insert(tk.END, f"Pajak PPh 23 Fintech Luar Negeri (20%): IDR {pajak_luar:,.0f}\n")
        else:
            pajak_npwp = calculate_pph23(amount, kategori, npwp=True, fintech=False, fintech_luar=False)
            pajak_no_npwp = calculate_pph23(amount, kategori, npwp=False, fintech=False, fintech_luar=False)
            result_text.insert(tk.END, f"Kategori: {kategori.capitalize()}\n")
            result_text.insert(tk.END, f"Pajak PPh 23 dengan NPWP: IDR {pajak_npwp:,.0f}\n")
            result_text.insert(tk.END, f"Pajak PPh 23 tanpa NPWP: IDR {pajak_no_npwp:,.0f}\n")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kalkulator Pajak Indonesia 2025 v1.0 | Made by Bintang")
    root.resizable(True, True)  # Membuat window resizable

    # Judul
    title_label = tk.Label(root, text="Kalkulator Pajak Indonesia 2025", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Frame untuk input
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # Kategori
    tk.Label(input_frame, text="Pilih Kategori:").grid(row=0, column=0, sticky="w")
    category_var = tk.StringVar()
    category_combo = ttk.Combobox(input_frame, textvariable=category_var, values=['Jasa', 'Dividen', 'Bunga', 'Royalti', 'Hadiah', 'Sewa', 'Fintech'], state="readonly")
    category_combo.grid(row=0, column=1, padx=10)
    category_combo.set('Jasa')  # Default

    # Nominal
    tk.Label(input_frame, text="Nominal Penghasilan (IDR):").grid(row=1, column=0, sticky="w")
    amount_var = tk.StringVar()
    amount_entry = tk.Entry(input_frame, textvariable=amount_var)
    amount_entry.grid(row=1, column=1, padx=10)
    amount_var.trace_add("write", format_amount_input)

    # Tombol Hitung
    calculate_button = tk.Button(root, text="Hitung Pajak", command=calculate_tax, font=("Arial", 12))
    calculate_button.pack(pady=10)

    # Hasil
    result_label = tk.Label(root, text="Hasil Perhitungan:", font=("Arial", 12, "bold"))
    result_label.pack(pady=5)
    result_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
    result_text.pack(pady=5)

    root.mainloop()
