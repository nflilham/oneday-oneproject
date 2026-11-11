# oneday-oneproject

Inisiatif harian untuk melatih kemampuan menyusun spesifikasi teknis, mengevaluasi hasil agent AI, dan membangun portofolio konsisten satu projek per hari.

Dikelola oleh **Naufal Ilham Fauzan** (Pendidikan Multimedia, Universitas Pendidikan Indonesia).

## Filosofi dan alur kerja

Setiap projek melewati empat tahap yang tidak boleh dilompati:

1. **Spesifikasi.** Menentukan tujuan, batasan teknologi, kriteria selesai, dan ruang lingkup secara presisi sebelum kode ditulis.
2. **Eksekusi.** Agent AI mengerjakan program berdasarkan `SPEC.md`, lalu menjalankannya dan mencocokkan hasil dengan kriteria selesai.
3. **Review.** Pemilik repo menguji keluaran secara mandiri, memeriksa kondisi batas, dan mencatat hasil evaluasi di `REVIEW.md`.
4. **Dokumentasi.** Menulis panduan penggunaan dan menyiapkan entri untuk web portofolio.

Tujuan utamanya bukan sekadar menambah karya, tetapi berlatih menulis spesifikasi yang jelas dan menilai hasil agent secara kritis.

## Daftar projek

| No | Projek | Fokus | Ringkasan | Status |
|:---:|:---|:---:|:---|:---:|
| 001 | [001_kalkulator-ipk](./001_kalkulator-ipk) | Python | Program terminal berbasis menu dengan penyimpanan JSON untuk menghitung IPK | Lolos |
| 002 | [002_homepage-warung-fiktif](./002_homepage-warung-fiktif) | Web | Halaman web statis dengan daftar menu dinamis JavaScript vanilla dan filter kategori | Lolos |

## Lingkungan dan standar teknis

- **Sistem operasi:** Windows 11 (64-bit)
- **Terminal:** PowerShell
- **Bahasa:** Python 3 dengan pustaka standar, dan HTML/CSS/JavaScript biasa untuk projek web
- **Gaya kode:** Sederhana dan mudah dibaca, dengan fungsi kecil, nama deskriptif, dan komentar berbahasa Indonesia

## Struktur repositori

```
oneday-oneproject/
  NNN_nama-projek/
    README.md      panduan menjalankan dan memakai
    REVIEW.md      catatan hasil evaluasi
    (kode projek)
```

Berkas `AGENTS.md` (instruksi kerja agent) dan `SPEC.md` (spesifikasi tiap projek) hanya disimpan lokal dan tidak diikutsertakan dalam repositori ini.
