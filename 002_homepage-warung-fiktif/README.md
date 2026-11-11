Tanggal: 2026-11-11

# Homepage Warung Makanan Fiktif

Halaman web statis untuk Warung Sedap Rasa yang menampilkan informasi operasional dan daftar menu interaktif berbasis JavaScript vanilla. Dilengkapi sistem filter kategori makanan dan minuman tanpa pustaka eksternal.

## Cara menjalankan

Buka PowerShell di folder repo, lalu jalankan:

```powershell
cd 002_homepage-warung-fiktif
Start-Process index.html
```

Atau klik dua kali file `index.html` langsung melalui File Explorer. Halaman berjalan langsung di browser tanpa butuh server maupun koneksi internet.

## Cara memakai

Saat halaman dibuka, informasi warung, jam operasional, dan 6 item menu akan otomatis ditampilkan dengan tombol "Semua" terpilih:

- Klik tombol **Makanan**: hanya 3 item makanan yang muncul.
- Klik tombol **Minuman**: hanya 3 item minuman yang muncul.
- Klik tombol **Semua**: seluruh 6 item menu kembali ditampilkan.

Tombol filter yang aktif ditandai dengan perubahan warna latar. Bila data menu pada `script.js` dikosongkan, halaman akan menampilkan pesan `"Menu belum tersedia"`.

## Catatan pelajaran

Membangun web statis interaktif tanpa library memperdalam pemahaman manipulasi DOM dan logika array dasar. Penggunaan CSS Grid modern memudahkan pembuatan tampilan responsif yang konsisten di berbagai ukuran layar.
