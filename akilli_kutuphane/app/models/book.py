from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    yazar = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50))
    stok = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler (Backref kullanıyoruz, User modelindeki gibi çakışma olmasın diye)
    # loans = db.relationship('Loan', backref='book', lazy=True)