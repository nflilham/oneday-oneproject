"""Kalkulator IPK: mengelola data mata kuliah di data.json lalu menghitung IPK."""

import json
import os

# Bobot setiap nilai huruf
BOBOT_NILAI = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}

# Nama file penyimpanan, berada di folder yang sama dengan main.py
FILE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def muat_data():
    """Membaca data.json dan mengembalikan list mata kuliah.

    Bila file belum ada, isinya rusak, atau bentuknya tidak sesuai, kembalikan list kosong
    supaya program tetap berjalan.
    """
    if not os.path.exists(FILE_DATA):
        return []
    try:
        with open(FILE_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError):
        print("Peringatan: data.json rusak atau tidak bisa dibaca. Data dimulai dari kosong.")
        return []

    # Pastikan bentuknya list berisi object dengan nama, nilai, dan sks yang benar
    if not isinstance(data, list):
        print("Peringatan: bentuk data.json tidak sesuai. Data dimulai dari kosong.")
        return []
    for baris in data:
        if (
            not isinstance(baris, dict)
            or not isinstance(baris.get("nama"), str)
            or not isinstance(baris.get("nilai"), str)
            or not isinstance(baris.get("sks"), int)
        ):
            print("Peringatan: isi data.json tidak sesuai. Data dimulai dari kosong.")
            return []
    return data


def simpan_data(daftar):
    """Menulis seluruh daftar mata kuliah ke data.json."""
    with open(FILE_DATA, "w", encoding="utf-8") as berkas:
        json.dump(daftar, berkas, ensure_ascii=False, indent=2)


def baca_nilai():
    """Meminta nilai huruf sampai valid (A-E, huruf kecil boleh), lalu mengembalikannya dalam huruf besar."""
    while True:
        nilai = input("Nilai huruf (A-E): ").strip().upper()
        if nilai in BOBOT_NILAI:
            return nilai
        print("Kesalahan: nilai harus salah satu dari A, B, C, D, E.")


def baca_sks():
    """Meminta SKS sampai valid (bilangan bulat positif), lalu mengembalikannya sebagai int."""
    while True:
        teks = input("SKS: ").strip()
        # isdecimal() hanya True untuk angka 0-9, jadi "abc", "-2", dan "2.5" otomatis ditolak
        if teks.isdecimal() and int(teks) > 0:
            return int(teks)
        print("Kesalahan: SKS harus bilangan bulat positif (contoh: 2).")


def hitung_total_sks(daftar):
    """Menjumlahkan SKS semua mata kuliah."""
    return sum(baris["sks"] for baris in daftar)


def hitung_ipk(daftar):
    """Menghitung IPK: jumlah (bobot x SKS) dibagi total SKS."""
    total_mutu = sum(BOBOT_NILAI[baris["nilai"]] * baris["sks"] for baris in daftar)
    return total_mutu / hitung_total_sks(daftar)


def cetak_tabel(daftar):
    """Mencetak tabel mata kuliah (No, Mata kuliah, Nilai, SKS), lalu total SKS dan IPK."""
    # Lebar kolom nama mengikuti nama terpanjang agar kolom tetap sejajar
    lebar_nama = max(len("Mata kuliah"), max(len(baris["nama"]) for baris in daftar))
    format_baris = "{:<4} {:<" + str(lebar_nama) + "} {:<5} {:>3}"
    garis = "-" * len(format_baris.format("", "", "", ""))

    print()
    print(format_baris.format("No", "Mata kuliah", "Nilai", "SKS"))
    print(garis)
    for nomor, baris in enumerate(daftar, start=1):
        print(format_baris.format(nomor, baris["nama"], baris["nilai"], baris["sks"]))
    print(garis)
    print("Total SKS :", hitung_total_sks(daftar))
    print(f"IPK       : {hitung_ipk(daftar):.2f}")


def lihat_data(daftar):
    """Menu 1: menampilkan tabel dan IPK, atau pesan bila data masih kosong."""
    if not daftar:
        print("Belum ada data")
        return
    cetak_tabel(daftar)


def tambah_data(daftar):
    """Menu 2: meminta satu mata kuliah baru, menambahkannya, lalu menyimpan ke file."""
    nama = input("Nama mata kuliah: ").strip()
    if nama == "":
        print("Kesalahan: nama tidak boleh kosong.")
        return
    nilai = baca_nilai()
    sks = baca_sks()

    daftar.append({"nama": nama, "nilai": nilai, "sks": sks})
    simpan_data(daftar)
    print(f"'{nama}' ditambahkan dan disimpan.")
    # Tampilkan tabel terbaru supaya hasil tambah langsung terlihat
    cetak_tabel(daftar)


def hapus_data(daftar):
    """Menu 3: menghapus satu mata kuliah berdasarkan nomor urut, lalu menyimpan ke file."""
    if not daftar:
        print("Belum ada data")
        return

    cetak_tabel(daftar)
    while True:
        teks = input(f"Nomor yang dihapus (1-{len(daftar)}): ").strip()
        try:
            nomor = int(teks)
        except ValueError:
            print("Kesalahan: masukkan angka nomor urut.")
            continue
        if 1 <= nomor <= len(daftar):
            break
        print(f"Kesalahan: nomor harus antara 1 dan {len(daftar)}.")

    terhapus = daftar.pop(nomor - 1)
    simpan_data(daftar)
    print(f"'{terhapus['nama']}' dihapus dan perubahan disimpan.")
    # Tampilkan tabel terbaru supaya hasil hapus langsung terlihat
    if daftar:
        cetak_tabel(daftar)
    else:
        print("Belum ada data")


def tampilkan_menu():
    """Mencetak pilihan menu utama."""
    print("\n=== Kalkulator IPK ===")
    print("1. Lihat data")
    print("2. Tambah data")
    print("3. Hapus 1 data")
    print("4. Keluar")


def main():
    """Alur utama: muat data sekali, lalu ulangi menu sampai pengguna memilih keluar."""
    daftar = muat_data()
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == "1":
            lihat_data(daftar)
        elif pilihan == "2":
            tambah_data(daftar)
        elif pilihan == "3":
            hapus_data(daftar)
        elif pilihan == "4":
            print("Program selesai.")
            break
        else:
            print("Kesalahan: pilihan harus 1, 2, 3, atau 4.")


if __name__ == "__main__":
    main()
