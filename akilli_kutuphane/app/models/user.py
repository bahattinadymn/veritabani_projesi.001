from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Şifre ve Rol alanları
    sifre_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

