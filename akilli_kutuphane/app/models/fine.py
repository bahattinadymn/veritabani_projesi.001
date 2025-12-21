from app import db
from datetime import datetime

class Fine(db.Model):
    __tablename__ = 'fines'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    tutar = db.Column(db.Numeric(10, 2), nullable=False)
    aciklama = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkiler (Veriye kolay erişim için)
    user = db.relationship('User', backref='fines')
    loan = db.relationship('Loan', backref='fine')