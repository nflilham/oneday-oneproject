Tanggal: 2026-11-21

# Forum Post dan Komentar

Aplikasi terminal Python bermodul untuk membuat, melihat, mencari, mengomentari, dan menghapus post dengan penyimpanan otomatis ke file `data_forum.json`. Sebagai hasil eksplorasi di luar spesifikasi awal, seluruh kolom masukan juga mendukung perintah `batal` untuk kembali ke menu utama tanpa menyimpan perubahan.

## Cara menjalankan

Buka PowerShell di folder repo, lalu jalankan program atau pengujian otomatis:

```powershell
cd 004_forum-post-komentar
python main.py
```

Untuk menjalankan pengujian otomatis:

```powershell
python -m unittest -v
```

## Cara memakai

Pilih nomor menu `1` sampai `6` untuk mengelola post dan komentar, ketik `batal` pada kolom masukan bila ingin membatalkan aksi, atau pilih `0` untuk keluar.

Contoh masukan dan keluaran saat membuat post lalu melihat daftarnya:

```text
Pilih menu: 2

--- Buat Post Baru ---
(Ketik 'batal' untuk kembali ke menu)
Nama penulis: Naufal
Judul post  : Belajar Python
Isi post    : Hari keempat latihan
Post berhasil dibuat dengan ID 1.

Pilih menu: 1

--- Daftar Post ---
[1] Belajar Python | oleh Naufal | 0 komentar | 2026-11-21 12:00
```

## Catatan pelajaran

Untuk kasus dasar seperti pembuatan aplikasi post dan komentar di Python, AI sudah sangat mampu menghasilkan kode yang terstruktur, modular, dan sesuai spesifikasi. Peran pengembang tetap penting pada perumusan spesifikasi awal, pengujian kasus batas, serta eksplorasi fitur tambahan agar program lebih nyaman digunakan.
