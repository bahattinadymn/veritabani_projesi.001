# 📚 KTÜ Kütüphane Otomasyon Sistemi

Bu proje, Karadeniz Teknik Üniversitesi (KTÜ) Veritabanı Yönetim Sistemleri dersi kapsamında geliştirilmiştir. Python (Flask) web çatısı ve MSSQL veritabanı kullanılarak hazırlanan tam kapsamlı bir kütüphane yönetim sistemidir.

## 🚀 Proje Özellikleri

Proje, veritabanı dersinin gerekliliklerini kapsayacak şekilde aşağıdaki teknik özellikleri içerir:

* **Trigger (Tetikleyici) Kullanımı:** Kitap ödünç alındığında veya iade edildiğinde, kitap stok bilgisi veritabanı seviyesinde (Trigger ile) otomatik olarak güncellenir.
* **Stored Procedure (Saklı Yordam):** İade işlemleri sırasında gecikme süresi ve ceza tutarı hesaplaması veritabanı içinde yazılan prosedürler tarafından yapılır.
* **Asenkron E-Posta Bildirimi:** Kitap iade işlemi tamamlandığında, sistem ana akışı bozmadan (Thread yapısı ile) 1 dakika gecikmeli olarak kullanıcıya bilgilendirme e-postası gönderir.
* **JWT Kimlik Doğrulama:** Kullanıcı giriş ve kayıt işlemleri JSON Web Token ile güvenli bir şekilde yönetilir.

---

## 🛠️ Kurulum Rehberi

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayınız.

### 1. Projeyi İndirme ve Hazırlık
Terminal veya komut satırını açarak projeyi bilgisayarınıza indirin:

bash
git clone [https://github.com/KULLANICI_ADIN/ktu-kutuphane-projesi.git](https://github.com/KULLANICI_ADIN/ktu-kutuphane-projesi.git)
cd ktu-kutuphane-projesi

2. Sanal Ortam ve Kütüphaneler
Python kütüphanelerinin çakışmaması için sanal ortam kurmanız önerilir:

Bash

# Sanal ortam oluşturma
python -m venv venv

# Sanal ortamı aktif etme (Windows için)
.\venv\Scripts\activate

# Gerekli paketleri yükleme
pip install -r requirements.txt

3. Veritabanı Kurulumu (ÖNEMLİ ⚠️)
Proje klasöründe bulunan database_backup.sql dosyası; gerekli tabloları, örnek verileri, Trigger ve Stored Procedure kodlarını içermektedir.

Bilgisayarınızda SQL Server Management Studio (SSMS) uygulamasını açın.

database_backup.sql dosyasını File > Open menüsünden açın.

Execute (F5) butonuna basarak veritabanını oluşturun.

4. Ayar Dosyasının (.env) Oluşturulması
Güvenlik nedeniyle veritabanı şifreleri ve gizli anahtarlar GitHub'a yüklenmemiştir. Projenin çalışabilmesi için ana dizinde .env adında bir dosya oluşturup aşağıdaki bilgileri içine yapıştırınız:


# .env Dosyası İçeriği

# --- Güvenlik Anahtarları ---
SECRET_KEY=gizli-proje-anahtari
JWT_SECRET_KEY=jwt-ozel-anahtari

# --- Veritabanı Bağlantısı ---
# Şablon: mssql+pyodbc://KULLANICI:SIFRE@SERVER/VERITABANI?driver=ODBC+Driver+17+for+SQL+Server
# Lütfen 'sa' ve 'sifreniz' kısımlarını kendi SQL Server bilgilerinize göre düzenleyin.
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://sa:123456@LOCALHOST/KutuphaneDB?driver=ODBC+Driver+17+for+SQL+Server

# --- E-Posta Ayarları (Gmail Örneği) ---
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=sizinmailiniz@gmail.com
MAIL_PASSWORD=mail_uygulama_sifreniz
Not: Eğer .env dosyası ile uğraşmak istemezseniz, bu ayarları doğrudan config.py dosyası içerisindeki ilgili alanlara da yazabilirsiniz.

5. Uygulamayı Başlatma
Tüm ayarlar yapıldıktan sonra terminalden aşağıdaki komutu çalıştırın:



python run.py
Uygulama http://127.0.0.1:5000 adresinde çalışmaya başlayacaktır.

BAHATTİN ADİYAMAN   445855
