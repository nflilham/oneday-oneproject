"""Modul antarmuka grafis (GUI) Forum Daun berbasis CustomTkinter dan sistem desain terpusat."""

from tkinter import messagebox
import customtkinter as ctk

from .aset import ambil_inisial, muat_gambar, muat_gambar_berwarna, pasang_ikon_jendela
from .layanan import (
    buat_post,
    cari_post,
    cari_post_berdasarkan_id,
    hapus_komentar,
    hapus_post,
    tambah_komentar,
)
from .penyimpanan import PATH_DATA_DEFAULT, muat_data, simpan_data
from .theme import (
    SKALA_FONT,
    UKURAN,
    WARNA,
    buat_cuplikan_satu_baris,
    buat_font,
    format_tanggal_ramah,
)


def buat_avatar_inisial(induk, nama, ukuran=UKURAN["avatar_daftar"]):
    """Membuat badge lingkaran inisial penulis dengan latar hijau muda dan huruf hijau tua kontras."""
    teks_inisial = ambil_inisial(nama)
    return ctk.CTkLabel(
        induk,
        text=teks_inisial,
        width=ukuran,
        height=ukuran,
        corner_radius=ukuran // 2,
        fg_color=WARNA["avatar_latar"],
        text_color=WARNA["avatar_teks"],
        font=buat_font("nama_penulis", tebal=True),
    )


class ItemDaftarPost(ctk.CTkFrame):
    """Komponen kartu satu item post di daftar panel kiri (judul, cuplikan isi, meta penulis & tanggal)."""

    def __init__(self, master, post, terpilih, on_pilih, ikon_komentar=None):
        """Merender kartu post dengan penanda visual saat terpilih dan pengikat klik di seluruh area."""
        super().__init__(
            master,
            corner_radius=UKURAN["radius_kartu"],
            cursor="hand2",
            fg_color=WARNA["kartu_aktif"] if terpilih else WARNA["bacaan"],
            border_width=2 if terpilih else 1,
            border_color=WARNA["aksen"] if terpilih else WARNA["garis"],
        )
        self.id_post = post["id"]
        self.on_pilih = on_pilih
        self.grid_columnconfigure(1, weight=1)

        # Strip aksen vertikal di kiri kartu saat item sedang aktif dipilih
        self.penanda_aktif = ctk.CTkFrame(
            self,
            width=4,
            corner_radius=2,
            fg_color=WARNA["aksen"] if terpilih else "transparent",
        )
        self.penanda_aktif.grid(row=0, column=0, rowspan=3, sticky="ns", padx=(6, 0), pady=8)

        self.avatar = buat_avatar_inisial(
            self,
            post["penulis"],
            ukuran=UKURAN["avatar_daftar"],
        )
        self.avatar.grid(row=0, column=0, rowspan=3, sticky="nw", padx=(14, 10), pady=12)

        judul_ringkas = buat_cuplikan_satu_baris(post["judul"], batas_karakter=36)
        self.label_judul = ctk.CTkLabel(
            self,
            text=judul_ringkas,
            anchor="w",
            cursor="hand2",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["aksen"] if terpilih else WARNA["teks"],
        )
        self.label_judul.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=(10, 1))

        cuplikan_isi = buat_cuplikan_satu_baris(post["isi"], batas_karakter=48)
        self.label_cuplikan = ctk.CTkLabel(
            self,
            text=cuplikan_isi,
            anchor="w",
            cursor="hand2",
            font=buat_font("isi_post"),
            text_color=WARNA["teks_sekunder"],
        )
        self.label_cuplikan.grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=(0, 3))

        tanggal_ramah = format_tanggal_ramah(post["waktu"])
        jumlah_komentar = len(post["komentar"])
        teks_meta = f"{post['penulis']}  •  {tanggal_ramah}  •  {jumlah_komentar} komentar"

        self.baris_meta = ctk.CTkFrame(self, fg_color="transparent")
        self.baris_meta.grid(row=2, column=1, sticky="ew", padx=(0, 12), pady=(0, 10))

        self.label_meta = ctk.CTkLabel(
            self.baris_meta,
            text=teks_meta,
            anchor="w",
            cursor="hand2",
            font=buat_font("meta"),
            text_color=WARNA["meta"],
            image=ikon_komentar,
            compound="left",
        )
        self.label_meta.pack(side="left")

        # Ikat klik pada kartu dan seluruh sub-elemennya agar responsif di titik mana pun
        for elemen in (
            self,
            self.penanda_aktif,
            self.avatar,
            self.label_judul,
            self.label_cuplikan,
            self.baris_meta,
            self.label_meta,
        ):
            elemen.bind("<Button-1>", self._tangani_klik)

    def _tangani_klik(self, _event=None):
        """Meneruskan aksi klik item post ke callback pemilihan di jendela utama."""
        self.on_pilih(self.id_post)


class KartuKomentar(ctk.CTkFrame):
    """Komponen kartu satu komentar dengan header penulis + tanggal sebaris dan tombol hapus sekunder."""

    def __init__(self, master, komentar, on_hapus, ikon_hapus=None):
        """Merender kartu komentar dengan padding konsisten dan aksi hapus."""
        super().__init__(
            master,
            fg_color=WARNA["panel"],
            border_width=1,
            border_color=WARNA["garis"],
            corner_radius=UKURAN["radius_kartu"],
        )
        self.id_komentar = komentar["id"]
        self.on_hapus = on_hapus
        self.grid_columnconfigure(1, weight=1)

        self.avatar = buat_avatar_inisial(
            self,
            komentar["penulis"],
            ukuran=UKURAN["avatar_komentar"],
        )
        self.avatar.grid(row=0, column=0, rowspan=2, sticky="nw", padx=(14, 10), pady=12)

        # Header satu baris: nama penulis tebal, tanggal kecil pucat di sebelahnya, tombol hapus di kanan
        baris_header = ctk.CTkFrame(self, fg_color="transparent")
        baris_header.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=(10, 2))
        baris_header.grid_columnconfigure(1, weight=1)

        self.label_penulis = ctk.CTkLabel(
            baris_header,
            text=komentar["penulis"],
            anchor="w",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["teks"],
        )
        self.label_penulis.grid(row=0, column=0, sticky="w")

        tanggal_ramah = format_tanggal_ramah(komentar["waktu"])
        self.label_tanggal = ctk.CTkLabel(
            baris_header,
            text=f"  •  {tanggal_ramah}",
            anchor="w",
            font=buat_font("tanggal"),
            text_color=WARNA["meta"],
        )
        self.label_tanggal.grid(row=0, column=1, sticky="w")

        self.tombol_hapus = ctk.CTkButton(
            baris_header,
            text="Hapus",
            width=66,
            height=UKURAN["tinggi_tombol_kecil"],
            corner_radius=UKURAN["tinggi_tombol_kecil"] // 2,
            fg_color="transparent",
            hover_color=WARNA["bahaya_hover_latar"],
            border_width=1,
            border_color=WARNA["garis"],
            text_color=WARNA["meta"],
            font=buat_font("meta"),
            image=ikon_hapus,
            compound="left",
            command=lambda: self.on_hapus(self.id_komentar),
        )
        self.tombol_hapus.grid(row=0, column=2, sticky="e", padx=(8, 0))

        self.label_isi = ctk.CTkLabel(
            self,
            text=komentar["isi"],
            anchor="w",
            justify="left",
            wraplength=460,
            font=buat_font("isi_komentar"),
            text_color=WARNA["teks"],
        )
        self.label_isi.grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=(2, 12))


class FormKomentar(ctk.CTkFrame):
    """Komponen form komentar satu baris (nama di kiri, komentar di tengah, tombol Kirim di kanan) + error inline."""

    def __init__(self, master, on_kirim, ikon_kirim=None):
        """Membangun baris input komentar, pengikat tombol Enter, dan label validasi merah di bawahnya."""
        super().__init__(
            master,
            corner_radius=UKURAN["radius_panel"],
            fg_color=WARNA["hero"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        self.on_kirim = on_kirim
        self.grid_columnconfigure(0, weight=1)

        baris_input = ctk.CTkFrame(self, fg_color="transparent")
        baris_input.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        baris_input.grid_columnconfigure(1, weight=1)

        self.entry_penulis = ctk.CTkEntry(
            baris_input,
            placeholder_text="Nama kamu...",
            width=UKURAN["lebar_input_nama_komentar"],
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["panel"],
            border_color=WARNA["garis_input"],
            border_width=1,
            text_color=WARNA["teks"],
            placeholder_text_color=WARNA["placeholder"],
            font=buat_font("input"),
        )
        self.entry_penulis.grid(row=0, column=0, padx=(0, 8))
        self.entry_penulis.bind("<Return>", lambda _event: self._picu_kirim())
        self.entry_penulis.bind("<KeyRelease>", lambda _event: self.sembunyikan_error())

        self.entry_isi = ctk.CTkEntry(
            baris_input,
            placeholder_text="Tulis komentar... (Enter untuk kirim)",
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["panel"],
            border_color=WARNA["garis_input"],
            border_width=1,
            text_color=WARNA["teks"],
            placeholder_text_color=WARNA["placeholder"],
            font=buat_font("input"),
        )
        self.entry_isi.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.entry_isi.bind("<Return>", lambda _event: self._picu_kirim())
        self.entry_isi.bind("<KeyRelease>", lambda _event: self.sembunyikan_error())

        self.tombol_kirim = ctk.CTkButton(
            baris_input,
            text="Kirim",
            width=96,
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["aksen"],
            hover_color=WARNA["aksen_hover"],
            text_color=WARNA["putih"],
            font=buat_font("tombol", tebal=True),
            image=ikon_kirim,
            compound="right",
            command=self._picu_kirim,
        )
        self.tombol_kirim.grid(row=0, column=2)

        self.label_error = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            height=18,
            font=buat_font("error"),
            text_color=WARNA["bahaya"],
        )
        self.label_error.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 6))
        self.label_error.grid_remove()

    def _picu_kirim(self):
        """Memanggil callback pengiriman komentar saat tombol Kirim atau Enter ditekan."""
        self.on_kirim()

    def tampilkan_error(self, pesan, target_fokus=None):
        """Menampilkan pesan error validasi berwarna merah di dekat form dan memfokuskan kolom kosong."""
        self.label_error.configure(text=pesan)
        self.label_error.grid()
        if target_fokus == "penulis":
            self.entry_penulis.configure(border_color=WARNA["bahaya"])
            self.entry_isi.configure(border_color=WARNA["garis_input"])
            self.entry_penulis.focus_set()
        elif target_fokus == "isi":
            self.entry_penulis.configure(border_color=WARNA["garis_input"])
            self.entry_isi.configure(border_color=WARNA["bahaya"])
            self.entry_isi.focus_set()

    def sembunyikan_error(self):
        """Menyembunyikan label error dan mengembalikan warna border input ke normal."""
        if self.label_error.cget("text"):
            self.label_error.configure(text="")
            self.label_error.grid_remove()
            self.entry_penulis.configure(border_color=WARNA["garis_input"])
            self.entry_isi.configure(border_color=WARNA["garis_input"])

    def atur_status_aktif(self, aktif):
        """Mengaktifkan atau menonaktifkan seluruh kontrol form komentar."""
        status = "normal" if aktif else "disabled"
        self.entry_penulis.configure(state=status)
        self.entry_isi.configure(state=status)
        self.tombol_kirim.configure(state=status)
        if not aktif:
            self.sembunyikan_error()


class DialogBuatPost(ctk.CTkToplevel):
    """Jendela dialog terpisah untuk mengisi formulir pembuatan post baru dengan validasi inline."""

    def __init__(self, master, on_simpan, ikon_simpan=None):
        """Menyiapkan tata letak input penulis, judul, isi, validasi inline, serta pintasan Enter/Ctrl+Enter."""
        super().__init__(master, fg_color=WARNA["latar"])
        self.on_simpan = on_simpan
        self.ikon_simpan = ikon_simpan

        self.title("Buat Post Baru")
        self.geometry("480x460")
        self.minsize(410, 390)
        pasang_ikon_jendela(self)

        # Jadikan jendela modal agar fokus pengguna tetap di formulir hingga selesai atau batal
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._batal)
        self.bind("<Escape>", lambda _event: self._batal())
        self.bind("<Control-Return>", lambda _event: self._simpan())

        self._bangun_formulir()
        self.after(50, self._fokus_awal)

    def _fokus_awal(self):
        """Memindahkan fokus ke kolom penulis bila jendela dialog masih aktif."""
        if self.winfo_exists():
            self.entry_penulis.focus_set()

    def _bangun_formulir(self):
        """Membangun komponen input teks, label error inline, dan tombol aksi di dalam dialog."""
        wadah = ctk.CTkFrame(
            self,
            corner_radius=UKURAN["radius_panel"],
            fg_color=WARNA["panel"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        wadah.pack(fill="both", expand=True, padx=16, pady=16)
        wadah.grid_columnconfigure(0, weight=1)
        wadah.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            wadah,
            text="Nama penulis",
            anchor="w",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 4))

        self.entry_penulis = ctk.CTkEntry(
            wadah,
            placeholder_text="Contoh: Naufal",
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_input"],
            fg_color=WARNA["bacaan"],
            border_color=WARNA["garis_input"],
            border_width=1,
            text_color=WARNA["teks"],
            placeholder_text_color=WARNA["placeholder"],
            font=buat_font("input"),
        )
        self.entry_penulis.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.entry_penulis.bind("<Return>", lambda _event: self._tangani_enter_entry(self.entry_judul))
        self.entry_penulis.bind("<KeyRelease>", lambda _event: self.sembunyikan_error())

        ctk.CTkLabel(
            wadah,
            text="Judul post",
            anchor="w",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 4))

        self.entry_judul = ctk.CTkEntry(
            wadah,
            placeholder_text="Tulis judul singkat",
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_input"],
            fg_color=WARNA["bacaan"],
            border_color=WARNA["garis_input"],
            border_width=1,
            text_color=WARNA["teks"],
            placeholder_text_color=WARNA["placeholder"],
            font=buat_font("input"),
        )
        self.entry_judul.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.entry_judul.bind("<Return>", lambda _event: self._tangani_enter_entry(self.teks_isi))
        self.entry_judul.bind("<KeyRelease>", lambda _event: self.sembunyikan_error())

        baris_label_isi = ctk.CTkFrame(wadah, fg_color="transparent")
        baris_label_isi.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 4))
        baris_label_isi.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            baris_label_isi,
            text="Isi post",
            anchor="w",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            baris_label_isi,
            text="Ctrl+Enter untuk simpan",
            anchor="e",
            font=buat_font("meta"),
            text_color=WARNA["meta"],
        ).grid(row=0, column=1, sticky="e")

        self.teks_isi = ctk.CTkTextbox(
            wadah,
            wrap="word",
            corner_radius=UKURAN["radius_input"],
            fg_color=WARNA["bacaan"],
            border_color=WARNA["garis_input"],
            border_width=1,
            text_color=WARNA["teks"],
            scrollbar_button_color=WARNA["scrollbar"],
            scrollbar_button_hover_color=WARNA["scrollbar_hover"],
            font=buat_font("isi_post"),
        )
        self.teks_isi.grid(row=5, column=0, sticky="nsew", padx=18, pady=(0, 8))
        self.teks_isi.bind("<Control-Return>", self._simpan_dari_shortcut)
        self.teks_isi.bind("<KeyRelease>", lambda _event: self.sembunyikan_error())

        self.label_error = ctk.CTkLabel(
            wadah,
            text="",
            anchor="w",
            font=buat_font("error"),
            text_color=WARNA["bahaya"],
        )
        self.label_error.grid(row=6, column=0, sticky="ew", padx=18, pady=(0, 8))
        self.label_error.grid_remove()

        baris_tombol = ctk.CTkFrame(wadah, fg_color="transparent")
        baris_tombol.grid(row=7, column=0, sticky="e", padx=18, pady=(0, 16))

        self.tombol_batal = ctk.CTkButton(
            baris_tombol,
            text="Batal",
            width=100,
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["kartu"],
            hover_color=WARNA["kartu_hover"],
            border_width=1,
            border_color=WARNA["garis_input"],
            text_color=WARNA["teks"],
            font=buat_font("tombol"),
            command=self._batal,
        )
        self.tombol_batal.pack(side="left", padx=(0, 8))

        self.tombol_simpan = ctk.CTkButton(
            baris_tombol,
            text="Simpan",
            width=120,
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["aksen"],
            hover_color=WARNA["aksen_hover"],
            text_color=WARNA["putih"],
            font=buat_font("tombol", tebal=True),
            image=self.ikon_simpan,
            compound="right",
            command=self._simpan,
        )
        self.tombol_simpan.pack(side="left")

    def _tangani_enter_entry(self, widget_berikutnya):
        """Memindahkan fokus ke kolom berikutnya, atau menyimpan jika seluruh kolom sudah terisi."""
        penulis = self.entry_penulis.get().strip()
        judul = self.entry_judul.get().strip()
        isi = self.teks_isi.get("1.0", "end-1c").strip()
        if penulis and judul and isi:
            self._simpan()
            return
        widget_berikutnya.focus_set()

    def _simpan_dari_shortcut(self, _event=None):
        """Menangani pintasan Ctrl+Enter di dalam textbox isi post tanpa menyisipkan baris baru."""
        self._simpan()
        return "break"

    def tampilkan_error(self, pesan, target_fokus=None):
        """Menampilkan pesan error validasi inline berwarna merah dan memfokuskan kolom yang kosong."""
        self.label_error.configure(text=pesan)
        self.label_error.grid()

        self.entry_penulis.configure(border_color=WARNA["garis_input"])
        self.entry_judul.configure(border_color=WARNA["garis_input"])
        self.teks_isi.configure(border_color=WARNA["garis_input"])

        if target_fokus == "penulis":
            self.entry_penulis.configure(border_color=WARNA["bahaya"])
            self.entry_penulis.focus_set()
        elif target_fokus == "judul":
            self.entry_judul.configure(border_color=WARNA["bahaya"])
            self.entry_judul.focus_set()
        elif target_fokus == "isi":
            self.teks_isi.configure(border_color=WARNA["bahaya"])
            self.teks_isi.focus_set()

    def sembunyikan_error(self):
        """Menyembunyikan pesan error inline dan mereset border kolom ke warna normal."""
        if self.label_error.cget("text"):
            self.label_error.configure(text="")
            self.label_error.grid_remove()
            self.entry_penulis.configure(border_color=WARNA["garis_input"])
            self.entry_judul.configure(border_color=WARNA["garis_input"])
            self.teks_isi.configure(border_color=WARNA["garis_input"])

    def _simpan(self):
        """Memvalidasi penulis, judul, dan isi post secara inline lalu menyimpan jika valid."""
        penulis = self.entry_penulis.get()
        judul = self.entry_judul.get()
        # "end-1c" memotong baris baru otomatis di akhir CTkTextbox agar validasi spasi akurat
        isi = self.teks_isi.get("1.0", "end-1c")

        if not penulis.strip():
            self.tampilkan_error("Nama penulis wajib diisi.", target_fokus="penulis")
            return
        if not judul.strip():
            self.tampilkan_error("Judul post wajib diisi.", target_fokus="judul")
            return
        if not isi.strip():
            self.tampilkan_error("Isi post wajib diisi.", target_fokus="isi")
            return

        if self.on_simpan(penulis, judul, isi, self):
            self.destroy()

    def _batal(self):
        """Menutup dialog pembuatan post tanpa mengubah data forum."""
        self.destroy()


class AplikasiForum(ctk.CTk):
    """Jendela utama dua panel aplikasi desktop Forum Daun dengan sistem desain terpusat."""

    def __init__(self, path_data=PATH_DATA_DEFAULT):
        """Menginisialisasi data JSON, aset gambar, tema daun, serta seluruh panel antarmuka."""
        ctk.set_appearance_mode("Light")
        super().__init__(fg_color=WARNA["latar"])

        self.path_data = path_data
        self.daftar_post, peringatan_awal = muat_data(self.path_data)
        self.kata_kunci_aktif = ""
        self.id_post_terpilih = self.daftar_post[0]["id"] if self.daftar_post else None
        self._dialog_aktif = None
        self._id_after_cari = None

        self.aset = {
            "logo": muat_gambar("logo_forum.png", (40, 40)),
            "ilustrasi": muat_gambar("ilustrasi_forum.png", (185, 185)),
            "ilustrasi_kecil": muat_gambar("ilustrasi_forum.png", (105, 105)),
            "tambah": muat_gambar("ikon_tambah.png", (16, 16)),
            "cari": muat_gambar("ikon_cari.png", (15, 15)),
            "reset": muat_gambar("ikon_reset.png", (14, 14)),
            "komentar": muat_gambar("ikon_komentar.png", (13, 13)),
            "panah": muat_gambar("ikon_panah.png", (15, 15)),
            "hapus": muat_gambar_berwarna("ikon_hapus.png", (14, 14), WARNA["bahaya"]),
            "hapus_kecil": muat_gambar_berwarna("ikon_hapus.png", (12, 12), WARNA["meta"]),
        }

        self.title("Forum Post dan Komentar")
        self.geometry(f"{UKURAN['lebar_jendela']}x{UKURAN['tinggi_jendela']}")
        self.minsize(UKURAN["min_lebar_jendela"], UKURAN["min_tinggi_jendela"])
        pasang_ikon_jendela(self)

        # Baris 0: header brand + statistik sekunder + CTA; Baris 1: panel kiri dan panel kanan
        self.grid_columnconfigure(0, weight=1, minsize=UKURAN["min_panel_kiri"])
        self.grid_columnconfigure(1, weight=2, minsize=UKURAN["min_panel_kanan"])
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._buat_header()
        self._buat_panel_kiri()
        self._buat_panel_kanan()
        self._perbarui_tampilan()

        # Tampilkan peringatan file JSON rusak setelah jendela utama siap dirender
        if peringatan_awal:
            self.after_idle(
                lambda pesan=peringatan_awal: messagebox.showwarning(
                    "Peringatan Data",
                    pesan,
                    parent=self,
                )
            )

    def _buat_header(self):
        """Membangun bar header atas berisi logo, judul aplikasi, statistik sekunder, dan tombol aksi utama."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 4))
        header.grid_columnconfigure(1, weight=1)

        # Sisi kiri: logo daun + judul aplikasi (20 bold) dan subjudul (10 bold)
        identitas = ctk.CTkFrame(header, fg_color="transparent")
        identitas.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            identitas,
            text="",
            image=self.aset["logo"],
        ).grid(row=0, column=0, rowspan=2, padx=(0, 10))

        ctk.CTkLabel(
            identitas,
            text="Forum Daun",
            anchor="w",
            font=buat_font("judul_aplikasi", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            identitas,
            text="DISKUSI & CATATAN LOKAL",
            anchor="w",
            font=buat_font("subjudul", tebal=True),
            text_color=WARNA["meta"],
        ).grid(row=1, column=1, sticky="w")

        # Sisi kanan: ringkasan statistik sekunder tanpa border mencolok + tombol utama Buat Post Baru
        sisi_kanan = ctk.CTkFrame(header, fg_color="transparent")
        sisi_kanan.grid(row=0, column=2, sticky="e")

        self.kartu_stat = ctk.CTkFrame(
            sisi_kanan,
            corner_radius=10,
            fg_color="transparent",
            border_width=0,
        )
        self.kartu_stat.pack(side="left", padx=(0, 14))

        self.label_stat_post = self._tambah_kolom_stat(self.kartu_stat, 0, "Post aktif")
        self._tambah_pemisah_stat(self.kartu_stat, 1)
        self.label_stat_komentar = self._tambah_kolom_stat(self.kartu_stat, 2, "Komentar")
        self._tambah_pemisah_stat(self.kartu_stat, 3)
        self.label_stat_penulis = self._tambah_kolom_stat(self.kartu_stat, 4, "Penulis")

        self.tombol_buat = ctk.CTkButton(
            sisi_kanan,
            text="Buat Post Baru",
            height=UKURAN["tinggi_tombol_utama"],
            corner_radius=UKURAN["tinggi_tombol_utama"] // 2,
            fg_color=WARNA["aksen"],
            hover_color=WARNA["aksen_hover"],
            text_color=WARNA["putih"],
            font=buat_font("tombol", tebal=True),
            image=self.aset["tambah"],
            compound="left",
            command=self._buka_dialog_buat_post,
        )
        self.tombol_buat.pack(side="left")

    def _tambah_kolom_stat(self, induk, kolom, keterangan):
        """Membuat satu item metrik sekunder yang ringkas di sebelah tombol Buat Post Baru."""
        kotak = ctk.CTkFrame(induk, fg_color="transparent")
        kotak.grid(row=0, column=kolom, padx=8, pady=2)

        label_angka = ctk.CTkLabel(
            kotak,
            text="0",
            anchor="e",
            font=buat_font("nama_penulis", tebal=True),
            text_color=WARNA["teks_sekunder"],
        )
        label_angka.pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            kotak,
            text=keterangan,
            anchor="w",
            font=buat_font("meta"),
            text_color=WARNA["meta"],
        ).pack(side="left")

        return label_angka

    def _tambah_pemisah_stat(self, induk, kolom):
        """Menambahkan titik pemisah halus antar metrik statistik sekunder."""
        pemisah = ctk.CTkLabel(
            induk,
            text="•",
            font=buat_font("meta"),
            text_color=WARNA["meta"],
        )
        pemisah.grid(row=0, column=kolom, padx=2)

    def _buat_panel_kiri(self):
        """Membangun panel kiri berisi pencarian langsung (live search dengan ikon 'x') dan daftar post."""
        panel_kiri = ctk.CTkFrame(
            self,
            corner_radius=UKURAN["radius_panel"],
            fg_color=WARNA["panel"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        panel_kiri.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(8, 16))
        panel_kiri.grid_columnconfigure(0, weight=1)
        panel_kiri.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            panel_kiri,
            text="Jelajahi Post",
            anchor="w",
            font=buat_font("subpanel", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 6))

        # Kolom pencarian terpadu: ikon cari di kiri, entry di tengah, tombol kecil 'x' di kanan dalam kolom
        self.kotak_cari = ctk.CTkFrame(
            panel_kiri,
            height=UKURAN["tinggi_input"],
            corner_radius=UKURAN["radius_pill"],
            fg_color=WARNA["bacaan"],
            border_width=1,
            border_color=WARNA["garis_input"],
        )
        self.kotak_cari.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))
        self.kotak_cari.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.kotak_cari,
            text="",
            image=self.aset["cari"],
        ).grid(row=0, column=0, padx=(12, 4), pady=6)

        self.entry_cari = ctk.CTkEntry(
            self.kotak_cari,
            placeholder_text="Cari judul, isi, atau penulis...",
            height=UKURAN["tinggi_input"] - 4,
            corner_radius=UKURAN["radius_pill"],
            fg_color="transparent",
            border_width=0,
            text_color=WARNA["teks"],
            placeholder_text_color=WARNA["placeholder"],
            font=buat_font("input"),
        )
        self.entry_cari.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=2)
        self.entry_cari.bind("<KeyRelease>", self._jadwalkan_pencarian_langsung)
        self.entry_cari.bind("<Return>", lambda _event: self._aksi_cari())
        self.entry_cari.bind("<Escape>", lambda _event: self._aksi_reset())

        # Tombol ikon 'x' kecil di dalam kolom pencarian; hanya muncul bila ada teks
        self.tombol_reset = ctk.CTkButton(
            self.kotak_cari,
            text="✕",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color=WARNA["kartu_hover"],
            text_color=WARNA["meta"],
            font=buat_font("meta", tebal=True),
            command=self._aksi_reset,
        )
        self.tombol_reset.grid(row=0, column=2, padx=(0, 6), pady=6)
        self.tombol_reset.grid_remove()

        self.label_status_daftar = ctk.CTkLabel(
            panel_kiri,
            text="Total: 0 post",
            anchor="w",
            text_color=WARNA["meta"],
            font=buat_font("meta"),
        )
        self.label_status_daftar.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 4))

        self.frame_daftar_post = ctk.CTkScrollableFrame(
            panel_kiri,
            fg_color="transparent",
            scrollbar_button_color=WARNA["scrollbar"],
            scrollbar_button_hover_color=WARNA["scrollbar_hover"],
        )
        self.frame_daftar_post.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 12))
        self.frame_daftar_post.grid_columnconfigure(0, weight=1)

    def _buat_panel_kanan(self):
        """Membangun panel kanan yang beralih antara kartu hero kosong dan detail post aktif."""
        self.panel_kanan = ctk.CTkFrame(
            self,
            corner_radius=UKURAN["radius_panel"],
            fg_color=WARNA["panel"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        self.panel_kanan.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(8, 16))
        self.panel_kanan.grid_columnconfigure(0, weight=1)
        self.panel_kanan.grid_rowconfigure(0, weight=1)
        self.panel_kanan.bind("<Configure>", self._saat_panel_kanan_berubah_ukuran)

        self._buat_hero_kosong()
        self._buat_konten_detail()

    def _buat_hero_kosong(self):
        """Membangun kartu hero berilustrasi saat belum ada post yang dipilih."""
        self.frame_hero_kosong = ctk.CTkFrame(
            self.panel_kanan,
            corner_radius=16,
            fg_color=WARNA["hero"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        self.frame_hero_kosong.grid_columnconfigure(0, weight=1)
        self.frame_hero_kosong.grid_rowconfigure(0, weight=1)

        konten = ctk.CTkFrame(self.frame_hero_kosong, fg_color="transparent")
        konten.grid(row=0, column=0, sticky="ew", padx=28, pady=28)
        konten.grid_columnconfigure(0, weight=1)

        kiri = ctk.CTkFrame(konten, fg_color="transparent")
        kiri.grid(row=0, column=0, sticky="w", padx=(0, 16))

        ctk.CTkLabel(
            kiri,
            text="  FORUM DISKUSI LOKAL  ",
            height=26,
            corner_radius=13,
            fg_color=WARNA["badge"],
            text_color=WARNA["aksen"],
            font=buat_font("subjudul", tebal=True),
        ).grid(row=0, column=0, sticky="w", pady=(0, 14))

        ctk.CTkLabel(
            kiri,
            text="Bagikan ide,\nlebih tenang.",
            anchor="w",
            justify="left",
            font=buat_font("hero", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        ctk.CTkLabel(
            kiri,
            text="Buat catatan atau topik baru, terima komentar, dan simpan seluruh diskusi secara lokal.",
            anchor="w",
            justify="left",
            wraplength=260,
            font=buat_font("isi_post"),
            text_color=WARNA["teks_sekunder"],
        ).grid(row=2, column=0, sticky="w", pady=(0, 18))

        ctk.CTkButton(
            kiri,
            text="Buat Post Baru",
            height=UKURAN["tinggi_tombol_utama"],
            corner_radius=UKURAN["tinggi_tombol_utama"] // 2,
            fg_color=WARNA["aksen"],
            hover_color=WARNA["aksen_hover"],
            text_color=WARNA["putih"],
            font=buat_font("tombol", tebal=True),
            image=self.aset["panah"],
            compound="right",
            command=self._buka_dialog_buat_post,
        ).grid(row=3, column=0, sticky="w")

        ctk.CTkLabel(
            konten,
            text="",
            image=self.aset["ilustrasi"],
        ).grid(row=0, column=1, sticky="e")

    def _buat_konten_detail(self):
        """Membangun tampilan baca post lengkap, area komentar yang dominan, dan form komentar satu baris."""
        self.frame_konten_detail = ctk.CTkFrame(self.panel_kanan, fg_color="transparent")
        self.frame_konten_detail.grid_columnconfigure(0, weight=1)
        # Baris 3 (area komentar) diberi weight=1 agar mengambil sisa ruang vertikal terbesar
        self.frame_konten_detail.grid_rowconfigure(3, weight=1)

        header_detail = ctk.CTkFrame(self.frame_konten_detail, fg_color="transparent")
        header_detail.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        header_detail.grid_columnconfigure(1, weight=1)

        self.wadah_avatar_detail = ctk.CTkFrame(header_detail, fg_color="transparent")
        self.wadah_avatar_detail.grid(row=0, column=0, rowspan=2, sticky="nw", padx=(0, 12))

        self.label_judul_detail = ctk.CTkLabel(
            header_detail,
            text="",
            anchor="w",
            justify="left",
            wraplength=420,
            text_color=WARNA["teks"],
            font=buat_font("judul_post", tebal=True),
        )
        self.label_judul_detail.grid(row=0, column=1, sticky="ew", padx=(0, 12))

        self.label_meta_detail = ctk.CTkLabel(
            header_detail,
            text="",
            anchor="w",
            text_color=WARNA["meta"],
            font=buat_font("meta"),
        )
        self.label_meta_detail.grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=(2, 0))

        # Tombol Hapus Post bergaya outline (latar transparan, border & teks merah #B23A3A, hover merah muda)
        self.tombol_hapus = ctk.CTkButton(
            header_detail,
            text="Hapus Post",
            width=114,
            height=UKURAN["tinggi_tombol"],
            corner_radius=UKURAN["tinggi_tombol"] // 2,
            fg_color="transparent",
            hover_color=WARNA["bahaya_hover_latar"],
            border_width=1,
            border_color=WARNA["bahaya_border"],
            text_color=WARNA["bahaya"],
            font=buat_font("tombol_kecil", tebal=True),
            image=self.aset["hapus"],
            compound="left",
            command=self._aksi_hapus_post,
        )
        self.tombol_hapus.grid(row=0, column=2, rowspan=2, sticky="ne")

        # Kotak isi post menyesuaikan tinggi konten hingga batas 30-35% tinggi panel
        self.teks_isi_detail = ctk.CTkTextbox(
            self.frame_konten_detail,
            height=UKURAN["tinggi_min_isi_post"],
            wrap="word",
            corner_radius=UKURAN["radius_kartu"],
            fg_color=WARNA["bacaan"],
            border_width=1,
            border_color=WARNA["garis"],
            text_color=WARNA["teks"],
            scrollbar_button_color=WARNA["scrollbar"],
            scrollbar_button_hover_color=WARNA["scrollbar_hover"],
            font=buat_font("isi_post"),
        )
        self.teks_isi_detail.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.teks_isi_detail.configure(state="disabled")

        baris_judul_komentar = ctk.CTkFrame(self.frame_konten_detail, fg_color="transparent")
        baris_judul_komentar.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 6))

        ctk.CTkLabel(
            baris_judul_komentar,
            text="",
            image=self.aset["komentar"],
        ).pack(side="left", padx=(0, 6))

        self.label_judul_komentar = ctk.CTkLabel(
            baris_judul_komentar,
            text="Komentar (0)",
            anchor="w",
            text_color=WARNA["teks"],
            font=buat_font("seksi", tebal=True),
        )
        self.label_judul_komentar.pack(side="left")

        self.frame_daftar_komentar = ctk.CTkScrollableFrame(
            self.frame_konten_detail,
            corner_radius=UKURAN["radius_kartu"],
            fg_color=WARNA["bacaan"],
            border_width=1,
            border_color=WARNA["garis"],
            scrollbar_button_color=WARNA["scrollbar"],
            scrollbar_button_hover_color=WARNA["scrollbar_hover"],
        )
        self.frame_daftar_komentar.grid(row=3, column=0, sticky="nsew", padx=18, pady=(0, 10))
        self.frame_daftar_komentar.grid_columnconfigure(0, weight=1)

        # Komponen form komentar satu baris beserta atribut kompatibilitas untuk akses langsung
        self.form_komentar = FormKomentar(
            self.frame_konten_detail,
            on_kirim=self._aksi_tambah_komentar,
            ikon_kirim=self.aset["panah"],
        )
        self.form_komentar.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 16))
        self.entry_penulis_komentar = self.form_komentar.entry_penulis
        self.entry_isi_komentar = self.form_komentar.entry_isi
        self.tombol_kirim_komentar = self.form_komentar.tombol_kirim
        self.label_error_komentar = self.form_komentar.label_error

    def _sesuaikan_tinggi_isi_post(self):
        """Menyesuaikan tinggi kotak isi post dengan kontennya (maks 33% panel kanan) dan mengatur scrollbar."""
        if not self.teks_isi_detail.winfo_exists():
            return

        self.update_idletasks()
        tinggi_panel = max(self.panel_kanan.winfo_height(), 460)
        batas_maks = max(110, int(tinggi_panel * UKURAN["rasio_maks_isi_post"]))

        teks_sekarang = self.teks_isi_detail.get("1.0", "end-1c")
        if not teks_sekarang:
            tinggi_konten = UKURAN["tinggi_min_isi_post"]
        else:
            hasil_hitung = self.teks_isi_detail._textbox.count("1.0", "end-1c", "displaylines")
            jumlah_baris_visual = (hasil_hitung[0] if hasil_hitung else 0) + 1
            tinggi_konten = max(
                UKURAN["tinggi_min_isi_post"],
                jumlah_baris_visual * UKURAN["tinggi_baris_isi_post"] + 20,
            )

        perlu_scroll = tinggi_konten > batas_maks
        tinggi_akhir = batas_maks if perlu_scroll else tinggi_konten
        self.teks_isi_detail.configure(height=tinggi_akhir)

        # Sembunyikan scrollbar vertikal bila seluruh teks muat tanpa melewati batas maksimum
        if perlu_scroll:
            self.teks_isi_detail._hide_y_scrollbar = False
        else:
            self.teks_isi_detail._textbox.yview_moveto(0.0)
            self.teks_isi_detail._hide_y_scrollbar = True
        self.teks_isi_detail._create_grid_for_text_and_scrollbars(re_grid_y_scrollbar=True)

    def _saat_panel_kanan_berubah_ukuran(self, _event=None):
        """Menghitung ulang batas tinggi kotak isi post dan wraplength saat ukuran panel kanan berubah."""
        if self.id_post_terpilih is not None:
            lebar_panel = self.panel_kanan.winfo_width()
            if lebar_panel > 260:
                self.label_judul_detail.configure(wraplength=max(240, lebar_panel - 220))
            self._sesuaikan_tinggi_isi_post()

    def _simpan_perubahan(self):
        """Menyimpan daftar post ke file JSON dan menangani kegagalan izin/kunci file tanpa crash."""
        try:
            simpan_data(self.daftar_post, self.path_data)
            return True
        except OSError as kesalahan:
            messagebox.showerror(
                "Gagal Menyimpan",
                f"Perubahan gagal disimpan ke file: {kesalahan}",
                parent=self,
            )
            return False

    def _daftar_terfilter(self):
        """Mengembalikan daftar post sesuai kata kunci aktif, atau seluruh post jika kosong."""
        if not self.kata_kunci_aktif:
            return self.daftar_post
        return cari_post(self.daftar_post, self.kata_kunci_aktif)

    def _pilih_post(self, id_post):
        """Mengubah post aktif berdasarkan ID lalu merender ulang daftar dan detailnya."""
        self.id_post_terpilih = id_post
        self.form_komentar.sembunyikan_error()
        self._perbarui_tampilan()

    def _perbarui_statistik(self):
        """Menghitung ulang metrik jumlah post, komentar, dan penulis unik pada header."""
        total_post = len(self.daftar_post)
        total_komentar = sum(len(post["komentar"]) for post in self.daftar_post)
        penulis_unik = {post["penulis"].lower() for post in self.daftar_post}
        for post in self.daftar_post:
            for komentar in post["komentar"]:
                penulis_unik.add(komentar["penulis"].lower())

        self.label_stat_post.configure(text=str(total_post))
        self.label_stat_komentar.configure(text=str(total_komentar))
        self.label_stat_penulis.configure(text=str(len(penulis_unik)))

    def _perbarui_tombol_reset_cari(self):
        """Menampilkan tombol ikon 'x' di dalam kolom pencarian hanya saat ada teks."""
        if self.entry_cari.get():
            self.tombol_reset.grid()
        else:
            self.tombol_reset.grid_remove()

    def _perbarui_tampilan(self):
        """Menyegarkan statistik header, daftar post di panel kiri, dan detail di panel kanan."""
        self._perbarui_statistik()
        self._perbarui_tombol_reset_cari()
        daftar_tampil = self._daftar_terfilter()

        if self.kata_kunci_aktif:
            self.label_status_daftar.configure(
                text=f"Hasil '{self.kata_kunci_aktif}': {len(daftar_tampil)} post"
            )
        else:
            self.label_status_daftar.configure(text=f"Total: {len(daftar_tampil)} post")

        # Pastikan ID terpilih tetap valid jika post sebelumnya baru saja dihapus
        if self.id_post_terpilih is not None:
            if cari_post_berdasarkan_id(self.daftar_post, self.id_post_terpilih) is None:
                self.id_post_terpilih = daftar_tampil[0]["id"] if daftar_tampil else None
        elif daftar_tampil and not self.kata_kunci_aktif:
            self.id_post_terpilih = daftar_tampil[0]["id"]

        self._render_daftar_post(daftar_tampil)
        self._render_detail_post()

    def _render_daftar_post(self, daftar_tampil):
        """Menggambar ulang daftar komponen ItemDaftarPost di dalam panel kiri."""
        for widget in self.frame_daftar_post.winfo_children():
            widget.destroy()

        if not daftar_tampil:
            kotak_kosong = ctk.CTkFrame(
                self.frame_daftar_post,
                corner_radius=UKURAN["radius_kartu"],
                fg_color=WARNA["hero"],
                border_width=1,
                border_color=WARNA["garis"],
            )
            kotak_kosong.grid(row=0, column=0, sticky="ew", padx=6, pady=12)
            kotak_kosong.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                kotak_kosong,
                text="",
                image=self.aset["ilustrasi_kecil"],
            ).grid(row=0, column=0, pady=(16, 8))

            pesan_kosong = (
                "Tidak ada post yang cocok"
                if self.kata_kunci_aktif
                else "Belum ada post.\nKlik 'Buat Post Baru' di atas."
            )
            self.label_pesan_kosong_daftar = ctk.CTkLabel(
                kotak_kosong,
                text=pesan_kosong,
                justify="center",
                font=buat_font("isi_post"),
                text_color=WARNA["teks_sekunder"],
            )
            self.label_pesan_kosong_daftar.grid(row=1, column=0, padx=12, pady=(0, 16))
            return

        for baris, post in enumerate(daftar_tampil):
            terpilih = post["id"] == self.id_post_terpilih
            kartu = ItemDaftarPost(
                self.frame_daftar_post,
                post=post,
                terpilih=terpilih,
                on_pilih=self._pilih_post,
                ikon_komentar=self.aset["komentar"],
            )
            kartu.grid(row=baris, column=0, sticky="ew", padx=4, pady=4)

    def _atur_teks_isi_detail(self, teks):
        """Mengisi CTkTextbox detail yang berstatus read-only lalu menyesuaikan tingginya."""
        self.teks_isi_detail.configure(state="normal")
        self.teks_isi_detail.delete("1.0", "end")
        self.teks_isi_detail.insert("1.0", teks)
        self.teks_isi_detail.configure(state="disabled")
        self._sesuaikan_tinggi_isi_post()

    def _render_detail_post(self):
        """Menampilkan kartu hero kosong atau detail post terpilih beserta daftar KartuKomentar."""
        for widget in self.frame_daftar_komentar.winfo_children():
            widget.destroy()
        for widget in self.wadah_avatar_detail.winfo_children():
            widget.destroy()

        post = (
            cari_post_berdasarkan_id(self.daftar_post, self.id_post_terpilih)
            if self.id_post_terpilih is not None
            else None
        )

        if post is None:
            self.label_judul_detail.configure(text="Belum ada post yang dipilih")
            self.label_meta_detail.configure(text="")
            self._atur_teks_isi_detail("")
            self.label_judul_komentar.configure(text="Komentar (0)")
            self.tombol_hapus.configure(state="disabled")
            self.form_komentar.atur_status_aktif(False)

            self.frame_konten_detail.grid_remove()
            self.frame_hero_kosong.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            return

        self.frame_hero_kosong.grid_remove()
        self.frame_konten_detail.grid(row=0, column=0, sticky="nsew")

        buat_avatar_inisial(
            self.wadah_avatar_detail,
            post["penulis"],
            ukuran=UKURAN["avatar_detail"],
        ).pack()

        tanggal_ramah = format_tanggal_ramah(post["waktu"])
        self.label_judul_detail.configure(text=post["judul"])
        self.label_meta_detail.configure(
            text=f"oleh {post['penulis']}  •  {tanggal_ramah}"
        )
        self._atur_teks_isi_detail(post["isi"])

        self.tombol_hapus.configure(state="normal")
        self.form_komentar.atur_status_aktif(True)

        daftar_komentar = post["komentar"]
        self.label_judul_komentar.configure(text=f"Komentar ({len(daftar_komentar)})")

        if not daftar_komentar:
            self.label_komentar_kosong = ctk.CTkLabel(
                self.frame_daftar_komentar,
                text="Belum ada komentar. Jadilah yang pertama.",
                anchor="w",
                font=buat_font("isi_komentar"),
                text_color=WARNA["meta"],
            )
            self.label_komentar_kosong.grid(row=0, column=0, sticky="ew", padx=14, pady=16)
            return

        for baris, komentar in enumerate(daftar_komentar):
            kartu = KartuKomentar(
                self.frame_daftar_komentar,
                komentar=komentar,
                on_hapus=self._aksi_hapus_komentar,
                ikon_hapus=self.aset["hapus_kecil"],
            )
            kartu.grid(row=baris, column=0, sticky="ew", padx=8, pady=6)

    def _scroll_komentar_ke_bawah(self):
        """Menggulir area komentar otomatis ke posisi paling bawah setelah komentar baru ditambahkan."""
        if not self.frame_daftar_komentar.winfo_exists():
            return
        self.update_idletasks()
        try:
            self.frame_daftar_komentar._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def _buka_dialog_buat_post(self):
        """Membuka jendela dialog Buat Post Baru atau memfokuskannya jika sudah terbuka."""
        if self._dialog_aktif is not None and self._dialog_aktif.winfo_exists():
            self._dialog_aktif.focus()
            return
        self._dialog_aktif = DialogBuatPost(
            self,
            self._proses_buat_post,
            ikon_simpan=self.aset["panah"],
        )

    def _proses_buat_post(self, penulis, judul, isi, jendela_dialog):
        """Memvalidasi masukan dialog, membuat post baru, dan menyimpan ke JSON."""
        try:
            post_baru = buat_post(self.daftar_post, penulis, judul, isi)
        except ValueError as kesalahan:
            jendela_dialog.tampilkan_error(str(kesalahan))
            return False

        self.kata_kunci_aktif = ""
        self.entry_cari.delete(0, "end")
        self.id_post_terpilih = post_baru["id"]
        self._simpan_perubahan()
        self._perbarui_tampilan()
        return True

    def _aksi_tambah_komentar(self):
        """Memvalidasi form komentar secara inline (tanpa popup) dan menambahkannya ke post terpilih."""
        if self.id_post_terpilih is None:
            return

        penulis = self.entry_penulis_komentar.get()
        isi = self.entry_isi_komentar.get()

        if not penulis.strip():
            self.form_komentar.tampilkan_error(
                "Nama penulis komentar tidak boleh kosong.",
                target_fokus="penulis",
            )
            return

        if not isi.strip():
            self.form_komentar.tampilkan_error(
                "Isi komentar tidak boleh kosong.",
                target_fokus="isi",
            )
            return

        try:
            tambah_komentar(self.daftar_post, self.id_post_terpilih, penulis, isi)
        except ValueError as kesalahan:
            self.form_komentar.tampilkan_error(str(kesalahan))
            return

        # Kosongkan kolom komentar saja dan pertahankan nama terakhir yang diketik
        self.form_komentar.sembunyikan_error()
        self.entry_isi_komentar.delete(0, "end")
        self._simpan_perubahan()
        self._perbarui_tampilan()
        self.after(20, self._scroll_komentar_ke_bawah)

    def _aksi_hapus_komentar(self, id_komentar):
        """Meminta konfirmasi lalu menghapus komentar tertentu dari post terpilih."""
        if self.id_post_terpilih is None:
            return

        setuju = messagebox.askyesno(
            "Konfirmasi Hapus Komentar",
            "Hapus komentar ini?",
            parent=self,
        )
        if not setuju:
            return

        terhapus = hapus_komentar(self.daftar_post, self.id_post_terpilih, id_komentar)
        if terhapus is not None:
            self._simpan_perubahan()
            self._perbarui_tampilan()

    def _jadwalkan_pencarian_langsung(self, _event=None):
        """Menjalankan pencarian langsung dengan jeda debounce 250 ms saat pengguna mengetik."""
        self._perbarui_tombol_reset_cari()
        if self._id_after_cari is not None:
            try:
                self.after_cancel(self._id_after_cari)
            except Exception:
                pass
        self._id_after_cari = self.after(UKURAN["debounce_cari_ms"], self._aksi_cari)

    def _aksi_cari(self):
        """Menerapkan kata kunci pencarian ke daftar post di panel kiri."""
        if self._id_after_cari is not None:
            try:
                self.after_cancel(self._id_after_cari)
            except Exception:
                pass
            self._id_after_cari = None

        self._perbarui_tombol_reset_cari()
        kata_kunci = self.entry_cari.get().strip()
        self.kata_kunci_aktif = kata_kunci
        hasil = self._daftar_terfilter()

        if hasil and cari_post_berdasarkan_id(hasil, self.id_post_terpilih) is None:
            self.id_post_terpilih = hasil[0]["id"]
        elif not hasil:
            self.id_post_terpilih = None

        self._perbarui_tampilan()

    def _aksi_reset(self):
        """Menghapus kata kunci pencarian dan menampilkan seluruh post kembali."""
        if self._id_after_cari is not None:
            try:
                self.after_cancel(self._id_after_cari)
            except Exception:
                pass
            self._id_after_cari = None

        self.entry_cari.delete(0, "end")
        self.kata_kunci_aktif = ""
        if self.daftar_post and self.id_post_terpilih is None:
            self.id_post_terpilih = self.daftar_post[0]["id"]
        self._perbarui_tampilan()

    def _aksi_hapus_post(self):
        """Menampilkan dialog konfirmasi Batal/Hapus lalu menghapus post terpilih beserta komentarnya."""
        if self.id_post_terpilih is None:
            return

        post = cari_post_berdasarkan_id(self.daftar_post, self.id_post_terpilih)
        if post is None:
            return

        if not self._konfirmasi_hapus_post():
            return

        hapus_post(self.daftar_post, post["id"])
        self.id_post_terpilih = None
        self._simpan_perubahan()
        self._perbarui_tampilan()

    def _konfirmasi_hapus_post(self):
        """Menampilkan dialog konfirmasi modal dengan teks 'Hapus post ini beserta semua komentarnya?' dan tombol Batal / Hapus."""
        hasil = {"setuju": False}

        dialog = ctk.CTkToplevel(self, fg_color=WARNA["latar"])
        dialog.title("Konfirmasi Hapus Post")
        dialog.geometry("390x185")
        dialog.resizable(False, False)
        pasang_ikon_jendela(dialog)
        dialog.transient(self)
        dialog.grab_set()

        wadah = ctk.CTkFrame(
            dialog,
            corner_radius=UKURAN["radius_panel"],
            fg_color=WARNA["panel"],
            border_width=1,
            border_color=WARNA["garis"],
        )
        wadah.pack(fill="both", expand=True, padx=14, pady=14)
        wadah.grid_columnconfigure(0, weight=1)
        wadah.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            wadah,
            text="Hapus Post?",
            anchor="w",
            font=buat_font("subpanel", tebal=True),
            text_color=WARNA["teks"],
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            wadah,
            text="Hapus post ini beserta semua komentarnya?",
            anchor="w",
            justify="left",
            wraplength=330,
            font=buat_font("isi_post"),
            text_color=WARNA["teks_sekunder"],
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 12))

        baris_tombol = ctk.CTkFrame(wadah, fg_color="transparent")
        baris_tombol.grid(row=2, column=0, sticky="e", padx=18, pady=(0, 14))

        def pilih_batal():
            hasil["setuju"] = False
            dialog.destroy()

        def pilih_hapus():
            hasil["setuju"] = True
            dialog.destroy()

        dialog.protocol("WM_DELETE_WINDOW", pilih_batal)
        dialog.bind("<Escape>", lambda _event: pilih_batal())

        tombol_batal = ctk.CTkButton(
            baris_tombol,
            text="Batal",
            width=92,
            height=UKURAN["tinggi_tombol"],
            corner_radius=UKURAN["tinggi_tombol"] // 2,
            fg_color=WARNA["kartu"],
            hover_color=WARNA["kartu_hover"],
            border_width=1,
            border_color=WARNA["garis_input"],
            text_color=WARNA["teks"],
            font=buat_font("tombol"),
            command=pilih_batal,
        )
        tombol_batal.pack(side="left", padx=(0, 8))

        tombol_hapus = ctk.CTkButton(
            baris_tombol,
            text="Hapus",
            width=96,
            height=UKURAN["tinggi_tombol"],
            corner_radius=UKURAN["tinggi_tombol"] // 2,
            fg_color=WARNA["bahaya"],
            hover_color=WARNA["aksen_hover"],
            text_color=WARNA["putih"],
            font=buat_font("tombol", tebal=True),
            command=pilih_hapus,
        )
        tombol_hapus.pack(side="left")

        self.wait_window(dialog)
        return hasil["setuju"]
