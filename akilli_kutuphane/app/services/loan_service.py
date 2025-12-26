from app import db
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
import datetime
from sqlalchemy import text
from app.services.email_service import send_email
from app.repositories.user_repository import UserRepository # Kullanıcı mailini bulmak için

class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()
        self.book_repo = BookRepository()

    def create_loan(self, user_id, book_id):
        # 1. KİTAP ve STOK KONTROLÜ
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Kitap bulunamadı!")
        
        if book.stok < 1:
            raise Exception("Üzgünüz, bu kitap stokta kalmadı!")

        # 2. ZATEN ALMIŞ MI?
        existing_loan = self.loan_repo.get_active_loan_by_user_and_book(user_id, book_id)
        if existing_loan:
            raise Exception("Bu kitabı zaten okuyorsunuz.")

        try:
            # 3. ÖDÜNÇ KAYDI OLUŞTUR
            son_teslim = datetime.datetime.utcnow() + datetime.timedelta(days=14)
            
            # BURADA SADECE KAYIT YAPIYORUZ
            # SQL Trigger devreye girip Stok sayısını kendisi düşürecek!
            new_loan = self.loan_repo.create(user_id, book_id, son_teslim)
            
            user = self.user_repo.get_by_id(user_id) # Kullanıcıyı bul
            
            icerik = f"""
            Merhaba {user.ad},
            
            '{book.ad}' isimli kitabı ödünç aldın.
            Son teslim tarihin: {son_teslim.strftime('%d.%m.%Y')}
            
            Lütfen zamanında getirmeyi unutma!
            Keyifli okumalar.
            """
            send_email("Kitap Ödünç Alma İşlemi Başarılı 📖", user.email, icerik)
            # -----------------------------------------------

            return new_loan
        except Exception as e:
            
            # Hata olursa geri al
            db.session.rollback()
            print(f"ÖDÜNÇ HATASI: {e}")
            raise Exception(f"İşlem başarısız: {str(e)}")

    def return_book(self, loan_id):
        # İade işlemi
        try:
            # SQL Prosedürünü çağır (Ceza hesaplaması için)
            db.session.execute(text("EXEC sp_KitapIadeEt :id"), {'id': loan_id})
            db.session.commit()
            return "İade işlemi başarılı."
        except Exception as e:
            # Prosedür yoksa veya hata verirse manuel iade yap
            print(f"Prosedür Hatası (Normal iade deneniyor): {e}")
            db.session.rollback()
            
            loan = self.loan_repo.get_by_id(loan_id)
            if loan and not loan.iade_tarihi:
                loan.iade_tarihi = datetime.datetime.utcnow()
                db.session.commit()
                return "İade edildi (Prosedürsüz)."
            else:
                raise Exception("İade işlemi yapılamadı.")