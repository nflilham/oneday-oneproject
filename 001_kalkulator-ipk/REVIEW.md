# REVIEW: kalkulator IPK

## Hasil
Lolos. Seluruh kriteria selesai terpenuhi sesuai harapan: menu navigasi berjalan lancar, perhitungan IPK dan total SKS akurat, validasi masukan kokoh, serta penyimpanan dan pembaruan berkas `data.json` berfungsi otomatis.

## Kesalahan agent
Tidak ada. Agent mengerjakan tugas sesuai instruksi dan mampu menyesuaikan perubahan alur secara cepat.

## Kesalahan spesifikasi
Secara teknis tidak ada kekeliruan pada draf awal, melainkan munculnya ide mendadak dari pengguna di tengah proses pengerjaan yang mengubah batasan ruang lingkup (menambahkan menu angka dan persistensi file JSON).

## Bagian kode yang belum dipahami
Tidak ada. Pembagian fungsi, validasi masukan dengan `try-except`, serta operasi baca-tulis file JSON dapat dipahami dengan baik.

## Revisi spesifikasi
Spesifikasi direvisi di tengah pengerjaan: program yang awalnya satu kali jalan diubah menjadi program berbasis menu angka (lihat, tambah, hapus 1 data, keluar), ditambahkan penyimpanan data ke berkas `data.json`, dan fitur hapus data langsung dieksekusi berdasarkan nomor urut baris.

## Pelajaran hari ini
Menyadari pentingnya merumuskan kebutuhan secara matang di awal agar alur pengembangan tidak bergeser di tengah jalan. Hari pertama menjadi awal yang baik untuk melatih evaluasi diri dan membangun konsistensi proyek harian.
