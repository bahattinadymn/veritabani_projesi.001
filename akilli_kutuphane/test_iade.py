import requests

# 1. Giriş Yap
session = requests.Session()
login_resp = session.post('http://127.0.0.1:5000/api/auth/login', 
                          json={"email": "ali.yilmaz@ornek.com", "sifre": "gucluSifre123"})

if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. İade Et (Ödünç ID'si 1 olan işlemi iade ediyoruz)
    # NOT: Eğer veritabanını sıfırlamadıysan ve ID 1 duruyorsa çalışır.
    print("--- Kitap İade Ediliyor ---")
    
    return_resp = session.post('http://127.0.0.1:5000/api/loans/return',
                               json={"loan_id": 1},
                               headers=headers)
                               
    print(f"Kod: {return_resp.status_code}")
    print(f"Cevap: {return_resp.json()}")
else:
    print("Giriş başarısız!")