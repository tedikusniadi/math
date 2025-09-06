# ========================
# Makefile untuk project math
# ========================

# Target default kalau cuma ketik "make"
default: help

# Jalankan script Python
run:
	python3 matematika_anak.py

# Commit + push ke GitHub (main)
push:
	git add .
	@if ! git diff --cached --quiet; then \
		git commit -m "Update: $$(date '+%Y-%m-%d %H:%M:%S')" && \
		git push origin main; \
	else \
		echo "⚠️  Tidak ada perubahan untuk di-commit."; \
	fi

# Pull dengan rebase (riwayat lebih rapi)
pull:
	git pull --rebase origin main

# Remaster: buang semua riwayat commit dan push ulang
remaster:
	git checkout --orphan temp_branch
	git add .
	git commit -m "first commit"
	- git branch -D main
	git branch -m main
	git push -f origin main

# Lihat status repo
status:
	git status
	git log --oneline

# Bantuan
help:
	@echo "📌 Perintah yang tersedia:"
	@echo "  make run      → Jalankan file Python"
	@echo "  make push     → Commit + Push ke GitHub (main)"
	@echo "  make pull     → Tarik perubahan terbaru (rebase)"
	@echo "  make remaster → Reset repo: hapus semua commit & push ulang"
	@echo "  make status   → Lihat status git"
