import requests

# 1. Giriş Yap ve Token Al
session = requests.Session()
login_resp = session.post('http://127.0.0.1:5000/api/auth/login', 
                          json={"email": "ali.yilmaz@ornek.com", "sifre": "gucluSifre123"})
token = login_resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

print(f"Giriş Başarılı! Token alındı.")

# 2. Kitap ID'si 1 olan kitabı ödünç al (Nutuk kitabını eklemiştik)
print("\n--- Kitap Ödünç Alınıyor ---")
loan_resp = session.post('http://127.0.0.1:5000/api/loans/borrow', 
                         json={"book_id": 1}, 
                         headers=headers)

print(f"Kod: {loan_resp.status_code}")
print(f"Cevap: {loan_resp.json()}")

# 3. Stok Kontrolü
# Normalde API ile bakarız ama şimdilik sonucu görmek için:
# Eğer trigger çalıştıysa veritabanında stok 1 azalmış olmalı.
print("\nNOT: Test başarılıysa SSMS'ten Books tablosunu kontrol et. Stok düşmüş olmalı!")