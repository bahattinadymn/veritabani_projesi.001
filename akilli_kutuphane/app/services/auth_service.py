from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, ad, soyad, email, sifre):
        if self.user_repo.get_by_email(email):
            raise Exception("Bu e-posta adresi zaten kayıtlı.")
            
        hashed_password = generate_password_hash(sifre)
        return self.user_repo.create(ad, soyad, email, hashed_password, role='user')

    def login_user(self, email, sifre):
        user = self.user_repo.get_by_email(email)
        
        if user and check_password_hash(user.sifre_hash, sifre):
            # --- DÜZELTME BURADA ---
            # Kütüphane hatasını önlemek için ID'yi string'e (yazıya) çeviriyoruz!
            # identity=str(user.id)
            token = create_access_token(identity=str(user.id))
            
            return token, user 
            
        raise Exception("E-posta veya şifre hatalı")