import csv
import os

# =========================================
# MINI PROJECT 1
# Python Dasar untuk Mengolah Data Sederhana
# Studi kasus: data penjualan toko kecil
# =========================================

# Path dibuat relatif terhadap lokasi FILE INI (src/), lalu naik satu level
# ke folder root proyek. Jadi script ini aman dijalankan dari folder mana pun.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "raw", "penjualan.csv")
OUTPUT_DETAIL = os.path.join(BASE_DIR, "outputs", "penjualan_detail.csv")
OUTPUT_RINGKASAN = os.path.join(BASE_DIR, "outputs", "ringkasan_penjualan.csv")

os.makedirs(os.path.join(BASE_DIR, "outputs"), exist_ok=True)

# 1. Baca data penjualan dari CSV (bukan hardcode lagi)
data_penjualan = []
with open(INPUT_CSV, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_penjualan.append({
            "produk": row["produk"],
            "jumlah": int(row["jumlah"]),
            "harga": int(row["harga"]),
        })

# 2. Fungsi untuk menghitung omzet per produk
def hitung_omzet_produk(jumlah, harga):
    return jumlah * harga

# 3. Fungsi untuk menghitung total omzet
def hitung_total_omzet(data):
    total = 0
    for item in data:
        total += item["omzet"]
    return total

# 4. Fungsi untuk menghitung rata-rata omzet
def hitung_rata_rata_omzet(data):
    if len(data) == 0:
        return 0
    return hitung_total_omzet(data) / len(data)

# 5. Fungsi mencari produk dengan omzet tertinggi
def cari_produk_omzet_tertinggi(data):
    produk_tertinggi = data[0]
    for item in data:
        if item["omzet"] > produk_tertinggi["omzet"]:
            produk_tertinggi = item
    return produk_tertinggi

# 6. Fungsi mencari produk dengan omzet terendah
def cari_produk_omzet_terendah(data):
    produk_terendah = data[0]
    for item in data:
        if item["omzet"] < produk_terendah["omzet"]:
            produk_terendah = item
    return produk_terendah

# 7. Fungsi mencari produk terlaris berdasarkan jumlah terjual
def cari_produk_terlaris(data):
    produk_terlaris = data[0]
    for item in data:
        if item["jumlah"] > produk_terlaris["jumlah"]:
            produk_terlaris = item
    return produk_terlaris

# 8. Tambahkan kolom omzet ke setiap produk
for item in data_penjualan:
    item["omzet"] = hitung_omzet_produk(item["jumlah"], item["harga"])

# 9. Hitung ringkasan
total_omzet = hitung_total_omzet(data_penjualan)
rata_rata_omzet = hitung_rata_rata_omzet(data_penjualan)
produk_omzet_tertinggi = cari_produk_omzet_tertinggi(data_penjualan)
produk_omzet_terendah = cari_produk_omzet_terendah(data_penjualan)
produk_terlaris = cari_produk_terlaris(data_penjualan)
nilai_maksimum = produk_omzet_tertinggi["omzet"]
nilai_minimum = produk_omzet_terendah["omzet"]

# 10. Tampilkan hasil ke layar
print("=" * 60)
print("RINGKASAN DATA PENJUALAN TOKO KECIL")
print("=" * 60)
for item in data_penjualan:
    print(
        f'Produk: {item["produk"]:<12} | '
        f'Jumlah: {item["jumlah"]:>3} | '
        f'Harga: Rp{item["harga"]:>7,} | '
        f'Omzet: Rp{item["omzet"]:>8,}'
    )
print("-" * 60)
print(f"Total omzet      : Rp{total_omzet:,.0f}")
print(f"Rata-rata omzet  : Rp{rata_rata_omzet:,.2f}")
print(f"Nilai maksimum   : Rp{nilai_maksimum:,.0f}")
print(f"Nilai minimum    : Rp{nilai_minimum:,.0f}")
print(f'Produk terlaris  : {produk_terlaris["produk"]} '
      f'({produk_terlaris["jumlah"]} unit)')
print(
    f'Omzet tertinggi  : {produk_omzet_tertinggi["produk"]} '
    f'(Rp{produk_omzet_tertinggi["omzet"]:,.0f})'
)
print(
    f'Omzet terendah   : {produk_omzet_terendah["produk"]} '
    f'(Rp{produk_omzet_terendah["omzet"]:,.0f})'
)
print("=" * 60)

# 11. Simpan data detail ke CSV
with open(OUTPUT_DETAIL, "w", newline="", encoding="utf-8") as file_csv:
    fieldnames = ["produk", "jumlah", "harga", "omzet"]
    writer = csv.DictWriter(file_csv, fieldnames=fieldnames)
    writer.writeheader()
    for item in data_penjualan:
        writer.writerow(item)

# 12. Simpan ringkasan ke CSV
with open(OUTPUT_RINGKASAN, "w", newline="", encoding="utf-8") as file_ringkasan:
    writer = csv.writer(file_ringkasan)
    writer.writerow(["metrik", "nilai"])
    writer.writerow(["total_omzet", total_omzet])
    writer.writerow(["rata_rata_omzet", rata_rata_omzet])
    writer.writerow(["nilai_maksimum", nilai_maksimum])
    writer.writerow(["nilai_minimum", nilai_minimum])
    writer.writerow(["produk_terlaris", produk_terlaris["produk"]])
    writer.writerow(["jumlah_terjual_terlaris", produk_terlaris["jumlah"]])
    writer.writerow(["produk_omzet_tertinggi", produk_omzet_tertinggi["produk"]])
    writer.writerow(["produk_omzet_terendah", produk_omzet_terendah["produk"]])

print("\nFile berhasil disimpan:")
print("-", OUTPUT_DETAIL)
print("-", OUTPUT_RINGKASAN)