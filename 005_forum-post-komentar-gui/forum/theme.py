"""Sistem desain terpusat (warna, tipografi, ukuran, pemeriksaan kontras WCAG, dan format teks)."""

from datetime import datetime
import customtkinter as ctk

FONT_UTAMA = "Segoe UI"

# Skala ukuran font terpusat sesuai spesifikasi desain
SKALA_FONT = {
    "hero": 24,
    "judul_aplikasi": 20,
    "judul_post": 20,
    "subpanel": 15,
    "seksi": 14,
    "stat_angka": 14,
    "isi_post": 13,
    "isi_komentar": 13,
    "nama_penulis": 13,
    "input": 13,
    "tombol": 13,
    "tombol_kecil": 12,
    "meta": 11,
    "tanggal": 11,
    "error": 11,
    "subjudul": 10,
}

# Palet warna hijau daun & netral hangat; seluruh pasangan teks/latar memenuhi WCAG AA >= 4.5:1
WARNA = {
    "latar": "#EFF4F0",
    "panel": "#FFFFFF",
    "hero": "#EAF2EC",
    "bacaan": "#F7FAF8",
    "kartu": "#EBF2ED",
    "kartu_aktif": "#E1EFE6",
    "kartu_hover": "#D7E7DD",
    "badge": "#D8EAE0",
    "avatar_latar": "#D8EAE0",
    "avatar_teks": "#1F513A",
    "garis": "#D8E2DC",
    "garis_input": "#C2D2C8",
    "scrollbar": "#BFD0C5",
    "scrollbar_hover": "#98B0A1",
    "teks": "#18241E",
    "teks_sekunder": "#4A5D52",
    "meta": "#526358",
    "placeholder": "#55665C",
    "aksen": "#2F6B4F",
    "aksen_hover": "#214E39",
    "bahaya": "#B23A3A",
    "bahaya_hover_latar": "#FDECEC",
    "bahaya_border": "#B23A3A",
    "putih": "#FFFFFF",
}

# Konstanta dimensi dan jarak komponen UI
UKURAN = {
    "lebar_jendela": 1060,
    "tinggi_jendela": 710,
    "min_lebar_jendela": 860,
    "min_tinggi_jendela": 560,
    "min_panel_kiri": 350,
    "min_panel_kanan": 480,
    "radius_panel": 14,
    "radius_kartu": 12,
    "radius_input": 10,
    "radius_pill": 18,
    "tinggi_input": 36,
    "tinggi_tombol_utama": 38,
    "tinggi_tombol": 34,
    "tinggi_tombol_kecil": 26,
    "lebar_input_nama_komentar": 170,
    "avatar_daftar": 36,
    "avatar_detail": 42,
    "avatar_komentar": 32,
    "debounce_cari_ms": 250,
    "rasio_maks_isi_post": 0.33,
    "tinggi_min_isi_post": 54,
    "tinggi_baris_isi_post": 21,
}

NAMA_BULAN_SINGKAT = (
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Agu",
    "Sep",
    "Okt",
    "Nov",
    "Des",
)

# Daftar pasangan warna (teks, latar) yang wajib lolos kontras WCAG AA >= 4.5:1
PASANGAN_KONTRAS_WAJIB = (
    ("teks", "panel"),
    ("teks", "latar"),
    ("teks", "bacaan"),
    ("teks", "kartu"),
    ("teks", "kartu_aktif"),
    ("teks", "kartu_hover"),
    ("teks_sekunder", "panel"),
    ("teks_sekunder", "latar"),
    ("teks_sekunder", "bacaan"),
    ("teks_sekunder", "kartu_aktif"),
    ("meta", "panel"),
    ("meta", "latar"),
    ("meta", "bacaan"),
    ("meta", "kartu_aktif"),
    ("meta", "kartu_hover"),
    ("placeholder", "panel"),
    ("placeholder", "bacaan"),
    ("aksen", "putih"),
    ("aksen", "badge"),
    ("putih", "aksen"),
    ("avatar_teks", "avatar_latar"),
    ("bahaya", "panel"),
    ("bahaya", "bacaan"),
    ("bahaya", "hero"),
    ("bahaya", "bahaya_hover_latar"),
)


def buat_font(kunci_ukuran="isi_post", tebal=False):
    """Membuat objek CTkFont Segoe UI berdasarkan kunci skala ukuran terpusat."""
    ukuran = SKALA_FONT[kunci_ukuran] if isinstance(kunci_ukuran, str) else int(kunci_ukuran)
    return ctk.CTkFont(
        family=FONT_UTAMA,
        size=ukuran,
        weight="bold" if tebal else "normal",
    )


def _kanal_ke_linear(nilai_8bit):
    """Mengubah nilai kanal sRGB (0-255) menjadi luminansi linear sesuai rumus WCAG 2.1."""
    normal = nilai_8bit / 255.0
    if normal <= 0.04045:
        return normal / 12.92
    return ((normal + 0.055) / 1.055) ** 2.4


def luminansi_relatif(warna_hex):
    """Menghitung luminansi relatif (0.0 - 1.0) dari kode warna hex #RRGGBB."""
    kode = warna_hex.lstrip("#")
    r = _kanal_ke_linear(int(kode[0:2], 16))
    g = _kanal_ke_linear(int(kode[2:4], 16))
    b = _kanal_ke_linear(int(kode[4:6], 16))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def hitung_rasio_kontras(warna_satu, warna_dua):
    """Menghitung rasio kontras WCAG antara dua kode warna hex."""
    lum_1 = luminansi_relatif(warna_satu)
    lum_2 = luminansi_relatif(warna_dua)
    terang, gelap = (lum_1, lum_2) if lum_1 >= lum_2 else (lum_2, lum_1)
    return (terang + 0.05) / (gelap + 0.05)


def periksa_semua_kontras(batas_minimum=4.5):
    """Memeriksa seluruh pasangan warna teks/latar dan mengembalikan hasil pemeriksaannya."""
    hasil = []
    for kunci_teks, kunci_latar in PASANGAN_KONTRAS_WAJIB:
        hex_teks = WARNA[kunci_teks]
        hex_latar = WARNA[kunci_latar]
        rasio = hitung_rasio_kontras(hex_teks, hex_latar)
        hasil.append(
            {
                "teks": kunci_teks,
                "latar": kunci_latar,
                "hex_teks": hex_teks,
                "hex_latar": hex_latar,
                "rasio": round(rasio, 2),
                "lolos": rasio >= batas_minimum,
            }
        )
    return hasil


def format_tanggal_ramah(waktu_str):
    """Mengubah 'YYYY-MM-DD HH:MM' menjadi format ramah pengguna seperti '21 Nov 2026, 12:30'."""
    if not isinstance(waktu_str, str):
        return ""
    teks = waktu_str.strip()
    for pola in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(teks, pola)
            nama_bulan = NAMA_BULAN_SINGKAT[dt.month]
            if pola == "%Y-%m-%d":
                return f"{dt.day} {nama_bulan} {dt.year}"
            return f"{dt.day} {nama_bulan} {dt.year}, {dt.strftime('%H:%M')}"
        except ValueError:
            continue
    return teks


def buat_cuplikan_satu_baris(teks, batas_karakter=52):
    """Meratakan teks multi-baris menjadi satu baris ringkas yang dipotong dengan '...' bila panjang."""
    if not isinstance(teks, str):
        return ""
    satu_baris = " ".join(teks.split())
    if len(satu_baris) <= batas_karakter:
        return satu_baris
    return f"{satu_baris[: batas_karakter - 3].rstrip()}..."
