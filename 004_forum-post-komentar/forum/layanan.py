"""Modul logika bisnis dan struktur data untuk post dan komentar forum."""

from datetime import datetime


def _waktu_sekarang():
    """Mengembalikan stempel waktu lokal saat ini dalam format YYYY-MM-DD HH:MM."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _bersihkan_teks(teks, nama_bidang):
    """Memvalidasi bahwa masukan berupa teks tidak kosong dan memangkas spasi tepi."""
    if not isinstance(teks, str):
        raise ValueError(f"{nama_bidang} harus berupa teks.")

    hasil = teks.strip()
    if not hasil:
        raise ValueError(f"{nama_bidang} tidak boleh kosong.")
    return hasil


def buat_id_baru(daftar_item):
    """Menghasilkan ID unik berurutan dari ID terbesar + 1 agar tidak bentrok setelah hapus."""
    if not daftar_item:
        return 1
    # Memakai max(id) + 1 dibanding len() + 1 mencegah duplikasi ID saat ada item yang dihapus
    return max(item["id"] for item in daftar_item) + 1


def cari_post_berdasarkan_id(daftar_post, id_post):
    """Mencari satu post berdasarkan ID secara linear, mengembalikan dict atau None."""
    for post in daftar_post:
        if post["id"] == id_post:
            return post
    return None


def buat_post(daftar_post, penulis, judul, isi, waktu=None):
    """Membuat post baru, menambahkannya ke daftar_post, dan mengembalikan dict post baru."""
    penulis_bersih = _bersihkan_teks(penulis, "Penulis")
    judul_bersih = _bersihkan_teks(judul, "Judul")
    isi_bersih = _bersihkan_teks(isi, "Isi post")

    post_baru = {
        "id": buat_id_baru(daftar_post),
        "penulis": penulis_bersih,
        "judul": judul_bersih,
        "isi": isi_bersih,
        "waktu": waktu if waktu is not None else _waktu_sekarang(),
        "komentar": [],
    }
    daftar_post.append(post_baru)
    return post_baru


def tambah_komentar(daftar_post, id_post, penulis, isi, waktu=None):
    """Menambahkan komentar baru pada post tertentu berdasarkan ID post."""
    post = cari_post_berdasarkan_id(daftar_post, id_post)
    if post is None:
        raise ValueError(f"Post dengan ID {id_post} tidak ditemukan.")

    penulis_bersih = _bersihkan_teks(penulis, "Penulis")
    isi_bersih = _bersihkan_teks(isi, "Isi komentar")

    komentar_baru = {
        "id": buat_id_baru(post["komentar"]),
        "penulis": penulis_bersih,
        "isi": isi_bersih,
        "waktu": waktu if waktu is not None else _waktu_sekarang(),
    }
    post["komentar"].append(komentar_baru)
    return komentar_baru


def cari_post(daftar_post, kata_kunci):
    """Mencari post secara linear (tanpa peka huruf besar/kecil) pada judul, isi, dan penulis."""
    if not isinstance(kata_kunci, str):
        return []

    kunci = kata_kunci.strip().lower()
    if not kunci:
        return []

    hasil = []
    # Ubah teks target menjadi huruf kecil agar pencarian tidak sensitif kapitalisasi
    for post in daftar_post:
        cocok_judul = kunci in post["judul"].lower()
        cocok_isi = kunci in post["isi"].lower()
        cocok_penulis = kunci in post["penulis"].lower()
        if cocok_judul or cocok_isi or cocok_penulis:
            hasil.append(post)

    return hasil


def hapus_post(daftar_post, id_post):
    """Menghapus post berdasarkan ID dan mengembalikan post terhapus, atau None jika tidak ada."""
    # enumerate memberi indeks posisi untuk menghapus langsung dari list dengan pop()
    for indeks, post in enumerate(daftar_post):
        if post["id"] == id_post:
            return daftar_post.pop(indeks)
    return None
