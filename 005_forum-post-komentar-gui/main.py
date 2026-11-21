"""Titik masuk utama aplikasi desktop GUI Forum Post dan Komentar."""

from forum import AplikasiForum


def jalankan():
    """Membuat jendela utama aplikasi GUI dan menjalankan loop acara CustomTkinter."""
    aplikasi = AplikasiForum()
    aplikasi.mainloop()


if __name__ == "__main__":
    jalankan()
