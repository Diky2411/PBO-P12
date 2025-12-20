import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- 1. KONFIGURASI LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger("RegistrasiApp")

@dataclass
class Mahasiswa:
    """Representasi data mahasiswa.

    Attributes:
        nama (str): Nama lengkap mahasiswa.
        jumlah_sks (int): Total SKS yang diambil.
        prasyarat (bool): Status kelulusan mata kuliah prasyarat.
    """
    nama: str
    jumlah_sks: int
    prasyarat: bool

# 2. ABSTRAKSI (DIP)
class IValidator(ABC):
    """Interface dasar untuk semua aturan validasi."""
    
    @abstractmethod
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        """Metode abstrak untuk memvalidasi data mahasiswa.

        Args:
            mahasiswa (Mahasiswa): Objek mahasiswa yang divalidasi.

        Returns:
            bool: True jika valid, False jika tidak.
        """
        pass

# 3. IMPLEMENTASI KONKRIT (SRP)
class SksValidator(IValidator):
    """Validator untuk memeriksa batasan SKS mahasiswa."""
    
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.jumlah_sks <= 24:
            LOGGER.info(f"Validasi SKS: {mahasiswa.nama} LULUS (SKS: {mahasiswa.jumlah_sks}).")
            return True
        LOGGER.error(f"Validasi SKS: {mahasiswa.nama} GAGAL (SKS: {mahasiswa.jumlah_sks} > 24).")
        return False

class PrasyaratValidator(IValidator):
    """Validator untuk memeriksa kelengkapan mata kuliah prasyarat."""
    
    def validasi(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.prasyarat:
            LOGGER.info(f"Validasi PRASYARAT: {mahasiswa.nama} LULUS.")
            return True
        LOGGER.warning(f"Validasi PRASYARAT: {mahasiswa.nama} GAGAL (Belum ambil prasyarat).")
        return False

# 4. KELAS KOORDINATOR (DIP & OCP)
class RegistrasiService:
    """Layanan untuk mengelola seluruh proses validasi registrasi.

    Args:
        validators (list[IValidator]): Daftar aturan validasi yang akan dijalankan.
    """
    def __init__(self, validators: list[IValidator]):
        self.validators = validators

    def run_validasi(self, mahasiswa: Mahasiswa) -> bool:
        """Menjalankan semua validator yang terdaftar untuk mahasiswa.

        Args:
            mahasiswa (Mahasiswa): Objek mahasiswa yang akan diproses.

        Returns:
            bool: Status akhir registrasi (Berhasil/Gagal).
        """
        LOGGER.info(f"Memulai proses registrasi untuk: {mahasiswa.nama}")
        hasil_akhir = True
        
        for v in self.validators:
            if not v.validasi(mahasiswa):
                hasil_akhir = False
        
        if hasil_akhir:
            LOGGER.info(f"HASIL AKHIR: Registrasi {mahasiswa.nama} BERHASIL")
        else:
            LOGGER.error(f"HASIL AKHIR: Registrasi {mahasiswa.nama} GAGAL")
        return hasil_akhir

# --- EKSEKUSI PROGRAM ---
if __name__ == "__main__":
    # Data Mahasiswa
    diky = Mahasiswa("Diky", 20, True)
    anwar = Mahasiswa("Anwar", 26, False)

    # List Validator
    list_validasi = [SksValidator(), PrasyaratValidator()]
    app = RegistrasiService(list_validasi)

    # Eksekusi
    app.run_validasi(diky)
    app.run_validasi(anwar)