import csv
import json
import pandas as pd

# A. Membaca file teks
with open("data/raw/catatan.txt", "r", encoding="utf-8") as file:
    isi = file.read()
print(isi)

# Menulis file teks
teks = "Ini catatan belajar Python di Ubuntu 26.04."
with open("outputs/hasil_catatan.txt", "w", encoding="utf-8") as file:
    file.write(teks)

# B. Membaca CSV dengan modul csv
with open("data/raw/nilai.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["nama"], row["nilai"])

# Membaca CSV dengan pandas
df = pd.read_csv("data/raw/nilai.csv")
print(df)
print("Rata-rata nilai:", df["nilai"].mean())

# C. Membaca JSON
with open("data/raw/mahasiswa.json", "r", encoding="utf-8") as file:
    data = json.load(file)
for item in data:
    print(item["nama"], item["nilai"])

# Menulis JSON
hasil = {
    "model": "Linear Regression",
    "akurasi": 0.91,
    "status": "baik"
}
with open("outputs/hasil_model.json", "w", encoding="utf-8") as file:
    json.dump(hasil, file, indent=4)