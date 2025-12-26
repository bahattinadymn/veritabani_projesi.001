from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.email_service import send_email

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()


    def register_user(self, ad, soyad, email, sifre):
        if self.user_repo.get_by_email(email):
            raise Exception("Bu e-posta adresi zaten kayıtlı.")
            
        hashed_password = generate_password_hash(sifre)
        
        # 1. Kullanıcıyı oluştur ve değişkene ata 
        user = self.user_repo.create(ad, soyad, email, hashed_password, role='user')

        # 2. Mail Gönder (user değişkeni oluştuktan sonra)
        try:
            icerik = f"""
            Merhaba {ad} {soyad},
            
            Akıllı Kütüphane sistemimize hoş geldin!
            Artık dilediğin kitabı ödünç alabilirsin.
            
            İyi okumalar dileriz.
            """
            send_email("Aramıza Hoş Geldin! 📚", email, icerik)
        except Exception as e:
            print(f"Mail hatası: {e}")

        # 3. En sonda kullanıcıyı döndür
        return user


    def login_user(self, email, sifre):
        user = self.user_repo.get_by_email(email)
        
        if user and check_password_hash(user.sifre_hash, sifre):
            # ID'yi string'e çevir
            token = create_access_token(identity=str(user.id))
            return token, user 
            
        raise Exception("E-posta veya şifre hatalı")