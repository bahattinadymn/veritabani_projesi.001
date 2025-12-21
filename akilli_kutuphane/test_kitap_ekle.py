import requests

# 1. ADIM: Önce giriş yapıp TOKEN alıyoruz
login_url = 'http://127.0.0.1:5000/api/auth/login'
login_data = {"email": "ali.yilmaz@ornek.com", "sifre": "gucluSifre123"}

session = requests.Session()
resp_login = session.post(login_url, json=login_data)

if resp_login.status_code == 200:
    token = resp_login.json()['access_token']
    print("Giriş başarılı, Token alındı!")
    
    # 2. ADIM: Token'ı kullanarak Kitap Ekliyoruz
    book_url = 'http://127.0.0.1:5000/api/books/'
    headers = {'Authorization': f'Bearer {token}'} # Token'ı başlığa ekliyoruz
    
    book_data = {
        "ad": "Nutuk",
        "yazar": "Mustafa Kemal Atatürk",
        "kategori": "Tarih",
        "stok": 10
    }
    
    resp_book = session.post(book_url, json=book_data, headers=headers)
    print("\nKitap Ekleme Sonucu:")
    print(f"Kod: {resp_book.status_code}")
    print(f"Cevap: {resp_book.json()}")
else:
    print("Giriş yapılamadı!")