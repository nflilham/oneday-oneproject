// Data menu warung. Kategori hanya boleh "makanan" atau "minuman".
// Kolom "ilustrasi" adalah nama kunci gambar di objek gambarSvg di bawah.
const dataMenu = [
  {
    nama: "Nasi Goreng Spesial",
    kategori: "makanan",
    deskripsi: "Nasi goreng bumbu rempah dengan telur mata sapi dan acar segar.",
    harga: 22000,
    ilustrasi: "nasiGoreng"
  },
  {
    nama: "Ayam Bakar Madu",
    kategori: "makanan",
    deskripsi: "Ayam bakar bumbu manis gurih disajikan dengan sambal terasi.",
    harga: 28000,
    ilustrasi: "ayamBakar"
  },
  {
    nama: "Mie Goreng Jawa",
    kategori: "makanan",
    deskripsi: "Mie kuning kenyal dimasak dengan kol, sawi, dan suwiran ayam.",
    harga: 18000,
    ilustrasi: "mieGoreng"
  },
  {
    nama: "Es Teh Manis",
    kategori: "minuman",
    deskripsi: "Teh melati seduh segar dengan gula tebu asli.",
    harga: 5000,
    ilustrasi: "esTeh"
  },
  {
    nama: "Es Jeruk Peras",
    kategori: "minuman",
    deskripsi: "Jeruk peras murni dengan es batu kristal.",
    harga: 8000,
    ilustrasi: "esJeruk"
  },
  {
    nama: "Kopi Tubruk Tuban",
    kategori: "minuman",
    deskripsi: "Kopi hitam robusta seduh tradisional beraroma mantap.",
    harga: 10000,
    ilustrasi: "kopiTubruk"
  }
];

// Ilustrasi makanan dan minuman berupa SVG yang digambar lewat kode.
// Semua memakai viewBox 200 x 120 supaya ukurannya seragam di tiap kartu.
const gambarSvg = {
  nasiGoreng:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<ellipse cx="100" cy="92" rx="76" ry="19" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M44 86 Q48 40 100 38 Q152 40 156 86 Q100 102 44 86Z" fill="#d9a441" stroke="#3b2314" stroke-width="3"/>' +
    '<ellipse cx="100" cy="54" rx="26" ry="15" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<circle cx="100" cy="53" r="9" fill="#e8a317" stroke="#3b2314" stroke-width="2"/>' +
    '<circle cx="168" cy="94" r="8" fill="#7a9a4a" stroke="#3b2314" stroke-width="2.5"/>' +
    '<circle cx="152" cy="102" r="8" fill="#7a9a4a" stroke="#3b2314" stroke-width="2.5"/>' +
    '</svg>',

  ayamBakar:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<ellipse cx="100" cy="92" rx="76" ry="19" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<line x1="132" y1="66" x2="162" y2="50" stroke="#3b2314" stroke-width="13" stroke-linecap="round"/>' +
    '<line x1="132" y1="66" x2="162" y2="50" stroke="#faf3e8" stroke-width="7" stroke-linecap="round"/>' +
    '<path d="M54 82 Q50 44 94 40 Q134 38 138 64 Q140 86 104 88 Q76 92 54 82Z" fill="#b85d19" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M76 56 Q92 50 108 58" fill="none" stroke="#3b2314" stroke-width="3" stroke-linecap="round"/>' +
    '<path d="M72 72 Q94 66 118 74" fill="none" stroke="#3b2314" stroke-width="3" stroke-linecap="round"/>' +
    '<ellipse cx="62" cy="98" rx="15" ry="6" fill="#8e2a12" stroke="#3b2314" stroke-width="2"/>' +
    '</svg>',

  mieGoreng:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<ellipse cx="100" cy="92" rx="76" ry="19" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M46 86 Q50 44 100 42 Q150 44 154 86 Q100 102 46 86Z" fill="#f0c25a" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M56 78 Q70 56 84 74 T112 70 T142 76" fill="none" stroke="#b8791f" stroke-width="5" stroke-linecap="round"/>' +
    '<path d="M60 62 Q76 44 92 60 T124 58 T146 64" fill="none" stroke="#b8791f" stroke-width="5" stroke-linecap="round"/>' +
    '<path d="M70 88 Q86 72 100 86 T128 84" fill="none" stroke="#b8791f" stroke-width="5" stroke-linecap="round"/>' +
    '<ellipse cx="86" cy="52" rx="8" ry="4" fill="#7a9a4a" stroke="#3b2314" stroke-width="2"/>' +
    '<ellipse cx="122" cy="48" rx="8" ry="4" fill="#7a9a4a" stroke="#3b2314" stroke-width="2"/>' +
    '</svg>',

  esTeh:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<line x1="114" y1="14" x2="104" y2="72" stroke="#3b2314" stroke-width="9" stroke-linecap="round"/>' +
    '<line x1="114" y1="14" x2="104" y2="72" stroke="#b85d19" stroke-width="5" stroke-linecap="round"/>' +
    '<path d="M70 28 L130 28 L122 104 Q121 110 115 110 L85 110 Q79 110 78 104Z" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M73.5 46 L126.5 46 L121 102 Q120 106 115 106 L85 106 Q80 106 79 102Z" fill="#c47a2c"/>' +
    '<rect x="82" y="54" width="17" height="17" rx="3" fill="#fff" fill-opacity="0.6" stroke="#fff" stroke-width="2"/>' +
    '<rect x="104" y="70" width="15" height="15" rx="3" fill="#fff" fill-opacity="0.6" stroke="#fff" stroke-width="2"/>' +
    '</svg>',

  esJeruk:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<path d="M70 28 L130 28 L122 104 Q121 110 115 110 L85 110 Q79 110 78 104Z" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M73.5 46 L126.5 46 L121 102 Q120 106 115 106 L85 106 Q80 106 79 102Z" fill="#f08a24"/>' +
    '<rect x="82" y="56" width="17" height="17" rx="3" fill="#fff" fill-opacity="0.6" stroke="#fff" stroke-width="2"/>' +
    '<rect x="104" y="72" width="15" height="15" rx="3" fill="#fff" fill-opacity="0.6" stroke="#fff" stroke-width="2"/>' +
    '<circle cx="132" cy="32" r="17" fill="#f5a623" stroke="#3b2314" stroke-width="3"/>' +
    '<circle cx="132" cy="32" r="11" fill="#fbd27a"/>' +
    '<line x1="132" y1="21" x2="132" y2="43" stroke="#f5a623" stroke-width="2"/>' +
    '<line x1="121" y1="32" x2="143" y2="32" stroke="#f5a623" stroke-width="2"/>' +
    '</svg>',

  kopiTubruk:
    '<svg viewBox="0 0 200 120" aria-hidden="true">' +
    '<path d="M86 40 Q78 30 86 20" fill="none" stroke="#6b4a35" stroke-width="3" stroke-linecap="round"/>' +
    '<path d="M100 38 Q92 28 100 16" fill="none" stroke="#6b4a35" stroke-width="3" stroke-linecap="round"/>' +
    '<path d="M114 40 Q106 30 114 20" fill="none" stroke="#6b4a35" stroke-width="3" stroke-linecap="round"/>' +
    '<ellipse cx="100" cy="100" rx="68" ry="11" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<path d="M138 62 Q164 60 162 78 Q160 92 134 88" fill="none" stroke="#3b2314" stroke-width="9" stroke-linecap="round"/>' +
    '<path d="M138 62 Q164 60 162 78 Q160 92 134 88" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>' +
    '<path d="M60 54 H140 V72 Q140 98 100 98 Q60 98 60 72Z" fill="#fff" stroke="#3b2314" stroke-width="3"/>' +
    '<ellipse cx="100" cy="54" rx="40" ry="7" fill="#3b2314"/>' +
    '</svg>'
};

const areaMenu = document.getElementById("daftar-menu");
const tombolFilter = document.querySelectorAll(".tombol-filter");

// Mengubah angka menjadi format rupiah bertitik, misalnya 18000 menjadi "Rp18.000".
function formatRupiah(angka) {
  const bertitik = String(angka).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return "Rp" + bertitik;
}

// Membuat satu kartu menu (elemen HTML) dari satu objek menu.
function buatKartuMenu(item) {
  const kartu = document.createElement("article");
  kartu.className = "kartu-menu";

  // Bagian atas kartu: ilustrasi SVG. Isinya teks buatan sendiri di atas, bukan input pengguna.
  const gambar = document.createElement("div");
  gambar.className = "gambar-menu gambar-" + item.kategori;
  gambar.innerHTML = gambarSvg[item.ilustrasi] || "";

  // Bagian bawah kartu: nama, garis titik penghubung, harga, lalu deskripsi.
  const isi = document.createElement("div");
  isi.className = "isi-kartu";

  const barisNama = document.createElement("div");
  barisNama.className = "baris-nama";

  const nama = document.createElement("h3");
  nama.textContent = item.nama;

  const titik = document.createElement("span");
  titik.className = "titik";
  titik.setAttribute("aria-hidden", "true");

  const harga = document.createElement("p");
  harga.className = "harga";
  harga.textContent = formatRupiah(item.harga);

  const deskripsi = document.createElement("p");
  deskripsi.className = "deskripsi";
  deskripsi.textContent = item.deskripsi;

  barisNama.append(nama, titik, harga);
  isi.append(barisNama, deskripsi);
  kartu.append(gambar, isi);
  return kartu;
}

// Menampilkan menu sesuai kategori ("semua", "makanan", atau "minuman").
function tampilkanMenu(kategori) {
  areaMenu.innerHTML = "";

  // Bila kategori bukan "semua", ambil hanya item dengan kategori yang cocok.
  const menuTerpilih = dataMenu.filter(function (item) {
    return kategori === "semua" || item.kategori === kategori;
  });

  // Bila tidak ada item sama sekali, tampilkan pesan pengganti.
  if (menuTerpilih.length === 0) {
    const pesan = document.createElement("p");
    pesan.className = "pesan-kosong";
    pesan.textContent = "Menu belum tersedia";
    areaMenu.appendChild(pesan);
    return;
  }

  menuTerpilih.forEach(function (item) {
    areaMenu.appendChild(buatKartuMenu(item));
  });
}

// Memindahkan penanda "aktif" ke tombol yang diklik, lalu menampilkan menunya.
function pilihFilter(tombol) {
  tombolFilter.forEach(function (t) {
    t.classList.remove("aktif");
    t.setAttribute("aria-pressed", "false");
  });
  tombol.classList.add("aktif");
  tombol.setAttribute("aria-pressed", "true");
  tampilkanMenu(tombol.dataset.kategori);
}

// Pasang aksi klik pada tiga tombol filter.
tombolFilter.forEach(function (tombol) {
  tombol.addEventListener("click", function () {
    pilihFilter(tombol);
  });
});

// Saat halaman pertama dibuka, tampilkan semua menu.
tampilkanMenu("semua");
