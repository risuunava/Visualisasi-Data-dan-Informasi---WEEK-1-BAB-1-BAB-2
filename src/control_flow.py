# if sederhana
nilai = 82
if nilai >= 75:
    print("Lulus")
else:
    print("Belum lulus")

# if - elif - else
nilai = 88
if nilai >= 90:
    print("Predikat A")
elif nilai >= 80:
    print("Predikat B")
elif nilai >= 70:
    print("Predikat C")
else:
    print("Perlu perbaikan")

# Validasi prediksi sederhana
akurasi = 0.87
if akurasi >= 0.9:
    print("Model sangat baik")
elif akurasi >= 0.8:
    print("Model cukup baik")
else:
    print("Model perlu diperbaiki")

# for
angka = [10, 20, 30, 40]
for item in angka:
    print("Nilai:", item)

# for - menjumlah nilai
nilai_list = [80, 75, 90, 88]
total = 0
for n in nilai_list:
    total = total + n

print("Total nilai:", total)
print("Rata-rata:", total / len(nilai_list))

# while
i = 1
while i <= 5:
    print("Perulangan ke-", i)
    i += 1

# Studi kasus: cek kelulusan dari dict
data_nilai = {
    "Andi": 78,
    "Budi": 65,
    "Citra": 92,
    "Dina": 74
}
for nama, nilai in data_nilai.items():
    if nilai >= 75:
        print(nama, "lulus")
    else:
        print(nama, "belum lulus")