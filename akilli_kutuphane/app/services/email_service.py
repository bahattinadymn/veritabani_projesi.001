from flask_mail import Message
from app import mail
from flask import current_app
from threading import Thread
import time  # 👈 EKLENDİ: Süre tutmak için gerekli kütüphane

# --- 1. ARKA PLAN GÖNDERİCİ (GÜNCELLENDİ) ---
def send_async_email(app, msg, delay=0):
    """
    Maili arka planda gönderir. 
    Eğer 'delay' (gecikme) süresi verilirse, o kadar saniye bekleyip sonra gönderir.
    """
    with app.app_context():
        try:
            if delay > 0:
                print(f"⏳ Mail kuyruğa alındı, {delay} saniye bekleniyor...")
                time.sleep(delay) # 👈 İŞTE BURASI: Arka plandaki işçiyi uyutuyoruz
            
            mail.send(msg)
            print(f"📧 Mail başarıyla gönderildi: {msg.recipients}")
            
        except Exception as e:
            print(f"❌ Mail Hatası: {e}")

# --- 2. GENEL MAİL FONKSİYONU (GÜNCELLENDİ) ---
def send_email(subject, recipient, body, delay=0):
    """
    Normal mailler için delay=0 (anında gider).
    İstenirse delay parametresi ile gecikme verilebilir.
    """
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        
        app = current_app._get_current_object()
        
        # Gecikme süresini (delay) de parametre olarak gönderiyoruz
        Thread(target=send_async_email, args=(app, msg, delay)).start()
        return True
    except Exception as e:
        print(f"Mail Servis Hatası: {e}")
        return False

# --- 3. İADE VE CEZA BİLDİRİMİ (GÜNCELLENDİ) ---
def send_return_notification(alici_email, kullanici_adi, kitap_adi, ceza_tutari=0):
    """
    Bu fonksiyon çağrıldığında maili hazırlar ama
    send_email fonksiyonuna '60 saniye bekle' emri verir.
    """
    try:
        konu = "📚 Kitap İade İşlemi Bildirimi"
        
        if ceza_tutari > 0:
            durum_mesaji = f"⚠️ GECİKME CEZASI: Hesabınıza {ceza_tutari} TL ceza yansıtılmıştır."
        else:
            durum_mesaji = "✅ TEŞEKKÜRLER: Kitabı zamanında iade ettiğiniz için teşekkür ederiz."

        icerik = f"""
        Sayın {kullanici_adi},

        '{kitap_adi}' isimli kitabın iade işlemi başarıyla gerçekleşmiştir.

        DURUM: {durum_mesaji}

        (Bu mail işleminizden 1 dakika sonra otomatik olarak gönderilmiştir.)

        İyi günler dileriz.
        KTÜ Kütüphane Otomasyonu
        """
        
        # 👇 HOCANIN İSTEDİĞİ KISIM: delay=60 (60 Saniye Gecikme)
        send_email(konu, alici_email, icerik, delay=60)
        
        return True

    except Exception as e:
        print(f"İade maili oluşturulurken hata: {e}")
        return False