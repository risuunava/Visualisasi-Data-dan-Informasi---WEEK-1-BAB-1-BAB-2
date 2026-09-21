# Tipe data dasar
jumlah_mahasiswa = 120
akurasi_model = 0.91
judul = "Pengantar Python"
lulus = True

print(type(jumlah_mahasiswa))
print(type(akurasi_model))
print(type(judul))
print(type(lulus))

# Operator aritmetika
a = 10
b = 3
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000

# Operator perbandingan
nilai = 85
print(nilai > 75)    # True
print(nilai == 100)  # False

# Operator logika
kehadiran = 90
print(nilai >= 75 and kehadiran >= 80)  # True
print(nilai >= 90 or kehadiran >= 90)   # True
print(not nilai < 75)                   # True

# Contoh praktis: nilai akhir
tugas = 80
uts = 78
uas = 90
nilai_akhir = (0.3 * tugas) + (0.3 * uts) + (0.4 * uas)
print("Nilai akhir:", nilai_akhir)  # 83.4