"""Titik masuk utama aplikasi CLI Forum Post dan Komentar."""

from forum import (
    buat_post,
    cari_post,
    cari_post_berdasarkan_id,
    hapus_post,
    minta_id_positif,
    minta_konfirmasi,
    minta_pilihan_menu,
    minta_teks_wajib,
    muat_data,
    simpan_data,
    tambah_komentar,
    tampilkan_daftar_post,
    tampilkan_detail_post,
    tampilkan_menu,
    tampilkan_pembuka,
)


def _simpan_perubahan(daftar_post):
    """Menyimpan daftar post terbaru ke file JSON dengan penanganan error penulisan."""
    try:
        simpan_data(daftar_post)
    except OSError as kesalahan:
        print(f"Peringatan: Perubahan gagal disimpan ke file ({kesalahan}).")


def aksi_buat_post(daftar_post):
    """Meminta masukan post baru dari pengguna, menambahkannya, lalu menyimpan ke JSON."""
    print("\n--- Buat Post Baru ---")
    print("(Ketik 'batal' untuk kembali ke menu)")

    penulis = minta_teks_wajib("Nama penulis: ")
    if penulis is None:
        print("Pembuatan post dibatalkan.")
        return

    judul = minta_teks_wajib("Judul post  : ")
    if judul is None:
        print("Pembuatan post dibatalkan.")
        return

    isi = minta_teks_wajib("Isi post    : ")
    if isi is None:
        print("Pembuatan post dibatalkan.")
        return

    post_baru = buat_post(daftar_post, penulis, judul, isi)
    _simpan_perubahan(daftar_post)
    print(f"Post berhasil dibuat dengan ID {post_baru['id']}.")


def aksi_lihat_detail(daftar_post):
    """Meminta ID post lalu menampilkan detail post dan komentarnya jika ditemukan."""
    id_post = minta_id_positif("Masukkan ID post (atau 'batal'): ")
    if id_post is None:
        print("Aksi dibatalkan.")
        return

    post = cari_post_berdasarkan_id(daftar_post, id_post)
    if post is None:
        print(f"Post dengan ID {id_post} tidak ditemukan.")
        return

    tampilkan_detail_post(post)


def aksi_tambah_komentar(daftar_post):
    """Meminta ID post dan data komentar baru, lalu menyimpannya ke file JSON."""
    id_post = minta_id_positif("Masukkan ID post yang dikomentari (atau 'batal'): ")
    if id_post is None:
        print("Penambahan komentar dibatalkan.")
        return

    post = cari_post_berdasarkan_id(daftar_post, id_post)
    if post is None:
        print(f"Post dengan ID {id_post} tidak ditemukan.")
        return

    print(f"Menambah komentar pada: [{post['id']}] {post['judul']}")
    print("(Ketik 'batal' untuk kembali ke menu)")

    penulis = minta_teks_wajib("Nama penulis: ")
    if penulis is None:
        print("Penambahan komentar dibatalkan.")
        return

    isi = minta_teks_wajib("Isi komentar: ")
    if isi is None:
        print("Penambahan komentar dibatalkan.")
        return

    komentar_baru = tambah_komentar(daftar_post, id_post, penulis, isi)
    _simpan_perubahan(daftar_post)
    print(f"Komentar #{komentar_baru['id']} berhasil ditambahkan.")


def aksi_cari_post(daftar_post):
    """Meminta kata kunci lalu menampilkan daftar post yang cocok."""
    kata_kunci = minta_teks_wajib("Kata kunci pencarian (atau 'batal'): ")
    if kata_kunci is None:
        print("Pencarian dibatalkan.")
        return

    hasil = cari_post(daftar_post, kata_kunci)
    tampilkan_daftar_post(
        hasil,
        judul_bagian=f"Hasil Pencarian '{kata_kunci}'",
        pesan_kosong="Tidak ada post yang sesuai dengan kata kunci.",
    )


def aksi_hapus_post(daftar_post):
    """Meminta ID post dan konfirmasi pengguna sebelum menghapus post beserta komentarnya."""
    id_post = minta_id_positif("Masukkan ID post yang akan dihapus (atau 'batal'): ")
    if id_post is None:
        print("Penghapusan dibatalkan.")
        return

    post = cari_post_berdasarkan_id(daftar_post, id_post)
    if post is None:
        print(f"Post dengan ID {id_post} tidak ditemukan.")
        return

    if not minta_konfirmasi(f"Yakin hapus post '[{post['id']}] {post['judul']}'?"):
        print("Penghapusan dibatalkan.")
        return

    hapus_post(daftar_post, id_post)
    _simpan_perubahan(daftar_post)
    print(f"Post ID {id_post} berhasil dihapus.")


def jalankan():
    """Memuat data awal dan menjalankan loop menu utama hingga pengguna keluar."""
    tampilkan_pembuka()
    daftar_post, peringatan = muat_data()
    if peringatan:
        print(peringatan)

    # Peta nomor menu ke fungsi aksi agar pemilihan menu bersih tanpa if/elif panjang
    aksi_menu = {
        "1": lambda: tampilkan_daftar_post(daftar_post),
        "2": lambda: aksi_buat_post(daftar_post),
        "3": lambda: aksi_lihat_detail(daftar_post),
        "4": lambda: aksi_tambah_komentar(daftar_post),
        "5": lambda: aksi_cari_post(daftar_post),
        "6": lambda: aksi_hapus_post(daftar_post),
    }
    pilihan_valid = set(aksi_menu.keys()) | {"0"}

    while True:
        tampilkan_menu()
        pilihan = minta_pilihan_menu(pilihan_valid)
        if pilihan == "0":
            print("Terima kasih, program selesai.")
            break

        aksi_menu[pilihan]()


if __name__ == "__main__":
    # Tangkap Ctrl+C atau EOF agar program berhenti rapi tanpa traceback panjang
    try:
        jalankan()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
