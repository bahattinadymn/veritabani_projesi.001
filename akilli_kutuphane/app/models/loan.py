from app import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loans'
    
    # --- BU SATIR ÇOK ÖNEMLİ (TRIGGER HATASINI ÇÖZER) ---
    # Trigger kullandığımız için SQLAlchemy'ye "OUTPUT kullanma" diyoruz.
    __table_args__ = {'implicit_returning': False}
    # ----------------------------------------------------

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    alis_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    son_teslim_tarihi = db.Column(db.DateTime, nullable=False)
    iade_tarihi = db.Column(db.DateTime, nullable=True)

    # --- YENİ EKLEDİĞİMİZ CEZA SÜTUNU ---
    ceza_tutari = db.Column(db.Numeric(10, 2), default=0) 

    # İlişkiler
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return f'<Loan {self.id}>'