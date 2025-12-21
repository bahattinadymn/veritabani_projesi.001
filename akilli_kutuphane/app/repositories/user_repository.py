from app import db
from app.models.user import User

class UserRepository:
    # Yeni kullanıcı oluşturma
    def create(self, ad, soyad, email, sifre_hash, role='user'):
        new_user = User(ad=ad, soyad=soyad, email=email, sifre_hash=sifre_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    # E-posta ile kullanıcı bulma (Giriş için)
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    # ID ile kullanıcı bulma
    def get_by_id(self, user_id):
        return User.query.get(user_id)