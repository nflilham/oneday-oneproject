# Spesifikasi desain: oneday-oneproject

Tanggal: 8 November 2026
Pemilik: Naufal Ilham Fauzan
Status: menunggu tinjauan pemilik

## 1. Tujuan

Naufal membuat satu projek kecil setiap hari dengan bantuan agent AI (Hermes dan OpenCode). Latihan ini punya dua tujuan yang berjalan bersamaan:

1. Melatih kemampuan mengarahkan agent: menulis spesifikasi, menyusun prompt, dan mereview hasil kerja agent (vibe coding yang terstruktur).
2. Mengumpulkan karya yang dipajang di web portofolio pribadi.

Keberhasilan diukur dari tiga hal: ada projek baru hampir setiap hari, tiap projek punya spesifikasi dan catatan review, dan portofolio terus bertambah tanpa kerja manual yang berat.

## 2. Batasan

- Waktu per hari: sekitar 2 sampai 3 jam, termasuk spesifikasi, eksekusi, review, dan dokumentasi.
- Ukuran projek: harus bisa dijelaskan dalam satu kalimat dan punya kriteria selesai yang bisa dicek.
- Bahasa: Python dan web (HTML, CSS, JavaScript), bergantian.
- Level pemilik: Python dasar sampai menengah, sehingga kode yang dihasilkan agent harus sederhana dan berkomentar.

Di luar lingkup: aplikasi besar, projek yang butuh basis data atau server berbayar, dan pengerjaan lebih dari satu hari untuk satu projek.

## 3. Alur satu hari

Satu hari terdiri dari empat tahap berurutan.

| Tahap | Durasi | Pelaku | Keluaran |
|---|---|---|---|
| Spesifikasi | 15 sampai 20 menit | Naufal | `SPEC.md` |
| Eksekusi | 60 sampai 90 menit | Agent | Kode projek |
| Review | 30 sampai 40 menit | Naufal | `REVIEW.md` |
| Dokumentasi dan publikasi | 10 sampai 15 menit | Naufal dan agent | `README.md`, commit, entri kartu |

Aturan alur:

- Agent tidak menulis kode sebelum `SPEC.md` ada dan lengkap.
- Jika hasil agent melenceng, perbaikan dimulai dari `SPEC.md`, bukan hanya prompt tambahan. Revisi spesifikasi dicatat di `REVIEW.md`.
- Jika waktu habis dan kriteria selesai belum tercapai, projek tetap di-commit dan kegagalannya dicatat apa adanya di `REVIEW.md`. Projek seperti ini tidak dipajang di portofolio.

## 4. Struktur repo

```
oneday-oneproject/
  AGENTS.md
  IDE.md
  001_nama-projek/
    SPEC.md
    REVIEW.md
    README.md
    (kode projek)
  002_nama-projek/
    ...
```

- Nomor urut tiga digit, dimulai dari `001`, dipakai di depan nama folder. Nama folder memakai huruf kecil dan tanda hubung.
- Tanggal pengerjaan ditulis di baris pertama `README.md`, karena nomor urut tidak selalu sejajar dengan tanggal bila ada hari yang terlewat.
- `AGENTS.md` berisi aturan kerja untuk agent (dibaca Hermes dan OpenCode). `IDE.md` adalah bank ide.

## 5. Pemilihan ide

1. Pola dasar: hari kuliah padat mendapat projek Python (biasanya tanpa tampilan), hari longgar dan akhir pekan mendapat projek web.
2. Tiap minggu boleh punya satu tema kecil sebagai pemandu (contoh minggu pertama: alat bantu mahasiswa), dengan bahasa yang tetap bergantian. Tema bisa disambungkan dengan materi kuliah, misalnya Algoritma dan Struktur Data.
3. Bank ide disimpan di `IDE.md`, setiap ide ditandai `[py]` atau `[web]`.
4. Sebuah ide layak dipakai bila bisa dijelaskan dalam satu kalimat dan punya kriteria selesai yang bisa dicek. Contoh yang lolos: "to-do list yang bisa menambah dan menghapus tugas". Contoh yang tidak lolos: "aplikasi manajemen kuliah lengkap".
5. Kesulitan naik pelan: minggu awal satu fitur per projek, lalu bertahap menambah fitur.

## 6. Kartu portofolio

Setiap projek yang lolos review mendapat satu kartu di web portofolio.

Isi kartu:

- Nomor projek (contoh `#001`)
- Judul
- Deskripsi satu sampai dua kalimat
- Label bahasa: `python` atau `web`
- Tanggal pengerjaan
- Tautan ke folder projek di GitHub

Aturan:

- Semua data kartu disimpan dalam satu file data di web portofolio (contoh `projects.json`). Halaman portofolio membaca file itu, sehingga menambah projek hanya berarti menambah satu entri.
- Contoh satu entri:

```json
{
  "id": 1,
  "title": "Kalkulator IPK",
  "description": "Program terminal yang menghitung IPK dari nilai dan SKS.",
  "tag": "python",
  "date": "2026-11-09",
  "link": "https://github.com/nflilham/oneday-oneproject/tree/main/001_kalkulator-ipk"
}
```

- Tampilan: projek terbaru di atas, dengan filter "Semua, Python, Web".
- Agent menyiapkan teks entri di akhir hari. Naufal yang menempelkannya ke `projects.json`, karena repo portofolio terpisah dari repo ini.
- Kartu hanya dibuat untuk projek yang lolos review.

## 7. Asumsi

Asumsi berikut dipakai karena belum dikonfirmasi pemilik. Pemilik cukup memberi tahu bila ada yang keliru.

- Nama repo adalah `oneday-oneproject` dan berada di akun GitHub yang sama dengan repo kuliah.
- Agent boleh membuat commit lokal, tetapi push ke GitHub hanya atas perintah Naufal.
- Tautan di kartu mengarah ke folder projek di cabang `main`.

## 8. Kriteria keberhasilan

- Minimal lima projek selesai dalam tujuh hari pertama, masing-masing dengan `SPEC.md`, `REVIEW.md`, dan `README.md`.
- Tiap `REVIEW.md` memuat sekurang-kurangnya satu catatan kesalahan agent atau kesalahan spesifikasi.
- Menambah kartu portofolio memakan waktu kurang dari lima menit per projek.
