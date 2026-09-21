import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "raw", "nilai.csv")

# 1. Fungsi untuk menentukan status kelulusan
def tentukan_status(nilai):
    if nilai >= 75:
        return "Lulus"
    return "Belum lulus"

# 2. Siapkan list kosong untuk menampung data
data_mahasiswa = []

# 3. Proses membaca dan mengolah file CSV
with open(INPUT_CSV, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        nama = row["nama"]
        nilai = int(row["nilai"])
        status = tentukan_status(nilai)

        data_mahasiswa.append({
            "nama": nama,
            "nilai": nilai,
            "status": status
        })

# 4. Tampilkan hasil akhir
print("Daftar Hasil Kelulusan:")
print("-" * 30)
for mhs in data_mahasiswa:
    print(f'{mhs["nama"]: <10} | {mhs["nilai"]: <5} | {mhs["status"]}')