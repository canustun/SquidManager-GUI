# Squid Proxy Yönetim Paneli

Bu proje, Windows üzerinde çalışan **Squid Proxy** sunucusunu kolayca yönetmek, hız limitleri koymak ve web sitelerini engellemek için geliştirilmiş bir **CustomTkinter** arayüzüdür.

## 🚀 Özellikler

* **URL Engelleme:** Belirlediğiniz web sitelerini anlık olarak yasaklı listesine ekler.
* **Hız Sınırlandırma (Bandwidth Limit):** Kullanıcıların internet hızını KB/s cinsinden kısıtlar.
* **İnternet Kilidi:** Tek bir tuşla proxy üzerinden internet erişimini tamamen keser veya açır.
* **Anlık Durum Kontrolü:** Squid servisinin çalışıp çalışmadığını izler ve yönetir (Başlat/Durdur).
* **Log Takibi:** Erişim loglarını tek tıkla görüntüleme imkanı sağlar.

## 🛠 Kurulum

1.  Bilgisayarınızda **Squid for Windows** kurulu olmalıdır (Varsayılan yol: `C:/Squid`).
2.  Gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install customtkinter
    ```
3.  Uygulamayı yönetici olarak çalıştırın (Servisleri yönetebilmek için gereklidir).

## 📁 Dosya Yapısı
Uygulama, Squid'in varsayılan yapılandırma dosyalarını (`squid.conf`, `blocked.acl`) otomatik olarak düzenleyecek şekilde ayarlanmıştır. İlk çalıştırmada mevcut ayarlarınızın yedeğini (`.bak`) oluşturur.

## 📄 Lisans
Bu proje [MIT](LICENSE) lisansı ile korunmaktadır.
