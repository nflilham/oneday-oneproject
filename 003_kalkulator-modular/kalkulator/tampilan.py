"""Modul input pengguna dan tampilan terminal untuk kalkulator modular."""

import math

from .operasi import OPERASI


def format_angka(angka):
    """Memformat bilangan agar angka bulat tampil tanpa '.0' di belakang koma."""
    if float(angka).is_integer():
        return str(int(angka))
    return str(angka)


def tampilkan_pembuka():
    """Menampilkan judul program dan panduan singkat penggunaan di awal."""
    print("=== KALKULATOR MODULAR ===")
    print("Masukkan angka dan operasi (+, -, *, /) secara bergantian.")
    print("Ketik '=' setelah minimal 2 angka untuk menghitung, atau 'q' untuk keluar.")


def _baca_angka(prompt, larang_nol=False):
    """Membaca satu masukan angka yang valid dari pengguna atau perintah keluar ('q')."""
    while True:
        masukan = input(prompt).strip()

        if masukan.lower() in ("q", "keluar"):
            return "q"

        if masukan == "=":
            print("Masukkan angka terlebih dahulu sebelum mengetik '='.")
            continue

        # Ubah masukan teks menjadi angka desimal, lalu pastikan bukan nan atau inf
        try:
            angka = float(masukan)
            if not math.isfinite(angka):
                raise ValueError("Angka harus bernilai hingga.")
        except ValueError:
            print("Input tidak valid. Masukkan angka atau 'q' untuk keluar.")
            continue

        # Cegah pembagian dengan nol jika operator tepat sebelumnya adalah '/'
        if larang_nol and angka == 0:
            print("Pembagian dengan nol tidak diizinkan. Masukkan angka lain.")
            continue

        return angka


def _baca_operasi(bisa_hitung):
    """Membaca satu simbol operasi (+, -, *, /), tanda '=', atau perintah keluar ('q')."""
    while True:
        masukan = input("Operasi (+, -, *, /, '=', atau 'q'): ").strip().lower()

        if masukan in ("q", "keluar"):
            return "q"

        if masukan == "=":
            if not bisa_hitung:
                print("Minimal 2 angka diperlukan sebelum menghitung hasil.")
                continue
            return "="

        if masukan in OPERASI:
            return masukan

        print("Operasi tidak valid. Masukkan +, -, *, /, '=', atau 'q'.")


def minta_ekspresi():
    """Meminta rangkaian angka dan operasi secara bergantian hingga '=' atau 'q'."""
    print("\n--- Perhitungan Baru ---")
    angka_pertama = _baca_angka("Angka ke-1 (atau 'q'): ")
    if angka_pertama == "q":
        return None

    daftar_angka = [angka_pertama]
    daftar_operasi = []

    while True:
        simbol = _baca_operasi(bisa_hitung=len(daftar_angka) >= 2)
        if simbol == "q":
            return None
        if simbol == "=":
            return daftar_angka, daftar_operasi

        daftar_operasi.append(simbol)

        nomor_berikutnya = len(daftar_angka) + 1
        angka_berikutnya = _baca_angka(
            f"Angka ke-{nomor_berikutnya} (atau 'q'): ",
            larang_nol=(simbol == "/"),
        )
        if angka_berikutnya == "q":
            return None

        daftar_angka.append(angka_berikutnya)


def tampilkan_hasil(daftar_angka, daftar_operasi, hasil):
    """Menampilkan ekspresi lengkap beserta hasil perhitungannya."""
    bagian = [format_angka(daftar_angka[0])]
    for indeks, simbol in enumerate(daftar_operasi):
        bagian.append(simbol)
        bagian.append(format_angka(daftar_angka[indeks + 1]))

    ekspresi = " ".join(bagian)
    print(f"Hasil: {ekspresi} = {format_angka(hasil)}")
