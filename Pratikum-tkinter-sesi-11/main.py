"""
Aplikasi Pendaftaran Kegiatan Mahasiswa
Praktikum Tkinter - Sesi 11
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime # Tambahan untuk waktu daftar

class AplikasiPendaftaran:
    PRODI = [
        "Teknik Informatika",
        "Sistem Informasi",
        "Teknik Elektro",
        "Teknik Industri",
        "Manajemen",
        "Akuntansi",
        "Hukum",
    ]
    KEGIATAN = [
        "Seminar Teknologi",
        "Lomba Coding",
        "Workshop Desain",
        "Bakti Sosial",
        "Turnamen Olahraga",
        "Pelatihan Kepemimpinan",
    ]
    PLACEHOLDER_PRODI = "-- Pilih Program Studi --"

    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pendaftaran Kegiatan Mahasiswa")
        self.root.geometry("900x620")
        self.root.minsize(820, 560)

        # Variabel kontrol
        self.var_nama = tk.StringVar()
        self.var_prodi = tk.StringVar()
        self.var_gender = tk.StringVar(value="")
        self.var_kegiatan = {k: tk.BooleanVar(value=False) for k in self.KEGIATAN}

        self.buat_menu()
        self.buat_layout()

        # Event keyboard: Enter = Submit
        self.root.bind("<Return>", self.on_enter)
        self.entry_nama.focus_set()

    # ------------------------------------------------------------------ MENU
    def buat_menu(self):
        menubar = tk.Menu(self.root)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Reset Form", command=self.reset)
        menu_file.add_separator()
        menu_file.add_command(label="Keluar", command=self.keluar, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=menu_file)

        menu_bantuan = tk.Menu(menubar, tearoff=0)
        menu_bantuan.add_command(label="About", command=self.tampilkan_about)
        menubar.add_cascade(label="Bantuan", menu=menu_bantuan)

        self.root.config(menu=menubar)
        self.root.bind("<Control-q>", lambda e: self.keluar())

    # ---------------------------------------------------------------- LAYOUT
    def buat_layout(self):
        judul = ttk.Label(
            self.root,
            text="Pendaftaran Kegiatan Mahasiswa",
            font=("Segoe UI", 16, "bold"),
        )
        judul.pack(pady=(12, 4))

        container = ttk.Frame(self.root, padding=10)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # ---------- Frame kiri: form input
        frame_form = ttk.LabelFrame(container, text="Form Pendaftaran", padding=10)
        frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        frame_form.columnconfigure(1, weight=1)

        # Nama (Entry)
        ttk.Label(frame_form, text="Nama:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_nama = ttk.Entry(frame_form, textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, sticky="ew", pady=4)

        # Program studi (Combobox)
        ttk.Label(frame_form, text="Program Studi:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_prodi = ttk.Combobox(
            frame_form, textvariable=self.var_prodi, values=self.PRODI, state="readonly"
        )
        self.combo_prodi.grid(row=1, column=1, sticky="ew", pady=4)
        self.combo_prodi.set(self.PLACEHOLDER_PRODI)

        # Jenis kelamin (Radiobutton)
        ttk.Label(frame_form, text="Jenis Kelamin:").grid(row=2, column=0, sticky="w", pady=4)
        frame_gender = ttk.Frame(frame_form)
        frame_gender.grid(row=2, column=1, sticky="w", pady=4)
        ttk.Radiobutton(frame_gender, text="Laki-laki", variable=self.var_gender,
                        value="Laki-laki").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(frame_gender, text="Perempuan", variable=self.var_gender,
                        value="Perempuan").pack(side="left")

        # Kegiatan (Checkbutton)
        ttk.Label(frame_form, text="Kegiatan:").grid(row=3, column=0, sticky="nw", pady=4)
        frame_cek = ttk.Frame(frame_form)
        frame_cek.grid(row=3, column=1, sticky="w", pady=4)
        for k in self.KEGIATAN:
            ttk.Checkbutton(
                frame_cek, text=k, variable=self.var_kegiatan[k],
                command=self.perbarui_listbox,
            ).pack(anchor="w")

        # Alasan (Text)
        ttk.Label(frame_form, text="Alasan\nMengikuti:").grid(row=4, column=0, sticky="nw", pady=4)
        self.text_alasan = tk.Text(frame_form, height=5, width=30, wrap="word")
        self.text_alasan.grid(row=4, column=1, sticky="ew", pady=4)

        # Tombol Submit & Reset
        frame_tombol = ttk.Frame(frame_form)
        frame_tombol.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(frame_tombol, text="Submit", command=self.submit).pack(side="left", padx=6)
        ttk.Button(frame_tombol, text="Reset", command=self.reset).pack(side="left", padx=6)

        # ---------- Frame kanan: Listbox + ringkasan
        frame_kanan = ttk.Frame(container)
        frame_kanan.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        frame_kanan.columnconfigure(0, weight=1)
        frame_kanan.rowconfigure(1, weight=1)

        frame_list = ttk.LabelFrame(frame_kanan, text="Kegiatan yang Dipilih", padding=8)
        frame_list.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        frame_list.columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(frame_list, height=6)
        scroll = ttk.Scrollbar(frame_list, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scroll.set)
        self.listbox.grid(row=0, column=0, sticky="ew")
        scroll.grid(row=0, column=1, sticky="ns")

        frame_ringkas = ttk.LabelFrame(frame_kanan, text="Ringkasan Pendaftaran", padding=8)
        frame_ringkas.grid(row=1, column=0, sticky="nsew")
        frame_ringkas.columnconfigure(0, weight=1)
        frame_ringkas.rowconfigure(0, weight=1)

        self.text_ringkasan = ScrolledText(frame_ringkas, height=12, wrap="word", state="disabled")
        self.text_ringkasan.grid(row=0, column=0, sticky="nsew")

        self.perbarui_listbox()

    # ------------------------------------------------------------- FUNGSI
    def kegiatan_terpilih(self):
        return [k for k, v in self.var_kegiatan.items() if v.get()]

    def perbarui_listbox(self):
        """Tampilkan kegiatan yang dicentang pada Listbox."""
        self.listbox.delete(0, tk.END)
        terpilih = self.kegiatan_terpilih()
        if terpilih:
            for k in terpilih:
                self.listbox.insert(tk.END, k)
        else:
            self.listbox.insert(tk.END, "(belum ada kegiatan dipilih)")

    def tampilkan_ringkasan(self, teks):
        self.text_ringkasan.config(state="normal")
        self.text_ringkasan.delete("1.0", tk.END)
        self.text_ringkasan.insert(tk.END, teks)
        self.text_ringkasan.config(state="disabled")

    def on_enter(self, event=None):
        fokus = self.root.focus_get()
        # Jangan submit kalau fokus di Text atau Combobox
        if fokus in (self.text_alasan, self.combo_prodi):
            return
        self.submit()

    def submit(self):
        nama = self.var_nama.get().strip()
        prodi = self.var_prodi.get()
        gender = self.var_gender.get()
        kegiatan = self.kegiatan_terpilih()
        alasan = self.text_alasan.get("1.0", tk.END).strip()

        # Validasi
        if not nama:
            messagebox.showwarning("Validasi", "Nama tidak boleh kosong!")
            self.entry_nama.focus_set()
            return
        if len(nama) < 3:
            messagebox.showwarning("Validasi", "Nama minimal 3 karakter.")
            self.entry_nama.focus_set()
            return
        if prodi == self.PLACEHOLDER_PRODI or prodi not in self.PRODI:
            messagebox.showwarning("Validasi", "Silakan pilih program studi.")
            return
        if not gender:
            messagebox.showwarning("Validasi", "Silakan pilih jenis kelamin.")
            return
        if not kegiatan:
            messagebox.showwarning("Validasi", "Pilih minimal satu kegiatan.")
            return
        if not alasan:
            messagebox.showwarning("Validasi", "Alasan mengikuti kegiatan harus diisi.")
            self.text_alasan.focus_set()
            return

        # Konfirmasi sebelum simpan
        if not messagebox.askyesno("Konfirmasi", "Simpan data pendaftaran ini?"):
            return

        ringkasan = (
            "=== RINGKASAN PENDAFTARAN ===\n\n"
            f"Waktu Daftar   : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"Nama           : {nama}\n"
            f"Program Studi  : {prodi}\n"
            f"Jenis Kelamin  : {gender}\n"
            f"Kegiatan       :\n"
            + "".join(f"   {i}. {k}\n" for i, k in enumerate(kegiatan, 1))
            + f"\nAlasan         :\n{alasan}\n"
        )
        self.tampilkan_ringkasan(ringkasan)
        messagebox.showinfo("Sukses", f"Pendaftaran atas nama {nama} berhasil disimpan!")

    def reset(self):
        # Cek apakah ada isi di form
        ada_isi = (
            self.var_nama.get().strip()
            or self.var_prodi.get() not in ("", self.PLACEHOLDER_PRODI)
            or self.var_gender.get()
            or self.kegiatan_terpilih()
            or self.text_alasan.get("1.0", tk.END).strip()
        )
        
        # Minta konfirmasi jika form terisi
        if ada_isi and not messagebox.askyesno("Reset", "Yakin ingin mereset form?"):
            return
            
        self.var_nama.set("")
        self.combo_prodi.set(self.PLACEHOLDER_PRODI)
        self.var_gender.set("")
        for v in self.var_kegiatan.values():
            v.set(False)
        self.text_alasan.delete("1.0", tk.END)
        self.tampilkan_ringkasan("")
        self.perbarui_listbox()
        self.entry_nama.focus_set()

    def keluar(self):
        if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.root.destroy()

    def tampilkan_about(self):
        about = tk.Toplevel(self.root)
        about.title("About")
        about.geometry("340x200")
        about.resizable(False, False)
        about.transient(self.root)
        about.grab_set()

        ttk.Label(about, text="Aplikasi Pendaftaran\nKegiatan Mahasiswa",
                  font=("Segoe UI", 13, "bold"), justify="center").pack(pady=(18, 6))
        ttk.Label(about, text="Versi 1.0\nPraktikum Tkinter - Sesi 11",
                  justify="center").pack()
        ttk.Label(about, text="Dibuat oleh: Ahmadal\nTeknik Informatika\nUniversitas Hasyim Asy'ari Jombang",
                  justify="center").pack(pady=8)
        ttk.Button(about, text="Tutup", command=about.destroy).pack(pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    AplikasiPendaftaran(root)
    root.mainloop()