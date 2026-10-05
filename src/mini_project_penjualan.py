"""Mini Project 1 - Analisis Penjualan Toko Kecil.

Sumber data: data/raw/penjualan.csv
Mode: 1) baca CSV -> laporan | 2) input manual -> append ke CSV -> laporan.
Output selalu ditulis ulang di outputs/: penjualan_detail.csv, ringkasan_penjualan.csv, penjualan.json.
"""

import csv
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "raw" / "penjualan.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

KATEGORI_VALID = ["Sembako", "Minuman", "Makanan ringan", "Makanan Instan"]
FIELDNAMES = ["produk", "kategori", "jumlah", "harga_modal", "harga_jual",
              "omzet", "laba", "margin_persen"]
HEADER_RAW_BARU = ["produk", "kategori", "jumlah", "harga_modal", "harga_jual"]
KOLOM_WAJIB = ["produk", "kategori", "jumlah", "harga_modal"]  # + harga / harga_jual


# --- Validasi ---
def bersihkan_angka(nilai):
    """Buang 'Rp', spasi, dan titik pemisah ribuan ('15.000' -> '15000')."""
    teks = re.sub(r"(?i)rp|\s", "", str(nilai).strip())
    return teks.replace(".", "") if re.fullmatch(r"\d{1,3}(\.\d{3})+", teks) else teks


def validasi_angka_tidak_negatif(nilai, nama_field):
    """Pastikan nilai angka dan tidak negatif."""
    try:
        angka = float(bersihkan_angka(nilai))
    except (ValueError, TypeError):
        raise ValueError(f"{nama_field} harus berupa angka, bukan '{nilai}'") from None
    if angka < 0:
        raise ValueError(f"{nama_field} tidak boleh negatif (diterima: {angka:g})")
    return int(angka) if angka == int(angka) else angka


def validasi_kategori(kategori):
    """Cocokkan kategori dengan KATEGORI_VALID (tidak peka huruf besar/kecil)."""
    cocok = next((v for v in KATEGORI_VALID if str(kategori).strip().lower() == v.lower()), None)
    if cocok is None:
        raise ValueError(f"Kategori '{kategori}' tidak dikenal. Pilihan: {', '.join(KATEGORI_VALID)}")
    return cocok


def validasi_produk(produk, kategori, jumlah, harga_modal, harga_jual):
    """Validasi satu produk, kembalikan dictionary bersih."""
    nama = str(produk).strip()
    if not nama:
        raise ValueError("Nama produk tidak boleh kosong")
    return {
        "produk": nama,
        "kategori": validasi_kategori(kategori),
        "jumlah": validasi_angka_tidak_negatif(jumlah, "Jumlah"),
        "harga_modal": validasi_angka_tidak_negatif(harga_modal, "Harga modal"),
        "harga_jual": validasi_angka_tidak_negatif(harga_jual, "Harga jual"),
    }


# --- Membaca CSV ---
def cek_header(fieldnames):
    """Pastikan kolom wajib ada. Kembalikan nama kolom harga jual ('harga'/'harga_jual')."""
    kolom = [f.strip().lower() for f in (fieldnames or [])]
    kolom_harga = "harga_jual" if "harga_jual" in kolom else "harga" if "harga" in kolom else None
    kurang = [k for k in KOLOM_WAJIB if k not in kolom]
    if kolom_harga is None:
        kurang.append("harga_jual (atau harga)")
    if kurang:
        raise ValueError(
            "Kolom CSV kurang: " + ", ".join(kurang)
            + "\n  Header yang dibutuhkan: produk,kategori,jumlah,harga_modal,harga_jual")
    return kolom_harga


def baca_data_csv(path):
    """Baca CSV, validasi tiap baris. Baris tidak valid dilewati dengan peringatan."""
    data = []
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        kolom_harga = cek_header(reader.fieldnames)
        for no_baris, row in enumerate(reader, start=2):  # baris 1 = header
            row = {(k or "").strip().lower(): v for k, v in row.items()}
            try:
                data.append(validasi_produk(
                    row["produk"], row["kategori"], row["jumlah"],
                    row["harga_modal"], row[kolom_harga]))
            except (ValueError, KeyError, AttributeError) as e:
                print(f"  [!] Baris {no_baris} dilewati: {e}")
    return data


# --- Input interaktif ---
def minta_input_angka(pesan, nama_field):
    """Ulangi pertanyaan sampai angka valid (tidak negatif)."""
    while True:
        try:
            return validasi_angka_tidak_negatif(input(pesan), nama_field)
        except ValueError as e:
            print(f"  [!] {e}. Silakan coba lagi.")


def minta_input_kategori():
    """Menu kategori bernomor, ulangi sampai valid."""
    while True:
        print("  Kategori:", ", ".join(f"{i}. {k}" for i, k in enumerate(KATEGORI_VALID, 1)))
        pilihan = input("  Pilih nomor kategori: ").strip()
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(KATEGORI_VALID):
            return KATEGORI_VALID[int(pilihan) - 1]
        print("  [!] Pilihan tidak valid.")


def input_data_interaktif():
    """Minta produk satu per satu. Enter kosong atau 'selesai' untuk berhenti."""
    data = []
    print("\n=== INPUT DATA PENJUALAN ===")
    print("Kosongkan nama produk lalu Enter (atau ketik 'selesai') untuk berhenti.")
    while True:
        nama = input(f"\n[{len(data) + 1}] Nama produk: ").strip()
        if nama == "" or nama.lower() == "selesai":
            break
        data.append(validasi_produk(
            nama, minta_input_kategori(),
            minta_input_angka("  Jumlah terjual: ", "Jumlah"),
            minta_input_angka("  Harga modal satuan (Rp): ", "Harga modal"),
            minta_input_angka("  Harga jual satuan (Rp): ", "Harga jual"),
        ))
        print(f"  [v] '{nama}' ditambahkan.")
    return data


# --- Perhitungan ---
def tambah_kolom_hitungan(data):
    """Tambahkan kolom omzet, laba, dan margin (%) ke tiap produk."""
    for item in data:
        item["omzet"] = item["jumlah"] * item["harga_jual"]
        item["laba"] = item["jumlah"] * (item["harga_jual"] - item["harga_modal"])
        item["margin_persen"] = round(item["laba"] / item["omzet"] * 100, 2) if item["omzet"] else 0
    return data


def ringkas_per_kategori(data):
    """Kelompokkan per kategori: jumlah produk, unit, omzet, laba."""
    hasil = {}
    for item in data:
        k = hasil.setdefault(item["kategori"], {"jumlah_produk": 0, "total_unit": 0,
                                                "total_omzet": 0, "total_laba": 0})
        k["jumlah_produk"] += 1
        k["total_unit"] += item["jumlah"]
        k["total_omzet"] += item["omzet"]
        k["total_laba"] += item["laba"]
    return hasil


def buat_ringkasan(data):
    """Kumpulkan semua metrik penting dalam satu dictionary."""
    total_omzet = sum(i["omzet"] for i in data)
    total_laba = sum(i["laba"] for i in data)
    terlaris = max(data, key=lambda i: i["jumlah"])
    omzet_max = max(data, key=lambda i: i["omzet"])["produk"]
    omzet_min = min(data, key=lambda i: i["omzet"])["produk"]
    laba_max = max(data, key=lambda i: i["laba"])["produk"]
    laba_min = min(data, key=lambda i: i["laba"])["produk"]
    return {
        "total_omzet": total_omzet,
        "total_modal": total_omzet - total_laba,
        "total_laba": total_laba,
        "rata_rata_omzet": total_omzet / len(data) if data else 0,
        "rata_rata_laba": total_laba / len(data) if data else 0,
        "produk_terlaris": terlaris["produk"],
        "jumlah_terjual_terlaris": terlaris["jumlah"],
        "produk_omzet_tertinggi": omzet_max,
        "produk_omzet_terendah": omzet_min,
        "produk_laba_tertinggi": laba_max,
        "produk_laba_terendah": laba_min,
        "per_kategori": ringkas_per_kategori(data),
    }


# --- Tampilan ---
def tampilkan_laporan(data, ringkasan, judul):
    garis = "=" * 96
    print("\n" + garis)
    print(judul)
    print(garis)
    print(f"{'Produk':<18}{'Kategori':<16}{'Jml':>5}{'Omzet (Rp)':>14}{'Laba (Rp)':>14}{'Margin':>9}")
    print("-" * 96)
    for i in data:
        print(f"{i['produk']:<18}{i['kategori']:<16}{i['jumlah']:>5}"
              f"{i['omzet']:>14,.0f}{i['laba']:>14,.0f}{i['margin_persen']:>8.1f}%")
    print("-" * 96)
    print(f"Total omzet            : Rp{ringkasan['total_omzet']:,.0f}")
    print(f"Total modal            : Rp{ringkasan['total_modal']:,.0f}")
    print(f"Total laba             : Rp{ringkasan['total_laba']:,.0f}")
    print(f"Rata-rata omzet        : Rp{ringkasan['rata_rata_omzet']:,.2f}")
    print(f"Rata-rata laba         : Rp{ringkasan['rata_rata_laba']:,.2f}")
    print(f"Produk terlaris        : {ringkasan['produk_terlaris']} ({ringkasan['jumlah_terjual_terlaris']} unit)")
    print(f"Omzet tertinggi        : {ringkasan['produk_omzet_tertinggi']}")
    print(f"Omzet terendah         : {ringkasan['produk_omzet_terendah']}")
    print(f"Laba tertinggi         : {ringkasan['produk_laba_tertinggi']}")
    print(f"Laba terendah          : {ringkasan['produk_laba_terendah']}")
    print("\nRingkasan per kategori:")
    for nama, k in ringkasan["per_kategori"].items():
        print(f"  - {nama:<15}: {k['jumlah_produk']} produk | {k['total_unit']} unit | "
              f"omzet Rp{k['total_omzet']:,.0f} | laba Rp{k['total_laba']:,.0f}")
    print(garis)


# --- Penyimpanan ---
def tambah_ke_raw(data_baru, path):
    """Tambahkan produk baru ke BAWAH CSV (mode 'a'). Ikuti header asli ('harga'/'harga_jual')."""
    path = Path(path)
    if not (path.exists() and path.stat().st_size > 0):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER_RAW_BARU)
            writer.writeheader()
            writer.writerows(data_baru)
        return

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        header = next(csv.reader(f), [])
    kolom_harga = cek_header(header)  # error jika kolom wajib kurang
    perlu_enter = Path(path).read_bytes()[-1:] not in (b"\n", b"\r")

    with open(path, "a", newline="", encoding="utf-8") as f:
        if perlu_enter:
            f.write("\r\n")
        writer = csv.writer(f)
        for item in data_baru:
            nilai = {"produk": item["produk"], "kategori": item["kategori"],
                     "jumlah": item["jumlah"], "harga_modal": item["harga_modal"],
                     kolom_harga: item["harga_jual"]}
            writer.writerow([nilai.get(k.strip().lower(), "") for k in header])


def proses_dan_simpan(data, judul):
    """Hitung, tampilkan, dan simpan hasil ke outputs/ (dipakai kedua opsi)."""
    data = tambah_kolom_hitungan(data)
    ringkasan = buat_ringkasan(data)
    tampilkan_laporan(data, ringkasan, judul)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "penjualan_detail.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)
    with open(OUTPUT_DIR / "ringkasan_penjualan.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metrik", "nilai"])
        writer.writerows([k, v] for k, v in ringkasan.items() if k != "per_kategori")
    with open(OUTPUT_DIR / "penjualan.json", "w", encoding="utf-8") as f:
        json.dump({"detail_produk": data, "ringkasan": ringkasan}, f, indent=4, ensure_ascii=False)
    print("\nFile disimpan di outputs/: penjualan_detail.csv, ringkasan_penjualan.csv, penjualan.json")


# --- Alur per opsi ---
def jalankan_opsi_1():
    """Opsi 1: baca data/raw/penjualan.csv."""
    if not INPUT_CSV.exists():
        print(f"File tidak ditemukan: {INPUT_CSV}")
        print("Jalankan opsi 2 untuk membuatnya.")
        return
    try:
        data = baca_data_csv(INPUT_CSV)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return
    if not data:
        print("Tidak ada data valid untuk diproses.")
        return
    proses_dan_simpan(data, f"RINGKASAN PENJUALAN ({len(data)} produk dari data/raw/penjualan.csv)")


def jalankan_opsi_2():
    """Opsi 2: input manual -> ditambahkan ke data/raw/penjualan.csv -> outputs diperbarui."""
    data_baru = input_data_interaktif()
    if not data_baru:
        print("Tidak ada data yang dimasukkan. File tidak diubah.")
        return
    try:
        tambah_ke_raw(data_baru, INPUT_CSV)
        data = baca_data_csv(INPUT_CSV)  # baca ulang SEMUA data (lama + baru)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return
    print(f"\n{len(data_baru)} produk baru ditambahkan ke data/raw/penjualan.csv")
    proses_dan_simpan(data, f"RINGKASAN SEMUA DATA ({len(data)} produk di data/raw/penjualan.csv)")


# --- Program utama ---
def pilih_mode():
    print("=== MINI PROJECT PENJUALAN ===")
    print("1. Baca data dari file CSV (data/raw/penjualan.csv)")
    print("2. Input data manual (ditambahkan ke data/raw/penjualan.csv)")
    while True:
        pilihan = input("Pilih mode (1/2): ").strip()
        if pilihan in ("1", "2"):
            return pilihan
        print("  [!] Masukkan 1 atau 2.")


def main():
    try:
        jalankan_opsi_1() if pilih_mode() == "1" else jalankan_opsi_2()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan (Ctrl+C). Data sesi ini belum disimpan.")


if __name__ == "__main__":
    main()
