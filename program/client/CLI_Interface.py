import time
from client.user import User
from server.item import Item
from server.admin import Admin
from server.order import Order, Status

class CLI_Interface:
    """
    Antarmuka antara sisi klien dan sisi server dalam bentuk CLI (Command Line Interface).
    """
    admin = Admin("admin", "admin")
    def __init__(self):
        pass

    def print_dl(self, text: str, **kwargs):
        """Mencetak baris dengan jeda waktu tertentu."""
        print(text, **kwargs)
        time.sleep(0.5)

    def print_dc(self, text: str, **kwargs):
        """Mencetak karakter dengan jeda waktu tertentu."""
        for char in text:
            print(char, end="")
            time.sleep(0.005)
        print(**kwargs)

    def header_halaman(self, pesan: str):
        """Membuat header pada halalamn"""
        self.print_dc("\n" + f"#{'=' * 100}#")
        self.print_dc(f"{pesan.center(100, "-")}")
        self.print_dc(f"#{'=' * 100}#" + "\n")

    def valid(self):
        """Validasi masukan berupa Pertanyaan Ya/Tidak"""
        while True:
            masukan =input("(Y/T) > ")
            if masukan == "Y" or masukan == "y":
                return True
            elif masukan == "T" or masukan == "t":
                return False
            else:
                self.print_dl("Masukan tidak dikenal.\n")

    def keluar(self):
        """Konfirmasi untuk keluar Program"""
        self.header_halaman("KELUAR")
        self.print_dl("Apakah Anda yakin ingin keluar dari aplikasi?", end = " ")
        if self.valid():
            exit()
        return
    
    def selamat_datang(self):
        self.print_dc(" ")
        self.print_dc("~"*100)
        self.print_dc("PANDA MANIS".center(100))
        self.print_dc("kaPAN DApat MAkanan gratISnya?".center(100))
        self.print_dc("~"*100)

        self.halaman_utama()

    def halaman_utama(self):
        """Halaman utama dan pertama ketika memulai program"""
        while True:
            self.header_halaman("HALAMAN UTAMA")
            self.print_dc(f"Pilih peran:")
            self.print_dc("1. Koki")
            self.print_dc("2. Pengguna")
            self.print_dc("X. Keluar")
            peran = input("> ")
            if peran == "1":
                self.masuk_koki()
            elif peran == "2":
                self.portal_pengguna()
            elif peran == "X" or peran == "x":
                self.keluar()
            else:
                self.print_dl("Masukan tidak dikenal.\n")
    
    def masuk_koki(self):
        """Portal masuk bagi koki."""
        self.header_halaman("MASUK: KOKI")
        while True:
            username = input("Username: > ")
            password = input("Password: > ")
            if CLI_Interface.admin.login(username, password):
                self.beranda_koki()
                break
            else:
                self.print_dl("Login gagal. Coba lagi?", end = " ")
                if not self.valid():
                    return

    def beranda_koki(self):
        """"Halaman beranda bagi koki"""
        self.header_halaman("BERANDA KOKI")
        while True:
            self.print_dc("A. Lihat Antrean")
            self.print_dc("B. Proses Pesanan")
            self.print_dc("C. Riwayat Pesanan")
            self.print_dc("X. Logout")
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.header_halaman("ANTREAN PESANAN")
                CLI_Interface.admin.lihat_antrean()
            elif pilihan == "B"or pilihan == "b":
                self.header_halaman("PROSES PESANAN")
                self.print_dc("Anda akan memproses pesanan terdepan. Lanjutkan?", end = " ")
                if self.valid():
                    CLI_Interface.admin.proses_order()
            elif pilihan == "C"or pilihan == "c":
                self.header_halaman("RIWAYAT PESANAN")
                if not Order.riwayat:
                    self.print_dl("Antrean kosong\n")
                else:
                    for order in Order.riwayat.values():
                        self.print_dl(order)
            elif pilihan == "X" or pilihan == "x":
                self.print_dc("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    self.admin.logout()
                    break
            else:
                self.print_dl("Masukan tidak dikenal.\n")
    
    def portal_pengguna(self):
        """Memisahkan pengguna yang sudah/belum punya User ID"""
        self.header_halaman("PORTAL PENGGUNA")
        self.print_dc("Apakah Anda sudah memiliki User ID?", end = " ")
        if self.valid():
            self.masuk_pengguna()
        else:
            self.daftar_pengguna()
    
    def masuk_pengguna(self):
        """Portal login dengan User ID"""
        self.header_halaman("MASUK PENGGUNA")
        while True:
            user_id = input("Masukkan User ID: > ")
            user = User.daftar.get(user_id)
            if user:
                telp = input("Masukkan No. Telepon: > ")
                self.beranda_pengguna(user)
                break
            else:
                print("User ID tidak ditemukan. Coba lagi?", end = " ")
                if not self.valid():
                    break
            
    def daftar_pengguna(self):
        """Membuat user baru dan login otomatis"""
        self.header_halaman("DAFTAR PENGUNA BARU")
        self.print_dl("Masukkan nama dan nomor telepon Anda!")
        self.print_dc("Keterangan: masukkan nomor telelpon dengan diawali 62\nContoh: 628123456789\n")
        while True:
            nama = input("Nama: > ").strip()
            if not nama.replace(" ", "").isalpha():
                self.print_dl("Nama hanya boleh berisi huruf dan/atau spasi!\n")
                continue
            telp = input("No. Telepon: > ").strip()
            if not (telp.startswith("628") and telp[3:].isdigit() and 8 <= len(telp[3:]) <= 12):
                self.print_dl("Nomor telepon harus dalam format 628XXXXXXXXX!\n")
                continue
            self.print_dc("Apakah data yang dimasukkan di atas sudah benar?", end = " ")
            if self.valid():
                user = User(nama, telp)
                self.print_dl("User berhasil dibuat!")
                self.print_dl(f"User ID Anda adalah: {user.ID}")
                self.beranda_pengguna(user)
                break
            else:
                self.print_dl("Silakan masukkan data kembali.\n")

    def beranda_pengguna(self, user: User):
        """Halaman beranda bagi pengguna"""
        self.header_halaman("BERANDA PENGGUNA")
        self.print_dl(user)
        self.print_dc(f"Selamat datang, {user.nama}!\n")
        while True:
            self.print_dc("A. Buat Pesanan Baru")
            self.print_dc("B. Lihat Daftar Pesanan")
            self.print_dc("X. Logout")
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.buat_pesanan(user)
            elif pilihan == "B"or pilihan == "b":
                self.pesanan_pengguna(user)
            elif pilihan == "X" or pilihan == "x":
                self.print_dc("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    break
            else:
                self.print_dl("Masukan tidak dikenal.")
                    
    def buat_pesanan(self, user: User):
        """Antarmuka membuat pesanann baru"""
        self.header_halaman("BUAT PESANAN BARU")
        while True:
            try: 
                meja = int(input("Masukkan Nomor Meja: "))
                self.print_dl("Apakah nomor meja sudah benar?", end = " ")
                if self.valid():
                    break
            except:
                self.print_dl("Masukan tidak valid.")
                continue
        order = Order(meja, user.ID)
        self.print_dc(f"Pesanan untuk meja {meja} oleh User ID {user.ID} dibuat.")
        self.print_dc(Item.lihat_menu())
        self.print_dc("Masukkan ID menu yang ingin dipesan dan jumlahnya.")
        while True:
            try:
                item_id = input("\nID Menu: > ")
                item = Item.menu[int(item_id)-1]
                qty = int(input("Jumlah: > "))
                if not (qty > 0):
                    self.print_dl("Jumlah harus berupa bilangan positif")
                    continue
            except:
                self.print_dl("Masukan tidak valid.")
                continue
            self.print_dc(f"Anda memilih: {item} | {qty} porsi")
            self.print_dl("Konfirmasi Item?", end = " ")
            if self.valid():
                order.tambah_item(item, qty)
                self.print_dl("Item berhasil ditambahkan.")
                self.print_dl("Tambah item?", end = " ")
                if self.valid():
                    continue
                else:
                    break        
        self.print_dc(f"\n{"KONFIRMASI PESANAN":^67}")
        self.print_dl(order.cetak_struk())
        self.print_dc("Konfirmasi Pesanan?")
        self.print_dl("Pesanan yang telah dikonfirmasi tidak bisa dibatalkan dan akan dikenakan biaya total.")
        if self.valid():
            user.tambah_order(order)
            self.print_dl("Pesanan berhasil dikonfirmasi!")
        else:
            user.tambah_order(order)
            order.edit_status(Status.CANCELED)
            Order.antrean.remove(order)
            self.print_dl("Pesanan dibatalkan.")
        self.print_dl("\nAnda kembali ke menu pengguna.")

    def pesanan_pengguna(self, user: User):
        """Antarmuka daftar pesanan pengguna"""
        self.header_halaman("DAFTAR PESANAN PENGGUNA")
        self.print_dl(user.lihat_daftar())
        self.print_dc("Apakah Anda ingin melihat detail pesanan?", end = " ")
        if self.valid():
            while True:
                order_id = input("Masukkan ID Pesanan: ")
                order: Order = user.orders.get(order_id)
                if order:
                    self.print_dl(order.cetak_struk())
                    break
                else:
                    self.print_dc("Pesanan tidak ditemukan. Coba lagi?", end = " ")
                    if not self.valid():
                        break
        self.print_dl("\nAnda kembali ke menu pengguna.")
