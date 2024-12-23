import os        # Import modul os untuk mengakses path logo
import ctypes    # Import modul ctypes untuk mengatur DPI agar GUI lebih jelas
import tkinter as tk # Import modul tkinter sebagai tk untuk membuat GUI
from tkinter import messagebox, font, ttk # Untuk menampilkan pesan error atau informasi dan mengubah font dan ukuran font
from PIL import Image, ImageTk # Import modul Image dan ImageTk dari PIL untuk menampilkan gambar
from client.admin_interface import admin_interface # Import class admin_interface dari file admin_interface.py
from server.user import User # Import class User dari file user.py
from server.item import Item # Import class Item dari file item.py
from server.order import Order, Status # Import class Order dan Enum Status dari file order.py

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Meningkatkan kualitas tampilan GUI pada layar dengan DPI tinggi
except Exception:
    pass

class user_interface:
    """
    Class user_interface berfungsi untuk membuat antarmuka pengguna yang dapat melakukan pemesanan makanan.

    Attribut Global:
    - `font_family: str` -> Nama font yang digunakan pada antarmuka.
    - `fsize_t: int` -> Ukuran font untuk judul.
    - `fsize_h1: int` -> Ukuran font untuk header 1.
    - `fsize_h2: int` -> Ukuran font untuk header 2.
    - `fsize_h3: int` -> Ukuran font untuk header 3.
    - `fsize_n: int` -> Ukuran font untuk teks biasa.
    - `current_dir: str` -> Path direktori saat ini.
    - `image_path: str` -> Path logo aplikasi.

    Atribut Lokal:
    - `admin: admin_interface` -> Class admin_interface untuk mengakses data dari admin.
    - `win_id: int` -> ID jendela.
    - `user_window: tk.Tk` -> Jendela utama aplikasi.

    Argumen inisialisasi: `user_interface(root: tk.Tk, admin: admin_interface, id: int) -> None`

    Metode:
    - `mulai_hal() -> None` -> Funsgi pembantu untuk menginisiasi pembuatan halaman.
    - `tutup_hal() -> None` -> Fungs pembantu untuk menutup jendela.
    - `buat_frame() -> tk.Frame` -> Fungsi pembantu untuk menginisiasi grid pada halaman.
    - `hal_utama() -> None` -> Membuat antarmuka utama untuk memilih sebagai pengguna atau koki.
    - `hal_daftar_pengguna() -> None` -> Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan.
    - `hal_masuk_pengguna() -> None` -> Membuat antarmuka untuk pengguna yang sudah ada untuk login.
    - `buat_user_baru() -> None` -> Membuat order baru berdasarkan input dari pengguna.
    - `masuk_user() -> None` -> Fungsi untuk login pengguna yang sudah ada.
    - `hal_beranda_user(user: User) -> None` -> Membuat antarmuka beranda setelah login pengguna.
    - `keluar_user() -> None` -> Keluar sebagai user.
    - `hal_lihat_pesanan(user: User, order: Order) -> None` -> Membuat antarmuka untuk melihat detail pesanan.
    - `hal_buat_pesanan_baru(user: User) -> None` -> Membuat antarmuka untuk membuat pesanan baru.
    - `hal_konfirmasi_pesanan(user: User) -> None` -> Membuat antarmuka untuk konfirmasi pesanan yang akan dibuat.
    - `buat_pesanan(user: User, meja: int, masukan_item_qty: dict) -> None` -> Membuat pesanan baru berdasarkan input dari pengguna.
    - `hal_edit_pesanan(user: User, order: Order) -> None` -> Membuat antarmuka untuk mengedit pesanan yang sudah ada jika statusnya benar.
    - `hal_konfirmasi_edit(user: User, order: Order) -> None` -> Mengonfirmasi pesanan yang akan diubah.
    - `batalkan_pesanan(user: User, order: Order) -> None` -> Membatalkan pesanan yang sedang dilihat.
    """

    # Set font default
    font_family = "Segoe UI"
    fsize_t = 18
    fsize_h1 = 14
    fsize_h2 = 12
    fsize_h3 = 10
    fsize_n = 8

    # Path Logo 
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "new_logo.png")

    def __init__(self, root: tk.Tk, admin: admin_interface, id: int):
        # Inisialisasi jendela
        self.admin = admin
        self.win_id = id
        self.user_window: tk.Tk = tk.Toplevel(root)
        self.user_window.title("Sistem Pemesanan Makanan - User")
        
        # Set font default
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.font_family, size=self.fsize_n)
        
        # Set ukuran jendela
        self.user_window.geometry(f"{admin.window_width}x{admin.window_height}")
        self.user_window.resizable(True, True)

        # Jalankan program
        self.hal_utama()
        self.user_window.protocol("WM_DELETE_WINDOW", self.tutup_hal)

    def mulai_hal(self):
        """Fungsi pembantu untuk menginisiasi pembuatan halaman"""
        # Membersihkan isi jendela sembelum mengisinya dengan widget baru
        for widget in self.user_window.winfo_children():
            widget.destroy()
    
    def tutup_hal(self):
        """Fungsi pembantu untuk menutup jendela"""
        self.admin.tutup_hal_user(self.win_id)
        self.user_window.destroy()

    def buat_frame(self) -> tk.Frame:
        """Fungsi pembantu untuk menginisiasi grid pada halaman"""
        # Persiapan membuat tata letak grid
        self.user_window.grid_rowconfigure(0, weight=1)
        self.user_window.grid_columnconfigure(0, weight=1)
        
        # Frame untuk menampilkan dashboard
        frame = tk.Frame(self.user_window)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return frame
        
    def hal_utama(self):
        """Membuat antarmuka utama untuk memilih sebagai pengguna atau koki"""
        self.mulai_hal()
        
        # Label Judul
        tk.Label(self.user_window, text="PANDA MANIS", font=(self.font_family, self.fsize_t)).pack(pady=(20, 0))
        tk.Label(self.user_window, text="kaPAN DApat MAkaNan gratISnya?", font=(self.font_family, self.fsize_h1)).pack(pady=5)

        try:
            # Tampilkan Gambar
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((150, 150), Image.LANCZOS) 
            self.image = ImageTk.PhotoImage(self.image)
            label_image = tk.Label(self.user_window, image=self.image)
            label_image.pack(pady=10)
        except FileNotFoundError:
            # Jika gambar tidak ditemukan
            pass

        # Label Info
        tk.Label(self.user_window, text="Projek II Kelompok 5", font=(self.font_family, self.fsize_h2)).pack(pady=(10, 5))
        tk.Label(self.user_window, text="Berpikir Komputasional - WI1102 Kelas 31", font=(self.font_family, self.fsize_h2)).pack(pady=5)
        tk.Label(self.user_window, text="Sistem Pemesanan Makanan", font=(self.font_family, self.fsize_h2)).pack(pady=(5, 10))
        tk.Label(self.user_window, text="Selamat Datang!", font=(self.font_family, self.fsize_t)).pack(pady=20)

        # Tombol Daftar Pengguna Baru
        self.tombol_daftar = tk.Button(self.user_window, text="Pengguna Baru", width=15, height=2, command=self.hal_daftar_pengguna)
        self.tombol_daftar.pack(pady=10)
        
        # Tombol Masuk bagi Pengguna Lama        
        self.tombol_masuk = tk.Button(self.user_window, text="Login Pengguna", width=15, height=2, command=self.hal_masuk_pengguna)
        self.tombol_masuk.pack(pady=10)

        # Tombol Keluar
        self.tombol_keluar = tk.Button(self.user_window, text="Keluar", width=15, height=2, command=self.tutup_hal)
        self.tombol_keluar.pack(pady=10)

    def hal_daftar_pengguna(self):
        """Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan"""
        self.mulai_hal()
        
        # Label Judul
        self.header = tk.Label(self.user_window, text="Daftar Pengguna Baru", font=(self.font_family, self.fsize_h1))
        self.header.pack(pady=20)

        # Kontainer masukan nama
        tk.Label(self.user_window, text="Nama: ").pack(pady=5)
        self.masukan_nama = tk.Entry(self.user_window)
        self.masukan_nama.pack(pady=10)

        # Kontainer masukan telepon
        tk.Label(self.user_window, text="Nomor Telepon: \nFormat: 628XXXXXXXX...").pack(pady=5)
        self.masukan_telp = tk.Entry(self.user_window)
        self.masukan_telp.pack(pady=10)

        # Tombol kirim
        tombol_kirim = tk.Button(self.user_window, text="Kirim", width=15, height=2, command=self.buat_user_baru)
        tombol_kirim.pack(pady=10)

        # Tombol kembali
        tombol_kembali = tk.Button(self.user_window, text="Kembali", width=15, height=2, command=self.hal_utama)
        tombol_kembali.pack(pady=10)

    def hal_masuk_pengguna(self):
        """Membuat antarmuka untuk pengguna yang sudah ada untuk login"""
        self.mulai_hal()
        
        # Label Judul
        self.header = tk.Label(self.user_window, text="Login Pengguna", font=(self.font_family, self.fsize_h1))
        self.header.pack(pady=20)

        # Kontainer masukan User ID
        tk.Label(self.user_window, text="Masukkan User ID: ").pack(pady=5)
        self.masukan_userID = tk.Entry(self.user_window)
        self.masukan_userID.pack(pady=10)

        # Kontainer masukan Telepon
        tk.Label(self.user_window, text="Masukkan Nomor Telepon: ").pack(pady=5)
        self.masukan_telp_ = tk.Entry(self.user_window)
        self.masukan_telp_.pack(pady=10)

        # Tombol Masuk
        tombol_masuk = tk.Button(self.user_window, text="Masuk", width=15, height=2, command=self.masuk_user)
        tombol_masuk.pack(pady=10)

        # Tombol Kembali
        tombol_kembali = tk.Button(self.user_window, text="Kembali", width=15, height=2, command=self.hal_utama)
        tombol_kembali.pack(pady=10)

    def buat_user_baru(self):
        """Membuat order baru berdasarkan input dari pengguna"""
        nama = self.masukan_nama.get().strip()
        telp = self.masukan_telp.get().strip()

        # Validasi Nama
        if not (nama.replace(" ", "").isalpha()):
            messagebox.showwarning("Input Error", "Nama hanya boleh mengandung huruf dan spasi!")
            return
        
        # Validasi Nomor Telepon
        if not (telp.startswith("628") and telp[3:].isdigit() and 8 <= len(telp[3:]) <= 12):
            messagebox.showwarning("Input Error", "Nomor telepon harus dalam format 628XXXXXXXXX!")
            return
        
        # Buat user baru
        user = User(nama, telp)
        messagebox.showinfo("Berhasil", f"User berhasil dibuat dengan ID: {user.ID}\n Ingat ID Anda untuk masuk selanjutnya.")
        self.hal_beranda_user(user)

    def masuk_user(self):
        """Fungsi untuk login pengguna yang sudah ada"""
        userID = self.masukan_userID.get().strip()
        telp = self.masukan_telp_.get().strip()

        # Validasi input
        if not (userID and telp):
            messagebox.showwarning("Input Error", "Semua bidang harus diisi!")
            return
        
        # Login
        if User.login(userID, telp):
            user = User.daftar[userID]
            self.hal_beranda_user(user)
        else:
            return

    def hal_beranda_user(self, user: User):
        """Membuat antarmuka beranda setelah login pengguna."""
        self.mulai_hal()
        frame_dashboard = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_dashboard, text=f"Halo, {user.nama}!", font=(self.font_family, self.fsize_h1), anchor='center').grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')
        
        # Label Detail Pengguna
        tk.Label(frame_dashboard, text=f"{user}", font=(self.font_family, self.fsize_n), anchor="w", justify="left").grid(row=1, column=0, columnspan=4, padx=20, pady=2, sticky='nsew')
        
        # Bagian Riwayat Pesanan
        tk.Label(frame_dashboard, text="Riwayat Pesanan", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=2, column=0, columnspan=4, pady=5, sticky='nsew')
        
        # Frame untuk menampilkan riwayat pesanan
        frame_order_history = tk.Frame(frame_dashboard, width=600)
        frame_order_history.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_order_history.grid_columnconfigure(0, weight=1)
        
        if user.orders:
            # Membuat header tabel riwayat pesanan
            tk.Label(frame_order_history, text="Order ID", font=(self.font_family, 12)).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Meja", font=(self.font_family, 12)).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Status", font=(self.font_family, 12)).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Total", font=(self.font_family, 12)).grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Lihat Pesanan", font=(self.font_family, 12)).grid(row=0, column=4, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(user.orders.values(), start=1):
                order: Order
                tk.Label(frame_order_history, text=f"{order.ID}").grid(row=idx, column=0, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.meja}").grid(row=idx, column=1, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.status.value}").grid(row=idx, column=2, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"Rp {order.cek_total():,.2f}").grid(row=idx, column=3, padx=5, sticky='nsew')
                tk.Button(frame_order_history, text="Lihat", command=lambda o=order: self.hal_lihat_pesanan(user, o)).grid(row=idx, column=4, padx=5, pady=2, sticky='nsew')
        else:
            # Jika belum ada riwayat pesanan
            tk.Label(frame_order_history, text="Belum ada riwayat pesanan.").grid(row=0, column=0, columnspan=4, pady=5)
        
        # Tombol refresh
        tk.Button(frame_dashboard, text="Refresh", command=lambda: self.hal_beranda_user(user)).grid(row=4, column=0, columnspan=1, pady=10)
        
        # Tombol untuk membuat pesanan baru
        tk.Button(frame_dashboard, text="Buat Pesanan Baru", command=lambda: self.hal_buat_pesanan_baru(user)).grid(row=4, column=1, columnspan=1, pady=10)
        
        # Tombol Keluar
        tk.Button(frame_dashboard, text="Keluar", command=self.hal_utama).grid(row=len(user.orders) + 5, column=0, columnspan=2, pady=10)

    def keluar_user(self):
        """Keluar sebagai user."""
        if messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
            self.hal_utama()
        else:
            return

    def hal_lihat_pesanan(self, user: User, order: Order):
        """Membuat antarmuka untuk melihat detail pesanan."""
        self.mulai_hal()
        frame_detail = self.buat_frame()

        # Label Detail Pesanan
        tk.Label(frame_detail, text="Detail Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        tk.Label(frame_detail, text=f"{user}", font=(self.font_family, self.fsize_n), anchor="e", justify="left").grid(row=1, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"{order}", font=(self.font_family, self.fsize_n), anchor="e", justify="left").grid(row=2, column=0, sticky='w', padx=10, pady=2)

        # Frame untuk menampilkan Detail Item
        frame_item = tk.Frame(frame_detail, width=800)
        frame_item.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_item.grid_columnconfigure(0, weight=1)
        
        # Label Detail Item
        tk.Label(frame_item, text="Detail Item", font=(self.font_family, self.fsize_h2)).grid(row=0, column=0, columnspan=6, pady=10, sticky='nsew')
        tk.Label(frame_item, text="No.", font=(self.font_family, self.fsize_n)).grid(row=1, column=0, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="ID", font=(self.font_family, self.fsize_n)).grid(row=1, column=1, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Item", font=(self.font_family, self.fsize_n)).grid(row=1, column=2, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Qty", font=(self.font_family, self.fsize_n)).grid(row=1, column=3, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Harga", font=(self.font_family, self.fsize_n)).grid(row=1, column=4, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Subtotal", font=(self.font_family, self.fsize_n)).grid(row=1, column=5, pady=5, sticky='nsew', padx=10)

        # Menampilkan detail item
        for idx, (item, qty) in enumerate(order.items.items(), start=1):
            item: Item
            subtotal = item.harga * qty
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Total Harga: Rp {order.cek_total():,.2f}", font=(self.font_family, self.fsize_n)).grid(row=4, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol mengedit pesanan
        tk.Button(frame_detail, text="Edit Pesanan", command=lambda: self.hal_edit_pesanan(user, order)).grid(row=5, column=0, columnspan=1, pady=5, sticky='n')

        # Tombol untuk membatalkan pesanan
        tk.Button(frame_detail, text="Batalkan Pesanan", command=lambda: self.batalkan_pesanan(user, order)).grid(row=5, column=1, columnspan=1, pady=5, sticky='n')

        # Tombol refresh
        tk.Button(frame_detail, text="Refresh", command=lambda: self.hal_lihat_pesanan(user, order)).grid(row=6, column=0, columnspan=1, pady=5, sticky='n')

        # Tombol untuk kembali
        tk.Button(frame_detail, text="Kembali", command=lambda: self.hal_beranda_user(user)).grid(row=6, column=1, columnspan=1, pady=5, sticky='n')

    def hal_buat_pesanan_baru(self, user: User):
        """Membuat antarmuka untuk membuat pesanan baru."""
        self.mulai_hal()
        frame_pesanan = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_pesanan, text=f"Buat Pesanan Baru", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

        # Kontainer Nomor Meja
        tk.Label(frame_pesanan, text="Nomor Meja: ").grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')
        self.masukan_meja = tk.Entry(frame_pesanan)
        self.masukan_meja.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')

        # Frame kontainer
        tk.Label(frame_pesanan, text="Daftar Menu", font=(self.font_family, self.fsize_h2)).grid(row=3, column=0, columnspan=2, pady=10, sticky='nsew')
        frame_canvas = tk.Frame(frame_pesanan, width=600)
        frame_canvas.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_canvas.grid_columnconfigure(0, weight=1)

        # Scrollbar untuk daftar menu
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame untuk menampilkan daftar menu
        frame_menu = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_menu, anchor='nw')
        frame_menu.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_menu.grid_columnconfigure(0, weight=1)

        # Header Tabel Menu
        tk.Label(frame_menu, text="ID").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Item").grid(row=0, column=1, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Harga").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Qty").grid(row=0, column=3, sticky='w', padx=5, pady=2)

        # Menampilkan daftar menu dan menerima input jumlah pesanan
        self.masukan_qty = {}
        for item_id, item in Item.menu.items():
            item: Item
            tk.Label(frame_menu, text=f"#{item.ID}").grid(row=item_id, column=0, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=item.nama).grid(row=item_id, column=1, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=f"Rp {item.harga:,.2f}").grid(row=item_id, column=2, sticky='w', padx=5, pady=2)
            qty = tk.Entry(frame_menu, width=5)
            qty.grid(row=item_id, column=3, padx=5, pady=2)
            self.masukan_qty[item] = qty
        
        # Tombol untuk konfirmasi pesanan
        tk.Button(frame_pesanan, text="Konfirmasi Pesanan", command=lambda: self.hal_konfirmasi_pesanan(user)).grid(row=5, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol untuk kembali
        tk.Button(frame_pesanan, text="Kembali", command=lambda: self.hal_beranda_user(user)).grid(row=6, column=0, columnspan=2, pady=5, sticky='n')

    def hal_konfirmasi_pesanan(self, user: User):
        """Membuat antarmuka untuk konfirmasi pesanan yang akan dibuat."""
        meja = self.masukan_meja.get()

        # Validasi Nomor Meja
        if not (meja.isdigit() and 0 <= int(meja) <= 99):
            messagebox.showwarning("Input Error", "Nomor meja harus berupa angka antara 0 hingga 99!")
            return
        meja = int(meja)

        # Validasi Jumlah Item
        daftar_qty = {}
        for item, entry in self.masukan_qty.items():
            entry: tk.Entry
            qty = entry.get()
            if qty.isdigit() and int(qty) > 0:
                daftar_qty[item] = int(qty)

        
        # Validasi Jumlah Item
        if not daftar_qty:
            messagebox.showwarning("Input Error", "Silakan masukkan jumlah untuk setidaknya satu item!")
            return
        
        self.mulai_hal()
        frame_konfirmasi = self.buat_frame()

        # Label Detail Pesanan
        tk.Label(frame_konfirmasi, text="Detail Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        tk.Label(frame_konfirmasi, text=f"{user}", font=(self.font_family, self.fsize_n), anchor="e", justify="left").grid(row=1, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Nomor Meja: {meja}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=4, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Status: {Status.PENDING.value}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=5, column=0, sticky='w', padx=10, pady=2)

        # Frame untuk menampilkan Detail Item
        frame_item = tk.Frame(frame_konfirmasi, width=800)
        frame_item.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_item.grid_columnconfigure(0, weight=1)
        
        # Label Detail Item
        tk.Label(frame_item, text="Detail Item", font=(self.font_family, self.fsize_h2)).grid(row=0, column=0, columnspan=6, pady=10, sticky='nsew')
        tk.Label(frame_item, text="No.", font=(self.font_family, self.fsize_n)).grid(row=1, column=0, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="ID", font=(self.font_family, self.fsize_n)).grid(row=1, column=1, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Item", font=(self.font_family, self.fsize_n)).grid(row=1, column=2, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Qty", font=(self.font_family, self.fsize_n)).grid(row=1, column=3, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Harga", font=(self.font_family, self.fsize_n)).grid(row=1, column=4, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Subtotal", font=(self.font_family, self.fsize_n)).grid(row=1, column=5, pady=5, sticky='nsew', padx=10)

        # Menampilkan detail item
        total_harga = 0
        for idx, (item, qty) in enumerate(daftar_qty.items(), start=1):
            item: Item
            subtotal = item.harga * qty
            total_harga += subtotal
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Total Harga: Rp {total_harga:,.2f}", font=(self.font_family, self.fsize_n+2)).grid(row=7, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol untuk membuat pesanan
        tk.Button(frame_konfirmasi, text="Buat Pesanan", command=lambda: self.buat_pesanan(user, meja, daftar_qty)).grid(row=8, column=0, pady=5, sticky='n', columnspan=2)

        # Tombol untuk kembali
        tk.Button(frame_konfirmasi, text="Batalkan", command=lambda: self.hal_buat_pesanan_baru(user)).grid(row=9, column=0, pady=5, sticky='n', columnspan=2)

    def buat_pesanan(self, user: User, meja: int, masukan_item_qty: dict):
        """Membuat pesanan baru berdasarkan input dari pengguna"""
        pesanan_baru = Order(meja, user.ID)
        for item, qty in masukan_item_qty.items():
            pesanan_baru.tambah_item(item, qty)
        user.tambah_order(pesanan_baru)
        messagebox.showinfo("Berhasil", f"Pesanan berhasil dibuat dengan ID: {pesanan_baru.ID}")
        self.hal_beranda_user(user)

    def hal_edit_pesanan(self, user: User, order: Order):
        """Membuat antarmuka untuk mengedit pesanan yang sudah ada jika statusnya benar."""
        
        # Memeriksa Status Pesanan
        if order.status != Status.CONFIRMED:
            messagebox.showwarning("Error", f"Tidak dapat mengedit pesanan. Status Pesanan: {order.status.value}")
            return
        
        # Inisialisasi Halaman
        self.mulai_hal()
        frame_edit = self.buat_frame()
        order.status = Status.PENDING        
        # Label Judul
        tk.Label(frame_edit, text="Edit Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

        # Kontainer Nomor Meja
        tk.Label(frame_edit, text="Nomor Meja: ").grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')
        self.editan_meja = tk.Entry(frame_edit)
        self.editan_meja.grid(row=2, column=1, pady=10, sticky='n')
        self.editan_meja.insert(0, str(order.meja))

        # Frame kontainer
        frame_canvas = tk.Frame(frame_edit, width=600)
        frame_canvas.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_canvas.grid_columnconfigure(0, weight=1)

        # Scrollbar untuk daftar menu
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame untuk menampilkan daftar menu
        frame_item = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_item, anchor='nw')
        frame_item.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_item.grid_columnconfigure(0, weight=1)

        # Header Tabel Menu
        tk.Label(frame_item, text="ID").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(frame_item, text="Item").grid(row=0, column=1, sticky='w', padx=5, pady=2)
        tk.Label(frame_item, text="Harga").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        tk.Label(frame_item, text="Qty").grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        # Menampilkan daftar menu dengan jumlah pesanan yang sudah diisi
        self.editan_qty = {}
        for item_id, item in Item.menu.items():
            item: Item
            tk.Label(frame_item, text=f"#{item.ID}").grid(row=item_id, column=0, sticky='w', padx=5, pady=2)
            tk.Label(frame_item, text=item.nama).grid(row=item_id, column=1, sticky='w', padx=5, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=item_id, column=2, sticky='w', padx=5, pady=2)
            entry_qty = tk.Entry(frame_item, width=5)
            entry_qty.insert(0, str(order.items.get(item, "")))
            entry_qty.grid(row=item_id, column=3, padx=5, pady=2)
            self.editan_qty[item] = entry_qty

        # Tombol Konfirmasi Edit
        tk.Button(frame_edit, text="Konfirmasi Edit", command=lambda: self.hal_konfirmasi_edit(user, order)).grid(row=4, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol Batalkan Pesanan
        tk.Button(frame_edit, text="Batalkan Pesanan", command=lambda: self.batalkan_pesanan(user, order)).grid(row=5, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol Kembali
        tk.Button(frame_edit, text="Batalkan Edit", command=lambda: self.batal_edit(user, order)).grid(row=6, column=0, columnspan=2, pady=10, sticky='n')

    def batal_edit(self, user: User, order: Order):
        """Membatalkan edit pesanan yang sedang dilakukan."""
        order.status = Status.CONFIRMED
        self.hal_lihat_pesanan(user, order)

    def hal_konfirmasi_edit(self, user: User, order: Order):
        """Mengonfirmasi pesanan yang akan diubah."""
        if not messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin mengubah pesanan?"):
            return

        # Validasi Nomor Meja
        meja = self.editan_meja.get()
        if not (meja.isdigit() and 0 <= int(meja) <= 99):
            messagebox.showwarning("Input Error", "Nomor meja harus berupa angka antara 0 hingga 99!")
            return
        meja = int(meja)

        # Mengumpulkan item yang dipesan
        masukan_item_qty = {}
        for item, entry in self.editan_qty.items():
            entry: tk.Entry
            qty = entry.get()
            if qty.isdigit() and int(qty) > 0:
                masukan_item_qty[item] = int(qty)
        
        # Validasi Jumlah Item
        if not masukan_item_qty:
            messagebox.showwarning("Input Error", "Silakan masukkan jumlah untuk setidaknya satu item!")
            return
                
        order.items.clear()
        for item, qty in masukan_item_qty.items():
            order.tambah_item(item, qty)

        order.meja = meja
        order.status = Status.CONFIRMED
        messagebox.showinfo("Berhasil", f"Pesanan berhasil diubah.")
        self.hal_lihat_pesanan(user, order)

    def batalkan_pesanan(self, user: User, order: Order):
        """Membatalkan pesanan yang sedang dilihat"""
        # Memeriksa Status Pesanan
        if order.status not in [Status.CONFIRMED, Status.PENDING]:
            messagebox.showerror("Error", f"Tidak dapat membatalkan pesanan. Status Pesanan: {order.status.value}")
            return
        if not messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin membatalkan pesanan?"):
            return
        
        # Membatalkan pesanan
        order.status = Status.CANCELED
        Order.antrean.remove(order)
        messagebox.showinfo("Info", "Pesanan dibatalkan. Pesanan tetap akan ada di riwayat namun tidak akan diproses.")
        self.hal_lihat_pesanan(user, order)
