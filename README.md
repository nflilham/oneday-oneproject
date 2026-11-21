# oneday-oneproject

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Web](https://img.shields.io/badge/Web-HTML%20%7C%20CSS%20%7C%20JS-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Status](https://img.shields.io/badge/Status-Active-2EA44F?style=for-the-badge)

Repositori latihan harian **satu projek per hari** untuk melatih perumusan spesifikasi teknis, kolaborasi terstruktur dengan AI coding agent, peninjauan kode secara kritis, dan dokumentasi karya portofolio.

---

## Alur Kerja Harian

Setiap projek dijalankan melalui empat tahap berurutan:

| Tahap | Fokus | Keluaran |
|:---:|:---|:---|
| **1. Spesifikasi** | Menetapkan tujuan, fitur inti, batasan teknologi, dan kriteria uji yang terukur | `SPEC.md` (lokal) |
| **2. Eksekusi** | Membangun program sesuai acuan awal sambil membuka ruang eksplorasi di chat | Kode projek |
| **3. Review** | Menguji program secara mandiri, memeriksa kasus batas, dan mencatat evaluasi | `REVIEW.md` |
| **4. Dokumentasi** | Menyusun panduan pakai, entri kartu portofolio, lalu commit ke repositori | `README.md` |

> Prinsip utama latihan ini adalah melatih kejelasan spesifikasi dan ketajaman review, bukan sekadar menghasilkan kode dengan cepat.

---

## Daftar Projek

| No | Projek | Stack | Ringkasan | Status |
|:---:|:---|:---:|:---|:---:|
| `001` | [001_kalkulator-ipk](./001_kalkulator-ipk) | Python | Program terminal berbasis menu untuk mencatat nilai/SKS, menghitung IPK, dan menyimpan data ke JSON | Lolos |
| `002` | [002_homepage-warung-fiktif](./002_homepage-warung-fiktif) | Web | Halaman web statis dengan daftar menu dinamis JavaScript vanilla dan filter kategori | Lolos |
| `003` | [003_kalkulator-modular](./003_kalkulator-modular) | Python | Kalkulator terminal dengan struktur paket modular dan evaluasi prioritas operator | Menunggu review |
| `004` | [004_forum-post-komentar](./004_forum-post-komentar) | Python | Aplikasi CLI post dan komentar bermodul dengan penyimpanan JSON, perintah `batal`, dan 13 unit test `unittest` | Lolos |

---

## Struktur Direktori

```text
oneday-oneproject/
├── 001_kalkulator-ipk/            # Projek 001: kalkulator IPK berbasis terminal & JSON
├── 002_homepage-warung-fiktif/    # Projek 002: homepage statis dengan filter kategori
├── 003_kalkulator-modular/        # Projek 003: kalkulator modular (iterasi awal)
├── 004_forum-post-komentar/       # Projek 004: aplikasi post & komentar CLI + unittest
├── IDE.md                         # Bank ide projek harian
├── .gitignore                     # Aturan pengecualian file lokal dan cache
└── README.md                      # Dokumentasi utama repositori
```

Di dalam setiap folder projek yang sudah selesai:

```text
NNN_nama-projek/
├── README.md                      # Panduan menjalankan, contoh pakai, dan catatan pelajaran
├── REVIEW.md                      # Hasil evaluasi mandiri terhadap spesifikasi dan kode
└── (berkas sumber & pengujian)
```

> Berkas `AGENTS.md`, `.agents/`, `SPEC.md`, cache Python, dan file data JSON lokal sengaja diabaikan melalui `.gitignore`.

---

## Lingkungan & Standar Teknis

- **Sistem operasi & terminal:** Windows 11 (64-bit) menggunakan PowerShell
- **Python:** Python 3 dengan pustaka standar saja (tanpa dependensi eksternal kecuali ditentukan)
- **Web:** HTML, CSS, dan JavaScript vanilla tanpa framework
- **Keterbacaan kode:** Fungsi kecil bertanggung jawab tunggal, penamaan deskriptif, komentar berbahasa Indonesia, dan validasi masukan

---

## Cara Menjalankan Projek

Kloning repositori lalu buka salah satu folder projek di PowerShell:

```powershell
git clone https://github.com/nflilham/oneday-oneproject.git
cd oneday-oneproject
```

Contoh menjalankan projek Python (`004_forum-post-komentar`):

```powershell
cd 004_forum-post-komentar
python main.py
python -m unittest -v
```

Contoh membuka projek Web (`002_homepage-warung-fiktif`):

```powershell
cd 002_homepage-warung-fiktif
Start-Process index.html
```
