"""Modul operasi matematika dasar dan evaluasi prioritas operator."""


def tambah(a, b):
    """Mengembalikan hasil penjumlahan a dan b."""
    return a + b


def kurang(a, b):
    """Mengembalikan hasil pengurangan a dengan b."""
    return a - b


def kali(a, b):
    """Mengembalikan hasil perkalian a dan b."""
    return a * b


def bagi(a, b):
    """Mengembalikan hasil pembagian a dengan b."""
    # Cegah pembagian dengan nol agar program tidak berhenti karena ZeroDivisionError liar
    if b == 0:
        raise ZeroDivisionError("Pembagian dengan nol tidak diizinkan.")
    return a / b


# Peta simbol operasi ke nama tampilan dan fungsinya
OPERASI = {
    "+": ("Penjumlahan", tambah),
    "-": ("Pengurangan", kurang),
    "*": ("Perkalian", kali),
    "/": ("Pembagian", bagi),
}


def hitung_ekspresi(daftar_angka, daftar_operasi):
    """Menghitung daftar angka dan operator dengan prioritas * dan / sebelum + dan -."""
    if len(daftar_angka) < 2:
        raise ValueError("Minimal 2 angka diperlukan untuk menghitung.")

    if len(daftar_operasi) != len(daftar_angka) - 1:
        raise ValueError("Jumlah operator harus satu kurangnya dari jumlah angka.")

    for simbol in daftar_operasi:
        if simbol not in OPERASI:
            raise ValueError(f"Operasi '{simbol}' tidak dikenal.")

    # Tahap 1: kerjakan perkalian (*) dan pembagian (/) terlebih dahulu dari kiri ke kanan
    angka_sisa = [daftar_angka[0]]
    operasi_sisa = []

    for indeks, simbol in enumerate(daftar_operasi):
        angka_kanan = daftar_angka[indeks + 1]
        if simbol in ("*", "/"):
            _, fungsi = OPERASI[simbol]
            angka_sisa[-1] = fungsi(angka_sisa[-1], angka_kanan)
        else:
            operasi_sisa.append(simbol)
            angka_sisa.append(angka_kanan)

    # Tahap 2: kerjakan penjumlahan (+) dan pengurangan (-) yang tersisa dari kiri ke kanan
    hasil = angka_sisa[0]
    for indeks, simbol in enumerate(operasi_sisa):
        _, fungsi = OPERASI[simbol]
        hasil = fungsi(hasil, angka_sisa[indeks + 1])

    return hasil
