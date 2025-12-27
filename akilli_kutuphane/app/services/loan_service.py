from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
# 👇 GÜNCELLEME: Yeni mail fonksiyonunu buraya ekledik
from app.services.email_service import send_email, send_return_notification
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
        son_teslim = datetime.utcnow() + timedelta(days=14)
        new_loan = self.loan_repo.create(user_id, book_id, son_teslim)
        
        # 5. MAİL GÖNDERME (Ödünç Alma)
        try:
            user = self.user_repo.get_by_id(user_id)
            
            if user: 
                icerik = f"""
                Merhaba {user.ad},
                
                '{book.ad}' kitabını ödünç alma işleminiz başarılı.
                
                Son Teslim Tarihi: {son_teslim.strftime('%d.%m.%Y')}
                
                Keyifli okumalar dileriz.
                """
                send_email("Kitap Ödünç Alındı 📖", user.email, icerik)
                
        except Exception as e:
            print(f"Ödünç alma mail hatası: {e}")

        return new_loan

    def return_book(self, loan_id):
        # 1. Kaydı Bul
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            raise Exception("Kayıt bulunamadı.")
        
        if loan.iade_tarihi:
            raise Exception("Bu kitap zaten iade edilmiş.")
            
        # 2. İade işlemini yap ve varsa cezayı hesapla
        ceza_tutari = self.loan_repo.return_loan(loan)
        
        # 3. 👇 YENİ EKLENEN KISIM: İADE VE CEZA MAİLİ GÖNDER 👇
        try:
            # Kullanıcı ve kitap bilgilerine ihtiyacımız var
            user = self.user_repo.get_by_id(loan.user_id)
            book = self.book_repo.get_by_id(loan.book_id)

            if user and book:
                # Az önce email_service dosyasına eklediğimiz özel fonksiyonu çağırıyoruz
                send_return_notification(user.email, user.ad, book.ad, ceza_tutari)
                print(f"✅ İade maili tetiklendi: {user.email}")
                
        except Exception as e:
            # Mail gitmese bile işlem başarılı sayılsın
            print(f"❌ İade maili gönderilemedi: {e}")
        
        return ceza_tutari