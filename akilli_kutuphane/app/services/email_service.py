from flask_mail import Message
from app import mail
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    # Arka planda mail atarken uygulama context'ine ihtiyaç duyar
    with app.app_context():
        try:
            mail.send(msg)
            print("📧 Mail başarıyla gönderildi!")
        except Exception as e:
            print(f"❌ Mail Hatası: {e}")

def send_email(subject, recipient, body):
    try:
        # Mesajı Hazırla
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        
        # Siteyi dondurmamak için işlemi yan şeride (Thread) alıyoruz
        app = current_app._get_current_object()
        Thread(target=send_async_email, args=(app, msg)).start()
        
    except Exception as e:
        print(f"Mail Servis Hatası: {e}")