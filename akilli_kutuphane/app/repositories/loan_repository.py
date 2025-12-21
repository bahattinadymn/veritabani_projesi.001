from app import db
from app.models.loan import Loan

class LoanRepository:
    def create(self, user_id, book_id, son_teslim_tarihi):
        new_loan = Loan(user_id=user_id, book_id=book_id, son_teslim_tarihi=son_teslim_tarihi)
        db.session.add(new_loan)
        db.session.commit()
        return new_loan

    # DÜZELTME: Profil sayfası bu fonksiyonu arıyordu!
    def get_active_loans_by_user(self, user_id):
        # İade tarihi BOŞ olanları (hala elinde olanları) getir
        return Loan.query.filter(Loan.user_id == user_id, Loan.iade_tarihi == None).all()

    def get_active_loan_by_user_and_book(self, user_id, book_id):
        return Loan.query.filter(Loan.user_id == user_id, Loan.book_id == book_id, Loan.iade_tarihi == None).first()
        
    def get_by_id(self, loan_id):
        return Loan.query.get(loan_id)