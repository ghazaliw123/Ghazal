import subprocess
import time
import sys
import os
from datetime import datetime

print("="*70)
print("🚀 برنامۀ اجرای پروژۀ شبیه‌سازی حملۀ DDoS")
print("="*70)
print()

# بررسی وجود فایل‌های مورد نیاز
required_files = ['server.py', 'ddos_attack.py', 'plot_metrics.py']
for file in required_files:
    if not os.path.exists(file):
        print(f"❌ فایل {file} پیدا نشد!")
        sys.exit(1)

print("✅ تمام فایل‌های مورد نیاز موجود هستند")
print()

print("="*70)
print("📋 مراحل اجرا:")
print("="*70)
print("1️⃣  سرور شروع می‌شود (بر روی http://localhost:8000)")
print("2️⃣  30 ثانیه صبر می‌کنیم (سرور آرام)")
print("3️⃣  حملۀ DDoS شروع می‌شود (30 ثانیه)")
print("4️⃣  حملهتمام می‌شود")
print("5️⃣  نمودار رسم می‌شود")
print()

input("🔔 برای شروع، Enter را فشار دهید...")

print()
print("="*70)
print(f"⏰ شروع: {datetime.now()}")
print("="*70)
print()

# شروع سرور
print("1️⃣  سرور شروع می‌شود...")
server_process = subprocess.Popen([sys.executable, 'server.py'])
time.sleep(3)  # صبر کن تا سرور شروع شود

print()
print("2️⃣  30 ثانیه صبر برای اندازه‌گیری حالت عادی...")
for i in range(30, 0, -1):
    print(f"⏳ {i} ثانیه...")
    time.sleep(1)

print()
print("3️⃣  حملۀ DDoS شروع می‌شود!")
print()

# شروع حمله
attack_process = subprocess.Popen([sys.executable, 'ddos_attack.py'])
attack_process.wait()  # منتظر تمام شدن حمله

print()
print("4️⃣  حمله تمام شد، 10 ثانیه صبر برای بازگشت سرور به حالت عادی...")
for i in range(10, 0, -1):
    print(f"⏳ {i} ثانیه...")
    time.sleep(1)

print()
print("5️⃣  نمودار رسم می‌شود...")
print()

# توقف سرور
server_process.terminate()
time.sleep(2)

# رسم نمودار
plotter_process = subprocess.Popen([sys.executable, 'plot_metrics.py'])
plotter_process.wait()

print()
print("="*70)
print("✅ پروژه کامل شد!")
print("="*70)
print()
print("📊 نتایج:")
print("  - فایل metrics.json (داده‌های جمع‌آوری شده)")
print("  - فایل ddos_analysis.png (نمودار)")
print()
print(f"⏰ پایان: {datetime.now()}")
print()