# Nama : Muhammad Sadikin Samir
# NIM : 2409116031

from prettytable import PrettyTable
from datetime import datetime
import pwinput
import time
import os

kue = {
    "pagi": [
        {"Croissant": 30},
        {"Dorayaki": 50},
        {"Cheese Cake": 40},
        {"Tiramisu": 30},
        {"Gulab Jamun": 20}
    ],
    "siang": [
        {"Mochi": 10},
        {"Baklava": 30},
        {"Puto": 20},
        {"Macaron": 50},
        {"Pavlova": 40}
    ],
    "malam": [
        {"Sachertore": 20},
        {"Songpyeon": 30},
        {"Brownies": 50},
        {"Tres Leches Cake": 40},
        {"Mandazi": 10}
    ]
}

akun = {
    "kategori": {
        "VIP": {
            "Sadikin": {"password": "memberkaya01", "saldo": 0, "poin": 0, "status":False }
        },
        "Reguler": {
            "Rehan": {"password": "memberbiasa01", "saldo": 0, "poin": 0,"status": False},
            "Niki": {"password": "memberbiasa02", "saldo": 0, "poin": 0, "status": False}
        }
    }
}

voucher = { 
    "KUEMURAH": {"status" : "belum", "diskon" : 0.05, "disc" : "5%"},
    "KUEENAK" : {"status" : "belum", "diskon" : 0.1, "disc" : "10%"},
    "KUESEDAP" : {"status" : "belum", "diskon" : 0.1, "disc" : "10%"}
}


def waktu():
    jam_sekarang = datetime.now().hour
    if 8 <= jam_sekarang < 12:
        return "pagi"
    elif 12 <= jam_sekarang < 18:
        return "siang"
    elif 18 <= jam_sekarang < 22:
        return "malam"
    return None 

def cek_status(nama):
    if nama in akun["kategori"]["VIP"]:
        return akun["kategori"]["VIP"][nama]["status"]
    elif nama in akun["kategori"]["Reguler"]:
        return akun["kategori"]["Reguler"][nama]["status"]
    return False

def login():
    os.system("cls")
    jams = datetime.now().hour
    coba = 0
    while coba < 3:
        if 8 <= jams < 22:
            print("╔═════════════════════════════════════╗")
            print("║  SELAMAT DATANG DI TOKO KUE DUNIA   ║")
            print("║            SILAHKAN LOGIN           ║")
            print("╚═════════════════════════════════════╝")
            nama = input("Masukkan username: ")
            if cek_status(nama):
                print("Akun anda terkunci. Silakan coba lagi nanti.")
                os.system("pause")
                login()
            
            pw = pwinput.pwinput("Masukkan password: ")
            if nama in akun["kategori"]["VIP"] and akun["kategori"]["VIP"][nama]["password"] == pw:
                print("Login berhasil sebagai member VIP.")
                os.system("pause")
                menu(nama)
            elif nama in akun["kategori"]["Reguler"] and akun["kategori"]["Reguler"][nama]["password"] == pw:
                print("Login berhasil sebagai member Reguler.")
                os.system("pause")
                menu(nama)
            coba += 1
            print("Username atau password salah, coba lagi.")
            if coba == 3:
                if nama in akun["kategori"]["VIP"]:
                    akun["kategori"]["VIP"][nama]["status"] = True
                elif nama in akun["kategori"]["Reguler"]:
                    akun["kategori"]["Reguler"][nama]["status"] = True
                
                print("Terlalu banyak percobaan. Akun anda terkunci. Silakan coba lagi dalam 10 detik.") 
                time.sleep(10)
                coba = 0
        else:
            print("╔═════════════════════════════════════╗")
            print("║  MAAF TOKO KUE DUNIA SEDANG TUTUP   ║")
            print("╚═════════════════════════════════════╝")
            return 
            
def lihat_kue(nama):
    os.system("cls")
    jam = waktu()
    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Kue", "Harga"]
    if jam:
        for no, kue_item in enumerate(kue[jam], start=1):
            tabel.add_row([no, list(kue_item.keys())[0], list(kue_item.values())[0]])
        print(tabel)
    else:
        print("Toko sedang tutup.")

def beli(nama):
    os.system("cls")
    print("╔═════════════════════════════════════╗")
    print("║            MENU BELI KUE            ║")
    print("╚═════════════════════════════════════╝")
    lihat_kue(nama)
    jam = waktu()   
    pilih = int(input("Pilih Kue yang ingin dibeli: "))
    jumlah = int(input("Masukkan jumlah kue: "))
    kuep = kue[jam][pilih - 1]
    nkue = list(kuep.keys())[0]
    hkue = kuep[nkue]
    while True:
        total = kue[jam][pilih - 1][list(kue[jam][pilih - 1].keys())[0]] * jumlah
        if nama in akun["kategori"]["VIP"]:
            print("Karena kamu member VIP, kamu mendapatkan diskon 10%")
            disvip = total-total*0.1
            while True:
                pvcr = input("Apakah anda ingin menggunakan voucher? (ya/tidak): ").lower()
                if pvcr == "ya":
                    vcr = input("Masukkan voucher: ")
                    if vcr in voucher and voucher[vcr]["status"] == "belum":
                        print(f"Voucher berhasil digunakan kamu mendapatkan diskon {voucher[vcr]['disc']}")
                        diskon = disvip-total*voucher[vcr]["diskon"]
                        print("\nKeterangan:")
                        print(f"Kue = {nkue}")
                        print(f"Jumlah = {jumlah}")
                        print(f"Harga Total = {diskon} Poin")                             
                        while True:
                            byr = input("Bayar? (ya/tidak): ").lower()
                            if byr == "ya":
                                if akun["kategori"]["VIP"][nama]["poin"] >= diskon:
                                    akun["kategori"]["VIP"][nama]["poin"] -= diskon
                                    print("Terima kasih sudah membeli.")
                                    voucher[vcr]["status"] = "sudah"
                                    os.system("pause")
                                    menu(nama)
                                else:
                                    print("Poin tidak mencukupi, Silahkan melakukan topup poin.")
                                    os.system("pause")
                                    menu(nama)
                            elif byr == "tidak":
                                print("Pembayaran dibatalkan.")
                                os.system("pause")
                                menu(nama)
                            else:
                                print("Pilihan tidak valid. Silakan coba lagi.")
                    else:
                        print("Maaf,Voucher telah digunakan")
                elif pvcr == "tidak":
                    print("\nKeterangan:")
                    print(f"Kue = {nkue}")
                    print(f"Jumlah = {jumlah}")
                    print(f"Harga Total = {total} Poin")
                    while True:
                        byr = input("Bayar? (ya/tidak): ").lower()
                        if byr == "ya":
                            if akun["kategori"]["VIP"][nama]["poin"] >= total:
                                akun["kategori"]["VIP"][nama]["poin"] -= total  
                                print("Terima kasih sudah membeli.")
                                os.system("pause")
                                menu(nama)
                            else:
                                print("Poin tidak mencukupi, Silahkan melakukan topup poin.")
                                os.system("pause")
                                menu(nama)      
                        elif byr == "tidak":
                            print("Pembayaran dibatalkan.")
                            os.system("pause")
                            menu(nama)
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
        else:
            while True:
                pvcr = input("Apakah anda ingin menggunakan voucher? (ya/tidak): ").lower()
                if pvcr == "ya":
                    vcr = input("Masukkan voucher: ")
                    if vcr in voucher and voucher[vcr]["status"] == "belum":
                        print(f"Voucher berhasil digunakan kamu mendapatkan diskon {voucher[vcr]['disc']}")
                        diskon = total-total*voucher[vcr]["diskon"]
                        print("\nKeterangan:")
                        print(f"Kue = {nkue}")
                        print(f"Jumlah = {jumlah}")
                        print(f"Harga Total = {diskon} Poin")                             
                        while True:
                            byr = input("Bayar? (ya/tidak): ").lower()
                            if byr == "ya":
                                if akun["kategori"]["Reguler"][nama]["poin"] >= diskon:
                                    akun["kategori"]["Reguler"][nama]["poin"] -= diskon
                                    print("Terima kasih sudah membeli.")
                                    os.system("pause")
                                    menu(nama)
                                else:
                                    print("Poin tidak mencukupi, Silahkan melakukan topup poin.")
                                    os.system("pause")
                                    menu(nama)
                            elif byr == "tidak":
                                print("Pembayaran dibatalkan.")
                                os.system("pause")
                                menu(nama)
                            else:
                                print("Pilihan tidak valid. Silakan coba lagi.")
                    else:
                        print("Maaf,Voucher telah digunakan")
                elif pvcr == "tidak":
                    print("\nKeterangan:")
                    print(f"Kue = {nkue}")
                    print(f"Jumlah = {jumlah}")
                    print(f"Harga Total = {total} Poin")
                    while True:
                        byr = input("Bayar? (ya/tidak): ").lower()
                        if byr == "ya":
                            if akun["kategori"]["Reguler"][nama]["poin"]:
                                akun["kategori"]["Reguler"][nama]["poin"]
                                print("Terima kasih sudah membeli.")
                                os.system("pause")
                                menu(nama)
                            else:
                                print("Poin tidak mencukupi, Silahkan melakukan topup poin.")
                                os.system("pause")
                                menu(nama)
                        elif byr == "tidak":
                            print("Pembayaran dibatalkan.")
                            os.system("pause")
                            menu(nama)
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")

def topup(nama):
    os.system("cls")
    print("╔═════════════════════════════════════╗")
    print("║               MENU TOPUP            ║")
    print("╚═════════════════════════════════════╝")
    if nama in akun["kategori"]["VIP"]:
        while True:
            print(f"Saldo Anda: {akun["kategori"]["VIP"][nama]["saldo"]}")
            print(f"Poin Anda: {akun["kategori"]["VIP"][nama]["poin"]}")
            print("[1] Topup Saldo")
            print("[2] Topup Poin")
            print("[3] Kembali")
            pilih = input("Pilih menu: ")
            if pilih == "1":
                Topup_Saldo(nama)
            elif pilih == "2":
                Topup_Poin(nama)
            elif pilih == "3":
                menu(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    else:
        while True:
            print(f"Saldo Anda: {akun["kategori"]["Reguler"][nama]["saldo"]}")
            print(f"Poin Anda: {akun["kategori"]["Reguler"][nama]["poin"]}")
            print("[1] Topup Saldo")
            print("[2] Topup Poin")
            print("[3] Kembali")
            
            pilih = input("Pilih menu: ")
            if pilih == "1":
                Topup_Saldo(nama)
            elif pilih == "2":
                Topup_Poin(nama)
            elif pilih == "3":
                menu(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
def Topup_Saldo(nama):
    os.system("cls")
    print("╔═════════════════════════════════════╗")
    print("║           MENU TOPUP SALDO          ║")
    print("╚═════════════════════════════════════╝")
    if nama in akun["kategori"]["VIP"]:
        while True:
            print("[1] Rp.50.000")
            print("[2] Rp.100.000")
            print("[3] Nominal Lain")
            print("[4] Kembali")
            pilih = input("Pilih menu: ")
            if pilih == "1":
                akun["kategori"]["VIP"][nama]["saldo"] += 50000
                print("Topup Saldo Berhasil")
                topup(nama)
            elif pilih == "2":
                akun["kategori"]["VIP"][nama]["saldo"] += 100000
                print("Topup Saldo Berhasil")
                topup(nama)
            elif pilih == "3":
                print("Minimal top up Rp.100000 dan maksimal Rp.500000")
                nominal = int(input("Masukkan nominal: "))
                if 100000<=nominal<=500000:
                    akun["kategori"]["VIP"][nama]["saldo"] += nominal
                    print("Topup Saldo Berhasil")
                    topup(nama)
                else:
                    print("Nominal tidak valid.")
            elif pilih == "4":
                topup(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    else:
        while True:
            print("[1] Rp.50.000")
            print("[2] Rp.100.000")
            print("[3] Nominal Lain")
            print("[4] Kembali")
            pilih = input("Pilih menu: ")
            if pilih == "1":
                akun["kategori"]["Reguler"][nama]["saldo"] += 50000
                print("Topup Saldo Berhasil")
                topup(nama)
            elif pilih == "2":
                akun["kategori"]["Reguler"][nama]["saldo"] += 100000
                print("Topup Saldo Berhasil")
                topup(nama)
            elif pilih == "3":
                print("Minimal top up Rp.100000 dan maksimal Rp.500000")
                nominal = int(input("Masukkan nominal: "))
                if 100000<=nominal<=500000:
                    akun["kategori"]["Reguler"][nama]["saldo"] += nominal
                    print("Topup Saldo Berhasil")
                    topup(nama)
                else:
                    print("Nominal tidak valid.")
            elif pilih == "4":
                topup(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

def Topup_Poin(nama):
    os.system("cls")
    print("╔═════════════════════════════════════╗")
    print("║           MENU TOPUP POIN           ║")
    print("╚═════════════════════════════════════╝")
    if nama in akun["kategori"]["VIP"]:
        while True:
            print("[1] 50 Poin = Rp.10.000")
            print("[2] 115 Poin = Rp.20.000")
            print("[3] 225 Poin = Rp.30.000")
            print("[4] 350 Poin = Rp.40.000")
            print("[5] 475 Poin = Rp.50.000")
            print("[6] Kembali")
            pilih = input("Pilih: ")
            if pilih == "1":
                if akun["kategori"]["VIP"][nama]["saldo"] >= 10000:
                    akun["kategori"]["VIP"][nama]["poin"] += 50
                    akun["kategori"]["VIP"][nama]["saldo"] -= 10000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "2":
                if akun["kategori"]["VIP"][nama]["saldo"] >= 20000:
                    akun["kategori"]["VIP"][nama]["poin"] += 115
                    akun["kategori"]["VIP"][nama]["saldo"] -= 20000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
                if akun["kategori"]["VIP"][nama]["saldo"] >= 30000:
                    akun["kategori"]["VIP"][nama]["poin"] += 225
                    akun["kategori"]["VIP"][nama]["saldo"] -= 30000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "4":
                if akun["kategori"]["VIP"][nama]["saldo"] >= 40000:
                    akun["kategori"]["VIP"][nama]["poin"] += 350
                    akun["kategori"]["VIP"][nama]["saldo"] -= 40000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "5":
                if akun["kategori"]["VIP"][nama]["saldo"] >= 50000:
                    akun["kategori"]["VIP"][nama]["poin"] += 475
                    akun["kategori"]["VIP"][nama]["saldo"] -= 50000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "6":
                topup(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    else:
        while True:
            print("[1] 50 Poin = Rp.10.000")
            print("[2] 115 Poin = Rp.20.000")
            print("[3] 225 Poin = Rp.30.000")
            print("[4] 350 Poin = Rp.40.000")
            print("[5] 475 Poin = Rp.50.000")
            print("[6] Kembali")
            pilih = input("Pilih menu: ")
            if pilih == "1":
                if akun["kategori"]["Reguler"][nama]["saldo"] >= 10000:
                    akun["kategori"]["Reguler"][nama]["poin"] += 50
                    akun["kategori"]["Reguler"][nama]["saldo"] -= 10000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "2":
                if akun["kategori"]["Reguler"][nama]["saldo"] >= 20000:
                    akun["kategori"]["Reguler"][nama]["poin"] += 115
                    akun["kategori"]["Reguler"][nama]["saldo"] -= 20000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "3":
                if akun["kategori"]["Reguler"][nama]["saldo"] >= 30000:
                    akun["kategori"]["Reguler"][nama]["poin"] += 225
                    akun["kategori"]["Reguler"][nama]["saldo"] -= 30000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "4":
                if akun["kategori"]["Reguler"][nama]["saldo"] >= 40000:
                    akun["kategori"]["Reguler"][nama]["poin"] += 350
                    akun["kategori"]["Reguler"][nama]["saldo"] -= 40000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "5":
                if akun["kategori"]["Reguler"][nama]["saldo"] >= 50000:
                    akun["kategori"]["Reguler"][nama]["poin"] += 475
                    akun["kategori"]["Reguler"][nama]["saldo"] -= 50000
                    print("Topup Poin Berhasil") 
                    topup(nama)
                else:
                    print("Saldo tidak mencukupi")
                    topup(nama)
            elif pilih == "6":
                topup(nama)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    
def menu(nama):
    os.system("cls")
    while True:
        print("╔═════════════════════════════════════╗")
        print("║              MENU UTAMA             ║")
        print("╚═════════════════════════════════════╝")
        print("[1] Lihat Kue")
        print("[2] Beli Kue")
        print("[3] Topup")
        print("[4] Keluar")
        pilih = input("Pilih menu: ")
        if pilih =="1":
            print("╔═════════════════════════════════════╗")
            print("║           MENU LIHAT KUE            ║")
            print("╚═════════════════════════════════════╝")
            lihat_kue(nama)
        elif pilih == "2":
            beli(nama)
        elif pilih == "3":
            topup(nama)
        elif pilih == "4":
            print("╔══════════════════════════════════════════════╗")
            print("║ TERIMAKASIH TELAH MENGUNJUNGI TOKO KUE DUNIA ║")
            print("╚══════════════════════════════════════════════╝")
            exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    login()                         
    
main()