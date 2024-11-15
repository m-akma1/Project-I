"""
SISTEM PEMESANAN MAKANAN
PROJEK 1 MATA KULIAH WI1102 - BERPIKIR KOMPUTASIONAL
KELAS 31 - KELOMPOK 5:
1. 19624218 Tiara Clianta Andiwi
2. 19624235 Muhammad Akmal
3. 19624250 Ahmad Rinofaros Muchtar
4. 19624264 Muh. Hartawan Haidir
5. 19624284 Muthia Ariesta Anggraeni

(c) 2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.
"""

"""
DESKRIPSI
Program ini adalah simulasi dari sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: sisi server dan sisi klien yang disatukan dalam satu sisi antarmuka. 

Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap. Sisi antarmuka menyatukan kedua sisi agar dapat berjalan dalam satu logika yang selaras.
"""

"""
KAMUS
Sistem penjelasan kamus variabel dilakukan pada setiap definisi untuk memudahkan pembacaan daripada mendefinsikan semua fungsi dan variabel di sini lantaran banyaknya nama yang harus dilacak. 

Kami menerapkan penggunaan docstring untuk setiap definisi kelas agar mempermudak melacak kelas dan memanfaatkan integrasi pada kode editor seperti VS Code. Fungsi dan metode yang diberi komentar/docstring adalah fungsi yang dibuat oleh penulis program. Kami mengasumsikan pembaca program sudah mengetahui fungsi bawaan seperti `__init__` dan `__str__` sehingga tidak perlu menjelaskan lagi.

Sebisa mungkin, kami menerapkan typehinting pada setiap parameter sesuai syntax Python, diindikasikan dengan format (nama_variabel: tipe_variabel). Typehinting dilakukan agar Pylance (ekstensi Python di VS Code) dapat mengenali objek dan menyesuaikan metode yang terdapat padanya. Jika tidak ada typehinting, tipe data bisa disimpulkan dari komentar yang ada.

"""

# ALGORITMA

import enum     # Modul Enumerasi, digunakan untuk membuat alias untuk mempermudah pengkategorian status pesanan
import datetime # Modul Tanggal dan Waktu, digunakan untuk mendapatkan data waktu dari komputer dalam membuat ID
import time     # Modul waktu untuk menunda tiap output agar tampilan lebih cantik

class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga (Rp): `harga: int`

    Argumen initialisasi: `(nama: str, harga: int) -> Item`
    """
    counter = 0 # Jumlah item yang telah dibuat
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
    
    def __str__(self):
        return f"#{self.ID:02d} | {self.nama:<15} | Rp {self.harga:10,.2f}"

class Status(enum.Enum):
    """Enumerasi status pesanan."""
    PENDING = "Menunggu dikonfirmasi"
    CONFIRMED = "Dikonfirmasi, dalam antrean"
    IN_PROGRESS = "Dalam proses"
    READY = "Siap diambil"
    COMPLETED = "Selesai"


# Daftar Menu
Menu = [
    Item("Ayam Goreng", 10000),
    Item("Ayam Bakar", 12000),
    Item("Ayam Geprek", 15000),
    Item("Ayam Kremes", 12000),
    Item("Bakso Sapi", 10000),
    Item("Bakso Beranak", 12000),
    Item("Mie Ayam", 12000),
    Item("Mie Goreng", 12000),
    Item("Mie Rebus", 12000),
    Item("Mie Pangsit", 12000),
    Item("Soto Ayam", 15000),
    Item("Soto Betawi", 20000),
    Item("Soto Padang", 25000),
    Item("Sate Ayam", 15000),
    Item("Sate Kambing", 20000),
    Item("Sate Padang", 25000),
    Item("Nasi Putih", 5000),
    Item("Nasi Goreng", 15000),
    Item("Nasi Uduk", 12000),
    Item("Nasi Kuning", 12000),
    Item("Air Mineral", 3000),
    Item("Es Teh", 5000),
    Item("Es Jeruk", 6000),
    Item("Es Campur", 8000),
    Item("Jus Alpukat", 10000),
    Item("Jus Mangga", 10000),
    Item("Jus Jeruk", 10000),
]

# Fungsi terpisah untuk melihat daftar menu
def lihat_menu():
    """Menampilkan **langsung** daftar menu makanan dan minuman."""
    # Output adalah variabel string sebagai kontainer sementara hingga f-string selesai diprint
    output = "\n"
    output += f"^" * 38 + "\n"
    output += "{}\n".format("Menu Makanan dan Minuman".center(38, "-"))
    output += f" {'ID'} | {'Item':^15} | {'Harga':^15}\n"
    output += f"-" * 38 + "\n"
    for item in Menu:
        output += f"{item}\n"
    output += f"^" * 38 + "\n"
    print(output)

class Order:
    """
    Representasi sebuah pesanan.
    
    Atribut:
    - ID Pesanan: `id: str`
    - No. Meja: `no_meja: int`
    - User pemesan: `user: User`
    - Daftar Pesanan: `items: List[[Item, int]]`
    - Status Pesanan: `status: str`
    - Total harga: `total: int`

    Argumen initialisasi: `(meja: int, user: User) -> Order`
    """
    counter = 0 # Jumlah order yang telah dibuat
    def __init__(self, meja: int, user: "User"):
        self.meja = meja
        self.user = user
        self.items = []
        self.status = Status.PENDING
        self.ID = self.id_generator()

    def id_generator(self):
        """
        Membuat ID komposit unik dengan format:
        `O-XXX-NO-USR--HHMMSS`
          - `O` mengindikasikan ini adalah ID Order (Pesanan)
          - `XXX` mengindikasikan nomor order
          - `NO` adalah 2 digit nomor meja
          - `USR` menunjuk pada inisial user
          - `HHMMSS` adalah waktu ketika pesanan dibuat
        """
        Order.counter += 1
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        return f"O-{Order.counter:03d}-{self.meja:02d}-{self.user.ID[-3:]}-{timestamp}"
    
    def cek_total(self):
        """Menghitung total harga pesanan."""
        total = 0
        for item in self.items:
            total += item[0].harga * item[1]
        return total

    def cek_jumlah(self):
        """Menghitung jumlah item dalam pesanan."""
        jumlah = 0
        for item in self.items:
            jumlah += item[1]
        return jumlah
    
    def tambah_item(self, item: Item, qty: int):
        """
        Menambahkan item ke dalam pesanan jika belum ada.
        Jika sudah ada, tambahkan jumlahnya.
        """
        for row in self.items:
            if row[0] == item:
                row[1] += qty
                return
        self.items.append([item, qty])
    
    def edit_item(self, item: "Item", qty: int):
        """Mengedit jumlah item dalam pesanan jika ada."""
        try:
            self.items[self.items.index(item)][1] = qty
            if qty <= 0:
                self.hapus_item(item)
        except:
            print("Item tidak ditemukan.")
    
    def hapus_item(self, item: "Item"):
        """Menghapus item dari pesanan jika ada."""
        try: 
            self.items.pop(self.items.index(item))
        except:
            print("Item tidak ditemukan.")
        
    def edit_status(self, status):
        """Mengubah status pesanan."""
        self.status = status
    
    def cetak_struk(self):
        """Membuat string untuk mencetak struk pesanan."""
        output = "~" * 67 + "\n"
        output += f"ID Pesanan: {self.ID:>54}\n"
        output += f"Nama: {self.user.nama:}\n"
        output += f"Telp: {self.user.telp}\n"
        output += f"Meja: {self.meja:02d}\nStatus Pesanan: {self.status.value}\n"
        output += f"{'No':<2} |  ID | {'Item':^15} | {'Harga':^13} | {'Qty':^5} | {"Subtotal":^13}\n"
        output += "-" * 67 + "\n"
        for item in self.items:
            item: list[Item, int]
            output += f"{self.items.index(item)+1:02d} | {item[0]} | {item[1]:^5} | Rp {item[0].harga * item[1]:10,.2f}\n"
        output += "-" * 67 + "\n"
        output += f"Total | Rp {self.cek_total():,.2f}\n".rjust(67)
        output += "~" * 67 + "\n"
        return output

    def __str__(self):
        output = f"ID Pesanan: {self.ID}\n"
        output += f"   Meja: {self.meja}\n"
        output += f"   Status Pesanan: {self.status.value}\n"
        output += f"   Jumlah Item: {self.cek_jumlah()}\n"
        output += f"   Total Harga: Rp {self.cek_total():,.2f}\n"
        return output
    
# Antrean Pesanan
order_queue = []

class User:
    """
    Berisi semua informasi berkaitan dengan data pemesan.

    Atribut:
    - User ID: `id: int`
    - Nama: `nama: str`
    - No. Telepon: `telp: str`
    - Daftar Pesanan: `orders: dictionary`
    """

    counter = 0 # Jumlah user yang telah dibuat
    def __init__(self, nama: str, telp: str):
        self.nama = nama
        self.telp = telp
        self.orders = {}
        self.ID = self.id_generator()
        return
    
    def id_generator(self):
        """
        Membuat ID komposit unik dengan format:
        U-XXX-ABC:
          - U mengindikasikan ini adalah ID User
          - XXX adalah urutan nomor user yang dibuat
          - ABC adalah inisial nama user
        """
        initial = self.nama[:3].upper()
        User.counter += 1
        return f"U-{User.counter:03d}-{initial}"

    def tambah_order(self, order: Order):
        """Menambahkan pesanan ke dalam daftar pesanan pengguna."""
        self.orders[order.ID] = order
        order_queue.append(order)
        order.status = Status.CONFIRMED
        return        

    def lihat_daftar(self):
        """Melihat daftar pesanan yang dimiliki pengguna."""
        output = ""
        for order in self.orders.values():
            output += f"{order}\n"
        return output
    
    def notifikasi(self, order: Order):
        """
        Memberitahu pengguna bahwa pesanannya sudah siap.
        Ke depannya jika memungkinkan akan mengirim SMS Notifikasi
        """
        print(f"Pesanan {order.ID} sudah siap diambil.")
        while True:
            jawab = input("Apakah pesanan sudah diambil? (Y/n) : ")
            if jawab == "Y":
                order.edit_status(Status.COMPLETED)
                print("Terima kasih telah memesan di restoran kami :)")
                break
            elif jawab == "n":
                print("Silahkan ambil pesanan anda.")
            else:
                print("Input tidak dikenal.")
        return

    def __str__(self):
        output = f"User ID: {self.ID}\n"
        output += f"Nama: {self.nama}\n"
        output += f"Telepon: {self.telp}\n"
        return output
    
class Admin:
    """
    Berisi semua informasi berkaitan dengan data dan perintah admin.

    Atribut (tersembunyi):
    - Username: `_username: str`
    - Password: `_password: str`

    Untuk menggunakan kemmampuan Admin, Admin harus login terlebih dahulu.
    """
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self.auth = False
        return
    
    def login(self, username: str, password: str):
        """Login ke sistem dengan memasukkan password."""
        if username == self._username:
            if password == self._password:
                self.auth = True
                print("Login berhasil!")
                return True
            else:
                print("Password salah.")
                return False
        else:
            print("Username tidak dikenal.")
            return False

    def logout(self):
        """Logout dari sistem."""
        if self.auth:
            self.auth = False
            print("Logout berhasil.")
        else:
            print("Anda belum login.")

    def lihat_antrean(self):
        """Melihat semua pesanan yang belum diproses."""
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        if not order_queue:
            print("Antrean kosong\n")
            return
        for urutan, order in enumerate(order_queue, start=1):
            print(f"{urutan}. {order}")         
        
    def proses_order(self):
        """Mengambil pesanan terdepan dari antrean, mengubah statusnya, lalu memproses tiap itemnya."""
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        if not order_queue:
            print("Antrean kosong\n")
            return
        order: Order = order_queue.pop(0)
        order.edit_status(Status.IN_PROGRESS)
        print(f"Memproses pesanan {order.ID}...")
        print("Untuk setiap pesanan, tekan Enter untuk melanjutkan.")
        for item in order.items:
            input(f"   Memproses {item[0].nama} x {item[1]}...")
        
        self.selesai_order(order)

    def selesai_order(self, order: Order):
        """
        Menyelesaikan pesanan, mengubah statusnya, dan memberitahu pengguna.
        """
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        
        order.edit_status(Status.READY)
        print(f"Pesanan {order.ID} selesai diproses.")
        order.cetak_struk()
        order.user.notifikasi(order)

class Interface:
    """
    Titik utama interaksi manusia komputer. Tidak ada argumen initialisasi.
    Hanya ada satu objek dalam kelas ini, sehingga atribut yang digunakan bersifat public class level.

    Atribut:
    - Daftar pengguna: `users: dictionary`
    - Admin: `admin = Admin`
    - Antrean: `queue: list = order_queue`
    """
    users = {}
    admin = Admin("admin", "admin")
    queue = order_queue

    def __init__(self):
        pass

    def header_halaman(self, pesan: str):
        """Membuat header pada halalamn"""
        print("\n" + f"#{'=' * 100}#")
        time.sleep(0.5)
        print(f"{pesan.center(100, "-")}")
        time.sleep(0.5)
        print(f"#{'=' * 100}#" + "\n")
        time.sleep(0.5)

    def valid(self):
        """Validasi masukan berupa Pertanyaan Ya/Tidak"""
        while True:
            masukan =input("(Y/T) > ")
            if masukan == "Y" or masukan == "y":
                return True
            elif masukan == "T" or masukan == "t":
                return False
            else:
                print("Masukan tidak dikenal.\n")

    def keluar(self):
        """Konfirmasi untuk keluar Program"""
        self.header_halaman("KELUAR")
        print("Apakah Anda yakin ingin keluar dari aplikasi?", end = " ")
        if self.valid():
            exit()
            return
        else:
            return
                

    def halaman_utama(self):
        """Halaman utama dan pertama ketika memulai program"""
        while True:
            self.header_halaman("HALAMAN UTAMA")
            print(f"Pilih peran:")
            time.sleep(0.5)
            print("1. Koki")
            time.sleep(0.5)
            print("2. Pengguna")
            time.sleep(0.5)
            print("X. Keluar")
            time.sleep(0.5)
            peran = input("> ")
            if peran == "1":
                self.login_koki()
            elif peran == "2":
                self.login_pengguna()
            elif peran == "X" or peran == "x":
                self.keluar()
            else:
                print("Masukan tidak dikenal.\n")
                time.sleep(0.5)
    
    def login_koki(self):
        """Portal koki login"""
        self.header_halaman("LOGIN KOKI")
        while True:
            time.sleep(0.5)
            username = input("Username: > ")
            password = input("Password: > ")
            if Interface.admin.login(username, password):
                self.menu_koki()
                break
            else:
                print("Login gagal. Coba lagi?", end = " ")
                if not self.valid():
                    return

    def menu_koki(self):
        """"Dashboard beranda bagi koki"""
        self.header_halaman("MENU KOKI")
        while True:
            time.sleep(0.5)
            print("A. Lihat Antrean")
            time.sleep(0.5)
            print("B. Proses Pesanan")
            time.sleep(0.5)
            print("X. Logout")
            time.sleep(0.5)
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.header_halaman("DAFTAR ANTREAN")
                Interface.admin.lihat_antrean()
            elif pilihan == "B"or pilihan == "b":
                self.header_halaman("PROSES PESANAN")
                time.sleep(0.5)
                print("Anda akan memproses pesanan terdepan. Lanjutkan?", end = " ")
                if self.valid():
                    Interface.admin.proses_order()
            elif pilihan == "X" or pilihan == "x":
                print("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    self.admin.logout()
                    break
            else:
                print("Masukan tidak dikenal.\n")
    
    def login_pengguna(self):
        """Memisahkan pengguna yang sudah/belum punya User ID"""
        self.header_halaman("LOGIN PENGGUNA")
        print("Apakah Anda sudah memiliki User ID?", end = " ")
        if self.valid():
            self.login_userID()
        else:
            self.daftar_user()
    
    def login_userID(self):
        """Portal login dengan User ID"""
        self.header_halaman("LOGIN PENGGUNA DENGAN USER ID")
        while True:
            user_id = input("Masukkan User ID: > ")
            user = Interface.users.get(user_id)
            if user:
                self.menu_pengguna(user)
                break
            else:
                print("User ID tidak ditemukan. Coba lagi?", end = " ")
                if not self.valid():
                    break
            
    def daftar_user(self):
        """Membuat user baru dan login otomatis"""
        self.header_halaman("DAFTAR PENGUNA BARU")
        print("Masukkan nama dan nomor telepon Anda!")
        time.sleep(0.5)
        print("Keterangan: masukkan nomor telelpon dengan diawali 62 atau kode negara Anda. \nContoh: 628123456789\n")
        time.sleep(0.5)
        while True:
            nama = input("Nama: > ").strip()
            if not nama.replace(" ", "").isalpha():
                print("Nama hanya boleh berisi huruf dan/atau spasi!\n")
                time.sleep(0.5)
                continue
            telp = input("No. Telepon: > ").strip()
            if not telp.isnumeric():
                print("Telepon hanya boleh berisi angka!\n")
                time.sleep(0.5)
                continue
            print("Apakah data yang dimasukkan di atas sudah benar?", end = " ")
            if self.valid():
                user = User(nama, telp)
                Interface.users[user.ID] = user
                print("User berhasil dibuat!")
                time.sleep(0.5)
                print(f"User ID Anda adalah: {user.ID}")
                time.sleep(0.5)
                self.menu_pengguna(user)
                break
            else:
                print("Silahkan masukkan data kembali.\n")
                time.sleep(0.5)

    def menu_pengguna(self, user: User):
        """Dasborad beranda bagi pengguna"""
        self.header_halaman("MENU PENGGUNA")
        print(user)
        print(f"Selamat datang, {user.nama}!\n")
        time.sleep(0.5)
        while True:
            print("A. Buat Pesanan Baru")
            time.sleep(0.5)
            print("B. Lihat Daftar Pesanan")
            time.sleep(0.5)
            print("X. Logout")
            time.sleep(0.5)
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.buat_pesanan(user)
            elif pilihan == "B"or pilihan == "b":
                self.pesanan_pengguna(user)
            elif pilihan == "X" or pilihan == "x":
                print("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    break
            else:
                print("Masukan tidak dikenal.")
                time.sleep(0.5)
    
    def buat_pesanan(self, user: User):
        """Antarmuka membuat pesanann baru"""
        self.header_halaman("BUAT PESANAN BARU")
        while True:
            try: 
                meja = int(input("Masukkan Nomor Meja: "))
                print("Apakah nomor meja sudah benar?", end = " ")
                if self.valid():
                    break
            except:
                print("Masukan tidak valid.")
                time.sleep(0.5)
                continue
        order = Order(meja, user)
        print(f"Pesanan untuk meja {meja} a.n. {user.nama} dibuat.")
        time.sleep(0.5)
        lihat_menu()
        time.sleep(0.5)
        print("Masukkan ID menu yang ingin dipesan dan jumlahnya.")
        time.sleep(0.5)
        while True:
            try:
                item_id = input("ID Menu: > ")
                item = Menu[int(item_id)-1]
                qty = int(input("Jumlah: > "))
                if not (qty > 0):
                    print("Jumlah harus berupa bilangan positif")
                    time.sleep(0.5)
                    continue
            except:
                print("Masukan tidak valid.")
                time.sleep(0.5)
                continue
            print(f"Anda memilih: {item} | {qty} porsi")
            time.sleep(0.5)
            print("Konfirmasi Item?", end = " ")
            if self.valid():
                order.tambah_item(item, qty)
                print("Item berhasil ditambahkan.")
                time.sleep(0.5)
                print("Pesan lagi?", end = " ")
                if self.valid():
                    continue
                else:
                    break        
        print(f"\n{"REVIEW PESANAN":^67}")
        time.sleep(0.5)
        print(order.cetak_struk())
        time.sleep(0.5)
        print("Konfirmasi Pesanan?")
        time.sleep(0.5)
        print("Pesanan yang telah dikonfirmasi tidak bisa dibatalkan dan akan dikenakan biaya total.")
        time.sleep(0.5)
        if self.valid():
            user.tambah_order(order)
            print("Pesanan berhasil dikonfirmasi!")
            time.sleep(0.5)
        else:
            print("Pesanan dibatalkan.")
            time.sleep(0.5)
        print("\nAnda kembali ke menu pengguna.")
        time.sleep(0.5)

    def pesanan_pengguna(self, user: User):
        """Antarmuka daftar pesanan pengguna"""
        self.header_halaman("DAFTAR PESANAN")
        print(user.lihat_daftar())
        time.sleep(0.5)
        print("Apakah Anda ingin melihat detail pesanan?", end = " ")
        time.sleep(0.5)
        if self.valid():
            while True:
                order_id = input("Masukkan ID Pesanan: ")
                order: Order = user.orders.get(order_id)
                if order:
                    print(order.cetak_struk())
                    break
                else:
                    print("Pesanan tidak ditemukan. Coba lagi? (Y/N)")
                    if input("> ") == "N":
                        break
        time.sleep(0.5)
        print("Kembali ke menu pengguna?", end = " ")
        if self.valid():
            return
        else:
            self.pesanan_pengguna()

### MAIN PROGRAM ###
print("")
print("~"*100)
time.sleep(0.5)
print("PANDA MANIS".center(100))
time.sleep(1)
print("kaPAN DApat MAkanan gratISnya?".center(100))
print("~"*100)
time.sleep(1)
Interface().halaman_utama()
