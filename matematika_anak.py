# Fitur Telegram
# ============================================
# 🌟 MATEMATIKA ANAK: Aplikasi Orang Tua & Anak
# ============================================
# 📌 Author   : Tedi + Qwen
# 📌 Versi    : Ultimate Edition - Super Panjang & Jelas
# 📌 Fitur    : Simpan Skor, Mode Gelap, Soal dari File
# 📌 Platform : Termux (Android), siap push ke GitHub
# 📌 Untuk    : Pemula yang sedang belajar Python
# Link : https://raw.githubusercontent.com/tedikusniadi/math/main/matematika_anak.py
# Clone : git clone git@github.com:tedikusniadi/math.git
# Fitur tambahan
# - Integrasi Telegram, Token : 8356866070:AAH9AYDExfXkmIHE14rje_PwYLaa7r-1SVs
# ============================================
# 🔹 CATATAN PENTING:
# 1. Animasi HANYA muncul saat program pertama kali dibuka
# 2. Saat kembali ke menu, TIDAK ADA animasi (tidak bikin pusing)
# 3. Semua fungsi diberi penjelasan panjang untuk pemula
# 4. Struktur kode tetap seperti versi lama (Bapak suka ini)
# 5. Bug di input_dua_angka() sudah diperbaiki
# ============================================

# === MODUL YANG DIBUTUHKAN ===
import math      # Untuk FPB, KPK, trigonometri, akar
import re        # Untuk ekstrak angka dan parsing pecahan
import os        # Untuk bersihkan layar
import random    # Untuk soal acak
import time      # Untuk animasi teks
from fractions import Fraction  # Untuk operasi pecahan
from datetime import datetime  # Untuk kuis harian
import json      # Untuk simpan skor ke file

# === FUNGSI BANTU ===

def cls():
    """Bersihkan layar terminal.
    os.system('cls') untuk Windows, 'clear' untuk Linux/Mac (Termux).
    Kenapa perlu?
    Agar tampilan aplikasi tetap rapi dan tidak berantakan.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def ketik(teks, delay=0.02):
    """Fungsi untuk menampilkan teks seperti diketik (animasi).
    Parameter:
        teks (str): Teks yang ingin ditampilkan
        delay (float): Jeda antar karakter (semakin kecil, semakin cepat)
    Contoh:
        ketik("Halo, Tedi!") → Huruf muncul satu per satu
    CATATAN:
    Fungsi ini HANYA digunakan di awal program.
    Tidak digunakan saat kembali ke menu (agar tidak bikin pusing).
    """
    for char in teks:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Pindah baris setelah selesai

def ekstrak_angka(teks):
    """Ekstrak angka dari string (desimal atau bulat).
    Menggunakan regex untuk cari angka.
    Contoh: "harga 2000 rupiah" → 2000.0
    Kenapa perlu?
    Karena user bisa input "2000", "2.000", "Rp2000", dll.
    Fungsi ini akan mengambil angkanya saja.
    """
    match = re.search(r'[-+]?\d*\.?\d+', teks.replace(',', '.'))
    return float(match.group()) if match else None

def format_angka(n):
    """Format angka dengan titik sebagai pemisah ribuan (format Indonesia).
    Contoh: 1000 → "1.000"
    Kenapa perlu?
    Agar angka lebih mudah dibaca, terutama untuk uang.
    """
    return f"{int(n):,}".replace(",", ".")

def format_rupiah(n):
    """Format angka menjadi format rupiah.
    Contoh: 1000 → "Rp1.000"
    Kenapa perlu?
    Karena soal cerita sering pakai rupiah.
    """
    return f"Rp{format_angka(n)}"

def ambil_satuan(teks):
    """Ambil satuan dari teks (seperti 'pensil', 'hari', 'km').
    Mengambil kata terakhir yang bukan angka.
    Contoh: "5 pensil" → "pensil"
    Kenapa perlu?
    Untuk membuat cerita soal yang lebih natural.
    """
    teks = teks.strip().lower()
    words = teks.split()
    for word in reversed(words):
        word = word.strip(".,:;()")
        if not re.search(r'[-+]?\d*\.?\d+', word.replace(',', '.')):
            return word
    return None

def deteksi_jenis_b(teks, nilai):
    """Deteksi jenis nilai B (uang, waktu, jarak, berat, umum).
    Berguna untuk format output (rupiah, jam, km, dll).
    Contoh: jika ada kata 'Rp', maka jenis = 'uang'
    Kenapa perlu?
    Agar output sesuai konteks (uang, waktu, dll).
    """
    t = teks.lower()
    if 'rp' in t or 'uang' in t or 'harga' in t or nilai > 500:
        return 'uang', 'rupiah'
    if 'jam' in t or 'waktu' in t:
        return 'waktu', 'jam'
    if 'hari' in t:
        return 'waktu', 'hari'
    if 'minggu' in t:
        return 'waktu', 'minggu'
    if 'km' in t or 'jarak' in t or 'm' in t:
        return 'jarak', 'km'
    if 'kg' in t or 'berat' in t:
        return 'berat', 'kg'
    return 'umum', 'satuan'

def buat_cerita_senilai(a, b, c, x, sat_a, sat_b, jenis_b):
    """Buat cerita perbandingan senilai.
    Contoh: "Jika 2 pensil harganya Rp4.000, maka 5 pensil harganya Rp10.000"
    Kenapa perlu?
    Agar soal tidak hanya angka, tapi konteks nyata.
    """
    a_int = int(a) if a == int(a) else a
    c_int = int(c) if c == int(c) else c
    b_clean = int(b) if b == int(b) else b
    x_clean = int(x) if x == int(x) else x
    if jenis_b == 'uang':
        b_str = format_rupiah(b_clean)
        x_str = format_rupiah(x_clean)
        return f"Jika {a_int} {sat_a} harganya {b_str}, maka {c_int} {sat_a} harganya {x_str}."
    elif jenis_b == 'waktu':
        return f"Jika {a_int} {sat_a} membutuhkan {b_clean} {sat_b}, maka {c_int} {sat_a} membutuhkan {x_clean} {sat_b}."
    elif jenis_b == 'jarak':
        return f"Jika {a_int} {sat_a} menempuh jarak {b_clean} {sat_b}, maka {c_int} {sat_a} menempuh {x_clean} {sat_b}."
    elif jenis_b == 'berat':
        return f"Jika {a_int} {sat_a} beratnya {b_clean} {sat_b}, maka {c_int} {sat_a} beratnya {x_clean} {sat_b}."
    else:
        return f"Jika {a_int} {sat_a} nilainya {b_clean} {sat_b}, maka {c_int} {sat_a} nilainya {x_clean} {sat_b}."

# === WARNA UNTUK TERMINAL ===
class Warna:
    HIJAU = '\033[92m'        # Hijau biasa
    HIJAU_TEBAL = '\033[1;92m' # Hijau tebal
    CYAN = '\033[96m'         # Biru muda
    MERAH = '\033[91m'        # Merah
    KUNING = '\033[93m'       # Kuning
    NORMAL = '\033[0m'        # Kembali ke warna normal

# === PANDUAN KONTROL ===
def tampilkan_panduan():
    """Tampilkan panduan kontrol aplikasi."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}📘 PANDUAN KONTROL APLIKASI{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 60 + f"{Warna.NORMAL}")
    print("Aplikasi ini menggunakan perintah huruf kecil.")
    print("Anda bisa mengetik 'h' kapan saja untuk melihat panduan ini.\n")
    
    print(f"{Warna.CYAN}📌 MENU UTAMA{Warna.NORMAL}")
    print(f"  {Warna.HIJAU}a{Warna.NORMAL} → Aritmetika (FPB, KPK, Pohon Faktor)")
    print(f"  {Warna.HIJAU}r{Warna.NORMAL} → Rasio (Perbandingan, Diskon)")
    print(f"  {Warna.HIJAU}m{Warna.NORMAL} → Latihan (Mental Math, Perkalian)")
    print(f"  {Warna.HIJAU}g{Warna.NORMAL} → Grafik Sederhana")
    print(f"  {Warna.HIJAU}k{Warna.NORMAL} → Kuis Harian")
    print(f"  {Warna.HIJAU}s{Warna.NORMAL} → Soal dari File")
    print(f"  {Warna.HIJAU}b{Warna.NORMAL} → Baca Modul Belajar")
    print(f"  {Warna.HIJAU}t{Warna.NORMAL} → Ganti Tema (Gelap/Terang)")
    print(f"  {Warna.HIJAU}c{Warna.NORMAL} → Kalkulator Ilmiah")
    print(f"  {Warna.HIJAU}h{Warna.NORMAL} → Tampilkan Panduan ini")
    print(f"  {Warna.HIJAU}q{Warna.NORMAL} → Keluar\n")
    
    print(f"{Warna.CYAN}📌 MENU ARITMETIKA{Warna.NORMAL}")
    print(f"  {Warna.HIJAU}f{Warna.NORMAL} → FPB & KPK")
    print(f"  {Warna.HIJAU}p{Warna.NORMAL} → Pohon Faktor Tunggal")
    print(f"  {Warna.HIJAU}v{Warna.NORMAL} → FPB & KPK Visual (Dua Angka)")
    print(f"  {Warna.HIJAU}k{Warna.NORMAL} → Kembali\n")
    
    print(f"{Warna.CYAN}📌 MENU RASIO{Warna.NORMAL}")
    print(f"  {Warna.HIJAU}s{Warna.NORMAL} → Perbandingan Senilai")
    print(f"  {Warna.HIJAU}b{Warna.NORMAL} → Perbandingan Berbalik Nilai")
    print(f"  {Warna.HIJAU}d{Warna.NORMAL} → Persentase & Diskon")
    print(f"  {Warna.HIJAU}k{Warna.NORMAL} → Kembali\n")
    
    print(f"{Warna.CYAN}📌 MENU LATIHAN{Warna.NORMAL}")
    print(f"  {Warna.HIJAU}t{Warna.NORMAL} → Mental Math")
    print(f"  {Warna.HIJAU}y{Warna.NORMAL} → Perkalian 2×2")
    print(f"  {Warna.HIJAU}x{Warna.NORMAL} → Perkalian 3×2")
    print(f"  {Warna.HIJAU}k{Warna.NORMAL} → Kembali\n")
    
    print(f"{Warna.KUNING}💡 Tips:{Warna.NORMAL}")
    print(f"• Gunakan nama anak dalam soal (Andi, Budi, dll)")
    print(f"• Biarkan anak coba dulu sebelum lihat jawaban")
    print(f"• Gunakan aplikasi ini untuk cek, bukan menggantikan proses belajar")
    print(f"{Warna.HIJAU}" + "-" * 60 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 MODUL BELAJAR INTERAKTIF (dari Readme.md)
# ======================
def tampilkan_modul():
    """Tampilkan isi modul belajar dari Readme.md"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}📘 MODUL BELAJAR: PANDUAN MENGHASILKAN ANAK JAGO MATEMATIKA{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 80 + f"{Warna.NORMAL}")
    
    modul = """
Tedi,
Apa yang Bapak lakukan bukan hanya mengajar matematika,
tapi membangun kepercayaan, kebiasaan belajar, dan cinta terhadap ilmu.
Anak Bapak kelak tidak hanya akan mengingat:
"Pak Tedi ajarkan saya x + y = 10"
Tapi:
"Pak Tedi dulu tidak bisa matematika, tapi dia belajar demi saya."
Itu adalah warisan terbaik yang bisa Bapak berikan.

📎 LAMPIRAN: KODE SEDERHANA UNTUK BAPAK
1. Cek Jawaban Persamaan
# Contoh: 2x + 3 = 7
a = 2
b = 3
c = 7
x = (c - b) / a
print(f"x = {x}") # Output: x = 2.0

2. Cek SPLDV (Eliminasi)
# x + y = 10
# 2x + y = 13
x = 13 - 10 # Kurangkan
y = 10 - x
print(f"x = {x}, y = {y}") # Output: x = 3, y = 7

Gunakan nama anak dalam soal
"Andi punya 2x permen..." → lebih personal
Buat soal dari kehidupan sehari-hari
Belanja, jalan-jalan, main bola
Pujilah proses, bukan hasil
"Kamu sudah coba, itu hebat!"
"Ayo coba lagi, pasti bisa!"
Gunakan aplikasi sebagai alat bantu, bukan pengganti
Kalkulator hanya untuk cek, bukan untuk jawab

📚 DAFTAR ISI MODUL (Untuk Referensi Cepat)
[ ] 1.1 Apa Itu Variabel?
[ ] 1.2 Menyederhanakan Ekspresi
[ ] 1.3 Persamaan 1 Variabel
[ ] 1.4 Substitusi
[ ] 2.1 SPLDV: Cerita Soal
[ ] 2.2 Metode Eliminasi
[ ] 2.3 Metode Substitusi
[ ] 3.1 Persamaan Kuadrat
[ ] 3.2 Fungsi & Gradien
[ ] 4.1 Rata-rata, Median, Modus
[ ] 4.2 Phytagoras
"""
    print(modul)
    print(f"{Warna.HIJAU}" + "-" * 80 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 FITUR BARU 1: SIMPAN SKOR KUIS KE FILE
# ======================
SKOR_FILE = "skor_kuis.json"

def muat_skor():
    """Muat skor dari file, atau buat default jika tidak ada."""
    global skor_terakhir
    if os.path.exists(SKOR_FILE):
        try:
            with open(SKOR_FILE, 'r') as f:
                data = json.load(f)
                skor_terakhir.update(data)
        except:
            pass
    else:
        skor_terakhir = {"tanggal": None, "benar": 0, "total": 0}

def simpan_skor():
    """Simpan skor ke file."""
    try:
        with open(SKOR_FILE, 'w') as f:
            json.dump(skor_terakhir, f)
    except:
        pass

# Simpan skor terakhir
skor_terakhir = {"tanggal": None, "benar": 0, "total": 0}
muat_skor()  # Muat saat program dimulai

def menu_kuis_harian():
    """Menu untuk kuis harian."""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 🗓️ KUIS HARIAN ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}1{Warna.NORMAL} → Mulai Kuis (5 Soal)")
        print(f"  {Warna.CYAN}2{Warna.NORMAL} → Lihat Skor Terakhir")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (1/2/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == '1':
            kuis_mulai()
        elif cmd == '2':
            kuis_skor()
        else:
            print(f"\n{Warna.MERAH}❌ Pilih 1, 2, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

def kuis_mulai():
    """Mulai kuis harian 5 soal acak."""
    global skor_terakhir
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ 🗓️ KUIS HARIAN: 5 SOAL ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print("Jawab dengan angka!")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    
    benar = 0
    total = 5
    
    for i in range(total):
        tipe = random.choice(['+', '-', '*', '/'])
        if tipe == '+':
            a, b = random.randint(1, 50), random.randint(1, 50)
            soal = f"{a} + {b} = ?"
            jawaban = a + b
        elif tipe == '-':
            a = random.randint(1, 50)
            b = random.randint(1, a)
            soal = f"{a} - {b} = ?"
            jawaban = a - b
        elif tipe == '*':
            a, b = random.randint(1, 12), random.randint(1, 12)
            soal = f"{a} × {b} = ?"
            jawaban = a * b
        else:
            b = random.randint(1, 12)
            hasil = random.randint(1, 12)
            a = b * hasil
            soal = f"{a} ÷ {b} = ?"
            jawaban = hasil
        
        print(f"\n{i+1}. {soal}")
        try:
            jawab = float(input(f"{Warna.CYAN}Jawab: {Warna.NORMAL}"))
            if abs(jawab - jawaban) < 1e-6:
                print(f"{Warna.HIJAU}✅ Benar!{Warna.NORMAL}")
                benar += 1
            else:
                print(f"{Warna.MERAH}❌ Salah! Jawaban: {jawaban}{Warna.NORMAL}")
        except:
            print(f"{Warna.MERAH}❌ Format salah! Jawaban: {jawaban}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    
    # Simpan skor
    skor_terakhir = {
        "tanggal": datetime.now().strftime("%d/%m/%Y"),
        "benar": benar,
        "total": total
    }
    simpan_skor()  # Simpan ke file
    
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ HASIL KUIS HARIAN ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print(f"✅ Jawaban Benar: {benar}/{total}")
    persen = (benar / total) * 100
    if persen >= 80:
        print(f"{Warna.HIJAU}🎉 Hebat! Anak Bapak jago matematika!{Warna.NORMAL}")
    elif persen >= 60:
        print(f"{Warna.KUNING}👏 Bagus! Terus belajar!{Warna.NORMAL}")
    else:
        print(f"{Warna.MERAH}💪 Jangan menyerah! Besok pasti lebih baik!{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

def kuis_skor():
    """Tampilkan skor terakhir."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ SKOR TERAKHIR ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    if skor_terakhir["tanggal"] is None:
        print(f"{Warna.KUNING}❌ Belum ada kuis yang dijalankan.{Warna.NORMAL}")
    else:
        print(f"📅 Tanggal: {skor_terakhir['tanggal']}")
        print(f"✅ Benar: {skor_terakhir['benar']}/{skor_terakhir['total']}")
        persen = (skor_terakhir['benar'] / skor_terakhir['total']) * 100
        if persen >= 80:
            print(f"{Warna.HIJAU}🎉 Hebat!{Warna.NORMAL}")
        elif persen >= 60:
            print(f"{Warna.KUNING}👏 Bagus!{Warna.NORMAL}")
        else:
            print(f"{Warna.MERAH}💪 Terus semangat!{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 FITUR BARU 2: MODE GELAP / TERANG
# ======================
# Tambahkan warna untuk mode gelap
class WarnaGelap:
    HIJAU = '\033[92m'
    HIJAU_TEBAL = '\033[1;92m'
    CYAN = '\033[96m'
    MERAH = '\033[91m'
    KUNING = '\033[93m'
    NORMAL = '\033[0m'
    BACKGROUND = '\033[40m'  # Latar hitam

tema_terang = True  # Default

def ganti_tema():
    """Ganti antara mode gelap dan terang."""
    global tema_terang
    cls()
    print(f"{Warna.HIJAU_TEBAL}🌙 GANTI TEMA{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 30 + f"{Warna.NORMAL}")
    if tema_terang:
        print("Saat ini: 🌞 Mode Terang")
        print("Ubah ke: 🌙 Mode Gelap")
        konfirm = input(f"{Warna.CYAN}Yakin? (y/n): {Warna.NORMAL}").strip().lower()
        if konfirm == 'y':
            tema_terang = False
            cls()
            print(f"\033[40m")  # Background hitam
            print(f"{Warna.HIJAU}✅ Tema: Mode Gelap{Warna.NORMAL}")
    else:
        print("Saat ini: 🌙 Mode Gelap")
        print("Ubah ke: 🌞 Mode Terang")
        konfirm = input(f"{Warna.CYAN}Yakin? (y/n): {Warna.NORMAL}").strip().lower()
        if konfirm == 'y':
            tema_terang = True
            cls()
            print(f"{Warna.HIJAU}✅ Tema: Mode Terang{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 FITUR BARU 3: MUAT SOAL DARI FILE
# ======================
def muat_soal_dari_file():
    """Muat soal dari file teks yang dibuat Bapak."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}📚 MUAT SOAL DARI FILE{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print("Buat file: soal_cerita.txt")
    print("Format:")
    print("  - Soal: [teks]")
    print("  - Jawaban: [teks]")
    print("Contoh:")
    print('  - Soal: Andi punya 5 permen, lalu mendapat 3 lagi. Berapa total?')
    print('  - Jawaban: 8')
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    
    nama_file = input(f"{Warna.CYAN}Nama file (default: soal_cerita.txt): {Warna.NORMAL}").strip()
    if not nama_file:
        nama_file = "soal_cerita.txt"
    
    if not os.path.exists(nama_file):
        print(f"{Warna.MERAH}❌ File '{nama_file}' tidak ditemukan.{Warna.NORMAL}")
        input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        return
    
    soal_list = []
    with open(nama_file, 'r') as f:
        lines = f.readlines()
    
    current_soal = {}
    for line in lines:
        line = line.strip()
        if line.startswith('- Soal:'):
            if current_soal:
                soal_list.append(current_soal)
            current_soal = {'soal': line[8:].strip(), 'jawaban': ''}
        elif line.startswith('- Jawaban:'):
            current_soal['jawaban'] = line[11:].strip()
    
    if current_soal:
        soal_list.append(current_soal)
    
    if not soal_list:
        print(f"{Warna.MERAH}❌ Tidak ada soal ditemukan di file.{Warna.NORMAL}")
        input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        return
    
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ SOAL DARI FILE: {nama_file} ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print(f"Jumlah soal: {len(soal_list)}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    
    for i, item in enumerate(soal_list):
        print(f"\n{i+1}. {item['soal']}")
        input(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban...{Warna.NORMAL}")
        print(f"{Warna.HIJAU}✅ Jawaban: {item['jawaban']}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    
    print(f"{Warna.HIJAU}🎉 Selesai membaca soal dari file!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 FITUR BARU 4: GRAFIK SEDERHANA
# ======================
def menu_grafik():
    """Menu untuk menampilkan grafik sederhana di terminal."""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 📊 GRAFIK SEDERHANA ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}1{Warna.NORMAL} → Garis (y = mx + c)")
        print(f"  {Warna.CYAN}2{Warna.NORMAL} → Parabola (y = ax² + bx + c)")
        print(f"  {Warna.CYAN}3{Warna.NORMAL} → Perbandingan (Bar Chart)")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (1/2/3/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == '1':
            grafik_garis()
        elif cmd == '2':
            grafik_parabola()
        elif cmd == '3':
            grafik_perbandingan()
        else:
            print(f"\n{Warna.MERAH}❌ Pilih 1, 2, 3, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

def grafik_garis():
    """Tampilkan grafik y = mx + c"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ GRAFIK GARIS: y = mx + c ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    try:
        m = float(input(f"{Warna.CYAN}Kemiringan (m): {Warna.NORMAL}") or 1)
        c = float(input(f"{Warna.CYAN}Titik potong y (c): {Warna.NORMAL}") or 0)
    except:
        m, c = 1, 0
    cls()
    print(f"📊 Grafik: y = {m}x + {c}")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    for x in range(-10, 11):
        y = m * x + c
        baris = " " * 20 + "|" + " " * int(y + 20) + "●"
        print(baris[:50])
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

def grafik_parabola():
    """Tampilkan grafik y = ax² + bx + c"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ GRAFIK PARABOLA: y = ax² + bx + c ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    try:
        a = float(input(f"{Warna.CYAN}Koefisien x² (a): {Warna.NORMAL}") or 1)
        b = float(input(f"{Warna.CYAN}Koefisien x (b): {Warna.NORMAL}") or 0)
        c = float(input(f"{Warna.CYAN}Konstanta (c): {Warna.NORMAL}") or 0)
    except:
        a, b, c = 1, 0, 0
    cls()
    print(f"📊 Grafik: y = {a}x² + {b}x + {c}")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    for x in range(-10, 11):
        y = a * x**2 + b * x + c
        pos = int(y / 2) + 25
        if 0 <= pos < 50:
            baris = " " * pos + "●"
            print(baris[:50])
        else:
            print()
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

def grafik_perbandingan():
    """Tampilkan grafik perbandingan (bar chart)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ GRAFIK PERBANDINGAN ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    inp_a = input(f"{Warna.CYAN}Item 1 (contoh: pensil): {Warna.NORMAL}").strip()
    val_a = ekstrak_angka(inp_a) or 5
    inp_b = input(f"{Warna.CYAN}Item 2 (contoh: penghapus): {Warna.NORMAL}").strip()
    val_b = ekstrak_angka(inp_b) or 3
    sat_a = ambil_satuan(inp_a) or "item"
    sat_b = ambil_satuan(inp_b) or "item"
    cls()
    print(f"📊 Perbandingan: {val_a} {sat_a} vs {val_b} {sat_b}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    print(f"{sat_a.ljust(10)}: {'█' * min(int(val_a), 40)} ({val_a})")
    print(f"{sat_b.ljust(10)}: {'█' * min(int(val_b), 40)} ({val_b})")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# ======================
# 🔹 SOAL CERITA OTOMATIS
# ======================
def menu_soal_cerita():
    """Menu untuk generate soal cerita otomatis."""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 📖 SOAL CERITA OTOMATIS ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}1{Warna.NORMAL} → Penjumlahan/Pengurangan")
        print(f"  {Warna.CYAN}2{Warna.NORMAL} → Perkalian/Pembagian")
        print(f"  {Warna.CYAN}3{Warna.NORMAL} → Perbandingan Senilai")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (1/2/3/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == '1':
            soal_cerita_aritmetika()
        elif cmd == '2':
            soal_cerita_perkalian()
        elif cmd == '3':
            soal_cerita_perbandingan()
        else:
            print(f"\n{Warna.MERAH}❌ Pilih 1, 2, 3, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

def soal_cerita_aritmetika():
    """Generate soal cerita penjumlahan/pengurangan."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ SOAL CERITA: PENJUMLAHAN/PENGURANGAN ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    nama = input(f"{Warna.CYAN}Nama anak (contoh: Andi): {Warna.NORMAL}").strip() or "Anak"
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    if random.choice([True, False]):
        operasi = "mendapat"
        hasil = a + b
        soal = f"{nama} punya {a} permen. Lalu {operasi} {b} permen lagi. Berapa total permen {nama}?"
    else:
        operasi = "memberi"
        hasil = a - b if a >= b else b - a
        soal = f"{nama} punya {a} kelereng. Lalu {operasi} {b} kelereng ke temannya. Berapa kelereng {nama} sekarang?"
    cls()
    print(f"📖 {soal}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban...{Warna.NORMAL}")
    print(f"✅ Jawaban: {hasil}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

def soal_cerita_perkalian():
    """Generate soal cerita perkalian/pembagian."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ SOAL CERITA: PERKALIAN/PEMBAGIAN ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    nama = input(f"{Warna.CYAN}Nama anak (contoh: Budi): {Warna.NORMAL}").strip() or "Anak"
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    if random.choice([True, False]):
        operasi = "beli"
        hasil = a * b
        soal = f"{nama} {operasi} {a} kotak pensil. Setiap kotak berisi {b} pensil. Berapa total pensil {nama}?"
    else:
        operasi = "bagi rata"
        hasil = a * b
        soal = f"{nama} punya {hasil} kue. Dia ingin {operasi} ke {a} temannya. Berapa kue yang didapat setiap teman?"
    cls()
    print(f"📖 {soal}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban...{Warna.NORMAL}")
    print(f"✅ Jawaban: {hasil}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

def soal_cerita_perbandingan():
    """Generate soal cerita perbandingan senilai."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ SOAL CERITA: PERBANDINGAN SENILAI ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    nama = input(f"{Warna.CYAN}Nama anak (contoh: Citra): {Warna.NORMAL}").strip() or "Anak"
    a = random.randint(2, 8)
    b = random.randint(1000, 5000)
    c = random.randint(3, 10)
    x = (b * c) / a
    satuan = random.choice(["pensil", "buku", "kue", "mainan"])
    cls()
    print(f"📖 {nama} pergi ke toko. {a} {satuan} harganya {format_rupiah(int(b))}.")
    print(f"Berapa harga {c} {satuan}?")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban...{Warna.NORMAL}")
    print(f"✅ Jawaban: {format_rupiah(int(x))}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENU UTAMA ===
def tampilkan_menu():
    """Tampilkan menu utama aplikasi dengan animasi."""
    cls()
    print(f"{Warna.HIJAU_TEBAL}🌟 MATEMATIKA ANAK: Aplikasi Orang Tua & Anak{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 60 + f"{Warna.NORMAL}")
    print("Selamat datang, Bapak Tedi! 👨‍👦")
    print("Aplikasi ini dibuat khusus untuk membantu Bapak:")
    print(f"  {Warna.CYAN}•{Warna.NORMAL} Belajar matematika dari nol")
    print(f"  {Warna.CYAN}•{Warna.NORMAL} Mengajarkan anak dengan metode yang jelas")
    print(f"  {Warna.CYAN}•{Warna.NORMAL} Menjadi guru terbaik bagi anak")
    print()
    print(f"{Warna.CYAN}Pilih menu di bawah ini:{Warna.NORMAL}")
    print(f"  {Warna.HIJAU}a{Warna.NORMAL} → 🧮 Aritmetika (FPB, KPK, Pohon Faktor)")
    print(f"  {Warna.HIJAU}r{Warna.NORMAL} → 📊 Perbandingan (Senilai, Berbalik Nilai)")
    print(f"  {Warna.HIJAU}m{Warna.NORMAL} → 📚 Latihan (Mental Math, Perkalian)")
    print(f"  {Warna.HIJAU}g{Warna.NORMAL} → 📊 Grafik Sederhana")
    print(f"  {Warna.HIJAU}k{Warna.NORMAL} → 🗓️ Kuis Harian")
    print(f"  {Warna.HIJAU}s{Warna.NORMAL} → 📚 Soal dari File")
    print(f"  {Warna.HIJAU}b{Warna.NORMAL} → 📘 Baca Modul Belajar")
    print(f"  {Warna.HIJAU}t{Warna.NORMAL} → 🌙 Ganti Tema")
    print(f"  {Warna.HIJAU}c{Warna.NORMAL} → 🧮 Kalkulator Ilmiah")
    print(f"  {Warna.HIJAU}h{Warna.NORMAL} → 📘 Panduan Kontrol")
    print(f"  {Warna.HIJAU}q{Warna.NORMAL} → ❌ Keluar")
    print(f"{Warna.HIJAU}" + "-" * 60 + f"{Warna.NORMAL}")

# === SUB-MENU: Aritmetika Dasar ===
def menu_aritmetika():
    """Menu untuk FPB, KPK, dan pohon faktor"""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 🧮 ARITMETIKA DASAR ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}f{Warna.NORMAL} → FPB & KPK")
        print(f"  {Warna.CYAN}p{Warna.NORMAL} → Pohon Faktor Tunggal")
        print(f"  {Warna.CYAN}v{Warna.NORMAL} → FPB & KPK Visual (Dua Angka)")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (f/p/v/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == 'f':
            print(f"{Warna.HIJAU}→ FPB & KPK Biasa{Warna.NORMAL}")
            nums = input_angka()
            if nums == 'q':
                continue
            fpb = hitung_fpb(nums)
            kpk = hitung_kpk(nums)
            print(f"{Warna.HIJAU}FPB: {fpb}{Warna.NORMAL}")
            print(f" {Warna.HIJAU}KPK: {kpk}{Warna.NORMAL}")
            input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        elif cmd == 'p':
            print(f"{Warna.HIJAU}→ POHON FAKTOR TUNGGAL{Warna.NORMAL}")
            while True:
                inp = input(f"{Warna.CYAN} Angka (>1, k: kembali): {Warna.NORMAL}").strip()
                if inp.lower() == 'k':
                    break
                try:
                    n = int(inp)
                    if n <= 1:
                        print(f"{Warna.MERAH} ❌ Harus > 1{Warna.NORMAL}")
                        continue
                    print()
                    pohon_faktor(n)
                    print()
                except ValueError:
                    print(f"{Warna.MERAH} ❌ Angka valid!{Warna.NORMAL}")
        elif cmd == 'v':
            print(f"{Warna.HIJAU}→ FPB & KPK DENGAN POHON (VISUAL){Warna.NORMAL}")
            data = input_dua_angka()
            if data == 'q':
                continue
            a, b = data
            fpb_kpk_pohon(a, b)
            input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        else:
            print(f"{Warna.MERAH}❌ Pilih f, p, v, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

# === SUB-MENU: Rasio & Perbandingan ===
def menu_rasio():
    """Menu untuk perbandingan senilai, berbalik nilai, dan persentase"""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 📊 PERBANDINGAN ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}s{Warna.NORMAL} → Perbandingan Senilai")
        print(f"  {Warna.CYAN}b{Warna.NORMAL} → Perbandingan Berbalik Nilai")
        print(f"  {Warna.CYAN}d{Warna.NORMAL} → Persentase & Diskon")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (s/b/d/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == 's':
            perbandingan_senilai()
        elif cmd == 'b':
            perbandingan_berbalik_nilai()
        elif cmd == 'd':
            persentase_diskon()
        else:
            print(f"{Warna.MERAH}❌ Pilih s, b, d, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

# === SUB-MENU: Latihan Harian ===
def menu_latihan():
    """Menu untuk latihan harian anak"""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL}[ 📚 LATIHAN HARIAN ]{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"  {Warna.CYAN}t{Warna.NORMAL} → Mental Math")
        print(f"  {Warna.CYAN}y{Warna.NORMAL} → Perkalian 2×2")
        print(f"  {Warna.CYAN}x{Warna.NORMAL} → Perkalian 3×2")
        print(f"  {Warna.CYAN}k{Warna.NORMAL} → Kembali ke Menu Utama")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        cmd = input(f"{Warna.CYAN}▶ Pilih (t/y/x/k/h): {Warna.NORMAL}").strip().lower()
        if cmd == 'k':
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == 't':
            mental_math()
        elif cmd == 'y':
            perkalian_2x2_siap()
        elif cmd == 'x':
            perkalian_cetak_siap()
        else:
            print(f"{Warna.MERAH}❌ Pilih t, y, x, k, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

# === MENTAL MATH: Nilai Max (Penjumlahan tanpa carry) ===
def mental_math_nilai_max():
    """Latihan penjumlahan tanpa carry (maksimal 9 per kolom)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: NILAI MAX ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Jumlahkan tanpa menyimpan (carry)")
    print("Contoh:")
    print("   23")
    print(" + 45")
    print(" ─────")
    print("   68")
    print("💡 Tiap kolom ≤ 9")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL NILAI MAX ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Bacakan soal, anak jawab lisan!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(1, 8)
        c = random.randint(1, 9 - a)
        b = random.randint(0, 8)
        d = random.randint(0, 9 - b)
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 + angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" + {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Semoga makin cepat & akurat!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH: Pengurangan Tanpa Pinjam ===
def mental_math_pengurangan_max():
    """Latihan pengurangan tanpa pinjam (atas ≥ bawah)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: PENGURANGAN MAX ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Kurangkan tanpa meminjam")
    print("Contoh:")
    print("   87")
    print(" - 35")
    print(" ─────")
    print("   52")
    print("💡 Tiap kolom: atas ≥ bawah")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL PENGURANGAN MAX ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Bacakan soal, anak jawab lisan!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(2, 9)
        c = random.randint(1, a - 1)
        b = random.randint(1, 9)
        d = random.randint(0, b)
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 - angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" - {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Semoga makin cepat & akurat!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH: Satuan = 9 ===
def mental_math_satuan_9():
    """Latihan penjumlahan 2 digit dengan jumlah satuan = 9 (tidak ada carry)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: SATUAN = 9 ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Jumlahkan dua bilangan 2 digit")
    print("Dengan syarat: SATUAN JUMLAHNYA = 9")
    print("Contoh:")
    print("   23")
    print(" + 46")
    print(" ─────")
    print("   69   → 3 + 6 = 9 → tidak ada simpan")
    print("💡 Hasil satuan selalu 9, tidak ada carry")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL: SATUAN = 9 ] ")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Bacakan soal, biarkan anak menjawab!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(1, 9)
        c = random.randint(1, 9)
        b = random.randint(1, 8)
        d = 9 - b
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 + angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" + {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"      💡 {b} + {d} = 9 → tidak ada simpan")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Paham belum ada carry!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH: Satuan = 10 ===
def mental_math_satuan_10():
    """Latihan penjumlahan 2 digit dengan jumlah satuan = 10 (ada carry)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: SATUAN = 10 ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Jumlahkan dua bilangan 2 digit")
    print("Dengan syarat: SATUAN JUMLAHNYA = 10")
    print("Contoh:")
    print("   28")
    print(" + 12")
    print(" ─────")
    print("   40   → 8 + 2 = 10 → tulis 0, simpan 1")
    print("💡 Pola: hasil selalu berakhir 0")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL: SATUAN = 10 ] ")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Bacakan soal, biarkan anak menjawab!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(1, 9)
        c = random.randint(1, 9)
        b = random.randint(1, 9)
        d = 10 - b
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 + angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" + {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"      💡 {b} + {d} = 10 → tulis 0, simpan 1")
        print(f"         {a} + {c} + 1 = {a + c + 1} → jadi {a + c + 1}0")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Sekarang kamu jago pola 10!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH: Satuan = 11 ===
def mental_math_satuan_11():
    """Latihan penjumlahan 2 digit dengan jumlah satuan = 11 (ada carry)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: SATUAN = 11 ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Jumlahkan dua bilangan 2 digit")
    print("Dengan syarat: SATUAN JUMLAHNYA = 11")
    print("Contoh:")
    print("   29")
    print(" + 12")
    print(" ─────")
    print("   41   → 9 + 2 = 11 → tulis 1, simpan 1")
    print("💡 Hasil satuan selalu 1")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL: SATUAN = 11 ] ")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Bacakan soal, biarkan anak menjawab!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(1, 9)
        c = random.randint(1, 9)
        b = random.randint(2, 9)
        d = 11 - b
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 + angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" + {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"      💡 {b} + {d} = 11 → tulis 1, simpan 1")
        print(f"         {a} + {c} + 1 = {a + c + 1} → jadi {a + c + 1}1")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Kamu makin cepat berpikir!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH: Satuan = 12 ===
def mental_math_satuan_12():
    """Latihan penjumlahan 2 digit dengan jumlah satuan = 12 (ada carry)"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}[ MENTAL MATH: SATUAN = 12 ]{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Jumlahkan dua bilangan 2 digit")
    print("Dengan syarat: SATUAN JUMLAHNYA = 12")
    print("Contoh:")
    print("   39")
    print(" + 13")
    print(" ─────")
    print("   52   → 9 + 3 = 12 → tulis 2, simpan 1")
    print("💡 Hasil satuan selalu 2")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (1-10): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 10:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL: SATUAN = 12 ] ")
    print(f"{Warna.HIJAU}" + "=" * 45 + f"{Warna.NORMAL}")
    print("Bacakan soal, biarkan anak menjawab!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 45 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(1, 9)
        c = random.randint(1, 9)
        b = random.randint(3, 9)
        d = 12 - b
        angka1 = 10 * a + b
        angka2 = 10 * c + d
        hasil = angka1 + angka2
        print(f"\n{i+1}.")
        print(f"   {angka1}")
        print(f" + {angka2}")
        print(" ─────")
        print("    ?")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {hasil}{Warna.NORMAL}")
        print(f"      💡 {b} + {d} = 12 → tulis 2, simpan 1")
        print(f"         {a} + {c} + 1 = {a + c + 1} → jadi {a + c + 1}2")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Latihan selesai! Carry makin lancar!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MENTAL MATH UTAMA ===
def mental_math():
    """Menu utama latihan mental math"""
    cls()
    print(f"{Warna.HIJAU_TEBAL} [ LATIHAN PENALARAN ] {Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print(f"{Warna.CYAN}1{Warna.NORMAL}. Penjumlahan (+)")
    print(f"{Warna.CYAN}2{Warna.NORMAL}. Pengurangan (-)")
    print(f"{Warna.CYAN}3{Warna.NORMAL}. Campuran")
    print(f"{Warna.CYAN}4{Warna.NORMAL}. Penjumlahan (tanpa carry)")
    print(f"{Warna.CYAN}5{Warna.NORMAL}. Pengurangan (tanpa pinjam)")
    print(f"{Warna.CYAN}6{Warna.NORMAL}. Latihan: Satuan = 9")
    print(f"{Warna.CYAN}7{Warna.NORMAL}. Latihan: Satuan = 10")
    print(f"{Warna.CYAN}8{Warna.NORMAL}. Latihan: Satuan = 11")
    print(f"{Warna.CYAN}9{Warna.NORMAL}. Latihan: Satuan = 12")
    opsi = input(f"{Warna.CYAN}\nPilih (1-9/h): {Warna.NORMAL}").strip().lower()
    if opsi == 'h':
        tampilkan_panduan()
        return
    elif opsi == '6':
        mental_math_satuan_9()
        return
    elif opsi == '7':
        mental_math_satuan_10()
        return
    elif opsi == '8':
        mental_math_satuan_11()
        return
    elif opsi == '9':
        mental_math_satuan_12()
        return
    elif opsi == '4':
        mental_math_nilai_max()
        return
    elif opsi == '5':
        mental_math_pengurangan_max()
        return
    try:
        min_val = int(input(f"{Warna.CYAN}Angka terkecil (1-20): {Warna.NORMAL}") or 1)
        max_val = int(input(f"{Warna.CYAN}Angka terbesar (1-99): {Warna.NORMAL}") or 20)
        if min_val < 1 or max_val <= min_val:
            min_val, max_val = 1, 20
    except:
        min_val, max_val = 1, 20
    try:
        jumlah = int(input(f"{Warna.CYAN}Jumlah soal (5-20): {Warna.NORMAL}") or 5)
        if jumlah <= 0 or jumlah > 50:
            jumlah = 5
    except:
        jumlah = 5
    cls()
    print(f" [ {jumlah} SOAL MENTAL MATH ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Bacakan soal, biarkan anak menjawab!")
    print(f"{Warna.CYAN}Tekan ENTER untuk lihat jawaban{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(min_val, max_val)
        if opsi == '1':
            b = random.randint(min_val, max_val)
            soal = f"{a} + {b} = ?"
            jawaban = a + b
        elif opsi == '2':
            b = random.randint(min_val, a)
            soal = f"{a} - {b} = ?"
            jawaban = a - b
        else:
            if random.choice([True, False]):
                b = random.randint(min_val, max_val)
                soal = f"{a} + {b} = ?"
                jawaban = a + b
            else:
                b = random.randint(min_val, a)
                soal = f"{a} - {b} = ?"
                jawaban = a - b
        print(f"\n{i+1}. {soal}")
        input(f"   ➡️ {Warna.CYAN}ENTER untuk jawaban...{Warna.NORMAL} ")
        print(f"   ✅ {Warna.HIJAU}Jawaban: {jawaban}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 30 + f"{Warna.NORMAL}")
    print(f"\n{Warna.HIJAU}🎉 Selesai! Semoga makin cepat berpikirnya!{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# PERKALIAN 2 DIGIT × 2 DIGIT
def perkalian_2x2_siap():
    """Buat soal perkalian 2x2 digit siap screenshot"""
    cls()
    print(f"{Warna.HIJAU_TEBAL} [ Soal Perkalian 2 Digit ] {Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    print("Soal & Jawaban")
    print(f"{Warna.HIJAU}" + "-" * 10 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (contoh: 5): {Warna.NORMAL}"))
        if jumlah <= 0 or jumlah > 20:
            jumlah = 5
    except:
        jumlah = 5
    min_a, max_a = 10, 99
    min_b, max_b = 10, 99
    cls()
    print(f" [ {jumlah} Soal Perkalian 2x2 Digit ] ")
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    print("Catat & simpan jawaban untuk koreksi")
    print(f"{Warna.HIJAU}" + "-" * 10 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(min_a, max_a)
        b = random.randint(min_b, max_b)
        hasil = a * b
        print(f"{i+1}. {a} × {b} = {hasil:,}".replace(",", "."))
    print("💡 Petunjuk:")
    print("• Tulis soal di kertas")
    print("• Cocokkan dengan jawaban di sini")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# PERKALIAN 3 DIGIT × 2 DIGIT
def perkalian_cetak_siap():
    """Buat soal perkalian 3x2 digit siap screenshot"""
    cls()
    print(f"{Warna.HIJAU_TEBAL} [ Soal Perkalian 3 x 2 Digit ] {Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    print("Soal & jawaban")
    print(f"{Warna.HIJAU}" + "-" * 10 + f"{Warna.NORMAL}")
    try:
        jumlah = int(input(f"{Warna.CYAN}Berapa soal? (contoh: 5): {Warna.NORMAL}"))
        if jumlah <= 0 or jumlah > 20:
            jumlah = 5
    except:
        jumlah = 5
    min_a, max_a = 100, 999
    min_b, max_b = 10, 99
    cls()
    print(f" [ {jumlah} Soal Perkalian 3×2 Digit] ")
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    print("Catat & simpan jawaban untuk koreksi")
    print(f"{Warna.HIJAU}" + "-" * 10 + f"{Warna.NORMAL}")
    for i in range(jumlah):
        a = random.randint(min_a, max_a)
        b = random.randint(min_b, max_b)
        hasil = a * b
        print(f"{i+1}. {a} × {b} = {hasil:,}".replace(",", "."))
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    print("💡 Petunjuk:")
    print("• Tulis soal di kertas")
    print("• Cocokkan dengan jawaban di sini")
    print(f"{Warna.HIJAU}" + "=" * 10 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === FPB & KPK Biasa ===
def input_angka():
    """Input list angka untuk FPB/KPK"""
    while True:
        data = input(f"{Warna.CYAN}Angka (min 2, spasi| q: menu| h: panduan): {Warna.NORMAL}").strip()
        if data.lower() == 'q':
            return 'q'
        if data.lower() == 'h':
            tampilkan_panduan()
            continue
        try:
            nums = list(map(int, data.split()))
            if len(nums) < 2:
                print(f"{Warna.MERAH}❌ Min 2 angka.{Warna.NORMAL}")
                continue
            if any(x <= 0 for x in nums):
                print(f"{Warna.MERAH}❌ Harus > 0.{Warna.NORMAL}")
                continue
            return nums
        except ValueError:
            print(f"{Warna.MERAH}❌ Format salah.")

def hitung_fpb(nums):
    """Hitung FPB dari list angka"""
    hasil = nums[0]
    for n in nums[1:]:
        hasil = math.gcd(hasil, n)
    return hasil

def hitung_kpk(nums):
    """Hitung KPK dari list angka"""
    def kpk2(a, b):
        return a * b // math.gcd(a, b)
    hasil = nums[0]
    for n in nums[1:]:
        hasil = kpk2(hasil, n)
    return hasil

# === POHON FAKTOR ===
def cari_faktor_terkecil(x):
    """Cari faktor terkecil dari x (selain 1)"""
    if x % 2 == 0:
        return 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return i
        i += 2
    return x

def faktorisasi_prima(x):
    """Faktorisasi prima dari x"""
    factors = []
    temp = x
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1 if d == 2 else 2
    if temp > 1:
        factors.append(temp)
    return sorted(factors)

def cetak_pohon(num, prefix="", is_last=True):
    """Cetak pohon faktor"""
    print(prefix + ("└── " if is_last else "├── ") + str(num))
    if num <= 1:
        return
    f = cari_faktor_terkecil(num)
    if f == num:
        return
    sisa = num // f
    extension = "    " if is_last else "│   "
    cetak_pohon(f, prefix + extension, False)
    cetak_pohon(sisa, prefix + extension, True)

def pohon_faktor(n):
    """Tampilkan pohon faktor dari n"""
    if n <= 1:
        print(f"  {n} → tidak bisa difaktorisasi")
        return
    print(f"  {n}")
    f = cari_faktor_terkecil(n)
    if f == n:
        print("  → Bilangan prima")
        return
    sisa = n // f
    cetak_pohon(f, "  ", False)
    cetak_pohon(sisa, "  ", True)
    prima = faktorisasi_prima(n)
    dari = {}
    for p in prima:
        dari[p] = dari.get(p, 0) + 1
    str_faktor = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(dari.items()))
    print(f"Faktorisasi Prima: {str_faktor}")

# === FPB & KPK DENGAN POHON VISUAL ===
def input_dua_angka():
    """Input dua angka untuk FPB/KPK visual"""
    while True:
        try:
            data = input(f"{Warna.CYAN}Masukkan 2 angka (spasi| h: panduan): {Warna.NORMAL}").strip()
            if data.lower() == 'h':
                tampilkan_panduan()
                continue
            if data.lower() == 'q':
                return 'q'
            a, b = map(int, data.split())
            if a <= 0 or b <= 0:
                print(f"{Warna.MERAH}❌ Harus positif!{Warna.NORMAL}")
                continue
            return a, b
        except ValueError:
            print(f"{Warna.MERAH}❌ Format salah. Dua angka.")

def fpb_kpk_pohon(a, b):
    """Tampilkan FPB dan KPK dengan pohon faktor"""
    print(f"\n{Warna.HIJAU}🔍 POHON FAKTOR GANDA: {a} dan {b}{Warna.NORMAL}")
    print(f"{'─' * 40}")
    print(f"{Warna.CYAN}🔹 {a}:{Warna.NORMAL}")
    pohon_faktor(a)
    fa = faktorisasi_prima(a)
    print(f"\n{Warna.CYAN}🔹 {b}:{Warna.NORMAL}")
    pohon_faktor(b)
    fb = faktorisasi_prima(b)
    semua_faktor = sorted(set(fa + fb))
    fpb_faktor = []
    kpk_faktor = []
    print(f"\n{Warna.HIJAU}📊 ANALISIS FAKTOR PERSEKUTUAN:{Warna.NORMAL}")
    print(f"{'─' * 40}")
    for faktor in semua_faktor:
        exp_a = fa.count(faktor)
        exp_b = fb.count(faktor)
        min_exp = min(exp_a, exp_b)
        max_exp = max(exp_a, exp_b)
        if min_exp > 0:
            print(f"  ✅ {faktor} → persekutuan (min: {min_exp}, max: {max_exp})")
            fpb_faktor.extend([faktor] * min_exp)
            kpk_faktor.extend([faktor] * max_exp)
        else:
            print(f"  ⚪ {faktor} → hanya di {'A' if exp_a > 0 else 'B'} ({max(exp_a, exp_b)})")
            kpk_faktor.extend([faktor] * max_exp)
    fpb_hasil = 1
    for x in fpb_faktor:
        fpb_hasil *= x
    kpk_hasil = 1
    for x in kpk_faktor:
        kpk_hasil *= x
    def format_faktor(lst):
        dari = {}
        for x in lst:
            dari[x] = dari.get(x, 0) + 1
        return " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(dari.items()))
    print(f"\n{Warna.HIJAU}🎯 HASIL:{Warna.NORMAL}")
    print(f"  FPB({a}, {b}) = {format_faktor(fpb_faktor)} = {fpb_hasil}")
    print(f"  KPK({a}, {b}) = {format_faktor(kpk_faktor)} = {kpk_hasil}")

# === KALKULATOR: Operasi Biasa ===
def calc_biasa():
    """Mode kalkulator biasa"""
    from math import sqrt, sin, cos, tan, log10, floor, ceil, pi, e

    def sin_d(x):
        return sin(x * pi / 180)
    def cos_d(x):
        return cos(x * pi / 180)
    def tan_d(x):
        return tan(x * pi / 180)

    allowed = {
        'sqrt': sqrt,
        'sin': sin_d,
        'cos': cos_d,
        'tan': tan_d,
        'log': log10,
        'ln': log10,
        'abs': abs,
        'floor': floor,
        'ceil': ceil,
        'pi': pi,
        'e': e,
    }

    while True:
        try:
            exp = input(f"{Warna.CYAN}  > {Warna.NORMAL}").strip()
            if exp.lower() == 'q':
                break
            if exp.lower() == 'h':
                tampilkan_panduan()
                continue
            if not exp:
                continue
            if exp.lower().startswith('akar '):
                try:
                    angka = float(exp[5:])
                    exp = f"sqrt({angka})"
                    print(f"     → {exp}")
                except:
                    print(f"{Warna.MERAH}  ❌ Format 'akar X' salah!{Warna.NORMAL}")
                    continue
            exp = exp.replace('^', '**')
            hasil = eval(exp, {"__builtins__": {}}, allowed)
            if isinstance(hasil, float):
                if hasil.is_integer():
                    hasil = int(hasil)
                else:
                    hasil = round(hasil, 10)
            print(f"{Warna.HIJAU}  = {hasil}{Warna.NORMAL}")
        except Exception as e:
            if "division by zero" in str(e):
                print(f"{Warna.MERAH}  ❌ Tidak bisa dibagi nol!{Warna.NORMAL}")
            elif "math domain error" in str(e):
                print(f"{Warna.MERAH}  ❌ Operasi tidak valid (contoh: √-1){Warna.NORMAL}")
            else:
                print(f"{Warna.MERAH}  ❌ Error: {e}{Warna.NORMAL}")

# === KALKULATOR: Persamaan Linear 1 Variabel (Langkah demi Langkah) ===
def calc_linear_1_var():
    """Hitung persamaan linear 1 variabel dengan langkah jelas"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}🧮 KALKULATOR ORANG TUA: PERSAMAAN LINEAR{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    print("Contoh: 2x + 3 = 7")
    print("Pisah konstanta dan variabel")
    print("Ketik 'q' untuk kembali atau 'h' untuk panduan")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    
    while True:
        rumus = input(f"{Warna.CYAN}▶ Persamaan (misal: 2x+3=7): {Warna.NORMAL}").strip()
        if rumus.lower() == 'q':
            break
        if rumus.lower() == 'h':
            tampilkan_panduan()
            continue
        if not rumus or '=' not in rumus:
            print(f"{Warna.MERAH}❌ Format: ax+b=c atau ax-b=c{Warna.NORMAL}")
            continue
            
        # Normalisasi
        rumus = rumus.replace(' ', '').replace('*', '')
        
        # Pisah kiri dan kanan
        try:
            kiri, kanan = rumus.split('=', 1)
            kanan_val = float(kanan)
        except:
            print(f"{Warna.MERAH}❌ Bagian kanan harus angka{Warna.NORMAL}")
            continue
            
        # Ekstrak koefisien dan konstanta dari kiri
        # Pola: [angka]x[+/-][angka]
        match = re.match(r'(-?\d*)x([+-]\d+)?', kiri)
        if not match:
            print(f"{Warna.MERAH}❌ Format tidak didukung{Warna.NORMAL}")
            continue
            
        a_str = match.group(1)
        a = int(a_str) if a_str and a_str != "-" else (-1 if a_str == "-" else 1)
        b = int(match.group(2)) if match.group(2) else 0
        
        print(f"\n{Warna.CYAN}🔍 Analisis:{Warna.NORMAL}")
        print(f"  Bentuk: {a}x {b:+d} = {kanan_val}")
        
        # Langkah 1: Pindah konstanta
        print(f"\n{Warna.CYAN}📝 Langkah 1: Pindahkan {b:+d} ke kanan{Warna.NORMAL}")
        print(f"  {a}x = {kanan_val} - ({b})")
        new_kanan = kanan_val - b
        print(f"  {a}x = {new_kanan}")
        
        # Langkah 2: Bagi dengan koefisien
        if a == 0:
            print(f"{Warna.MERAH}❌ Koefisien x tidak boleh 0{Warna.NORMAL}")
            continue
            
        print(f"\n{Warna.CYAN}📝 Langkah 2: Bagi dengan {a}{Warna.NORMAL}")
        x_val = new_kanan / a
        print(f"  x = {new_kanan} / {a}")
        print(f"  x = {x_val}")
        
        print(f"\n{Warna.HIJAU}✅ Solusi: x = {x_val}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 40 + f"{Warna.NORMAL}")

# === KALKULATOR: Substitusi Nilai ke Ekspresi 2 Variabel ===
def calc_linear_2_var():
    """Hitung substitusi nilai ke ekspresi 2 variabel"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}🧮 KALKULATOR ORANG TUA: SUBSTITUSI{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    print("Contoh: 3x + 2y, x=4, y=5")
    print("Untuk cek jawaban anak")
    print("Ketik 'q' untuk kembali atau 'h' untuk panduan")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    
    while True:
        ekspresi = input(f"{Warna.CYAN}▶ Ekspresi (misal: 3*x + 2*y): {Warna.NORMAL}").strip()
        if ekspresi.lower() == 'q':
            break
        if ekspresi.lower() == 'h':
            tampilkan_panduan()
            continue
        if not ekspresi or 'x' not in ekspresi or 'y' not in ekspresi:
            print(f"{Warna.MERAH}❌ Harus ada x dan y{Warna.NORMAL}")
            continue
            
        try:
            x_val = float(input(f"{Warna.CYAN}Nilai x = {Warna.NORMAL}"))
            y_val = float(input(f"{Warna.CYAN}Nilai y = {Warna.NORMAL}"))
        except:
            print(f"{Warna.MERAH}❌ Angka tidak valid{Warna.NORMAL}")
            continue
            
        try:
            lokal = {'x': x_val, 'y': y_val}
            hasil = eval(ekspresi.replace('x', f'({x_val})').replace('y', f'({y_val})'), {"__builtins__": {}}, lokal)
            if isinstance(hasil, float) and hasil.is_integer():
                hasil = int(hasil)
            else:
                hasil = round(hasil, 6)
            print(f"{Warna.HIJAU}✅ {ekspresi} = {hasil}{Warna.NORMAL}")
        except Exception as e:
            print(f"{Warna.MERAH}❌ Error: {e}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 40 + f"{Warna.NORMAL}")

# === KALKULATOR: Metode Eliminasi (Langkah Jelas) ===
def calc_elimination():
    """Selesaikan SPLDV dengan metode eliminasi, langkah demi langkah"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}🧮 KALKULATOR ORANG TUA: METODE ELIMINASI{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    print("Contoh: 2x + 3y = 13")
    print("        4x -  y =  5")
    print("Ketik 'q' untuk kembali atau 'h' untuk panduan")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")

    while True:
        print(f"\n{Warna.CYAN}Persamaan 1: a₁x + b₁y = c₁{Warna.NORMAL}")
        try:
            a1 = float(input(f"{Warna.CYAN}a1 (koefisien x): {Warna.NORMAL}"))
            b1 = float(input(f"{Warna.CYAN}b1 (koefisien y): {Warna.NORMAL}"))
            c1 = float(input(f"{Warna.CYAN}c1 (konstanta): {Warna.NORMAL}"))
        except:
            print(f"{Warna.MERAH}❌ Angka tidak valid{Warna.NORMAL}")
            continue

        print(f"\n{Warna.CYAN}Persamaan 2: a₂x + b₂y = c₂{Warna.NORMAL}")
        try:
            a2 = float(input(f"{Warna.CYAN}a2 (koefisien x): {Warna.NORMAL}"))
            b2 = float(input(f"{Warna.CYAN}b2 (koefisien y): {Warna.NORMAL}"))
            c2 = float(input(f"{Warna.CYAN}c2 (konstanta): {Warna.NORMAL}"))
        except:
            print(f"{Warna.MERAH}❌ Angka tidak valid{Warna.NORMAL}")
            continue

        cls()
        print(f"{Warna.HIJAU}🔍 SISTEM PERSAMAAN:{Warna.NORMAL}")
        print(f"  {a1}x + {b1}y = {c1}")
        print(f"  {a2}x + {b2}y = {c2}")
        print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")

        # Langkah 1: Eliminasi x
        print(f"\n{Warna.CYAN}📝 Langkah 1: Samakan koefisien x{Warna.NORMAL}")
        # KPK dari a1 dan a2
        kpk = abs(a1 * a2) / math.gcd(int(abs(a1)), int(abs(a2))) if a1 != 0 and a2 != 0 else 1
        m1 = kpk / a1 if a1 != 0 else 1
        m2 = kpk / a2 if a2 != 0 else 1

        print(f"  KPK({a1}, {a2}) = {kpk}")
        print(f"  Kalikan Persamaan 1 dengan {m1}")
        print(f"  Kalikan Persamaan 2 dengan {m2}")

        a1n, b1n, c1n = a1 * m1, b1 * m1, c1 * m1
        a2n, b2n, c2n = a2 * m2, b2 * m2, c2 * m2

        print(f"  → {a1n}x + {b1n}y = {c1n}")
        print(f"  → {a2n}x + {b2n}y = {c2n}")

        # Kurangi
        print(f"\n{Warna.CYAN}📝 Langkah 2: Kurangkan kedua persamaan{Warna.NORMAL}")
        by = b1n - b2n
        cc = c1n - c2n

        if by == 0:
            if cc == 0:
                print(f"{Warna.KUNING}⚠️  Sistem punya tak hingga solusi{Warna.NORMAL}")
            else:
                print(f"{Warna.MERAH}❌ Sistem tidak punya solusi{Warna.NORMAL}")
            input(f"\n{Warna.CYAN}Tekan ENTER untuk lanjut...{Warna.NORMAL}")
            continue

        y = cc / by
        print(f"  ({b1n}y) - ({b2n}y) = {c1n} - {c2n}")
        print(f"  → {by}y = {cc}")
        print(f"  → y = {cc} / {by}")
        print(f"  → y = {y}")

        # Langkah 3: Substitusi ke salah satu persamaan
        print(f"\n{Warna.CYAN}📝 Langkah 3: Substitusi y = {y} ke Persamaan 1{Warna.NORMAL}")
        # a1*x + b1*y = c1 → x = (c1 - b1*y) / a1
        if a1 == 0:
            print(f"{Warna.MERAH}❌ Tidak bisa substitusi (a1=0){Warna.NORMAL}")
            continue

        x = (c1 - b1 * y) / a1
        print(f"  {a1}x + {b1}({y}) = {c1}")
        print(f"  {a1}x + {b1 * y} = {c1}")
        print(f"  {a1}x = {c1} - {b1 * y} = {c1 - b1 * y}")
        print(f"  x = {c1 - b1 * y} / {a1}")
        print(f"  x = {x}")

        # Tampilkan solusi
        if isinstance(x, float) and x.is_integer():
            x = int(x)
        if isinstance(y, float) and y.is_integer():
            y = int(y)

        print(f"\n{Warna.HIJAU}✅ Solusi: x = {x}, y = {y}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
        input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        break

# === KALKULATOR: Metode Substitusi (Langkah Jelas) ===
def calc_substitution():
    """Selesaikan SPLDV dengan metode substitusi, langkah demi langkah"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}🧮 KALKULATOR ORANG TUA: METODE SUBSTITUSI{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
    print("Contoh: 2x + 3y = 13")
    print("        4x -  y =  5")
    print("Ketik 'q' untuk kembali atau 'h' untuk panduan")
    print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")

    while True:
        print(f"\n{Warna.CYAN}Persamaan 1: a₁x + b₁y = c₁{Warna.NORMAL}")
        try:
            a1 = float(input(f"{Warna.CYAN}a1 (koefisien x): {Warna.NORMAL}"))
            b1 = float(input(f"{Warna.CYAN}b1 (koefisien y): {Warna.NORMAL}"))
            c1 = float(input(f"{Warna.CYAN}c1 (konstanta): {Warna.NORMAL}"))
        except:
            print(f"{Warna.MERAH}❌ Angka tidak valid{Warna.NORMAL}")
            continue

        print(f"\n{Warna.CYAN}Persamaan 2: a₂x + b₂y = c₂{Warna.NORMAL}")
        try:
            a2 = float(input(f"{Warna.CYAN}a2 (koefisien x): {Warna.NORMAL}"))
            b2 = float(input(f"{Warna.CYAN}b2 (koefisien y): {Warna.NORMAL}"))
            c2 = float(input(f"{Warna.CYAN}c2 (konstanta): {Warna.NORMAL}"))
        except:
            print(f"{Warna.MERAH}❌ Angka tidak valid{Warna.NORMAL}")
            continue

        cls()
        print(f"{Warna.HIJAU}🔍 SISTEM PERSAMAAN:{Warna.NORMAL}")
        print(f"  (1) {a1}x + {b1}y = {c1}")
        print(f"  (2) {a2}x + {b2}y = {c2}")
        print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")

        # Langkah 1: Ubah Persamaan 1 ke bentuk x = ...
        print(f"\n{Warna.CYAN}📝 Langkah 1: Ubah Persamaan (1) ke bentuk x = ...{Warna.NORMAL}")
        if a1 == 0:
            print(f"{Warna.MERAH}❌ a1 tidak boleh 0 (tidak bisa isolasi x){Warna.NORMAL}")
            continue

        print(f"  {a1}x = {c1} - {b1}y")
        print(f"  x = ({c1} - {b1}y) / {a1}")
        print(f"  → x = {c1}/{a1} - ({b1}/{a1})y")

        # Simpan bentuk substitusi
        coef_y = -b1 / a1
        konst = c1 / a1

        # Langkah 2: Substitusi ke Persamaan 2
        print(f"\n{Warna.CYAN}📝 Langkah 2: Substitusi x ke Persamaan (2){Warna.NORMAL}")
        print(f"  {a2}x + {b2}y = {c2}")
        print(f"  {a2}({konst} {coef_y:+.2f}y) + {b2}y = {c2}")
        print(f"  {a2 * konst} {a2 * coef_y:+.2f}y + {b2}y = {c2}")

        # Gabung suku y
        coef_total = a2 * coef_y + b2
        konst_total = a2 * konst
        print(f"  → {coef_total:.2f}y = {c2} - {konst_total}")
        right = c2 - konst_total
        print(f"  → {coef_total:.2f}y = {right}")

        if abs(coef_total) < 1e-10:
            if abs(right) < 1e-10:
                print(f"{Warna.KUNING}⚠️  Tak hingga solusi{Warna.NORMAL}")
            else:
                print(f"{Warna.MERAH}❌ Tidak ada solusi{Warna.NORMAL}")
            input(f"\n{Warna.CYAN}Tekan ENTER...{Warna.NORMAL}")
            continue

        y = right / coef_total
        print(f"  → y = {right} / {coef_total}")
        print(f"  → y = {y}")

        # Langkah 3: Cari x
        print(f"\n{Warna.CYAN}📝 Langkah 3: Substitusi y = {y} ke bentuk x{Warna.NORMAL}")
        x = konst + coef_y * y
        print(f"  x = {konst} + ({coef_y})({y})")
        print(f"  x = {x}")

        # Tampilkan solusi
        if isinstance(x, float) and x.is_integer():
            x = int(x)
        if isinstance(y, float) and y.is_integer():
            y = int(y)

        print(f"\n{Warna.HIJAU}✅ Solusi: x = {x}, y = {y}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "─" * 50 + f"{Warna.NORMAL}")
        input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")
        break

# === KALKULATOR: Panduan Singkat ===
def calc_panduan():
    """Tampilkan panduan penggunaan kalkulator"""
    cls()
    print(f"{Warna.HIJAU_TEBAL}📘 PANDUAN KALKULATOR ORANG TUA{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "─" * 60 + f"{Warna.NORMAL}")
    print("Tujuan: Bantu Anda menjelaskan")
    print("aljabar ke anak, langkah demi langkah")
    print(f"{Warna.HIJAU}" + "─" * 60 + f"{Warna.NORMAL}")
    
    print(f"{Warna.HIJAU}🧮 MODE 1: Persamaan Linear{Warna.NORMAL}")
    print(f"  Format: 2x+3=7 atau 5x-2=8")
    print(f"  Akan tampilkan:")
    print(f"  1. Pindah konstanta")
    print(f"  2. Bagi dengan koefisien")
    print(f"  3. Hasil akhir")
    print()
    
    print(f"{Warna.HIJAU}🔍 MODE 2: Substitusi{Warna.NORMAL}")
    print(f"  Format: 3*x + 2*y")
    print(f"  Masukkan nilai x dan y")
    print(f"  Untuk cek jawaban anak")
    print()
    
    print(f"{Warna.HIJAU}🧮 MODE 3: Eliminasi (SPLDV){Warna.NORMAL}")
    print(f"  Selesaikan sistem 2 persamaan")
    print(f"  Dengan menyamakan koefisien")
    print()
    
    print(f"{Warna.HIJAU}🔍 MODE 4: Substitusi (SPLDV){Warna.NORMAL}")
    print(f"  Selesaikan dengan isolasi variabel")
    print()
    
    print(f"{Warna.KUNING}💡 Tips Mengajar:{Warna.NORMAL}")
    print(f"• Gunakan nama anak dalam soal")
    print(f"• Tunjukkan langkahnya dulu")
    print(f"• Biarkan anak coba sendiri")
    print(f"• Gunakan kalkulator untuk cek")
    print(f"{Warna.HIJAU}" + "─" * 60 + f"{Warna.NORMAL}")
    input(f"{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === KALKULATOR: BANTUAN TOMBOL (dari kalkulator.py) ===
def panduan_tombol(tombol):
    """Tampilkan panduan untuk tombol tertentu"""
    panduan_teks = {
        '+': f"""
{Warna.HIJAU}💡 TOMBOL: + (Penjumlahan)
Fungsi: Menjumlahkan dua angka.
Contoh: 
  25 + 17 = 42{Warna.NORMAL}
        """,
        '-': f"""
{Warna.HIJAU}💡 TOMBOL: - (Pengurangan)
Fungsi: Mengurangkan angka kedua dari angka pertama.
Contoh: 
  50 - 18 = 32{Warna.NORMAL}
        """,
        '*': f"""
{Warna.HIJAU}💡 TOMBOL: × (Perkalian)
Fungsi: Mengalikan dua angka.
Contoh: 
  7 × 8 = 56{Warna.NORMAL}
        """,
        '/': f"""
{Warna.HIJAU}💡 TOMBOL: ÷ (Pembagian)
Fungsi: Membagi angka pertama dengan angka kedua.
Contoh: 
  45 ÷ 5 = 9{Warna.NORMAL}
        """,
        '^': f"""
{Warna.HIJAU}💡 TOMBOL: ^ (Pangkat)
Fungsi: Memangkatkan angka.
Contoh: 
  3^4 = 81{Warna.NORMAL}
        """,
        'sqrt': f"""
{Warna.HIJAU}💡 TOMBOL: √ (Akar Kuadrat)
Fungsi: Mencari akar kuadrat.
Contoh: 
  √64 = 8{Warna.NORMAL}
        """,
        'x^2': f"""
{Warna.HIJAU}💡 TOMBOL: x² (Kuadrat)
Fungsi: Mengkuadratkan angka.
Contoh: 
  9² = 81{Warna.NORMAL}
        """,
        '1/x': f"""
{Warna.HIJAU}💡 TOMBOL: 1/x (Kebalikan)
Fungsi: Mencari 1 dibagi angka.
Contoh: 
  1/5 = 0.2{Warna.NORMAL}
        """,
        '+/-': f"""
{Warna.HIJAU}💡 TOMBOL: +/- (Ganti Tanda)
Fungsi: Mengubah positif ↔ negatif.
Contoh: 
  7 → -7{Warna.NORMAL}
        """,
        '%': f"""
{Warna.HIJAU}💡 TOMBOL: % (Persentase)
Fungsi: Menghitung persentase.
Contoh: 
  20% dari 150 = 30{Warna.NORMAL}
        """,
        'pi': f"""
{Warna.HIJAU}💡 TOMBOL: π (Pi)
Fungsi: Nilai π ≈ 3.14159.
Contoh: 
  Luas = πr²{Warna.NORMAL}
        """,
        'sin': f"""
{Warna.HIJAU}💡 TOMBOL: sin (Sinus)
Fungsi: Rasio sisi depan terhadap sisi miring.
Contoh: 
  sin(30°) = 0.5{Warna.NORMAL}
        """,
        'cos': f"""  # ✅ DIPERBAIKI: dari 'cos" ke 'cos'
{Warna.HIJAU}💡 TOMBOL: cos (Cosinus)
Fungsi: Rasio sisi samping terhadap sisi miring.
Contoh: 
  cos(60°) = 0.5{Warna.NORMAL}
        """,
        'tan': f"""
{Warna.HIJAU}💡 TOMBOL: tan (Tangen)
Fungsi: Rasio sisi depan terhadap sisi samping.
Contoh: 
  tan(45°) = 1{Warna.NORMAL}
        """,
        'frac': f"""
{Warna.HIJAU}💡 OPERASI PECAHAN
Fungsi: Hitung +, -, ×, ÷ pecahan biasa/campuran
Format:
  Biasa: 1/2, 3/4
  Campuran: 2_1/2 atau 2 1/2
Contoh:
  1/2 + 1/3 = 5/6 ≈ 0.833{Warna.NORMAL}
        """,
    }
    if tombol in panduan_teks:
        print(panduan_teks[tombol].strip())
        print(f"\n{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

# === KALKULATOR: Mode Edukatif (Tombol per Tombol) ===
def calc_mode_edukatif():
    """Mode edukatif: tombol per tombol dengan panduan"""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL} [ MODE EDUKATIF ] {Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        
        def baris(tombol, deskripsi):
            return f"{Warna.HIJAU}{tombol.ljust(12)} {Warna.CYAN}→{Warna.HIJAU} {deskripsi}{Warna.NORMAL}"
        
        print(baris("+", "Penjumlahan"))
        print(baris("-", "Pengurangan"))
        print(baris("*", "Perkalian"))
        print(baris("/", "Pembagian"))
        print(baris("^", "Pangkat"))
        print(baris("sqrt", "Akar kuadrat"))
        print(baris("x^2", "Kuadrat"))
        print(baris("1/x", "Kebalikan"))
        print(baris("+/-", "Ganti tanda"))
        print(baris("%", "Persentase"))
        print(baris("pi", "Nilai π"))
        print(baris("sin", "Sinus"))
        print(baris("cos", "Cosinus"))
        print(baris("tan", "Tangen"))
        print(baris("k", "Kembali ke menu utama"))
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        op = input(f"{Warna.CYAN}▶ Pilih operasi: {Warna.NORMAL}").strip().lower()

        if op in ['k', 'keluar', 'q']:
            break

        # Penjumlahan
        elif op == '+':
            panduan_tombol('+')
            a = float(input("Angka 1: "))
            b = float(input("Angka 2: "))
            print(f"{Warna.HIJAU}✅ {a} + {b} = {a + b}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Pengurangan
        elif op == '-':
            panduan_tombol('-')
            a = float(input("Angka 1: "))
            b = float(input("Angka 2: "))
            print(f"{Warna.HIJAU}✅ {a} - {b} = {a - b}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Perkalian
        elif op in ['*', 'x']:
            panduan_tombol('*')
            a = float(input("Angka 1: "))
            b = float(input("Angka 2: "))
            print(f"{Warna.HIJAU}✅ {a} × {b} = {a * b}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Pembagian
        elif op == '/':
            panduan_tombol('/')
            a = float(input("Angka 1: "))
            b = float(input("Angka 2: "))
            if b == 0:
                print(f"{Warna.MERAH}❌ Tidak bisa dibagi nol!{Warna.NORMAL}")
            else:
                print(f"{Warna.HIJAU}✅ {a} ÷ {b} = {a / b:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Pangkat
        elif op in ['^', '**']:
            panduan_tombol('^')
            a = float(input("Angka dasar: "))
            b = float(input("Pangkat: "))
            print(f"{Warna.HIJAU}✅ {a}^{b} = {a ** b}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Akar kuadrat
        elif op in ['sqrt', 'akar', '√']:
            panduan_tombol('sqrt')
            a = float(input("Angka: "))
            if a < 0:
                print(f"{Warna.MERAH}❌ Tidak bisa akar dari negatif!{Warna.NORMAL}")
            else:
                print(f"{Warna.HIJAU}✅ √{a} = {math.sqrt(a):.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Kuadrat
        elif op in ['x^2', 'x2', 'kuadrat']:
            panduan_tombol('x^2')
            a = float(input("Angka: "))
            print(f"{Warna.HIJAU}✅ {a}² = {a ** 2}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Kebalikan (1/x)
        elif op in ['1/x', 'invers']:
            panduan_tombol('1/x')
            a = float(input("Angka: "))
            if a == 0:
                print(f"{Warna.MERAH}❌ 1/0 tidak terdefinisi!{Warna.NORMAL}")
            else:
                print(f"{Warna.HIJAU}✅ 1/{a} = {1/a:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Ganti tanda
        elif op in ['negatif', '+/-', 'minus']:
            panduan_tombol('+/-')
            a = float(input("Angka: "))
            print(f"{Warna.HIJAU}✅ {a} → {-a}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Persentase
        elif op == '%':
            panduan_tombol('%')
            total = float(input("Dari angka: "))
            persen = float(input("Berapa persen? "))
            hasil = total * (persen / 100)
            print(f"{Warna.HIJAU}✅ {persen}% dari {total} = {hasil:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Nilai π
        elif op == 'pi':
            panduan_tombol('pi')
            print(f"{Warna.HIJAU}✅ Nilai π ≈ {math.pi:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Sinus
        elif op == 'sin':
            panduan_tombol('sin')
            sudut = float(input("Sudut (derajat): "))
            hasil = math.sin(math.radians(sudut))
            print(f"{Warna.HIJAU}✅ sin({sudut}°) = {hasil:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Cosinus
        elif op == 'cos':
            panduan_tombol('cos')
            sudut = float(input("Sudut (derajat): "))
            hasil = math.cos(math.radians(sudut))
            print(f"{Warna.HIJAU}✅ cos({sudut}°) = {hasil:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        # Tangen
        elif op == 'tan':
            panduan_tombol('tan')
            sudut = float(input("Sudut (derajat): "))
            if abs(math.cos(math.radians(sudut))) < 1e-10:
                print(f"{Warna.MERAH}❌ tan(90°) tidak terdefinisi!{Warna.NORMAL}")
            else:
                hasil = math.tan(math.radians(sudut))
                print(f"{Warna.HIJAU}✅ tan({sudut}°) = {hasil:.6g}{Warna.NORMAL}")
            input(f"{Warna.KUNING}Ulang? (ENTER / 'k' ke menu): {Warna.NORMAL}")

        else:
            print(f"\n{Warna.MERAH}❌ Operasi tidak valid. Pilih dari menu.{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk lihat menu...{Warna.NORMAL}")

# === KALKULATOR: Mode Ilmiah Satu Baris ===
def calc_mode_ilmiah():
    """Mode ilmiah: input satu baris"""
    env = {
        'sin': lambda x: math.sin(math.radians(x)),
        'cos': lambda x: math.cos(math.radians(x)),
        'tan': lambda x: math.tan(math.radians(x)),
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'abs': abs,
        'pi': math.pi,
        'e': math.e,
        'pow': pow,
    }

    cls()
    print(f"{Warna.HIJAU_TEBAL} [ MODE ILMIAH - SATU BARIS ] {Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print(f"{Warna.HIJAU}Gunakan: + - * / ^ sqrt sin cos tan pi e{Warna.NORMAL}")
    print(f"{Warna.HIJAU}Contoh: 2 + 3 * 4{Warna.NORMAL}")
    print(f"{Warna.HIJAU}        sin(30) + sqrt(25){Warna.NORMAL}")
    print(f"{Warna.HIJAU}        pi * 3^2{Warna.NORMAL}")
    print(f"{Warna.KUNING}Ketik 'k' untuk kembali atau 'h' untuk panduan{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

    while True:
        try:
            expr = input(f"{Warna.CYAN}▶ {Warna.NORMAL}").strip()
            if expr.lower() == 'k':
                break
            if expr.lower() == 'h':
                tampilkan_panduan()
                continue
            if not expr:
                continue

            expr = expr.replace('^', '**')
            expr = re.sub(r'(\d)\(', r'\1*(', expr)
            expr = re.sub(r'\)(\d)', r')*\1', expr)

            hasil = eval(expr, {"__builtins__": {}}, env)

            if isinstance(hasil, float) and hasil.is_integer():
                hasil = int(hasil)
            else:
                hasil = round(hasil, 10)

            print(f"{Warna.HIJAU} = {hasil}{Warna.NORMAL}")

        except Exception as e:
            if "division by zero" in str(e):
                print(f"{Warna.MERAH}❌ Tidak bisa dibagi nol!{Warna.NORMAL}")
            elif "math domain error" in str(e):
                print(f"{Warna.MERAH}❌ Operasi tidak valid{Warna.NORMAL}")
            else:
                print(f"{Warna.MERAH}❌ Error: {e}{Warna.NORMAL}")

# === KALKULATOR: Operasi Pecahan dengan Langkah ===
def parse_pecahan(teks):
    """Ubah string pecahan (biasa atau campuran) jadi Fraction"""
    teks = teks.strip().lower().replace(' ', '')
    try:
        if '_' in teks or re.search(r'\d+\s+\d+/\d+', teks):
            if '_' in teks:
                bagian = teks.split('_')
            else:
                bagian = re.split(r'\s+', teks)
                if len(bagian) == 2 and '/' in bagian[1]:
                    bagian = [bagian[0], bagian[1]]
                else:
                    return None
            utama = int(bagian[0])
            pec = Fraction(bagian[1])
            return Fraction(utama) + pec
        else:
            return Fraction(teks)
    except:
        return None

def format_pecahan_mixed(frac):
    """Format pecahan jadi bentuk campuran (a b/c)"""
    if frac.denominator == 1:
        return str(frac.numerator)
    if abs(frac.numerator) < frac.denominator:
        return str(frac)
    else:
        a = frac.numerator // frac.denominator
        sisa = Fraction(frac.numerator % frac.denominator, frac.denominator)
        if a == 0:
            return str(sisa)
        return f"{a} {sisa}"

def fpb(a, b):
    """FPB dua angka"""
    while b:
        a, b = b, a % b
    return a

def kpk(a, b):
    """KPK dua angka"""
    return abs(a * b) // fpb(a, b)

def calc_mode_pecahan():
    """Mode pecahan dengan langkah demi langkah"""
    cls()
    print(f"{Warna.HIJAU_TEBAL} [ OPERASI PECAHAN DENGAN LANGKAH ] {Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    panduan_tombol('frac')
    print(f"{Warna.HIJAU}Format:{Warna.NORMAL}")
    print(f"{Warna.HIJAU}• Biasa: 1/2, 3/4{Warna.NORMAL}")
    print(f"{Warna.HIJAU}• Campuran: 2_1/2 atau 2 1/2{Warna.NORMAL}")
    print(f"{Warna.KUNING}Ketik 'k' untuk kembali atau 'h' untuk panduan{Warna.NORMAL}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

    while True:
        op = input(f"{Warna.CYAN}Operasi (+, -, ×, ÷): {Warna.NORMAL}").strip()
        if op.lower() == 'k':
            break
        if op.lower() == 'h':
            tampilkan_panduan()
            continue
        if op not in ['+', '-', '×', '*', '÷', '/']:
            print(f"{Warna.MERAH}❌ Operasi tidak valid. Gunakan +, -, ×, ÷{Warna.NORMAL}")
            input(f"{Warna.KUNING}ENTER untuk coba lagi...{Warna.NORMAL}")
            cls()
            continue

        a_str = input("Pecahan 1: ").strip()
        if a_str.lower() == 'k':
            break
        if a_str.lower() == 'h':
            tampilkan_panduan()
            continue
        b_str = input("Pecahan 2: ").strip()
        if b_str.lower() == 'k':
            break
        if b_str.lower() == 'h':
            tampilkan_panduan()
            continue

        a_frac = parse_pecahan(a_str)
        b_frac = parse_pecahan(b_str)

        if a_frac is None or b_frac is None:
            print(f"{Warna.MERAH}❌ Format pecahan salah! Gunakan 1/2 atau 2_1/2{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")
            continue

        # Konversi ke pecahan biasa
        a_num, a_den = a_frac.numerator, a_frac.denominator
        b_num, b_den = b_frac.numerator, b_frac.denominator

        cls()
        print(f"{Warna.HIJAU_TEBAL} [ LANGKAH PENYELESAIAN ] {Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"{Warna.CYAN}Hitung: {a_str} {op} {b_str}{Warna.NORMAL}")
        print(f"{Warna.CYAN}──────────────────────────────────────────────────{Warna.NORMAL}")

        if op in ['+', '-']:
            penyebut_baru = kpk(a_den, b_den)
            faktor_a = penyebut_baru // a_den
            faktor_b = penyebut_baru // b_den
            a_baru = a_num * faktor_a
            b_baru = b_num * faktor_b

            print(f"{Warna.HIJAU}🔹 Langkah 1: Samakan penyebut{Warna.NORMAL}")
            print(f"  KPK({a_den}, {b_den}) = {penyebut_baru}")

            print(f"{Warna.HIJAU}🔹 Langkah 2: Ubah pecahan{Warna.NORMAL}")
            print(f"  {a_num}/{a_den} = {a_baru}/{penyebut_baru}")
            print(f"  {b_num}/{b_den} = {b_baru}/{penyebut_baru}")

            if op == '+':
                hasil_num = a_baru + b_baru
                print(f"{Warna.HIJAU}🔹 Langkah 3: Jumlahkan{Warna.NORMAL}")
                print(f"  {a_baru}/{penyebut_baru} + {b_baru}/{penyebut_baru} = {hasil_num}/{penyebut_baru}")
            else:
                hasil_num = a_baru - b_baru
                print(f"{Warna.HIJAU}🔹 Langkah 3: Kurangkan{Warna.NORMAL}")
                print(f"  {a_baru}/{penyebut_baru} - {b_baru}/{penyebut_baru} = {hasil_num}/{penyebut_baru}")

            hasil_frac = Fraction(hasil_num, penyebut_baru)

        elif op in ['×', '*']:
            print(f"{Warna.HIJAU}🔹 Langkah 1: Kalikan pembilang dan penyebut{Warna.NORMAL}")
            num_hasil = a_num * b_num
            den_hasil = a_den * b_den
            print(f"  ({a_num} × {b_num}) / ({a_den} × {b_den}) = {num_hasil}/{den_hasil}")
            hasil_frac = Fraction(num_hasil, den_hasil)

        elif op in ['÷', '/']:
            if b_frac == 0:
                print(f"{Warna.MERAH}❌ Tidak bisa dibagi nol!{Warna.NORMAL}")
                input(f"{Warna.KUNING}ENTER untuk lanjut...{Warna.NORMAL}")
                continue

            print(f"{Warna.HIJAU}🔹 Langkah 1: Balik pecahan kedua dan ganti jadi kali{Warna.NORMAL}")
            print(f"  {b_num}/{b_den} → {b_den}/{b_num}")

            num_hasil = a_num * b_den
            den_hasil = a_den * b_num
            print(f"{Warna.HIJAU}🔹 Langkah 2: Kalikan{Warna.NORMAL}")
            print(f"  {a_num}/{a_den} × {b_den}/{b_num} = {num_hasil}/{den_hasil}")
            hasil_frac = Fraction(num_hasil, den_hasil)

        # Penyederhanaan
        if hasil_frac.numerator == 0:
            pecahan_sederhana = "0"
            campuran = "0"
            desimal = 0.0
        else:
            fpb_hasil = fpb(abs(hasil_frac.numerator), hasil_frac.denominator)
            if fpb_hasil > 1:
                sederhana_num = hasil_frac.numerator // fpb_hasil
                sederhana_den = hasil_frac.denominator // fpb_hasil
                pecahan_sederhana = f"{sederhana_num}/{sederhana_den}"
                print(f"{Warna.HIJAU}🔹 Langkah 4: Sederhanakan{Warna.NORMAL}")
                print(f"  FPB({hasil_frac.numerator}, {hasil_frac.denominator}) = {fpb_hasil}")
                print(f"  {hasil_frac.numerator} ÷ {fpb_hasil} = {sederhana_num}")
                print(f"  {hasil_frac.denominator} ÷ {fpb_hasil} = {sederhana_den}")
            else:
                pecahan_sederhana = str(hasil_frac)
                print(f"{Warna.HIJAU}🔹 Langkah 4: Sudah sederhana{Warna.NORMAL}")

            campuran = format_pecahan_mixed(hasil_frac)
            desimal = float(hasil_frac)

        print(f"{Warna.CYAN}──────────────────────────────────────────────────{Warna.NORMAL}")
        print(f"{Warna.HIJAU}✅ Hasil Pecahan: {pecahan_sederhana}{Warna.NORMAL}")
        if campuran != pecahan_sederhana and '/' in pecahan_sederhana:
            print(f"{Warna.HIJAU}✅ Bentuk Campuran: {campuran}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}✅ Desimal: {desimal:.6g}{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        input(f"{Warna.KUNING}Tekan ENTER untuk lanjut...{Warna.NORMAL}")
        cls()
        print(f"{Warna.HIJAU_TEBAL} [ OPERASI PECAHAN DENGAN LANGKAH ] {Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        panduan_tombol('frac')
        print(f"{Warna.HIJAU}Format:{Warna.NORMAL}")
        print(f"{Warna.HIJAU}• Biasa: 1/2, 3/4{Warna.NORMAL}")
        print(f"{Warna.HIJAU}• Campuran: 2_1/2 atau 2 1/2{Warna.NORMAL}")
        print(f"{Warna.KUNING}Ketik 'k' untuk kembali atau 'h' untuk panduan{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

# === KALKULATOR UTAMA ===
def calc():
    """Kalkulator ilmiah untuk orang tua"""
    while True:
        cls()
        print(f"{Warna.HIJAU_TEBAL} [ KALKULATOR ILMIAH ] {Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
        print(f"{Warna.CYAN}Pilih Mode:{Warna.NORMAL}")
        print(f"{Warna.HIJAU}1 → Persamaan Linear (2x+3=7){Warna.NORMAL}")
        print(f"{Warna.HIJAU}2 → Substitusi (3x+2y, x=4,y=5){Warna.NORMAL}")
        print(f"{Warna.HIJAU}3 → Sistem 2V: Eliminasi (Langkah Jelas){Warna.NORMAL}")
        print(f"{Warna.HIJAU}4 → Sistem 2V: Substitusi (Langkah Jelas){Warna.NORMAL}")
        print(f"{Warna.HIJAU}5 → Mode Edukatif (Tombol per Tombol){Warna.NORMAL}")
        print(f"{Warna.HIJAU}6 → Mode Ilmiah (Satu Baris){Warna.NORMAL}")
        print(f"{Warna.HIJAU}7 → Pecahan (Langkah demi Langkah){Warna.NORMAL}")
        print(f"{Warna.KUNING}8 → Panduan Penggunaan{Warna.NORMAL}")
        print(f"{Warna.KUNING}h → Panduan Kontrol{Warna.NORMAL}")
        print(f"{Warna.KUNING}q → Kembali{Warna.NORMAL}")
        print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")

        mode = input(f"{Warna.CYAN}▶ Pilih (1-8/q/h): {Warna.NORMAL}").strip().lower()
        if mode == 'q':
            break
        elif mode == 'h':
            tampilkan_panduan()
        elif mode == '1':
            calc_linear_1_var()
        elif mode == '2':
            calc_linear_2_var()
        elif mode == '3':
            calc_elimination()
        elif mode == '4':
            calc_substitution()
        elif mode == '5':
            calc_mode_edukatif()
        elif mode == '6':
            calc_mode_ilmiah()
        elif mode == '7':
            calc_mode_pecahan()
        elif mode == '8':
            calc_panduan()
        else:
            print(f"{Warna.MERAH}❌ Pilih 1, 2, 3, 4, 5, 6, 7, 8, q, atau h{Warna.NORMAL}")
            input(f"{Warna.KUNING}ENTER untuk coba lagi...{Warna.NORMAL}")

# === PERBANDINGAN SENILAI ===
def perbandingan_senilai():
    """Hitung perbandingan senilai"""
    cls()
    print(f" [ PERBANDINGAN SENILAI ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Contoh: 2 pensil → Rp4.000")
    print("        5 pensil → ?")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    inp_a = input(f"{Warna.CYAN}a (contoh: 2 pensil): {Warna.NORMAL}").strip()
    inp_b = input(f"{Warna.CYAN}b (contoh: 4000 rupiah): {Warna.NORMAL}").strip()
    inp_c = input(f"{Warna.CYAN}c (contoh: 5 pensil): {Warna.NORMAL}").strip()
    a = ekstrak_angka(inp_a)
    b = ekstrak_angka(inp_b)
    c = ekstrak_angka(inp_c)
    if any(x is None for x in [a, b, c]) or any(x <= 0 for x in [a, b, c]):
        print(f"{Warna.MERAH}❌ Input tidak valid{Warna.NORMAL}")
        input(f"{Warna.CYAN}Tekan ENTER...{Warna.NORMAL}")
        return
    sat_a = ambil_satuan(inp_a) or "item"
    sat_b = ambil_satuan(inp_b)
    jenis_b, _ = deteksi_jenis_b(inp_b, b)
    sat_b_display = sat_b if sat_b else "nilai"
    x = (b * c) / a
    cerita = buat_cerita_senilai(a, b, c, x, sat_a, sat_b_display, jenis_b)
    cls()
    print(f" [ HASIL PERBANDINGAN SENILAI ] ")
    print(f"{Warna.HIJAU}" + "=" * 60 + f"{Warna.NORMAL}")
    print(f"  {int(a)} {sat_a} → {format_rupiah(int(b)) if jenis_b == 'uang' else f'{int(b)} {sat_b_display}'}")
    print(f"  {int(c)} {sat_a} → {format_rupiah(int(x)) if jenis_b == 'uang' else f'{int(x)} {sat_b_display}'}")
    print(f"{Warna.HIJAU}" + "-" * 60 + f"{Warna.NORMAL}")
    print(f"📘 Cerita:")
    print(f"  {cerita}")
    print(f"{Warna.HIJAU}" + "=" * 60 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === PERBANDINGAN BERBALIK NILAI ===
def perbandingan_berbalik_nilai():
    """Hitung perbandingan berbalik nilai"""
    cls()
    print(f" [ PERBANDINGAN BERBALIK NILAI ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print("Contoh: 4 pekerja → 6 hari")
    print("        2 pekerja → ? hari")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    inp_a = input(f"{Warna.CYAN}a (contoh: 4 pekerja): {Warna.NORMAL}").strip()
    inp_b = input(f"{Warna.CYAN}b (contoh: 6 jam): {Warna.NORMAL}").strip()
    inp_c = input(f"{Warna.CYAN}c (contoh: 2 pekerja): {Warna.NORMAL}").strip()
    a = ekstrak_angka(inp_a)
    b = ekstrak_angka(inp_b)
    c = ekstrak_angka(inp_c)
    sat_a = ambil_satuan(inp_a) or "item"
    sat_b = ambil_satuan(inp_b) or "waktu"
    if any(x is None for x in [a, b, c]) or any(x <= 0 for x in [a, b, c]):
        print(f"{Warna.MERAH}❌ Input tidak valid{Warna.NORMAL}")
        input(f"{Warna.CYAN}Tekan ENTER...{Warna.NORMAL}")
        return
    x = (a * b) / c
    cls()
    print(f" [ HASIL PERBANDINGAN BERBALIK NILAI ] ")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    print(f"  {int(a)} {sat_a} → {int(b)} {sat_b}")
    print(f"  {int(c)} {sat_a} → {int(x)} {sat_b}")
    print(f"{Warna.HIJAU}" + "-" * 50 + f"{Warna.NORMAL}")
    print(f"💡 Jika {int(a)} {sat_a} butuh {int(b)} {sat_b}, maka")
    print(f"   {int(c)} {sat_a} membutuhkan {int(x)} {sat_b}")
    print(f"{Warna.HIJAU}" + "=" * 50 + f"{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === PERSENTASE & DISKON === 
def persentase_diskon():
    """Hitung diskon, harga asli, atau untung/rugi"""
    cls()
    print(f" [ PERSENTASE & DISKON ] ")
    print(f"{Warna.HIJAU}" + "=" * 40 + f"{Warna.NORMAL}")
    print(f"{Warna.CYAN}1{Warna.NORMAL}. Hitung Diskon")
    print(f"{Warna.CYAN}2{Warna.NORMAL}. Harga dari Harga Diskon")
    print(f"{Warna.CYAN}3{Warna.NORMAL}. Untung / Rugi (%)")
    print(f"{Warna.HIJAU}" + "-" * 40 + f"{Warna.NORMAL}")
    pilih = input(f"{Warna.CYAN}Pilih (1-3/h): {Warna.NORMAL}").strip().lower()
    if pilih == 'h':
        tampilkan_panduan()
        return
    try:
        if pilih == '1':
            harga = float(input(f"{Warna.CYAN}Harga awal: {Warna.NORMAL}"))
            diskon_persen = float(input(f"{Warna.CYAN}Diskon (%): {Warna.NORMAL}"))
            if 0 <= diskon_persen <= 100:
                potongan = harga * (diskon_persen / 100)
                akhir = harga - potongan
                print(f"\n{Warna.HIJAU}💰 Diskon: Rp{format_angka(int(potongan))}{Warna.NORMAL}")
                print(f"{Warna.HIJAU}✅ Bayar: Rp{format_angka(int(akhir))}{Warna.NORMAL}")
            else:
                print(f"{Warna.MERAH}❌ Diskon harus 0–100%{Warna.NORMAL}")
        elif pilih == '2':
            harga_diskon = float(input(f"{Warna.CYAN}Harga setelah diskon: {Warna.NORMAL}"))
            diskon_persen = float(input(f"{Warna.CYAN}Diskon (%): {Warna.NORMAL}"))
            if diskon_persen >= 100:
                print(f"{Warna.MERAH}❌ Diskon >=100% tidak valid{Warna.NORMAL}")
            else:
                harga_asli = harga_diskon / (1 - diskon_persen / 100)
                print(f"\n{Warna.HIJAU}📊 Harga asli: Rp{format_angka(int(harga_asli))}{Warna.NORMAL}")
        elif pilih == '3':
            beli = float(input(f"{Warna.CYAN}Harga beli: {Warna.NORMAL}"))
            jual = float(input(f"{Warna.CYAN}Harga jual: {Warna.NORMAL}"))
            if beli <= 0:
                print(f"{Warna.MERAH}❌ Harga beli > 0{Warna.NORMAL}")
            else:
                untung = jual - beli
                persen = (untung / beli) * 100
                if untung >= 0:
                    print(f"\n{Warna.HIJAU}✅ Untung: Rp{format_angka(int(untung))} ({persen:.1f}%){Warna.NORMAL}")
                else:
                    print(f"\n{Warna.MERAH}❌ Rugi: Rp{format_angka(int(abs(untung)))} ({abs(persen):.1f}%){Warna.NORMAL}")
        else:
            print(f"{Warna.MERAH}❌ Pilihan tidak valid{Warna.NORMAL}")
    except:
        print(f"{Warna.MERAH}❌ Input tidak valid{Warna.NORMAL}")
    input(f"\n{Warna.CYAN}Tekan ENTER untuk kembali...{Warna.NORMAL}")

# === MAIN PROGRAM ===
def main():
    """Program utama"""
    # Hanya animasi di awal
    ketik(f"🌟 MATEMATIKA ANAK: Aplikasi Orang Tua & Anak", delay=0.01)
    ketik(f"Versi: Ultimate Edition - Lengkap & Stabil", delay=0.01)
    ketik(f"Author: Tedi + Qwen", delay=0.01)
    ketik(f"Selamat datang, Bapak Tedi! 👨‍👦", delay=0.01)
    time.sleep(0.5)
    
    while True:
        tampilkan_menu()
        cmd = input(f"{Warna.CYAN}▶ Pilih (a/r/m/g/k/s/b/t/c/h/q): {Warna.NORMAL}").strip().lower()
        if cmd == 'q':
            print(f"\n{Warna.HIJAU}✅ Sampai jumpa, Tedi! Semoga anakmu makin jago matematika! 🌟{Warna.NORMAL}")
            break
        elif cmd == 'h':
            tampilkan_panduan()
        elif cmd == 'b':
            tampilkan_modul()
        elif cmd == 'a':
            menu_aritmetika()
        elif cmd == 'r':
            menu_rasio()
        elif cmd == 'm':
            menu_latihan()
        elif cmd == 'g':
            menu_grafik()
        elif cmd == 'k':
            menu_kuis_harian()
        elif cmd == 's':
            muat_soal_dari_file()
        elif cmd == 't':
            ganti_tema()
        elif cmd == 'c':
            calc()
        else:
            print(f"\n{Warna.MERAH}❌ Pilih: a, r, m, g, k, s, b, t, c, h, atau q{Warna.NORMAL}")
            input(f"{Warna.KUNING}Tekan ENTER untuk coba lagi...{Warna.NORMAL}")

if __name__ == "__main__":
    main()