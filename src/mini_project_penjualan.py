import csv
import json
import os

# =========================================================
# MINI PROJECT 1 — VERSI LANJUTAN
# Python Dasar untuk Mengolah Data Sederhana
# Studi kasus: data penjualan toko kecil
#
# Penambahan dari versi dasar:
# 1. Validasi input (jumlah & harga tidak boleh negatif)
# 2. Fitur kategori produk (Sembako, Minuman, Makanan Instan, dst)
# 3. Perhitungan laba (harga_modal vs harga_jual)
# 4. Simpan hasil ke JSON selain CSV
# 5. Kode dipecah jadi fungsi-fungsi kecil (modular)
# 6. Mode interaktif: input data lewat input()
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "raw", "penjualan.csv")
OUTPUT_DETAIL_CSV = os.path.join(BASE_DIR, "outputs", "penjualan_detail.csv")
OUTPUT_RINGKASAN_CSV = os.path.join(BASE_DIR, "outputs", "ringkasan_penjualan.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "outputs", "penjualan.json")


# =========================================================
# 1. VALIDASI INPUT
# =========================================================

def validasi_item(produk, kategori, jumlah, harga_modal, harga_jual):
    """
    Mengecek satu baris data penjualan.
    Mengembalikan (True, "") kalau valid, atau (False, pesan_error) kalau tidak.
    """
    if jumlah < 0:
        return False, f"Jumlah tidak boleh negatif (produk: {produk}, jumlah: {jumlah})"
    if harga_modal < 0:
        return False, f"Harga modal tidak boleh negatif (produk: {produk})"
    if harga_jual < 0:
        return False, f"Harga jual tidak boleh negatif (produk: {produk})"
    if not produk.strip():
        return False, "Nama produk tidak boleh kosong"
    if not kategori.strip():
        return False, f"Kategori tidak boleh kosong (produk: {produk})"
    return True, ""


# =========================================================
# 2 & 3. BACA DATA (dengan kategori & harga modal) DARI CSV
# =========================================================

def baca_data_csv(path):
    """
    Membaca file CSV dan mengembalikan list data yang SUDAH divalidasi.
    Baris yang tidak valid akan dilewati, dengan pesan peringatan ke layar.
    """
    data_penjualan = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for nomor_baris, row in enumerate(reader, start=2):  # baris 1 = header
            produk = row["produk"]
            kategori = row["kategori"]
            jumlah = int(row["jumlah"])
            harga_modal = int(row["harga_modal"])
            harga_jual = int(row["harga_jual"])

            valid, pesan = validasi_item(produk, kategori, jumlah, harga_modal, harga_jual)
            if not valid:
                print(f"[Dilewati] Baris {nomor_baris}: {pesan}")
                continue

            data_penjualan.append({
                "produk": produk,
                "kategori": kategori,
                "jumlah": jumlah,
                "harga_modal": harga_modal,
                "harga_jual": harga_jual,
            })

    return data_penjualan


# =========================================================
# 3. FUNGSI PERHITUNGAN: OMZET & LABA
# =========================================================

def hitung_omzet_produk(jumlah, harga_jual):
    return jumlah * harga_jual


def hitung_modal_produk(jumlah, harga_modal):
    return jumlah * harga_modal


def hitung_laba_produk(omzet, modal):
    return omzet - modal


def proses_data(data):
    """
    Menambahkan kolom omzet, modal, dan laba ke setiap item.
    """
    for item in data:
        omzet = hitung_omzet_produk(item["jumlah"], item["harga_jual"])
        modal = hitung_modal_produk(item["jumlah"], item["harga_modal"])
        laba = hitung_laba_produk(omzet, modal)

        item["omzet"] = omzet
        item["modal"] = modal
        item["laba"] = laba
    return data


# =========================================================
# FUNGSI AGREGASI / RINGKASAN
# =========================================================

def hitung_total(data, kunci):
    return sum(item[kunci] for item in data)


def hitung_rata_rata(data, kunci):
    if len(data) == 0:
        return 0
    return hitung_total(data, kunci) / len(data)


def cari_item_tertinggi(data, kunci):
    tertinggi = data[0]
    for item in data:
        if item[kunci] > tertinggi[kunci]:
            tertinggi = item
    return tertinggi


def cari_item_terendah(data, kunci):
    terendah = data[0]
    for item in data:
        if item[kunci] < terendah[kunci]:
            terendah = item
    return terendah


def hitung_ringkasan(data):
    """
    Mengembalikan satu dictionary berisi seluruh metrik ringkasan.
    """
    produk_omzet_tertinggi = cari_item_tertinggi(data, "omzet")
    produk_omzet_terendah = cari_item_terendah(data, "omzet")
    produk_terlaris = cari_item_tertinggi(data, "jumlah")
    produk_laba_tertinggi = cari_item_tertinggi(data, "laba")

    return {
        "total_omzet": hitung_total(data, "omzet"),
        "total_modal": hitung_total(data, "modal"),
        "total_laba": hitung_total(data, "laba"),
        "rata_rata_omzet": hitung_rata_rata(data, "omzet"),
        "nilai_maksimum": produk_omzet_tertinggi["omzet"],
        "nilai_minimum": produk_omzet_terendah["omzet"],
        "produk_terlaris": produk_terlaris["produk"],
        "jumlah_terjual_terlaris": produk_terlaris["jumlah"],
        "produk_omzet_tertinggi": produk_omzet_tertinggi["produk"],
        "produk_omzet_terendah": produk_omzet_terendah["produk"],
        "produk_laba_tertinggi": produk_laba_tertinggi["produk"],
        "laba_tertinggi": produk_laba_tertinggi["laba"],
    }


# =========================================================
# TAMPILAN
# =========================================================

def tampilkan_hasil(data, ringkasan):
    print("=" * 70)
    print("RINGKASAN DATA PENJUALAN TOKO KECIL")
    print("=" * 70)
    for item in data:
        print(
            f'Produk: {item["produk"]:<14} | '
            f'Kategori: {item["kategori"]:<15} | '
            f'Jumlah: {item["jumlah"]:>3} | '
            f'Omzet: Rp{item["omzet"]:>9,} | '
            f'Laba: Rp{item["laba"]:>8,}'
        )
    print("-" * 70)
    print(f"Total omzet          : Rp{ringkasan['total_omzet']:,.0f}")
    print(f"Total modal          : Rp{ringkasan['total_modal']:,.0f}")
    print(f"Total laba           : Rp{ringkasan['total_laba']:,.0f}")
    print(f"Rata-rata omzet      : Rp{ringkasan['rata_rata_omzet']:,.2f}")
    print(f"Nilai maksimum       : Rp{ringkasan['nilai_maksimum']:,.0f}")
    print(f"Nilai minimum        : Rp{ringkasan['nilai_minimum']:,.0f}")
    print(f"Produk terlaris      : {ringkasan['produk_terlaris']} "
          f"({ringkasan['jumlah_terjual_terlaris']} unit)")
    print(f"Omzet tertinggi      : {ringkasan['produk_omzet_tertinggi']} "
          f"(Rp{ringkasan['nilai_maksimum']:,.0f})")
    print(f"Omzet terendah       : {ringkasan['produk_omzet_terendah']} "
          f"(Rp{ringkasan['nilai_minimum']:,.0f})")
    print(f"Laba tertinggi       : {ringkasan['produk_laba_tertinggi']} "
          f"(Rp{ringkasan['laba_tertinggi']:,.0f})")
    print("=" * 70)


# =========================================================
# 4. SIMPAN HASIL: CSV & JSON
# =========================================================

def simpan_detail_csv(data, path):
    fieldnames = ["produk", "kategori", "jumlah", "harga_modal", "harga_jual", "modal", "omzet", "laba"]
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def simpan_ringkasan_csv(ringkasan, path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["metrik", "nilai"])
        for metrik, nilai in ringkasan.items():
            writer.writerow([metrik, nilai])


def simpan_json(data, ringkasan, path):
    """
    Menyimpan detail produk + ringkasan dalam satu struktur JSON.
    JSON dipilih karena strukturnya (list of dict + dict) sangat mirip
    dengan struktur data Python asli, dan lazim dipakai untuk API/aplikasi modern.
    """
    hasil = {
        "detail_produk": data,
        "ringkasan": ringkasan,
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(hasil, file, indent=4, ensure_ascii=False)


def simpan_semua_hasil(data, ringkasan):
    os.makedirs(os.path.join(BASE_DIR, "outputs"), exist_ok=True)
    simpan_detail_csv(data, OUTPUT_DETAIL_CSV)
    simpan_ringkasan_csv(ringkasan, OUTPUT_RINGKASAN_CSV)
    simpan_json(data, ringkasan, OUTPUT_JSON)

    print("\nFile berhasil disimpan:")
    print("-", OUTPUT_DETAIL_CSV)
    print("-", OUTPUT_RINGKASAN_CSV)
    print("-", OUTPUT_JSON)


# =========================================================
# 6. MODE INTERAKTIF: INPUT DATA LEWAT input()
# =========================================================

def input_angka(pesan, boleh_negatif=False):
    """
    Meminta input angka ke user, mengulang terus sampai valid.
    Dipakai untuk jumlah, harga_modal, harga_jual agar validasi konsisten
    dengan validasi_item() di atas.
    """
    while True:
        nilai_teks = input(pesan)
        try:
            nilai = int(nilai_teks)
        except ValueError:
            print("  -> Input harus berupa angka bulat. Coba lagi.")
            continue

        if not boleh_negatif and nilai < 0:
            print("  -> Nilai tidak boleh negatif. Coba lagi.")
            continue

        return nilai


def input_data_interaktif():
    """
    Meminta user memasukkan data penjualan satu per satu lewat input().
    Ketik nama produk kosong (Enter langsung) untuk berhenti.
    """
    data_penjualan = []
    print("=== INPUT DATA PENJUALAN (mode interaktif) ===")
    print("Kosongkan nama produk lalu Enter untuk selesai.\n")

    nomor = 1
    while True:
        produk = input(f"[{nomor}] Nama produk: ").strip()
        if produk == "":
            break

        kategori = input("    Kategori (Sembako/Minuman/Makanan Instan/dst): ").strip()
        jumlah = input_angka("    Jumlah terjual: ")
        harga_modal = input_angka("    Harga modal per unit (Rp): ")
        harga_jual = input_angka("    Harga jual per unit (Rp): ")

        valid, pesan = validasi_item(produk, kategori, jumlah, harga_modal, harga_jual)
        if not valid:
            print(f"    -> Data ditolak: {pesan}\n")
            continue

        data_penjualan.append({
            "produk": produk,
            "kategori": kategori,
            "jumlah": jumlah,
            "harga_modal": harga_modal,
            "harga_jual": harga_jual,
        })
        print(f"    -> '{produk}' berhasil ditambahkan.\n")
        nomor += 1

    return data_penjualan


# =========================================================
# 5. PROGRAM UTAMA (MODULAR)
# =========================================================

def jalankan_dari_csv():
    data = baca_data_csv(INPUT_CSV)
    if not data:
        print("Tidak ada data valid untuk diproses.")
        return
    data = proses_data(data)
    ringkasan = hitung_ringkasan(data)
    tampilkan_hasil(data, ringkasan)
    simpan_semua_hasil(data, ringkasan)


def jalankan_interaktif():
    data = input_data_interaktif()
    if not data:
        print("Tidak ada data yang dimasukkan.")
        return
    data = proses_data(data)
    ringkasan = hitung_ringkasan(data)
    tampilkan_hasil(data, ringkasan)
    simpan_semua_hasil(data, ringkasan)


def main():
    print("Pilih mode:")
    print("1. Baca data dari file CSV (data/raw/penjualan.csv)")
    print("2. Input data manual lewat keyboard (interaktif)")
    pilihan = input("Masukkan pilihan (1/2): ").strip()

    if pilihan == "1":
        jalankan_dari_csv()
    elif pilihan == "2":
        jalankan_interaktif()
    else:
        print("Pilihan tidak dikenali. Program dihentikan.")


if __name__ == "__main__":
    main()