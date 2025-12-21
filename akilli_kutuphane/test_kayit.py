import requests

# Sunucumuzun adresi
url = 'http://127.0.0.1:5000/api/auth/register'

# Göndereceğimiz test verisi
veri = {
    "ad": "Ali",
    "soyad": "Yilmaz",
    "email": "ali.yilmaz@ornek.com",
    "sifre": "gucluSifre123"
}

try:
    # İsteği gönderiyoruz
    response = requests.post(url, json=veri)
    
    # Sonucu ekrana yazdırıyoruz
    print(f"Durum Kodu: {response.status_code}")
    print(f"Cevap: {response.json()}")
    
except Exception as e:
    print(f"Hata oluştu: {e}")