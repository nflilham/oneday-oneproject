# SPEC: kalkulator IPK

## Tujuan
Program terminal berbasis menu untuk mengelola daftar mata kuliah (lihat, tambah, hapus) dan menghitung IPK, dengan data yang disimpan permanen di `data.json`.

## Fitur inti
1. Menu angka di awal program: 1 lihat data, 2 tambah data, 3 hapus 1 data, 4 keluar.
2. Data mata kuliah (nama, nilai huruf, SKS) disimpan di `data.json` berbentuk list of object sederhana `[{"nama": "...", "nilai": "...", "sks": 3}]`. Data disimpan ke file sesaat setelah berhasil menambah atau menghapus.
3. Penghapusan memakai nomor urut pada tabel, langsung dieksekusi tanpa konfirmasi, dengan validasi try-except agar nomor yang salah tidak menghentikan program.

## Batasan teknologi
- Python 3, pustaka standar saja (`json` termasuk pustaka standar), tanpa pustaka eksternal.
- Satu file `main.py` (plus `data.json` yang dibuat otomatis). Dijalankan dengan `python main.py` di PowerShell.
- Bobot nilai disimpan dalam satu dictionary.
- Logika dipisah menjadi fungsi-fungsi kecil (muat data, simpan data, baca masukan, hitung IPK, cetak tabel, menu utama).
- Tanpa basis data dan tanpa tampilan grafis.

## Kriteria selesai
- Saat program start, `data.json` dibaca. Bila file belum ada, program membuat data kosong tanpa error.
- Bila isi `data.json` rusak atau tidak sesuai bentuk, program menampilkan pesan dan mulai dari data kosong tanpa berhenti.
- Menu 1 menampilkan tabel rapi (No, Mata kuliah, Nilai, SKS), total SKS, dan IPK dua desimal. Bila kosong, tampil "Belum ada data".
- Menu 2 memvalidasi nama tidak kosong, nilai huruf A-E (huruf kecil diterima), dan SKS bilangan bulat positif. Masukan salah diminta ulang, program tidak berhenti.
- Hasil tambah langsung terlihat dan langsung tersimpan di `data.json`.
- Menu 3 meminta nomor urut; nomor yang bukan angka atau di luar daftar ditolak dengan try-except dan diminta ulang. Penghapusan langsung dieksekusi tanpa konfirmasi dan langsung tersimpan.
- Menu 4 keluar dengan bersih. Pilihan menu selain 1-4 ditolak dan diminta ulang.
- Data yang dihitung: (Algoritma, A, 3) dan (Kalkulus, B, 2) menghasilkan total SKS 5 dan IPK 3.60.
- Setiap fungsi punya komentar berbahasa Indonesia yang menjelaskan tugasnya.

## Di luar lingkup
- Tidak ada konfirmasi sebelum menghapus data.
- Tidak menghitung beberapa semester sekaligus dan tidak menghitung IPS terpisah.
- Tidak ada nilai dengan tanda plus atau minus, atau nilai tambahan seperti AB dan BC.
- Tidak ada tampilan grafis.
