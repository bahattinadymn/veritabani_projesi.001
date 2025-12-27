from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository # 1. Import Eklendi
from app.services.email_service import send_email
from datetime import datetime, timedelta

class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()
        self.book_repo = BookRepository()
        self.user_repo = UserRepository() 

    def create_loan(self, user_id, book_id):
        # 1. Kitabı Bul
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Kitap bulunamadı.")
            
        # 2. Stok Kontrolü
        if book.stok < 1:
            raise Exception("Bu kitap stokta yok.")
            
        # 3. Kullanıcının elinde bu kitap var mı?
        existing_loan = self.loan_repo.get_active_loan_by_user_and_book(user_id, book_id)
        if existing_loan:
            raise Exception("Bu kitabı zaten ödünç aldınız ve henüz iade etmediniz.")

        # 4. Kitabı Ver (Veritabanına Kayıt)
        # 14 gün sonrasını hesapla
        son_teslim = datetime.utcnow() + timedelta(days=14)
        new_loan = self.loan_repo.create(user_id, book_id, son_teslim)
        
        # 5. MAİL GÖNDERME İŞLEMİ (Hata veren yer burasıydı)
        try:
            # Artık self.user_repo tanımlı olduğu için çalışacak
            user = self.user_repo.get_by_id(user_id)
            
            if user: # Kullanıcı bulunduysa mail at
                icerik = f"""
                Merhaba {user.ad},
                
                '{book.ad}' kitabını ödünç alma işleminiz başarılı.
                
                Son Teslim Tarihi: {son_teslim.strftime('%d.%m.%Y')}
                
                Keyifli okumalar dileriz.
                """
                send_email("Kitap Ödünç Alındı 📖", user.email, icerik)
                
        except Exception as e:
            # Mail atılamasa bile işlem başarılı sayılsın, hata verip süreci durdurmasın
            print(f"Mail gönderme hatası: {e}")

        return new_loan

    def return_book(self, loan_id):
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            raise Exception("Kayıt bulunamadı.")
        
        if loan.iade_tarihi:
            raise Exception("Bu kitap zaten iade edilmiş.")
            
        # İade işlemini yap ve varsa cezayı döndür
        ceza_tutari = self.loan_repo.return_loan(loan)
        
        return ceza_tutari