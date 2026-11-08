Tanggal: 2026-11-08

# Kalkulator IPK

Program terminal berbasis menu untuk mencatat mata kuliah (nama, nilai huruf, SKS),
menghitung IPK, dan menyimpan datanya di `data.json` agar tidak hilang saat program ditutup.

## Cara menjalankan

Buka PowerShell di folder repo, lalu:

```powershell
cd 001_kalkulator-ipk
python main.py
```

File `data.json` dibuat otomatis saat data pertama ditambahkan, jadi tidak perlu dibuat manual.
Jika file itu rusak atau bentuknya tidak sesuai, program memberi peringatan lalu mulai dari data kosong.

## Cara memakai

Pilih menu dengan mengetik angkanya:

```
=== Kalkulator IPK ===
1. Lihat data
2. Tambah data
3. Hapus 1 data
4. Keluar
```

Contoh: pilih `2`, lalu isi `Algoritma`, nilai `A`, SKS `3`. Ulangi untuk `Kalkulus`, nilai `B`, SKS `2`.
Setelah itu pilih `1` untuk melihat hasil:

```
No   Mata kuliah Nilai SKS
--------------------------
1    Algoritma   A       3
2    Kalkulus    B       2
--------------------------
Total SKS : 5
IPK       : 3.60
```

Masukan yang salah tidak menghentikan program. Nilai selain A-E, SKS bukan bilangan bulat positif,
nama kosong, atau nomor hapus di luar daftar akan ditolak dan ditanyakan ulang.

Untuk menghapus, pilih `3` lalu ketik nomor urut baris yang ingin dihapus. Penghapusan langsung
dijalankan tanpa konfirmasi dan langsung disimpan ke `data.json`.

## Catatan pelajaran

Merumuskan kebutuhan secara matang di awal membuat alur pengembangan tidak bergeser di tengah jalan.
Hari pertama ini jadi latihan mengevaluasi hasil kerja sendiri dan membangun konsistensi satu projek per hari.
