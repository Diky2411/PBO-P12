from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Mahasiswa:
    nama: str
    jumlah_sks: int
    prasyarat: bool

# 2. ABSTRAKSI (DIP)
class IValidator(ABC):
    @abstractmethod
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        pass

# 3. IMPLEMENTASI KONKRIT (SRP)
class SksValidator(IValidator):
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.jumlah_sks <= 24:
            print(f"Validasi SKS: {mahasiswa.nama} Valid (SKS: {mahasiswa.jumlah_sks}).")
            return True
        print(f"Validasi SKS: {mahasiswa.nama} Gagal (SKS > 24).")
        return False

class PrasyaratValidator(IValidator):
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.prasyarat:
            print(f"Validasi PRASYARAT: {mahasiswa.nama} Memenuhi Syarat.")
            return True
        print(f"Validasi PRASYARAT: {mahasiswa.nama} Gagal (Belum prasyarat).")
        return False

# 4. KELAS KOORDINATOR (DIP & OCP)
class RegistrasiService:
    def __init__(self, validators: list[IValidator]):
        self.validators = validators

    def run_validasi(self, mahasiswa: Mahasiswa):
        print(f"\n--- Memulai Validasi Registrasi: {mahasiswa.nama} ---")
        hasil_akhir = True
        
        for v in self.validators:
            if not v.validasi(mahasiswa):
                hasil_akhir = False
        
        if hasil_akhir:
            print(f"--> Registrasi {mahasiswa.nama} Berhasil")
        else:
            print(f"--> Registrasi {mahasiswa.nama} Gagal")
        return hasil_akhir

# --- EKSEKUSI PROGRAM ---
if __name__ == "__main__":
    # Data Mahasiswa
    diky = Mahasiswa("Diky", 20, True)
    anwar = Mahasiswa("Anwar", 26, False)

    # Validasi Standar (SKS & Prasyarat)
    print("=== contoh 1: VALIDASI===")
    list_validasi = [SksValidator(), PrasyaratValidator()]
    
    app = RegistrasiService(list_validasi)
    app.run_validasi(diky)
    app.run_validasi(anwar)

    # bikin Fitur Baru (OCP)
    print("\n=== contoh 2: FITUR BARU===")
    
    class BerkasValidator(IValidator):
        def validasi(self, mahasiswa: Mahasiswa) -> bool:
            print(f"Validasi BERKAS: Berkas {mahasiswa.nama} Lengkap.")
            return True

    #list baru tambahan fitur baru
    list_validasi_baru = [SksValidator(), PrasyaratValidator(), BerkasValidator()]
    
    app_new = RegistrasiService(list_validasi_baru)
    app_new.run_validasi(diky)