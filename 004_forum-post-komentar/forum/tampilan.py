"""Modul antarmuka terminal (input, validasi, dan tampilan) untuk aplikasi forum."""

PERINTAH_BATAL = "batal"


def tampilkan_pembuka():
    """Menampilkan judul aplikasi dan panduan pembatalan saat program dimulai."""
    print("=== FORUM POST DAN KOMENTAR ===")
    print("Ketik 'batal' pada kolom masukan untuk kembali ke menu utama.")


def tampilkan_menu():
    """Menampilkan daftar pilihan menu utama aplikasi forum."""
    print("\nMenu:")
    print("1. Lihat daftar post")
    print("2. Buat post baru")
    print("3. Lihat detail post")
    print("4. Tambah komentar")
    print("5. Cari post")
    print("6. Hapus post")
    print("0. Keluar")


def minta_pilihan_menu(pilihan_valid):
    """Meminta pilihan menu hingga pengguna memasukkan opsi yang terdaftar."""
    while True:
        pilihan = input("Pilih menu: ").strip()
        if pilihan in pilihan_valid:
            return pilihan
        print("Pilihan menu tidak valid. Masukkan angka sesuai menu.")


def minta_teks_wajib(label):
    """Meminta masukan teks wajib; kembalikan None jika pengguna mengetik 'batal'."""
    while True:
        masukan = input(label).strip()
        if not masukan:
            print("Masukan tidak boleh kosong. Silakan isi kembali.")
            continue
        # Pakai perbandingan persis (==) agar teks seperti "acara batal" tetap valid
        if masukan.lower() == PERINTAH_BATAL:
            return None
        return masukan


def minta_id_positif(label):
    """Meminta ID bilangan bulat positif; kembalikan None jika mengetik 'batal'."""
    while True:
        masukan = input(label).strip()
        # Cek pembatalan sebelum mengubah ke int agar kata 'batal' tidak dianggap error angka
        if masukan.lower() == PERINTAH_BATAL:
            return None
        # Tangkap ValueError ketika masukan bukan bilangan bulat (misal huruf atau desimal)
        try:
            nilai = int(masukan)
        except ValueError:
            print("ID tidak valid. Masukkan angka bulat positif.")
            continue

        if nilai <= 0:
            print("ID harus lebih besar dari 0.")
            continue

        return nilai


def minta_konfirmasi(pesan):
    """Meminta konfirmasi ya/tidak dari pengguna dan mengembalikan nilai boolean."""
    while True:
        jawaban = input(f"{pesan} (y/n): ").strip().lower()
        if jawaban in ("y", "ya"):
            return True
        if jawaban in ("n", "tidak"):
            return False
        print("Jawaban tidak valid. Ketik 'y' untuk ya atau 'n' untuk tidak.")


def tampilkan_daftar_post(
    daftar_post,
    judul_bagian="Daftar Post",
    pesan_kosong="Belum ada post.",
):
    """Menampilkan ringkasan seluruh post beserta jumlah komentarnya."""
    print(f"\n--- {judul_bagian} ---")
    if not daftar_post:
        print(pesan_kosong)
        return

    for post in daftar_post:
        jumlah_komentar = len(post["komentar"])
        print(
            f"[{post['id']}] {post['judul']} | "
            f"oleh {post['penulis']} | "
            f"{jumlah_komentar} komentar | "
            f"{post['waktu']}"
        )


def tampilkan_detail_post(post):
    """Menampilkan isi lengkap satu post beserta seluruh daftar komentarnya."""
    print("\n--- Detail Post ---")
    print(f"ID      : {post['id']}")
    print(f"Judul   : {post['judul']}")
    print(f"Penulis : {post['penulis']}")
    print(f"Waktu   : {post['waktu']}")
    print(f"Isi     :\n{post['isi']}")

    daftar_komentar = post["komentar"]
    print(f"\nKomentar ({len(daftar_komentar)}):")
    if not daftar_komentar:
        print("Belum ada komentar.")
        return

    for komentar in daftar_komentar:
        print(
            f"  [#{komentar['id']}] {komentar['penulis']} "
            f"({komentar['waktu']}): {komentar['isi']}"
        )
