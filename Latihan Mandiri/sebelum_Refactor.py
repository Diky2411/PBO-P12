from dataclasses import dataclass

@dataclass
class Mahasiswa:
    nama: str
    jumlah_sks: int
    prasyarat: bool

class ValidatorManager:
    # Melanggar SRP: Satu kelas menangani berbagai logika validasi
    # Melanggar OCP: Menambah validasi baru memaksa kita mengubah kode logika
    # Melanggar DIP: Bergantung pada implementasi konkrit, bukan abstraksi
    
    def validasi_registrasi(self, mahasiswa: Mahasiswa, validation_type: str):
        print(f"\n--- Memulai Validasi untuk {mahasiswa.nama} ---")

        # LOGIKA VALIDASI SKS
        if validation_type == "sks":
            if mahasiswa.jumlah_sks <= 24:
                print(f"validasi SKS: jumlah SKS {mahasiswa.nama} Valid.")
                return True
            else:
                print(f"Validasi SKS: {mahasiswa.nama} Gagal (SKS > 24).")
                return False

        # LOGIKA VALIDASI PRASYARAT
        elif validation_type == "prasyarat":
            if mahasiswa.prasyarat:
                print(f"Validasi PRASYARAT: {mahasiswa.nama} Memenuhi Syarat.")
                return True
            else:
                print(f"VALIDASI PRASYARAT: {mahasiswa.nama} Tidak Memenuhi Syarat.")
                return False
        
        else:
            print("Gagal.")
            return False

# --- EKSEKUSI ---
diki = Mahasiswa("diki", 23, True)
dono = Mahasiswa("dono", 25, False)
manager = ValidatorManager()

#panggil validasi
print("contoh 1")
manager.validasi_registrasi(diki, "sks")
manager.validasi_registrasi(diki, "prasyarat")

print("\ncontoh 2")
manager.validasi_registrasi(dono, "sks")
manager.validasi_registrasi(dono, "prasyarat")