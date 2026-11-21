"""Pengujian otomatis modul layanan, penyimpanan JSON, sistem desain terpusat, dan alur GUI forum."""

from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

from forum.aset import ambil_inisial
from forum.layanan import (
    buat_post,
    cari_post,
    cari_post_berdasarkan_id,
    hapus_komentar,
    hapus_post,
    tambah_komentar,
)
from forum.penyimpanan import muat_data, simpan_data
from forum.theme import (
    FONT_UTAMA,
    SKALA_FONT,
    WARNA,
    buat_cuplikan_satu_baris,
    format_tanggal_ramah,
    hitung_rasio_kontras,
    periksa_semua_kontras,
)


class TestTemaDesain(unittest.TestCase):
    """Kumpulan pengujian sistem desain terpusat, skala tipografi, format tanggal, dan kontras WCAG."""

    def test_skala_font_dan_warna_utama(self):
        """Font utama Segoe UI, skala ukuran font, dan warna utama hijau tua tersedia sesuai spesifikasi."""
        self.assertEqual(FONT_UTAMA, "Segoe UI")
        self.assertEqual(SKALA_FONT["judul_post"], 20)
        self.assertEqual(SKALA_FONT["judul_aplikasi"], 20)
        self.assertEqual(SKALA_FONT["isi_post"], 13)
        self.assertEqual(SKALA_FONT["isi_komentar"], 13)
        self.assertEqual(SKALA_FONT["nama_penulis"], 13)
        self.assertEqual(SKALA_FONT["meta"], 11)
        self.assertEqual(SKALA_FONT["subjudul"], 10)
        self.assertEqual(WARNA["aksen"], "#2F6B4F")
        self.assertEqual(WARNA["bahaya"], "#B23A3A")

    def test_semua_pasangan_warna_lolos_wcag_aa(self):
        """Seluruh pasangan warna teks dan latar mencapai rasio kontras WCAG minimal 4.5:1."""
        hasil = periksa_semua_kontras(batas_minimum=4.5)
        gagal = [item for item in hasil if not item["lolos"]]
        self.assertEqual(gagal, [], msg=f"Pasangan warna gagal kontras 4.5:1: {gagal}")
        self.assertGreaterEqual(
            hitung_rasio_kontras(WARNA["avatar_teks"], WARNA["avatar_latar"]),
            4.5,
        )

    def test_format_tanggal_dan_cuplikan(self):
        """Format tanggal ramah pengguna dan cuplikan satu baris bekerja dengan akurat."""
        self.assertEqual(format_tanggal_ramah("2026-11-21 12:30"), "21 Nov 2026, 12:30")
        self.assertEqual(
            buat_cuplikan_satu_baris("Baris satu\n\nBaris dua panjang sekali", batas_karakter=20),
            "Baris satu Baris...",
        )

    def test_tidak_ada_warna_hex_atau_ukuran_font_tersebar_di_gui(self):
        """Memastikan forum/gui.py hanya memakai token dari theme.py tanpa warna hex atau font angka acak."""
        import re
        path_gui = Path(__file__).resolve().parent / "forum" / "gui.py"
        teks_gui = path_gui.read_text(encoding="utf-8")
        for nomor, baris in enumerate(teks_gui.splitlines(), 1):
            kode = baris.split("#", 1)[0]
            self.assertIsNone(
                re.search(r"#[0-9A-Fa-f]{6}", baris) if not baris.lstrip().startswith("#") else None,
                msg=f"Ditemukan kode warna hex langsung di gui.py baris {nomor}: {baris}",
            )
            self.assertIsNone(
                re.search(r"buat_font\(\s*\d+", kode),
                msg=f"Ditemukan ukuran font angka mentah di gui.py baris {nomor}: {baris}",
            )
            self.assertIsNone(
                re.search(r"CTkFont\(", kode),
                msg=f"Ditemukan pemanggilan CTkFont langsung di gui.py baris {nomor}: {baris}",
            )


class TestLayananForum(unittest.TestCase):
    """Kumpulan pengujian logika pembuatan, pencarian, komentar, dan penghapusan post."""

    def test_buat_post_berhasil(self):
        """Post baru tersimpan dengan ID 1, teks terpangkas, dan komentar kosong."""
        daftar_post = []
        post = buat_post(
            daftar_post,
            "  Naufal  ",
            "  Belajar GUI  ",
            "  Hari kelima latihan  ",
            waktu="2026-11-21 12:25",
        )

        self.assertEqual(len(daftar_post), 1)
        self.assertEqual(post["id"], 1)
        self.assertEqual(post["penulis"], "Naufal")
        self.assertEqual(post["judul"], "Belajar GUI")
        self.assertEqual(post["isi"], "Hari kelima latihan")
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

    def test_tambah_dan_hapus_komentar_berhasil(self):
        """Komentar baru masuk ke post target dengan ID berurutan dan dapat dihapus per item."""
        daftar_post = []
        buat_post(daftar_post, "Naufal", "Belajar GUI", "Hari kelima")

        komentar_1 = tambah_komentar(
            daftar_post,
            1,
            "Budi",
            "Tampilannya jelas",
            waktu="2026-11-21 12:30",
        )
        komentar_2 = tambah_komentar(
            daftar_post,
            1,
            "Sari",
            "Setuju sekali",
            waktu="2026-11-21 12:31",
        )

        post = cari_post_berdasarkan_id(daftar_post, 1)
        self.assertEqual(komentar_1["id"], 1)
        self.assertEqual(komentar_2["id"], 2)
        self.assertEqual(len(post["komentar"]), 2)

        terhapus = hapus_komentar(daftar_post, 1, 1)
        self.assertIsNotNone(terhapus)
        self.assertEqual(terhapus["id"], 1)
        self.assertEqual(len(post["komentar"]), 1)
        self.assertIsNone(hapus_komentar(daftar_post, 1, 99))
        self.assertIsNone(hapus_komentar(daftar_post, 99, 2))

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
        buat_post(daftar_post, "Naufal", "Belajar GUI", "Hari kelima latihan")
        buat_post(daftar_post, "Sari", "Catatan Kuliah", "Membahas struktur data")

        self.assertEqual(len(cari_post(daftar_post, "gui")), 1)
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
            buat_post(daftar_awal, "Naufal", "Belajar GUI", "Hari kelima latihan")
            tambah_komentar(daftar_awal, 1, "Budi", "Tampilannya jelas")

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


class TestGuiForum(unittest.TestCase):
    """Pengujian integrasi GUI di proses terpisah agar mainloop CustomTkinter bersih."""

    def test_ambil_inisial_penulis(self):
        """Pembentukan inisial avatar menangani satu kata, dua kata, dan teks kosong."""
        self.assertEqual(ambil_inisial("Naufal Ilham Fauzan"), "NI")
        self.assertEqual(ambil_inisial("admin"), "AD")
        self.assertEqual(ambil_inisial("   "), "?")

    def _jalankan_skrip_gui(self, kode_skrip, path_json):
        """Menjalankan skrip Python uji GUI dalam proses terpisah menggunakan file JSON sementara."""
        folder_projek = Path(__file__).resolve().parent
        hasil = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(kode_skrip), str(path_json)],
            cwd=folder_projek,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            hasil.returncode,
            0,
            msg=f"Stdout:\n{hasil.stdout}\nStderr:\n{hasil.stderr}",
        )
        self.assertEqual(hasil.stderr.strip(), "", msg=f"Error Tkinter:\n{hasil.stderr}")

    def test_alur_lengkap_gui_dan_persistensi_lintas_sesi(self):
        """Menguji buat post, validasi inline, komentar Enter & simpan nama, cari langsung, hapus komentar & post."""
        with tempfile.TemporaryDirectory() as folder_uji:
            path_json = Path(folder_uji) / "data_forum.json"

            sesi_satu = """
            import sys
            from pathlib import Path
            from unittest.mock import patch
            from forum.gui import AplikasiForum, ItemDaftarPost, KartuKomentar

            path_json = Path(sys.argv[1])
            app = AplikasiForum(path_data=path_json)
            assert app.title() == "Forum Post dan Komentar"
            assert app._iconbitmap_method_called is True
            assert all(aset is not None for aset in app.aset.values())
            assert app.label_stat_post.cget("text") == "0"
            assert not app.tombol_reset.winfo_ismapped()

            def langkah_1():
                app._buka_dialog_buat_post()
                app.after(80, langkah_2)

            def langkah_2():
                # Tekan Batal tidak menambah post dan tidak membuat file JSON
                dialog = app._dialog_aktif
                dialog.entry_penulis.insert(0, "Naufal")
                dialog._batal()
                assert app.daftar_post == []
                assert not path_json.exists()

                app._buka_dialog_buat_post()
                app.after(80, langkah_3)

            def langkah_3():
                dialog = app._dialog_aktif
                # Validasi inline pada dialog Buat Post Baru (tanpa popup)
                dialog._simpan()
                assert dialog.label_error.cget("text") != ""
                assert dialog.winfo_exists()

                dialog.entry_penulis.insert(0, "Naufal")
                dialog.entry_judul.insert(0, "Belajar GUI")
                dialog.teks_isi.insert("1.0", "Hari kelima latihan membuat antarmuka hijau.")
                dialog._simpan()

                assert len(app.daftar_post) == 1
                assert app.id_post_terpilih == 1
                assert path_json.exists()

                # Pastikan kartu daftar post tidak memakai prefiks [1], melainkan judul saja + cuplikan + tanggal
                kartu_item = [
                    w for w in app.frame_daftar_post.winfo_children()
                    if isinstance(w, ItemDaftarPost)
                ][0]
                assert kartu_item.label_judul.cget("text") == "Belajar GUI"
                assert "Hari kelima latihan" in kartu_item.label_cuplikan.cget("text")
                assert "Naufal  •  " in kartu_item.label_meta.cget("text")

                # Meta detail post memakai format "oleh Naufal  •  ..." tanpa "ID #1"
                teks_meta_detail = app.label_meta_detail.cget("text")
                assert teks_meta_detail.startswith("oleh Naufal  •  ")
                assert "ID #" not in teks_meta_detail

                # Pesan komentar kosong harus sesuai spesifikasi
                assert app.label_komentar_kosong.cget("text") == "Belum ada komentar. Jadilah yang pertama."

                # Validasi komentar kosong menampilkan error inline merah dan bukan popup
                app._aksi_tambah_komentar()
                assert app.label_error_komentar.cget("text") != ""

                # Kirim komentar: kolom nama tetap tersimpan, kolom komentar dikosongkan
                app.entry_penulis_komentar.insert(0, "Budi")
                app.entry_isi_komentar.insert(0, "Tampilannya jelas")
                app._aksi_tambah_komentar()
                assert app.label_error_komentar.cget("text") == ""
                assert app.entry_penulis_komentar.get() == "Budi"
                assert app.entry_isi_komentar.get() == ""
                assert app.label_judul_komentar.cget("text") == "Komentar (1)"
                assert app.label_stat_post.cget("text") == "1"
                assert app.label_stat_komentar.cget("text") == "1"
                assert app.label_stat_penulis.cget("text") == "2"

                # Kartu komentar tidak mengandung nomor [#1]
                kartu_kom = [
                    w for w in app.frame_daftar_komentar.winfo_children()
                    if isinstance(w, KartuKomentar)
                ][0]
                assert kartu_kom.label_penulis.cget("text") == "Budi"
                assert "[#" not in kartu_kom.label_tanggal.cget("text")

                # Pencarian langsung (live search dengan debounce) + ikon reset 'x'
                app.entry_cari.insert(0, "gui")
                app._jadwalkan_pencarian_langsung()
                app.after(320, langkah_4)

            def langkah_4():
                assert app.tombol_reset.winfo_ismapped()
                assert app.label_status_daftar.cget("text") == "Hasil 'gui': 1 post"

                app.entry_cari.delete(0, "end")
                app.entry_cari.insert(0, "tidakada")
                app._jadwalkan_pencarian_langsung()
                app.after(320, langkah_5)

            def langkah_5():
                assert app.label_status_daftar.cget("text") == "Hasil 'tidakada': 0 post"
                assert app.label_pesan_kosong_daftar.cget("text") == "Tidak ada post yang cocok"
                assert app.id_post_terpilih is None

                app._aksi_reset()
                assert not app.tombol_reset.winfo_ismapped()
                assert app.label_status_daftar.cget("text") == "Total: 1 post"
                assert app.id_post_terpilih == 1
                app.after(60, app.destroy)

            app.after(80, langkah_1)
            app.mainloop()
            """
            self._jalankan_skrip_gui(sesi_satu, path_json)

            sesi_dua = """
            import sys
            from pathlib import Path
            from unittest.mock import patch
            from forum.gui import AplikasiForum

            path_json = Path(sys.argv[1])
            app = AplikasiForum(path_data=path_json)

            def cek_dan_hapus():
                assert len(app.daftar_post) == 1
                assert app.daftar_post[0]["judul"] == "Belajar GUI"
                assert app.daftar_post[0]["komentar"][0]["isi"] == "Tampilannya jelas"

                # Uji hapus komentar: batal dulu, lalu setuju
                with patch("forum.gui.messagebox.askyesno", return_value=False):
                    app._aksi_hapus_komentar(1)
                assert len(app.daftar_post[0]["komentar"]) == 1

                with patch("forum.gui.messagebox.askyesno", return_value=True):
                    app._aksi_hapus_komentar(1)
                assert len(app.daftar_post[0]["komentar"]) == 0
                assert app.label_komentar_kosong.cget("text") == "Belum ada komentar. Jadilah yang pertama."

                # Uji hapus post: batal tidak menghapus, setuju menghapus
                with patch.object(app, "_konfirmasi_hapus_post", return_value=False):
                    app._aksi_hapus_post()
                assert len(app.daftar_post) == 1

                # Uji resize jendela dan tinggi dinamis kotak isi post (<= 35% tinggi panel kanan)
                app.geometry("1200x800")
                app.update_idletasks()
                app._saat_panel_kanan_berubah_ukuran()
                tinggi_panel = app.panel_kanan.winfo_height()
                tinggi_isi = app.teks_isi_detail.cget("height")
                assert tinggi_isi <= int(tinggi_panel * 0.35) + 5

                with patch.object(app, "_konfirmasi_hapus_post", return_value=True):
                    app._aksi_hapus_post()
                assert app.daftar_post == []
                app.after(60, app.destroy)

            app.after(80, cek_dan_hapus)
            app.mainloop()
            """
            self._jalankan_skrip_gui(sesi_dua, path_json)

    def test_gui_json_rusak_tampilkan_peringatan_tanpa_crash(self):
        """Aplikasi tetap terbuka dengan daftar kosong dan memanggil peringatan bila JSON rusak."""
        with tempfile.TemporaryDirectory() as folder_uji:
            path_json = Path(folder_uji) / "data_forum.json"
            path_json.write_text("{json rusak", encoding="utf-8")

            skrip = """
            import sys
            from pathlib import Path
            from unittest.mock import patch
            from forum.gui import AplikasiForum

            path_json = Path(sys.argv[1])
            with patch("forum.gui.messagebox.showwarning") as mock_warn:
                app = AplikasiForum(path_data=path_json)

                def cek_peringatan():
                    assert mock_warn.called
                    assert app.daftar_post == []
                    app.after(60, app.destroy)

                app.after(80, cek_peringatan)
                app.mainloop()
            """
            self._jalankan_skrip_gui(skrip, path_json)


if __name__ == "__main__":
    unittest.main()
