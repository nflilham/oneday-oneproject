"""Modul pembantu pemuatan aset gambar, ikon jendela, dan avatar inisial untuk GUI."""

from pathlib import Path
from PIL import Image, ImageTk
import customtkinter as ctk

# Lokasi folder assets relatif terhadap akar projek 005
FOLDER_ASET = Path(__file__).resolve().parent.parent / "assets"


def muat_gambar(nama_file, ukuran):
    """Memuat file gambar PNG dari folder assets menjadi objek CTkImage berukuran tetap."""
    path_gambar = FOLDER_ASET / nama_file
    if not path_gambar.exists():
        return None

    try:
        with Image.open(path_gambar) as berkas:
            # Salin ke memori agar berkas gambar di disk segera tertutup
            gambar = berkas.convert("RGBA").copy()
        return ctk.CTkImage(light_image=gambar, size=ukuran)
    except OSError:
        return None


def muat_gambar_berwarna(nama_file, ukuran, warna_hex):
    """Memuat ikon PNG dan mewarnai pikselnya dengan warna hex tertentu sambil mempertahankan alpha."""
    path_gambar = FOLDER_ASET / nama_file
    if not path_gambar.exists():
        return None

    kode = warna_hex.lstrip("#")
    r_target, g_target, b_target = int(kode[0:2], 16), int(kode[2:4], 16), int(kode[4:6], 16)

    try:
        with Image.open(path_gambar) as berkas:
            gambar = berkas.convert("RGBA").copy()
        _, _, _, alpha = gambar.split()
        gambar_warna = Image.new("RGBA", gambar.size, (r_target, g_target, b_target, 255))
        gambar_warna.putalpha(alpha)
        return ctk.CTkImage(light_image=gambar_warna, size=ukuran)
    except OSError:
        return None


def pasang_ikon_jendela(jendela):
    """Mengatur ikon titlebar dan taskbar Windows memakai logo daun."""
    path_ico = FOLDER_ASET / "logo_forum.ico"
    path_png = FOLDER_ASET / "logo_forum.png"

    if path_ico.exists():
        try:
            # Pemanggilan iconbitmap juga mencegah CTk menimpa ikon setelah 200 ms
            jendela.iconbitmap(str(path_ico))
        except Exception:
            pass

    if path_png.exists():
        try:
            with Image.open(path_png) as berkas:
                gambar = berkas.convert("RGBA").copy()
            foto = ImageTk.PhotoImage(gambar, master=jendela)
            # Simpan referensi di objek jendela agar foto tidak dihapus garbage collector
            jendela._ikon_jendela_ref = foto
            jendela.iconphoto(False, foto)
        except Exception:
            pass


def ambil_inisial(nama):
    """Mengambil maksimal dua huruf inisial dari nama penulis untuk badge avatar."""
    bagian = [kata for kata in nama.strip().split() if kata]
    if not bagian:
        return "?"
    if len(bagian) == 1:
        return bagian[0][:2].upper()
    return f"{bagian[0][0]}{bagian[1][0]}".upper()
