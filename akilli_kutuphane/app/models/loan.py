from app import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loans'
    
    # --- İŞTE SİHİRLİ SATIR BURASI ---
    # Bu ayar, SQL Server'da Trigger varken hata almanı engeller.
    # SQLAlchemy'ye "ID'yi almak için OUTPUT komutunu kullanma" der.
    __table_args__ = {'implicit_returning': False}
    # ---------------------------------

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    alis_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    son_teslim_tarihi = db.Column(db.DateTime, nullable=False)
    iade_tarihi = db.Column(db.DateTime, nullable=True)

    # İlişkiler
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))