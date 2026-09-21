# list
buah = ["apel", "jeruk", "mangga"]
print(buah[0])

buah.append("pisang")
print(buah)

nilai = [88, 75, 93, 81]
print("Jumlah data:", len(nilai))
print("Nilai tertinggi:", max(nilai))
print("Nilai terendah:", min(nilai))

# tuple
koordinat = (10, 20)
print(koordinat[0])

# set
angka = {1, 2, 2, 3, 4, 4, 5}
print(angka)

# dict
mahasiswa = {
    "nama": "Andi",
    "umur": 20,
    "jurusan": "Informatika"
}
print(mahasiswa["nama"])

mahasiswa["ipk"] = 3.72
print(mahasiswa)

# list berisi dict
data_siswa = [
    {"nama": "Andi", "nilai": 80},
    {"nama": "Budi", "nilai": 70},
    {"nama": "Citra", "nilai": 95}
]
for siswa in data_siswa:
    if siswa["nilai"] >= 75:
        print(siswa["nama"], "lulus")
    else:
        print(siswa["nama"], "belum lulus")