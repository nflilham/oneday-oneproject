"""Modul penyimpanan data forum ke file JSON lokal."""

import json
from pathlib import Path

# Lokasi file data default berada di folder projek agar aman dijalankan dari mana saja
PATH_DATA_DEFAULT = Path(__file__).resolve().parent.parent / "data_forum.json"

KUNCI_POST_WAJIB = {"id", "penulis", "judul", "isi", "waktu", "komentar"}
KUNCI_KOMENTAR_WAJIB = {"id", "penulis", "isi", "waktu"}


def _id_positif_valid(nilai):
    """Memastikan ID bertipe int positif dan bukan bool (karena bool turunan int di Python)."""
    return isinstance(nilai, int) and not isinstance(nilai, bool) and nilai > 0


def _komentar_valid(item):
    """Memeriksa apakah satu dictionary komentar memiliki kunci dan tipe data yang valid."""
    if not isinstance(item, dict):
        return False
    if not KUNCI_KOMENTAR_WAJIB.issubset(item.keys()):
        return False
    return (
        _id_positif_valid(item["id"])
        and isinstance(item["penulis"], str)
        and isinstance(item["isi"], str)
        and isinstance(item["waktu"], str)
    )


def _post_valid(item):
    """Memeriksa apakah satu dictionary post dan daftar komentarnya berformat valid."""
    if not isinstance(item, dict):
        return False
    if not KUNCI_POST_WAJIB.issubset(item.keys()):
        return False
    if not (
        _id_positif_valid(item["id"])
        and isinstance(item["penulis"], str)
        and isinstance(item["judul"], str)
        and isinstance(item["isi"], str)
        and isinstance(item["waktu"], str)
        and isinstance(item["komentar"], list)
    ):
        return False

    # Pastikan seluruh komentar di dalam post juga memenuhi struktur yang diharapkan
    return all(_komentar_valid(komentar) for komentar in item["komentar"])


def muat_data(path_file=PATH_DATA_DEFAULT):
    """Memuat daftar post dari file JSON, mengembalikan tuple (daftar_post, pesan_peringatan)."""
    path = Path(path_file)

    # Jika file belum pernah dibuat, mulai dengan daftar kosong tanpa peringatan
    if not path.exists():
        return [], None

    # Tangkap error baca file atau JSON rusak agar aplikasi tetap berjalan aman
    try:
        teks_mentah = path.read_text(encoding="utf-8")
        data = json.loads(teks_mentah)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as kesalahan:
        return [], f"Peringatan: Gagal membaca file data ({kesalahan}). Memulai dengan daftar kosong."

    # Tolak struktur akar yang bukan list atau berisi item post tidak valid
    if not isinstance(data, list) or not all(_post_valid(item) for item in data):
        return [], "Peringatan: Format data JSON tidak sesuai. Memulai dengan daftar kosong."

    return data, None


def simpan_data(daftar_post, path_file=PATH_DATA_DEFAULT):
    """Menyimpan daftar post ke file JSON dengan format rapi dan UTF-8."""
    path = Path(path_file)
    # Buat folder induk otomatis bila belum ada (berguna juga untuk direktori uji sementara)
    path.parent.mkdir(parents=True, exist_ok=True)
    # ensure_ascii=False menjaga karakter non-ASCII terbaca alami di file JSON
    teks_json = json.dumps(daftar_post, indent=2, ensure_ascii=False)
    path.write_text(teks_json, encoding="utf-8")
