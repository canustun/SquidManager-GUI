import os
import subprocess
import customtkinter as ctk
import time
import shutil

# --- DOSYA YOLLARI ---
SQUID_PATH = r"C:/Squid/bin/squid.exe"
SQUID_CONF = r"C:/Squid/etc/squid/squid.conf"
BLOCKED_ACL = r"C:/Squid/etc/blocked.acl"
LOG_FILE = r"C:/Squid/var/log/squid/access.log"
PID_FILE = r"C:/Squid/var/run/squid.pid"

# --- SQUID DURUM KONTROL ---
def squid_calisiyor_mu():
    try:
        result = subprocess.run(
            'tasklist | findstr squid.exe',
            shell=True,
            capture_output=True,
            text=True
        )
        return "squid.exe" in result.stdout
    except:
        return False

# --- ZORLA KAPAT ---
def squid_zorla_kapat():
    subprocess.run(
        "taskkill /F /IM squid.exe",
        shell=True,
        capture_output=True,
        creationflags=0x08000000
    )
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    time.sleep(1)

# --- GÜVENLİ RESTART ---
def tam_restart():
    squid_zorla_kapat()
    subprocess.Popen([SQUID_PATH, "-f", SQUID_CONF], creationflags=0x08000000)
    squid_button.configure(text="Proxy Durdur", fg_color="red")

# --- SQUID.CONF ALT YAPI ---
def config_alt_yapi_kontrol():
    if not os.path.exists(SQUID_CONF):
        return

    shutil.copy(SQUID_CONF, SQUID_CONF + ".bak")

    with open(SQUID_CONF, "r", encoding="utf-8") as f:
        content = f.read()

    if "# --- OTOMATIK AYARLAR ---" in content:
        return

    otomatik = f"""# --- OTOMATIK AYARLAR ---
acl yasakli_siteler dstdomain "{BLOCKED_ACL}"

http_access deny yasakli_siteler
http_access allow all

delay_pools 1
delay_class 1 1
delay_parameters 1 -1/-1
delay_access 1 allow all
# --- OTOMATIK AYARLAR SONU ---
"""

    with open(SQUID_CONF, "w", encoding="utf-8") as f:
        f.write(otomatik + "\n" + content)

# --- HIZ YÖNETİMİ ---
def hiz_yonet():
    deger = hiz_entry.get().strip()
    if not deger.isdigit():
        ctk.CTkMessagebox.show_info("Hata", "Lütfen geçerli bir sayı girin!")
        return

    byte = int(deger) * 1024
    yeni = f"delay_parameters 1 {byte}/{byte}\n"

    with open(SQUID_CONF, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(SQUID_CONF, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip().startswith("delay_parameters 1"):
                f.write(yeni)
            else:
                f.write(line)

    tam_restart()

# --- URL KAYDET VE YENİLE ---
def url_kaydet_ve_yenile():
    icerik = engellenecekURLWidget.get("1.0", "end-1c")
    temiz = "\n".join(l.strip() for l in icerik.splitlines() if l.strip())

    if not temiz:
        ctk.CTkMessagebox.show_info("Uyarı", "Liste boş! En az bir URL girin.")
        return

    with open(BLOCKED_ACL, "w", encoding="utf-8") as f:
        f.write(temiz)

    tam_restart()

# --- İNTERNET KES / AÇ ---
def erisim_kes_fonksiyonu():
    with open(SQUID_CONF, "r", encoding="utf-8") as f:
        lines = f.readlines()

    deny_satiri = "http_access deny all\n"

    if deny_satiri in lines:
        lines.remove(deny_satiri)
        erişim_kes_btn.configure(text="İnternet Erişimini Kes", fg_color="green")
    else:
        # allow all satırından önce ekle
        for i, line in enumerate(lines):
            if line.strip() == "http_access allow all":
                lines.insert(i, deny_satiri)
                break
        else:
            lines.append(deny_satiri)
        erişim_kes_btn.configure(text="İnternet Erişimini Aç", fg_color="red")

    with open(SQUID_CONF, "w", encoding="utf-8") as f:
        f.writelines(lines)

    tam_restart()

# --- BAŞLAT / DURDUR ---
def baslat_durdur():
    if squid_calisiyor_mu():
        squid_zorla_kapat()
        squid_button.configure(text="Proxy Başlat", fg_color="green")
    else:
        squid_zorla_kapat()
        subprocess.Popen([SQUID_PATH, "-f", SQUID_CONF], creationflags=0x08000000)
        squid_button.configure(text="Proxy Durdur", fg_color="red")

# --- LOG ---
def log_ac():
    if os.path.exists(LOG_FILE):
        os.startfile(LOG_FILE)

# ================= GUI =================
ctk.set_appearance_mode("dark")
pencere = ctk.CTk()
pencere.title("SQUID Full Yönetim Paneli")
pencere.geometry("700x650")

config_alt_yapi_kontrol()

ctk.CTkLabel(pencere, text="Engellenecek URL Listesi").pack(pady=10)
engellenecekURLWidget = ctk.CTkTextbox(pencere, width=600, height=250)
if os.path.exists(BLOCKED_ACL):
    with open(BLOCKED_ACL, "r", encoding="utf-8") as f:
        engellenecekURLWidget.insert("1.0", f.read())
engellenecekURLWidget.pack()

ctk.CTkButton(pencere,text="Listeyi Kaydet ve Yeniden Başlat",command=url_kaydet_ve_yenile).pack(pady=10)

hiz_frame = ctk.CTkFrame(pencere)
hiz_frame.pack(pady=10)

ctk.CTkLabel(hiz_frame, text="Hız (KB/s):").grid(row=0, column=0, padx=10)
hiz_entry = ctk.CTkEntry(hiz_frame, width=100)
hiz_entry.insert(0, "100")
hiz_entry.grid(row=0, column=1)

ctk.CTkButton(hiz_frame,text="Uygula",command=hiz_yonet).grid(row=0, column=2, padx=10)

btn_frame = ctk.CTkFrame(pencere, fg_color="transparent")
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame, text="Logları Gör", command=log_ac).grid(row=0, column=0, padx=5)

squid_button = ctk.CTkButton(btn_frame,text="Proxy Durdur" if squid_calisiyor_mu() else "Proxy Başlat",fg_color="red" if squid_calisiyor_mu() else "green",command=baslat_durdur)
squid_button.grid(row=0, column=1, padx=5)

erişim_kes_btn = ctk.CTkButton(btn_frame,text="İnternet Erişimini Kes",command=erisim_kes_fonksiyonu,fg_color="green")
erişim_kes_btn.grid(row=0, column=2, padx=5)

pencere.mainloop()
