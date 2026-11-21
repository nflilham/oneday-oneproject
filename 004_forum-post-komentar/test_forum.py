"""Pengujian otomatis untuk modul layanan dan penyimpanan aplikasi forum."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from forum.layanan import (
    buat_post,
    cari_post,
    cari_post_berdasarkan_id,
    hapus_post,
    tambah_komentar,
)
from forum.penyimpanan import muat_data, simpan_data
from forum.tampilan import minta_id_positif, minta_teks_wajib


class TestLayananForum(unittest.TestCase):
    """Kumpulan pengujian logika pembuatan, pencarian, komentar, dan penghapusan post."""

    def test_buat_post_berhasil(self):
        """Post baru tersimpan dengan ID 1, teks terpangkas, dan komentar kosong."""
        daftar_post = []
        post = buat_post(
            daftar_post,
            "  Naufal  ",
            "  Belajar Python  ",
            "  Hari keempat latihan  ",
            waktu="2026-11-21 12:00",
        )

        self.assertEqual(len(daftar_post), 1)
        self.assertEqual(post["id"], 1)
        self.assertEqual(post["penulis"], "Naufal")
        self.assertEqual(post["judul"], "Belajar Python")
        self.assertEqual(post["isi"], "Hari keempat latihan")
        self.assertEqual(post["komentar"], [])

    def test_buat_post_input_kosong_ditolak(self):
        """Input kosong atau hanya spasi pada penulis, judul, atau isi memicu ValueError."""
        daftar_post = []
        with self.assertRaises(ValueError):
            buat_post(daftar_post, "   ", "Judul", "Isi")
        with self.assertRaises(ValueError):
            buat_post(daftar_post, "Naufal", "", "Isi")
        with self.assertRaises(ValueError):
            buat_post(daftar_post, "Naufal", "Judul", "  \t ")
        self.assertEqual(daftar_post, [])

    def test_tambah_komentar_berhasil(self):
        """Komentar baru masuk ke daftar komentar post target dengan ID berurutan."""
        daftar_post = []
        buat_post(daftar_post, "Naufal", "Belajar Python", "Hari keempat")

        komentar = tambah_komentar(
            daftar_post,
            1,
            "Budi",
            "Semangat",
            waktu="2026-11-21 12:05",
        )

        post = cari_post_berdasarkan_id(daftar_post, 1)
        self.assertEqual(komentar["id"], 1)
        self.assertEqual(len(post["komentar"]), 1)
        self.assertEqual(post["komentar"][0]["penulis"], "Budi")
        self.assertEqual(post["komentar"][0]["isi"], "Semangat")

    def test_tambah_komentar_error_id_atau_input_kosong(self):
        """Komentar pada ID yang tidak ada atau berisi teks kosong memicu ValueError."""
        daftar_post = []
        buat_post(daftar_post, "Naufal", "Judul", "Isi")

        with self.assertRaises(ValueError):
            tambah_komentar(daftar_post, 99, "Budi", "Halo")
        with self.assertRaises(ValueError):
            tambah_komentar(daftar_post, 1, "  ", "Halo")
        with self.assertRaises(ValueError):
            tambah_komentar(daftar_post, 1, "Budi", "")

    def test_cari_post_tidak_peka_kapital(self):
        """Pencarian cocok di judul, isi, atau penulis tanpa membedakan huruf besar/kecil."""
        daftar_post = []
        buat_post(daftar_post, "Naufal", "Belajar Python", "Hari keempat latihan")
        buat_post(daftar_post, "Sari", "Catatan Kuliah", "Membahas struktur data")

        self.assertEqual(len(cari_post(daftar_post, "python")), 1)
        self.assertEqual(len(cari_post(daftar_post, "STRUKTUR")), 1)
        self.assertEqual(len(cari_post(daftar_post, "naufal")), 1)
        self.assertEqual(cari_post(daftar_post, "tidakada"), [])
        self.assertEqual(cari_post(daftar_post, "   "), [])

    def test_hapus_post_dan_id_baru_tidak_bentrok(self):
        """Setelah menghapus ID 1 dari [1, 2], post baru mendapat ID 3 dan bukan ID 2."""
        daftar_post = []
        buat_post(daftar_post, "Naufal", "Post Satu", "Isi satu")
        buat_post(daftar_post, "Budi", "Post Dua", "Isi dua")

        terhapus = hapus_post(daftar_post, 1)
        self.assertIsNotNone(terhapus)
        self.assertEqual(terhapus["id"], 1)
        self.assertIsNone(hapus_post(daftar_post, 99))

        post_ketiga = buat_post(daftar_post, "Sari", "Post Tiga", "Isi tiga")
        self.assertEqual(post_ketiga["id"], 3)
        self.assertEqual([p["id"] for p in daftar_post], [2, 3])


class TestPenyimpananForum(unittest.TestCase):
    """Kumpulan pengujian simpan dan muat JSON memakai direktori sementara."""

    def test_muat_data_saat_file_belum_ada(self):
        """Jika file JSON belum ada, kembalikan daftar kosong tanpa peringatan."""
        with tempfile.TemporaryDirectory() as folder_uji:
            path_file = Path(folder_uji) / "belum_ada.json"
            data, peringatan = muat_data(path_file)
            self.assertEqual(data, [])
            self.assertIsNone(peringatan)

    def test_simpan_dan_muat_data_utuh(self):
        """Data post beserta komentar tersimpan ke JSON dan terbaca kembali dengan utuh."""
        with tempfile.TemporaryDirectory() as folder_uji:
            path_file = Path(folder_uji) / "data_forum.json"
            daftar_awal = []
            buat_post(daftar_awal, "Naufal", "Belajar Python", "Hari keempat latihan")
            tambah_komentar(daftar_awal, 1, "Budi", "Semangat")

            simpan_data(daftar_awal, path_file)
            data_muat, peringatan = muat_data(path_file)

            self.assertIsNone(peringatan)
            self.assertEqual(data_muat, daftar_awal)

    def test_muat_data_json_rusak_atau_format_salah(self):
        """File JSON rusak atau bukan list post valid tetap aman dengan daftar kosong."""
        with tempfile.TemporaryDirectory() as folder_uji:
            path_rusak = Path(folder_uji) / "rusak.json"
            path_rusak.write_text("{ini bukan json valid", encoding="utf-8")

            data_rusak, peringatan_rusak = muat_data(path_rusak)
            self.assertEqual(data_rusak, [])
            self.assertIsNotNone(peringatan_rusak)

            path_salah = Path(folder_uji) / "salah.json"
            path_salah.write_text('{"bukan": "list"}', encoding="utf-8")

            data_salah, peringatan_salah = muat_data(path_salah)
            self.assertEqual(data_salah, [])
            self.assertIsNotNone(peringatan_salah)


class TestTampilanForum(unittest.TestCase):
    """Kumpulan pengujian validasi input terminal dan perintah pembatalan."""

    def test_minta_teks_wajib_bisa_batal(self):
        """Perintah 'batal' tanpa peka kapital mengembalikan None."""
        for masukan in ("batal", "BATAL"):
            with patch("builtins.input", return_value=masukan):
                self.assertIsNone(minta_teks_wajib("Input: "))

    def test_minta_teks_wajib_tolak_kosong_dan_terima_kalimat_berkata_batal(self):
        """Input kosong ditolak, sedangkan kalimat berisi kata 'batal' tetap diterima."""
        with patch("builtins.print"), patch(
            "builtins.input",
            side_effect=["", "   ", "Acara batal hari ini"],
        ):
            hasil = minta_teks_wajib("Input: ")
        self.assertEqual(hasil, "Acara batal hari ini")

    def test_minta_id_positif_bisa_batal(self):
        """Perintah 'batal' pada input ID mengembalikan None."""
        with patch("builtins.input", return_value="batal"):
            self.assertIsNone(minta_id_positif("ID: "))

    def test_minta_id_positif_tolak_tidak_valid_lalu_terima_angka_positif(self):
        """Huruf, nol, dan angka negatif ditolak sebelum menerima angka bulat positif."""
        with patch("builtins.print"), patch(
            "builtins.input",
            side_effect=["abc", "0", "-1", "2"],
        ):
            hasil = minta_id_positif("ID: ")
        self.assertEqual(hasil, 2)


if __name__ == "__main__":
    unittest.main()
