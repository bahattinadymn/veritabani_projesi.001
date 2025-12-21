import requests

# Kaydettiğin kullanıcının bilgileriyle giriş yapıyoruz
url = 'http://127.0.0.1:5000/api/auth/login'
veri = {
    "email": "ali.yilmaz@ornek.com",
    "sifre": "gucluSifre123"
}

try:
    response = requests.post(url, json=veri)
    print(f"Durum Kodu: {response.status_code}")
    print("Gelen Cevap:")
    print(response.json())
except Exception as e:
    print(f"Hata: {e}")