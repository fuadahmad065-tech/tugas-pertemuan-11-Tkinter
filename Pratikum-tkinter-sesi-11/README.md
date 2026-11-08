# Aplikasi Pendaftaran Kegiatan Mahasiswa

Tugas Praktikum Python Tkinter - Sesi 11 (Advanced Widgets dan Event Handling)

## Tujuan
Membangun aplikasi GUI menggunakan Python Tkinter dengan memanfaatkan berbagai widget, event handling, validasi input, menu, dan dialog.

## Fitur Aplikasi
1. **Form Input:**
   - `Entry` untuk memasukkan nama.
   - `Combobox` (Readonly) untuk memilih program studi.
   - `Radiobutton` untuk memilih jenis kelamin.
   - `Checkbutton` untuk memilih kegiatan (bisa lebih dari satu).
   - `Text` untuk memasukkan alasan mengikuti kegiatan.
2. **Validasi Input:** Memastikan nama tidak kosong (minimal 3 karakter), prodi, gender, kegiatan, dan alasan sudah diisi sebelum disubmit.
3. **Event Handling:**
   - Tombol `Enter` pada keyboard untuk menjalankan fungsi Submit.
   - Shortcut `Ctrl+Q` untuk keluar dari aplikasi.
4. **Listbox:** Menampilkan daftar kegiatan yang dipilih secara *real-time* saat Checkbutton dicentang.
5. **Ringkasan:** Menampilkan hasil input (beserta waktu pendaftaran) pada area `ScrolledText` di sebelah kanan.
6. **Menu & Dialog:**
   - Menu File (Reset Form, Keluar).
   - Menu Bantuan (About).
   - Menggunakan `Messagebox` untuk notifikasi validasi, konfirmasi, dan sukses.
   - Menggunakan `Toplevel` untuk jendela About.

## Cara Menjalankan Aplikasi
1. Pastikan Python 3 sudah terinstal di komputer kamu.
2. Buka terminal atau Command Prompt (CMD), lalu arahkan ke folder proyek ini.
3. Jalankan perintah berikut:
   ```bash
   python main.py