"""Titik masuk utama program kalkulator modular."""

from kalkulator import (
    hitung_ekspresi,
    minta_ekspresi,
    tampilkan_hasil,
    tampilkan_pembuka,
)


def jalankan():
    """Menjalankan loop perhitungan berulang hingga pengguna memilih keluar."""
    tampilkan_pembuka()

    while True:
        masukan = minta_ekspresi()

        if masukan is None:
            print("Terima kasih, program kalkulator selesai.")
            break

        daftar_angka, daftar_operasi = masukan

        # Tangkap error perhitungan sebagai pengaman tambahan jika ada nilai tidak valid
        try:
            hasil = hitung_ekspresi(daftar_angka, daftar_operasi)
        except (ValueError, ZeroDivisionError) as kesalahan:
            print(f"Terjadi kesalahan: {kesalahan}")
            continue

        tampilkan_hasil(daftar_angka, daftar_operasi, hasil)


if __name__ == "__main__":
    # Tangani penghentian mendadak (Ctrl+C atau EOF) agar keluar dengan pesan bersih
    try:
        jalankan()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
