from tkinter import messagebox # Import messagebox dari tkinter
from server.order import Order, Status # Import class Order dan Enum Status dari file order.py
from server.user import User # Import class User dari file user.py

class Admin:
    """
    Berisi semua informasi berkaitan dengan data dan perintah admin. Untuk menggunakan kemmampuan Admin, Admin harus login terlebih dahulu.

    Atribut Lokal:
    - Username (tersembunyi): `_username: str`
    - Password (tersembunyi): `_password: str`
    - Autentikasi: `auth: bool`

    Argumen initialisasi: `Admin(username: str, password: str) -> Admin`

    Metode:
    - `login(username: str, password: str) -> bool`: Login ke sistem dengan memasukkan password.
    - `logout()`: Logout dari sistem.
    - `proses_order()`: Memproses tiap item dalam suatu pesanan jika status pesanan memenuhi.

    """
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self.auth = False
        return
    
    def login(self, username: str, password: str) -> bool:
        """Login ke sistem dengan memasukkan password."""
        if username == self._username:
            if password == self._password:
                self.auth = True
                messagebox.showinfo("Berhasil", "Login berhasil. Selamat datang, Admin!")
                return True
            else:
                messagebox.showerror("Gagal", "Password salah. Coba lagi.")
                return False
        else:
            messagebox.showerror("Gagal", "Username tidak dikenal, coba lagi.")
            return False

    def logout(self):
        """Logout dari sistem."""
        if self.auth:
            self.auth = False
            messagebox.showinfo("Berhasil", "Logout berhasil.")
        
    def proses_order(self, order: Order, selesai: list):
        """Memproses tiap item dalam suatu pesanan jika status pesanan memenuhi."""
        if order.status != Status.IN_PROGRESS:
            messagebox.showerror("Error", "Tidak dapat memproses pesanan ini. Pesanan tidak dalam antrean.")
            return
        
        for i, (item, qty) in enumerate(order.items.items(), start=0):
            if selesai[i].get() == 0:
                messagebox.showerror("Error", f"Item {item.nama} x {qty} buah belum diselesaikan.")
                return
        order = Order.antrean.pop(0)        
        order.status = Status.READY
        
        print(f"Pesanan {order.ID} selesai diproses.\n")
        print(order.cetak_struk())
        user: User = User.daftar.get(order.user_id)
        user.notifikasi(order)
