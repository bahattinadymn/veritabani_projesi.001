import os
from dotenv import load_dotenv

# .env dosyasını yükle
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
  
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:12345@LOCALHOST/KutuphaneDB?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'cok-gizli-super-sifre'

    # 2. MAİL AYARLARI (HATA BURADAYDI)
    # Burası kesinlikle 'smtp.gmail.com' olmalı. Boşluk olmamalı.
    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    # 3. KULLANICI BİLGİLERİ (.env dosyasından gelir)
    MAIL_USERNAME = os.getenv('MAIL_KULLANICI')
    MAIL_PASSWORD = os.getenv('MAIL_SIFRE')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_KULLANICI')

# --- KONTROL ---
print("--- MAİL AYARLARI KONTROLÜ ---")
print(f"Sunucu: {Config.MAIL_SERVER} (smtp.gmail.com olmalı)")
print(f"Kullanıcı: {Config.MAIL_USERNAME}")
print("------------------------------")
