# AGENTS.md: aturan kerja repo oneday-oneproject

Berkas ini adalah instruksi untuk agent AI (Hermes Agent dan OpenCode) yang bekerja di repo ini. Baca seluruhnya sebelum melakukan apa pun, dan ikuti setiap kali ada sesi baru.

Bila aturan di berkas ini bertentangan dengan `AGENTS.md` lain di folder induk (misalnya folder home), aturan di berkas ini yang dipakai untuk pekerjaan di dalam repo ini. Itu berlaku juga untuk kebiasaan bertanya "mode" sebelum mengerjakan tugas: di repo ini jangan bertanya mode, ikuti alur di bagian 3.

## 1. Konteks

Pemilik repo adalah Naufal Ilham Fauzan, mahasiswa S1 Pendidikan Multimedia UPI semester 3. Ia membuat satu projek kecil setiap hari untuk dua tujuan: melatih kemampuannya menulis spesifikasi dan mereview hasil agent, serta mengumpulkan karya untuk web portofolio.

Kemampuan Python Naufal ada di level dasar sampai menengah. Ia ingin memahami kode yang kamu tulis, bukan hanya menerima hasilnya. Ia berkomunikasi dalam bahasa Indonesia, jadi semua penjelasan, komentar kode, dan dokumentasi ditulis dalam bahasa Indonesia.

Lingkungan Naufal: Windows 11 (64-bit). Terminal agent mungkin berupa bash (git-bash), tetapi Naufal menjalankan hasilnya di PowerShell. Karena itu:

- Tulis perintah di `README.md` untuk PowerShell (contoh: `python main.py`, path memakai backslash).
- Hindari perintah khusus Linux di dalam kode dan dokumentasi.
- Bila hasil uji di terminalmu bisa berbeda dari PowerShell (misalnya encoding konsol), catat perbedaannya di laporan.

Memulai sesi: sesi Hermes sebaiknya dijalankan dari folder repo supaya berkas ini terbaca otomatis. Bila sesi tidak dimulai dari folder repo, Naufal akan membuka dengan perintah "baca AGENTS.md di repo oneday-oneproject".

## 2. Struktur repo

```
oneday-oneproject/
  AGENTS.md
  IDE.md
  001_nama-projek/
    SPEC.md
    REVIEW.md
    README.md
    (kode projek)
```

Di akar repo juga ada `.gitattributes` berisi `* text=auto` agar akhir baris (LF dan CRLF) konsisten di Windows.

- Setiap projek punya satu folder bernama `NNN_nama-projek`. `NNN` adalah nomor urut tiga digit yang melanjutkan nomor terakhir, dan nama memakai huruf kecil dengan tanda hubung.
- Seluruh pekerjaan satu projek tinggal di dalam foldernya. Jangan mengubah folder projek lain.
- `IDE.md` adalah bank ide milik Naufal. Naufal yang memilih ide harian dan menandai ide yang sudah dipakai (contoh: `(dipakai: 003)`). Jangan mengubah `IDE.md`. Bila ia meminta usulan ide, tulis usulannya di chat saja, dan ikuti aturan ukuran ide: bisa dijelaskan dalam satu kalimat dan punya kriteria selesai yang bisa dicek.

## 3. Alur kerja harian

Satu projek berjalan dalam empat tahap. Jangan melompati tahap.

1. **Spesifikasi.** Naufal menulis `SPEC.md`. Tugasmu pada tahap ini hanya membantu bila diminta (misalnya mengecek apakah spesifikasinya cukup jelas).
2. **Eksekusi.** Kamu mengerjakan projek berdasarkan `SPEC.md`.
3. **Review.** Naufal membaca dan menjalankan hasilnya, lalu mengisi `REVIEW.md`.
4. **Dokumentasi dan publikasi.** Kamu menulis `README.md` dan menyiapkan entri kartu portofolio.

## 4. Aturan eksekusi

### Sebelum menulis kode

- Cek bahwa `SPEC.md` ada di folder projek dan semua bagian wajibnya terisi (lihat templat di bagian 6). Jika tidak ada atau belum lengkap, berhenti dan minta Naufal melengkapinya. Jangan menebak isinya.
- Jika ada bagian spesifikasi yang ambigu, ajukan satu pertanyaan singkat sebelum mulai. Jangan memilih tafsir sendiri secara diam-diam.
- Baca `SPEC.md` sampai habis. Fitur, batasan, dan kriteria selesai di sana adalah satu-satunya acuan kerjamu.

### Saat menulis kode

- Kerjakan hanya fitur yang tercantum di `SPEC.md`. Jangan menambah fitur, pustaka, atau struktur yang tidak diminta. Jika menurutmu ada tambahan yang berguna, tulis sebagai saran di akhir, jangan langsung dikerjakan.
- Pakai teknologi yang ditetapkan di `SPEC.md`. Untuk projek Python, utamakan pustaka standar. Untuk projek web, pakai HTML, CSS, dan JavaScript biasa tanpa kerangka kerja, kecuali spesifikasi menyebutnya.
- Tulis kode yang sederhana dan mudah dibaca untuk level dasar sampai menengah. Pilih konstruksi yang umum daripada trik singkat yang sulit dipahami.
- Beri komentar berbahasa Indonesia yang menjelaskan fungsi tiap bagian penting dan maksud baris yang tidak langsung jelas. Pakai nama variabel dan fungsi yang deskriptif.
- Kerjakan satu bagian kecil, jalankan, lalu lanjut. Jangan menulis seluruh projek sekaligus tanpa pernah menjalankannya.
- Selalu jalankan hasilnya dan cocokkan dengan kriteria selesai di `SPEC.md` sebelum menyatakan pekerjaan selesai. Laporkan hasil pengujian apa adanya, termasuk yang gagal.

### Saat melaporkan hasil

- Ringkas apa yang dibuat dan file mana yang dibuat atau diubah.
- Jelaskan alur kerja kodenya secara berurutan dengan bahasa yang bisa diikuti pemula, dan tunjukkan bagian yang paling layak dibaca teliti saat review.
- Sebutkan terus terang bagian yang tidak yakin kamu selesaikan dengan benar, asumsi yang kamu ambil, dan kriteria yang belum terpenuhi. Jangan mengklaim berhasil bila belum diuji.

### Batasan tindakan

- Kamu yang membuat commit lokal, satu commit per projek, setelah Naufal menyatakan review selesai dan `README.md` sudah ditulis. Pesan commit berbahasa Indonesia dan menyebut nomor serta nama projek:
  - Projek lolos: `001 kalkulator-ipk: selesai sesuai SPEC`
  - Projek tidak lolos: `001 kalkulator-ipk: belum selesai, lihat REVIEW.md`
- Projek yang tidak lolos tetap di-commit, tetapi tidak dibuatkan entri kartu portofolio.
- Jangan melakukan `git push`, menghapus folder atau file di luar folder projek, atau mengubah repo lain tanpa perintah eksplisit dari Naufal.
- Jangan memasang dependensi global atau mengubah pengaturan sistem tanpa bertanya.

## 5. Dokumentasi dan kartu portofolio

Setelah Naufal menyatakan review selesai, lakukan dua hal.

### README.md projek

Tulis `README.md` singkat di folder projek dengan urutan berikut:

1. Baris pertama: `Tanggal: YYYY-MM-DD` (tanggal pengerjaan).
2. Judul projek dan deskripsi satu sampai dua kalimat.
3. Cara menjalankan (perintah yang tepat untuk Windows).
4. Cara memakai, dengan satu contoh masukan dan keluaran.
5. Catatan pelajaran hari itu, diambil dari `REVIEW.md`.

### Entri kartu portofolio

Jika projek lolos review (semua kriteria selesai terpenuhi), tampilkan di chat satu entri JSON untuk ditempelkan Naufal ke `projects.json` di web portofolionya. Jangan mengubah repo portofolio sendiri. Jika projek tidak lolos, jangan buat entri.

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

Aturan isian: `id` sama dengan nomor projek tanpa nol di depan, `tag` hanya `python` atau `web`, `date` berformat `YYYY-MM-DD` dan berisi tanggal pengerjaan yang sebenarnya (tanggal pada contoh di atas hanya ilustrasi), dan `description` paling banyak dua kalimat tanpa kata superlatif.

## 6. Templat berkas

### SPEC.md (diisi Naufal)

```markdown
# SPEC: nama projek

## Tujuan
Satu kalimat tentang apa yang dibuat dan untuk apa.

## Fitur inti
1. (maksimal tiga fitur)

## Batasan teknologi
Bahasa, pustaka yang boleh dipakai, dan hal yang tidak boleh dipakai.

## Kriteria selesai
Daftar hal yang bisa dicek, misalnya "menerima 5 nilai dan mencetak
rata-rata", "input huruf tidak membuat program berhenti".

## Di luar lingkup
Hal yang sengaja tidak dikerjakan hari ini.
```

Bagian wajib: Tujuan, Fitur inti, Batasan teknologi, dan Kriteria selesai.

### REVIEW.md (diisi Naufal)

```markdown
# REVIEW: nama projek

## Hasil
Lolos atau tidak lolos, disertai kriteria selesai mana yang terpenuhi.

## Kesalahan agent
Hal yang dikerjakan agent dengan keliru atau di luar spesifikasi.

## Kesalahan spesifikasi
Bagian SPEC.md yang kurang jelas atau kurang lengkap.

## Bagian kode yang belum dipahami
Catatan untuk dipelajari lebih lanjut.

## Revisi spesifikasi
Perubahan pada SPEC.md selama pengerjaan, bila ada.

## Pelajaran hari ini
Satu sampai tiga kalimat.
```

## 7. Gaya komunikasi

- Jawab dalam bahasa Indonesia semi-formal, singkat, dan langsung ke inti. Tanpa emoji.
- Jika Naufal keliru dalam pemahaman, kode, atau spesifikasi, sampaikan langsung beserta alasannya.
- Jika kamu tidak yakin, katakan terus terang. Jangan menebak.
