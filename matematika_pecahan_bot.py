# matematika_anak.py
# Bot Matematika Anak - Versi: Simpel, Cepat, Tanpa Ribet
# 📌 Author: Bapak Tedi + Qwen
# 📌 Tujuan: Anak hanya klik tombol, tidak ketik perintah

"""
📘 MANUAL PENGGUNAAN BOT MATEMATIKA ANAK (Untuk Orang Tua & Guru)

Bot ini dirancang agar **anak tidak perlu mengetik perintah**.
Cukup klik tombol!

───────────────────────────────────────────────────────────────
🎯 TUJUAN UTAMA
───────────────────────────────────────────────────────────────
- Anak belajar tanpa ketik /login, /menu, /nilai
- Cukup ketik `/mulai`, lalu klik tombol
- Progres tetap disimpan
- Cocok untuk anak SD

───────────────────────────────────────────────────────────────
📌 ALUR BARU (Untuk Anak)
───────────────────────────────────────────────────────────────
1. Buka Telegram, cari bot Anda
2. Ketik: /mulai
3. Klik: 🔐 LOGIN
4. Masukkan kode: TEDI01
5. Klik: 📚 LATIHAN
6. Pilih jenis soal
7. Kerjakan → lihat hasil
8. Klik: 📊 NILAI → cek progres

Semua dalam satu antarmuka! Tidak perlu hafal perintah.

───────────────────────────────────────────────────────────────
🔧 FITUR UTAMA
───────────────────────────────────────────────────────────────
1. ✅ /mulai → tampilkan semua menu
2. ✅ Login dengan kode (TEDI01 → TEDI KUSNIADI)
3. ✅ Soal: Penjumlahan, Pengurangan, Satuan 9-12
4. ✅ Progres & Nilai dengan bintang
5. ✅ Tombol "Kembali" di setiap layar

───────────────────────────────────────────────────────────────
💡 TIPS UNTUK BAPAK
───────────────────────────────────────────────────────────────
- Ajarkan anak: "Klik /mulai, lalu pilih"
- Tidak perlu jelaskan perintah
- Fokus pada proses belajar, bukan teknis bot

Tedi,
Anak bukan programmer. Mereka butuh kemudahan.
Dengan menu ini, anak bisa fokus belajar, bukan menghafal perintah.
Itu adalah langkah kecil, tapi dampaknya besar.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random
import json
import os
import re
from fractions import Fraction

# 🔑 GANTI TOKEN INI
TOKEN = "8356866070:AAH9AYDExfXkmIHE14rje_PwYLaa7r-1SVs"

# 📁 File untuk simpan data
SKOR_FILE = "skor.json"
KODE_FILE = "kode.json"

# 📝 Data sementara untuk tiap user
user_data = {}

# 🎨 Fungsi: Ubah angka ke emoji
def ke_emoji(n):
    emoji_map = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    return ''.join(emoji_map[d] for d in str(n))

# 🌟 Fungsi: Buat visual bintang berdasar nilai
def bintang_nilai(nilai):
    if nilai >= 90: return "⭐⭐⭐⭐⭐"
    elif nilai >= 75: return "⭐⭐⭐⭐☆"
    elif nilai >= 60: return "⭐⭐⭐☆☆"
    elif nilai >= 40: return "⭐⭐☆☆☆"
    elif nilai >= 20: return "⭐☆☆☆☆"
    else: return "☆☆☆☆☆"

# 💾 Muat data dari file
def muat_skor():
    global user_data
    if os.path.exists(SKOR_FILE):
        try:
            with open(SKOR_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    user_data = {}
                    return
                raw = json.loads(content)
                user_data = {int(k): v for k, v in raw.items()}
        except Exception as e:
            print(f"Gagal muat skor.json: {e}")
            user_data = {}
    else:
        user_data = {}

# 💾 Simpan data ke file
def simpan_skor():
    try:
        with open(SKOR_FILE, 'w') as f:
            data_str = {str(k): v for k, v in user_data.items()}
            json.dump(data_str, f, indent=2)
    except Exception as e:
        print(f"Gagal simpan skor.json: {e}")

# 🔐 Muat kode login
def muat_kode():
    if os.path.exists(KODE_FILE):
        try:
            with open(KODE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "TEDI01": "TEDI KUSNIADI",
        "SITI02": "SITI AISAH",
        "ANDI03": "ANDI SAPUTRA",
        "BUDI04": "BUDI NUGRAHA"
    }

# 🎯 Perintah /start (hanya sambutan)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 <b>Halo! Selamat datang di Bot Matematika Anak!</b>\n\n"
        "Ketik /mulai untuk mulai belajar dengan menu interaktif.",
        parse_mode="HTML"
    )

# 🎯 Perintah /mulai → tampilkan menu utama
async def mulai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 <b>MENU UTAMA</b>\n"
        "Pilih yang ingin Anda lakukan:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔐 LOGIN", callback_data="login")],
            [InlineKeyboardButton("📚 LATIHAN", callback_data="menu")],
            [InlineKeyboardButton("📊 NILAI", callback_data="nilai")],
            [InlineKeyboardButton("🧮 KALKULATOR", callback_data="kalkulator")]
        ]),
        parse_mode="HTML"
    )

# 📊 Tampilkan nilai
async def tampilkan_nilai(update, user_id):
    data = user_data[user_id]
    nama = data.get("nama", "ANAK")
    benar = data.get("total_benar", 0)
    total = data.get("total_soal", 0)
    kuis = data.get("kuis_selesai", 0)
    akurasi = (benar / total * 100) if total > 0 else 0
    nilai = int(akurasi)
    bintang = bintang_nilai(akurasi)

    if akurasi >= 80:
        pesan = "🎉 Hebat! Anak Bapak jago matematika!"
    elif akurasi >= 60:
        pesan = "👏 Bagus! Terus belajar!"
    else:
        pesan = "💪 Jangan menyerah! Besok pasti lebih baik!"

    await update.callback_query.edit_message_text(
        f"📊 <b>PROGRES BELAJAR: {nama}</b>\n"
        f"───────────────────────────────\n"
        f"✅ <b>Benar</b>: {benar}\n"
        f"🔢 <b>Total</b>: {total}\n"
        f"📈 <b>Akurasi</b>: {akurasi:.1f}%\n"
        f"🏁 <b>Kuis</b>: {kuis} selesai\n"
        f"⭐ <b>Nilai</b>: {nilai}/100\n"
        f"🌟 <b>Bintang</b>: {bintang}\n\n"
        f"💡 {pesan}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="utama")]
        ])
    )

# 📚 Tampilkan menu latihan
async def tampilkan_menu(update):
    await update.callback_query.edit_message_text(
        "📋 <b>PILIH JENIS LATIHAN</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Penjumlahan", callback_data="plus")],
            [InlineKeyboardButton("➖ Pengurangan", callback_data="minus")],
            [InlineKeyboardButton("🎯 Satuan = 9", callback_data="s9")],
            [InlineKeyboardButton("🎯 Satuan = 10", callback_data="s10")],
            [InlineKeyboardButton("🎯 Satuan = 11", callback_data="s11")],
            [InlineKeyboardButton("🎯 Satuan = 12", callback_data="s12")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="utama")]
        ])
    )

# 🧮 Tampilkan menu kalkulator
async def tampilkan_kalkulator(update):
    await update.callback_query.edit_message_text(
        "🧮 <b>MODE KALKULATOR</b>\n"
        "Pilih mode bantuan:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🧮 Kalkulator Ilmiah", callback_data="calc_scientific")],
            [InlineKeyboardButton("🧩 Pecahan (Langkah)", callback_data="calc_pecahan")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="utama")]
        ])
    )

# 📤 Kirim soal
async def kirim_soal(update: Update, data: dict, index: int):
    try:
        a, b, _, simbol = data["soal"][index]
        a_emoji = ke_emoji(a)
        b_emoji = ke_emoji(b)
        nomor = index + 1

        if nomor % 2 == 1:
            soal_text = (
                f"Soal {nomor}\n"
                f"{a_emoji}\n"
                f"{b_emoji}\n"
                f"─── {simbol}\n"
                f" 🟰"
            )
        else:
            soal_text = f"Soal {nomor}\n{a_emoji} {simbol} {b_emoji} 🟰"

        await update.message.reply_text(
            f"<pre>{soal_text}</pre>",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text("❌ Terjadi kesalahan saat menampilkan soal.")

# 🔍 Ekstrak pecahan dari teks (termasuk campuran)
def parse_pecahan(teks):
    """Ubah string pecahan (biasa atau campuran) jadi Fraction"""
    teks = teks.strip().lower().replace(' ', '')
    try:
        # Format campuran: 2_1/2 atau 2 1/2
        if '_' in teks or re.search(r'\d+\s+\d+/\d+', teks):
            if '_' in teks:
                bagian = teks.split('_')
            else:
                bagian = re.split(r'\s+', teks)
            if len(bagian) == 2 and '/' in bagian[1]:
                utama = int(bagian[0])
                pec = Fraction(bagian[1])
                return Fraction(utama) + pec
            else:
                return None
        else:
            return Fraction(teks)
    except:
        return None

# 🧩 Format pecahan campuran (a b/c)
def format_pecahan_mixed(frac):
    """Format pecahan jadi bentuk campuran (a b/c)"""
    if frac.denominator == 1:
        return str(frac.numerator)
    if abs(frac.numerator) < frac.denominator:
        return str(frac)
    a = frac.numerator // frac.denominator
    sisa = Fraction(frac.numerator % frac.denominator, frac.denominator)
    if a == 0:
        return str(sisa)
    return f"{a} {sisa}"

# 🧮 Kalkulator Pecahan (Langkah demi Langkah)
async def kalkulator_pecahan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = update.message.text.strip()
    user_id = update.effective_user.id

    # ❌ Jika user belum login
    if user_id not in user_data or user_data[user_id]["nama"] == "ANAK":
        await update.message.reply_text(
            "❌ Silakan LOGIN dulu.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔐 LOGIN", callback_data="login")]
            ])
        )
        return

    # 📌 Format: 2 1/3 + 3 1/2
    # Cari operasi
    if '+' in pesan:
        op = '+'
    elif '-' in pesan:
        op = '-'
    elif '*' in pesan or '×' in pesan:
        op = '*'
    elif '/' in pesan or '÷' in pesan:
        op = '/'
    else:
        await update.message.reply_text("❌ Format salah. Contoh: 1/2 + 3/4")
        return

    # Pisah berdasarkan operasi
    parts = re.split(r'[+\-×*/]', pesan)
    if len(parts) != 2:
        await update.message.reply_text("❌ Format salah. Harus ada dua angka.")
        return

    a_str = parts[0].strip()
    b_str = parts[1].strip()

    a_frac = parse_pecahan(a_str)
    b_frac = parse_pecahan(b_str)

    if a_frac is None or b_frac is None:
        await update.message.reply_text("❌ Format pecahan salah! Gunakan 1/2 atau 2 1/2")
        return

    # Ambil nilai
    a_num, a_den = a_frac.numerator, a_frac.denominator
    b_num, b_den = b_frac.numerator, b_frac.denominator

    # Kirim langkah
    langkah = f"🧩 <b>LANGKAH PENYELESAIAN</b>\n"
    langkah += f"Hitung: <code>{a_str} {op} {b_str}</code>\n"
    langkah += "───────────────────────────────\n"

    if op == '+':
        penyebut_baru = a_den * b_den // math.gcd(a_den, b_den)
        a_baru = a_num * (penyebut_baru // a_den)
        b_baru = b_num * (penyebut_baru // b_den)
        hasil_num = a_baru + b_baru
        langkah += f"🔹 Ubah penyebut sama:\n   {a_num}/{a_den} = {a_baru}/{penyebut_baru}\n   {b_num}/{b_den} = {b_baru}/{penyebut_baru}\n"
        langkah += f"🔹 Jumlahkan: {a_baru}/{penyebut_baru} + {b_baru}/{penyebut_baru} = {hasil_num}/{penyebut_baru}\n"
    elif op == '-':
        penyebut_baru = a_den * b_den // math.gcd(a_den, b_den)
        a_baru = a_num * (penyebut_baru // a_den)
        b_baru = b_num * (penyebut_baru // b_den)
        hasil_num = a_baru - b_baru
        langkah += f"🔹 Ubah penyebut sama:\n   {a_num}/{a_den} = {a_baru}/{penyebut_baru}\n   {b_num}/{b_den} = {b_baru}/{penyebut_baru}\n"
        langkah += f"🔹 Kurangkan: {a_baru}/{penyebut_baru} - {b_baru}/{penyebut_baru} = {hasil_num}/{penyebut_baru}\n"
    elif op == '*':
        hasil_num = a_num * b_num
        hasil_den = a_den * b_den
        langkah += f"🔹 Kalikan pembilang & penyebut:\n   ({a_num} × {b_num}) / ({a_den} × {b_den}) = {hasil_num}/{hasil_den}\n"
    elif op == '/':
        if b_frac == 0:
            await update.message.reply_text("❌ Tidak bisa dibagi nol!")
            return
        hasil_num = a_num * b_den
        hasil_den = a_den * b_num
        langkah += f"🔹 Balik pecahan kedua:\n   {b_num}/{b_den} → {b_den}/{b_num}\n"
        langkah += f"🔹 Kalikan: {a_num}/{a_den} × {b_den}/{b_num} = {hasil_num}/{hasil_den}\n"

    # Hitung hasil
    if op in ['+', '-']:
        hasil_frac = Fraction(hasil_num, penyebut_baru)
    elif op == '*':
        hasil_frac = Fraction(hasil_num, hasil_den)
    elif op == '/':
        hasil_frac = Fraction(hasil_num, hasil_den)

    # Sederhanakan
    pecahan_sederhana = f"{hasil_frac.numerator}/{hasil_frac.denominator}"
    campuran = format_pecahan_mixed(hasil_frac)
    desimal = float(hasil_frac)

    # Tampilkan hasil
    hasil_text = f"✅ <b>Hasil Akhir</b>\n"
    hasil_text += f"• Pecahan: <b>{pecahan_sederhana}</b>\n"
    if '/' in campuran and campuran != pecahan_sederhana:
        hasil_text += f"• Campuran: <b>{campuran}</b>\n"
    hasil_text += f"• Desimal: <b>{desimal:.6g}</b>"

    await update.message.reply_text(langkah + hasil_text, parse_mode="HTML")

# 📥 Terima pesan (kode login atau jawaban)
async def terima_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pesan = update.message.text.strip().upper()

    # ✅ Pastikan user_id ada
    if user_id not in user_data:
        user_data[user_id] = {
            "nama": "ANAK",
            "total_benar": 0,
            "total_soal": 0,
            "kuis_selesai": 0,
            "status": "idle"
        }

    data = user_data[user_id]
    status = data.get("status", "idle")

    # Proses login
    if status == "tunggu_kode":
        kode_login = muat_kode()
        pesan_upper = pesan.upper()

        if pesan_upper in kode_login:
            nama = kode_login[pesan_upper]
            user_data[user_id]["nama"] = nama
            user_data[user_id]["status"] = "login_selesai"
            await update.message.reply_text(
                f"✅ Login berhasil!\n"
                f"Halo, <b>{nama}</b>! 🌟\n\n"
                "Pilih LATIHAN dari menu.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📚 Mulai Latihan", callback_data="menu")]
                ])
            )
        else:
            await update.message.reply_text(
                "❌ Kode salah. Coba lagi (contoh: TEDI01):",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Batalkan", callback_data="utama")]
                ])
            )
        return

    # Tunggu jumlah soal
    if status == "tunggu_jumlah":
        try:
            jumlah = int(pesan)
            if jumlah < 10:
                await update.message.reply_text("❌ Minimal 10 soal.", parse_mode="HTML")
                return

            # Generate soal sesuai mode
            soal_list = []
            mode = data["mode"]

            for _ in range(jumlah):
                if mode == "plus":
                    a_puluhan = random.randint(1, 8)
                    c_puluhan = random.randint(1, 9 - a_puluhan)
                    a_satuan = random.randint(0, 8)
                    c_satuan = random.randint(0, 9 - a_satuan)
                    angka1 = 10 * a_puluhan + a_satuan
                    angka2 = 10 * c_puluhan + c_satuan
                    hasil = angka1 + angka2
                    simbol = "➕"

                elif mode == "minus":
                    a_puluhan = random.randint(1, 9)
                    c_puluhan = random.randint(1, a_puluhan)
                    a_satuan = random.randint(0, 9)
                    c_satuan = random.randint(0, a_satuan)
                    angka1 = 10 * a_puluhan + a_satuan
                    angka2 = 10 * c_puluhan + c_satuan
                    hasil = angka1 - angka2
                    simbol = "➖"

                elif mode == "s9":
                    a = random.randint(1, 9)
                    c = random.randint(1, 9)
                    b = random.randint(1, 8)
                    d = 9 - b
                    angka1 = 10 * a + b
                    angka2 = 10 * c + d
                    hasil = angka1 + angka2
                    simbol = "➕"

                elif mode == "s10":
                    a = random.randint(1, 9)
                    c = random.randint(1, 9)
                    b = random.randint(1, 9)
                    d = 10 - b
                    angka1 = 10 * a + b
                    angka2 = 10 * c + d
                    hasil = angka1 + angka2
                    simbol = "➕"

                elif mode == "s11":
                    a = random.randint(1, 9)
                    c = random.randint(1, 9)
                    b = random.randint(2, 9)
                    d = 11 - b
                    angka1 = 10 * a + b
                    angka2 = 10 * c + d
                    hasil = angka1 + angka2
                    simbol = "➕"

                elif mode == "s12":
                    a = random.randint(1, 9)
                    c = random.randint(1, 9)
                    b = random.randint(3, 9)
                    d = 12 - b
                    angka1 = 10 * a + b
                    angka2 = 10 * c + d
                    hasil = angka1 + angka2
                    simbol = "➕"

                soal_list.append((angka1, angka2, hasil, simbol))

            # Update data
            data["soal"] = soal_list
            data["jumlah"] = jumlah
            data["index"] = 0
            data["benar"] = 0
            data["status"] = "dalam_kuis"

            # Kirim soal pertama
            await kirim_soal(update, data, 0)

        except ValueError:
            await update.message.reply_text("❌ Masukkan angka, bukan teks.", parse_mode="HTML")
        return

    # DALAM KUIS: Cek jawaban
    if status == "dalam_kuis":
        try:
            index = data["index"]
            a, b, jawaban_benar, simbol = data["soal"][index]
        except (IndexError, KeyError):
            await update.message.reply_text("❌ Soal tidak tersedia. Mulai dari /mulai.")
            data["status"] = "login_selesai"
            return

        try:
            jawaban_anak = int(pesan)
        except ValueError:
            await update.message.reply_text("❌ Masukkan angka, bukan teks.", parse_mode="HTML")
            return

        if jawaban_anak == jawaban_benar:
            await update.message.reply_text("<b>🎉✅ BENAR!</b> Hebat! 🏆", parse_mode="HTML")
            data["benar"] += 1
        else:
            await update.message.reply_text(f"❌ Salah! Jawabannya adalah {jawaban_benar}.", parse_mode="HTML")

        data["index"] += 1

        if data["index"] < data["jumlah"]:
            await kirim_soal(update, data, data["index"])
        else:
            # Update progres
            data["total_benar"] += data["benar"]
            data["total_soal"] += data["jumlah"]
            data["kuis_selesai"] += 1

            # Simpan ke file
            simpan_skor()

            # Hitung akurasi
            akurasi = (data["total_benar"] / data["total_soal"]) * 100 if data["total_soal"] > 0 else 0
            nilai = int(akurasi)
            bintang = bintang_nilai(akurasi)

            if akurasi >= 80:
                pesan = "🎉 Hebat! Anak Bapak jago matematika!"
            elif akurasi >= 60:
                pesan = "👏 Bagus! Terus belajar!"
            else:
                pesan = "💪 Jangan menyerah! Besok pasti lebih baik!"

            await update.message.reply_text(
                f"🏆 <b>KUIS SELESAI!</b>\n"
                f"✅ Benar: {data['benar']}/{data['jumlah']}\n\n"
                f"📊 <b>PROGRES BELAJAR: {data['nama']}</b>\n"
                f"───────────────────────────────\n"
                f"✅ <b>Benar</b>: {data['total_benar']}\n"
                f"🔢 <b>Total</b>: {data['total_soal']}\n"
                f"📈 <b>Akurasi</b>: {akurasi:.1f}%\n"
                f"🏁 <b>Kuis</b>: {data['kuis_selesai']} selesai\n"
                f"⭐ <b>Nilai</b>: {nilai}/100\n"
                f"🌟 <b>Bintang</b>: {bintang}\n\n"
                f"💡 {pesan}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="utama")]
                ])
            )

            # Reset sementara
            del data["soal"]
            del data["jumlah"]
            del data["index"]
            del data["benar"]
            del data["status"]

    # 🧮 Kalkulator Pecahan
    elif data.get("status") == "kalkulator_pecahan":
        await kalkulator_pecahan(update, context)

# 📌 Saat tombol diklik
async def pilih_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # ✅ Pastikan user_id ada
    if user_id not in user_data:
        user_data[user_id] = {
            "nama": "ANAK",
            "total_benar": 0,
            "total_soal": 0,
            "kuis_selesai": 0,
            "status": "idle"
        }

    if query.data == "utama":
        await query.edit_message_text(
            "🏠 <b>MENU UTAMA</b>\n"
            "Pilih yang ingin Anda lakukan:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔐 LOGIN", callback_data="login")],
                [InlineKeyboardButton("📚 LATIHAN", callback_data="menu")],
                [InlineKeyboardButton("📊 NILAI", callback_data="nilai")],
                [InlineKeyboardButton("🧮 KALKULATOR", callback_data="kalkulator")]
            ]),
            parse_mode="HTML"
        )
    elif query.data == "login":
        user_data[user_id]["status"] = "tunggu_kode"
        await mulai_login(update)
    elif query.data == "menu":
        if user_data[user_id]["nama"] == "ANAK":
            await query.edit_message_text(
                "❌ Silakan LOGIN dulu.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 LOGIN", callback_data="login")]
                ])
            )
        else:
            await tampilkan_menu(update)
    elif query.data == "nilai":
        if user_data[user_id]["nama"] == "ANAK":
            await query.edit_message_text(
                "❌ Login dulu untuk lihat nilai.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 LOGIN", callback_data="login")]
                ])
            )
        else:
            await tampilkan_nilai(update, user_id)
    elif query.data == "kalkulator":
        await tampilkan_kalkulator(update)
    elif query.data == "calc_pecahan":
        user_data[user_id]["status"] = "kalkulator_pecahan"
        await query.edit_message_text(
            "🧩 <b>KALKULATOR PECAHAN</b>\n\n"
            "Ketik langsung soal:\n"
            "<code>2 1/3 + 3 1/2</code>\n"
            "<code>1/2 - 1/4</code>\n"
            "<code>3/4 × 2/3</code>\n"
            "<code>5/6 ÷ 1/3</code>\n\n"
            "Ketik <code>k</code> untuk kembali.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Kembali", callback_data="utama")]
            ])
        )
    else:
        # Pilih jenis soal
        if user_data[user_id]["nama"] == "ANAK":
            await query.edit_message_text("❌ Login dulu.")
            return
        user_data[user_id]["mode"] = query.data
        user_data[user_id]["status"] = "tunggu_jumlah"
        await query.edit_message_text(
            "🔢 Berapa soal yang ingin dikerjakan?\n"
            "Minimal 10 soal.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu")]
            ])
        )

# 🚀 Main Program
if __name__ == "__main__":
    muat_skor()
    print("🚀 Bot Matematika Anak sedang berjalan...")
    print("💡 Ketik /mulai untuk mulai")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mulai", mulai))
    app.add_handler(CallbackQueryHandler(pilih_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, terima_jawaban))

    app.run_polling()