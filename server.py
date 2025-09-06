# server.py
# Dashboard + Login + Reset + Ganti Password
# Versi: 100% Stabil, untuk Bapak Tedi

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from hashlib import sha256

# 📁 Folder utama
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📄 File data
KODE_FILE = os.path.join(BASE_DIR, 'kode.json')
SKOR_FILE = os.path.join(BASE_DIR, 'skor.json')
LOGIN_FILE = os.path.join(BASE_DIR, 'login.json')

# 🏠 Default login (admin / tedi123)
# Password "tedi123" -> SHA-256
# Cek Password : echo -n "rahasia123" | sha256sum atau
# echo -n "tedi123" | sha256sum
DEFAULT_LOGIN = {
    "username": "admin",
    "password": "93422391a5a3345cf0bb2505bd036e5ad1591ca397edf0360dcb6214519784dd"
}

# 🏠 Default kode anak
DEFAULT_KODE = {
    "TEDI01": "TEDI KUSNIADI",
    "REFI02": "REFI HERFIAWATI",
    "FIDI03": "FIDI HADIANSYAH",
    "FITE04": "FITE KARIM"
}

# ✅ Hash password
def hash_password(pwd):
    return sha256(pwd.encode()).hexdigest()

# ✅ Auto-buat file jika belum ada
def init_files():
    # 1. login.json
    if not os.path.exists(LOGIN_FILE):
        print(f"📁 Membuat {LOGIN_FILE}...")
        with open(LOGIN_FILE, 'w') as f:
            json.dump(DEFAULT_LOGIN, f, indent=2)
    else:
        try:
            with open(LOGIN_FILE, 'r') as f:
                json.load(f)
        except:
            print("⚠️ login.json rusak, memperbaiki...")
            with open(LOGIN_FILE, 'w') as f:
                json.dump(DEFAULT_LOGIN, f, indent=2)

    # 2. kode.json
    if not os.path.exists(KODE_FILE):
        print(f"📁 Membuat {KODE_FILE}...")
        with open(KODE_FILE, 'w') as f:
            json.dump(DEFAULT_KODE, f, indent=2)

    # 3. skor.json
    if not os.path.exists(SKOR_FILE):
        print(f"📁 Membuat {SKOR_FILE}...")
        with open(SKOR_FILE, 'w') as f:
            json.dump({}, f, indent=2)

# ✅ Reset kode.json ke default
def reset_kode():
    with open(KODE_FILE, 'w') as f:
        json.dump(DEFAULT_KODE, f, indent=2)

# ✅ Reset skor.json
def reset_skor():
    with open(SKOR_FILE, 'w') as f:
        json.dump({}, f, indent=2)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 🔐 Cek login (kecuali halaman login)
        if not self.is_logged_in() and path not in ['/login.html', '/login']:
            self.redirect('/login.html')
            return

        # Redirect / → /index.html
        if path == '/' or path == '/index.html':
            path = '/index.html'

        file_path = os.path.join(BASE_DIR, path.lstrip('/'))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            if file_path.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif file_path.endswith('.json'):
                self.send_header('Content-type', 'application/json')
            elif file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            else:
                self.send_header('Content-type', 'text/plain')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        if self.path == '/login':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            try:
                login_data = json.loads(data)
                username = login_data.get('username', '').strip()
                password = login_data.get('password', '').strip()

                with open(LOGIN_FILE, 'r') as f:
                    login = json.load(f)

                if username == login['username'] and hash_password(password) == login['password']:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Set-Cookie', 'logged_in=true; Path=/; HttpOnly; SameSite=Lax')
                    self.end_headers()
                    self.wfile.write(b'{"success": true}')
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'{"success": false, "error": "Username atau password salah"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
            return

        # Proteksi: hanya yang login yang bisa POST
        if not self.is_logged_in():
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "Akses ditolak"}')
            return

        # API: simpan kode
        if self.path == '/simpan_kode':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            try:
                kode = json.loads(data)
                with open(KODE_FILE, 'w') as f:
                    json.dump(kode, f, indent=2)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"success": true}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())

        # API: reset kode
        elif self.path == '/reset_kode':
            reset_kode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"success": true, "message": "kode.json direset"}')

        # API: reset skor
        elif self.path == '/reset_skor':
            reset_skor()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"success": true, "message": "skor.json dikosongkan"}')

        # API: ganti password
        elif self.path == '/ganti_password':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            try:
                pwd_data = json.loads(data)
                old = pwd_data.get('old_password', '')
                new1 = pwd_data.get('new_password1', '')
                new2 = pwd_data.get('new_password2', '')

                with open(LOGIN_FILE, 'r') as f:
                    login = json.load(f)

                if hash_password(old) != login['password']:
                    raise Exception("Password lama salah")

                if new1 != new2:
                    raise Exception("Password baru tidak cocok")

                if len(new1) < 4:
                    raise Exception("Password minimal 4 karakter")

                login['password'] = hash_password(new1)
                with open(LOGIN_FILE, 'w') as f:
                    json.dump(login, f, indent=2)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"success": true, "message": "Password berhasil diubah"}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())

        # API: logout
        elif self.path == '/logout':
            self.send_response(200)
            self.send_header('Set-Cookie', 'logged_in=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Lax')
            self.end_headers()
            self.wfile.write(b'{"success": true}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # 🔐 Cek apakah user sudah login
    def is_logged_in(self):
        cookies = self.headers.get('Cookie', '')
        return 'logged_in=true' in cookies

    # 🔀 Redirect helper
    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

def run():
    init_files()
    print("🚀 Dashboard jalan di http://localhost:5000")
    print("💡 Buka di browser: http://localhost:5000")
    server = HTTPServer(('0.0.0.0', 5000), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server dihentikan.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()