from app import db
from app.models.loan import Loan
from sqlalchemy import text 
from datetime import datetime

class LoanRepository:
    # 1. YENİ ÖDÜNÇ KAYDI
    def create(self, user_id, book_id, son_teslim):
        new_loan = Loan(user_id=user_id, book_id=book_id, son_teslim_tarihi=son_teslim)
        db.session.add(new_loan)
        db.session.commit()
        return new_loan

    # 2. ID İLE BULMA
    def get_by_id(self, loan_id):
        return Loan.query.get(loan_id)

    # 3. İADE ETME VE CEZA YAZMA
    def return_loan(self, loan):
        simdi = datetime.now()
        hesaplanan_ceza = 0
        
        # Ceza hesapla
        if loan.son_teslim_tarihi and simdi > loan.son_teslim_tarihi:
            gecikme = (simdi - loan.son_teslim_tarihi).days
            if gecikme > 0:
                hesaplanan_ceza = gecikme * 5 # Günlük 5 TL
        
        loan.iade_tarihi = simdi
        loan.ceza_tutari = hesaplanan_ceza
        db.session.commit()
        return hesaplanan_ceza

    # 4. AKTİF KİTAP KONTROLÜ
    def get_active_loan_by_user_and_book(self, user_id, book_id):
        return Loan.query.filter_by(user_id=user_id, book_id=book_id, iade_tarihi=None).first()

    # 5. CEZA SORGUSU (STORED PROCEDURE)
    def get_loans_with_penalty_procedure(self, user_id):
        try:
            sql = text("EXEC sp_KullaniciCezalariniGetir :uid")
            result = db.session.execute(sql, {'uid': user_id})
            loans_data = []
            for row in result:
                loans_data.append({
                    "loan_id": row.loan_id,
                    "kitap_adi": row.kitap_adi,
                    "yazar": row.yazar,
                    "alis_tarihi": row.alis_tarihi,
                    "son_teslim_tarihi": row.son_teslim_tarihi,
                    "gecikme_gun": row.gecikme_gun,
                    "ceza_tutari": row.ceza_tutari
                })
            return loans_data
        except Exception as e:
            print(f"Prosedür Hatası: {e}")
            return []

    # --- EKSİK OLAN KISIMLAR (UNDEFINED HATASINI ÇÖZECEK) ---
    
    # 6. İSTATİSTİKLERİ GETİR
    def get_user_stats(self, user_id):
        # Okunan (İade edilmiş) kitap sayısı
        okunan = Loan.query.filter(Loan.user_id == user_id, Loan.iade_tarihi != None).count()
        # Aktif kitap sayısı
        aktif = Loan.query.filter(Loan.user_id == user_id, Loan.iade_tarihi == None).count()
        # Toplam ödenen ceza
        toplam_ceza = db.session.query(db.func.sum(Loan.ceza_tutari)).filter(Loan.user_id == user_id).scalar() or 0
        
        return {
            "okunan": okunan,
            "aktif": aktif,
            "toplam_ceza": toplam_ceza
        }

    # 7. CEZA GEÇMİŞİNİ GETİR
    def get_fine_history(self, user_id):
        # Sadece cezası olan ve iade edilmişleri getir
        return Loan.query.filter(Loan.user_id == user_id, Loan.ceza_tutari > 0).order_by(Loan.iade_tarihi.desc()).all()