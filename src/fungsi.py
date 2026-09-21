def sapa():
    print("Halo, selamat belajar Python!")

sapa()

def sapa_nama(nama):
    print("Halo,", nama)

sapa_nama("Dina")

def hitung_rata_rata(a, b, c):
    return (a + b + c) / 3

hasil = hitung_rata_rata(80, 90, 70)
print("Rata-rata:", hasil)

def klasifikasi_kelulusan(nilai):
    if nilai >= 75:
        return "Lulus"
    return "Belum lulus"

print(klasifikasi_kelulusan(88))
print(klasifikasi_kelulusan(60))

def hitung_statistik_sederhana(data):
    total = sum(data)
    jumlah = len(data)
    rata_rata = total / jumlah
    return total, jumlah, rata_rata

nilai = [80, 85, 90, 75, 88]
total, jumlah, rata = hitung_statistik_sederhana(nilai)
print("Total:", total)
print("Jumlah data:", jumlah)
print("Rata-rata:", rata)