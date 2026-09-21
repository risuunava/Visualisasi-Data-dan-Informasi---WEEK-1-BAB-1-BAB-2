# try-except dasar
try:
    hasil = 10 / 0
except ZeroDivisionError:
    print("Error: pembagian dengan nol tidak diperbolehkan")

# Menangani beberapa jenis error
try:
    nilai = int("abc")
except (ValueError, TypeError):
    print("Input tidak valid")

# else dan finally
try:
    angka = int("123")
except ValueError:
    print("Konversi gagal")
else:
    print("Konversi berhasil:", angka)
finally:
    print("Program selesai")

# Debugging dengan print()
def cari_maksimum(data):
    max_val = data[0]
    for item in data:
        print("Item saat ini:", item, "| Maks saat ini:", max_val)
        if item > max_val:
            max_val = item
    return max_val

angka = [2, 4, 6, 1, 9]
print("Maksimum:", cari_maksimum(angka))

# Contoh mini debugging
nilai = [80, 90, 100]
total = 0
for n in nilai:
    total += n
rata_rata = total / len(nilai)
print("Rata-rata:", rata_rata)