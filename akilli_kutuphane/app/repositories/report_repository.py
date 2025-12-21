from app import db
from app.models.user import User
from app.models.loan import Loan
from sqlalchemy import func, desc

class ReportRepository:
    def get_top_readers(self):
        """
        En çok kitap ödünç alan kullanıcıları çoktan aza doğru sıralar.
        SQL Karşılığı:
        SELECT u.ad, u.soyad, COUNT(l.id) as kitap_sayisi 
        FROM users u 
        JOIN loans l ON u.id = l.user_id 
        GROUP BY u.id, u.ad, u.soyad 
        ORDER BY kitap_sayisi DESC
        """
        results = db.session.query(
            User.ad,
            User.soyad,
            func.count(Loan.id).label('kitap_sayisi')
        ).join(Loan, User.id == Loan.user_id)\
         .group_by(User.id, User.ad, User.soyad)\
         .order_by(desc('kitap_sayisi'))\
         .limit(10).all()
        
        return results