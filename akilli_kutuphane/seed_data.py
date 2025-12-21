from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app.models.fine import Fine
from werkzeug.security import generate_password_hash

app = create_app()

def veri_yukle():
    with app.app_context():
        print("--- Veritabanı Temizleniyor ---")
        
        # Sadece bu tabloları hedef alıyoruz (View'lara dokunma!)
        tablolar = [Fine.__table__, Loan.__table__, Book.__table__, User.__table__]
        
        # Önce tabloları sil (Hata vermemesi için)
        db.metadata.drop_all(bind=db.engine, tables=tablolar)
        
        # Sonra tabloları yeniden oluştur
        db.metadata.create_all(bind=db.engine, tables=tablolar)

        print("--- Kullanıcılar Ekleniyor ---")
        admin = User(
            ad="Admin", soyad="Yonetici", 
            email="admin@kutuphane.com", 
            sifre=generate_password_hash("admin123"), 
            rol="admin"
        )
        
        ogr1 = User(ad="Ahmet", soyad="Yilmaz", email="ahmet@ogr.com", sifre=generate_password_hash("1234"), rol="student")
        ogr2 = User(ad="Ayse", soyad="Demir", email="ayse@ogr.com", sifre=generate_password_hash("1234"), rol="student")
        ogr3 = User(ad="Mehmet", soyad="Kaya", email="mehmet@ogr.com", sifre=generate_password_hash("1234"), rol="student")
        
        # Kullanıcıları ekle
        db.session.add_all([admin, ogr1, ogr2, ogr3])
        db.session.commit() # ID'lerin oluşması için commit şart
        
        print("--- Kitaplar Ekleniyor ---")
        kitaplar = [
            Book(ad="Çalıkuşu", yazar="Reşat Nuri Güntekin", kategori="Roman", stok=5),
            Book(ad="Saatleri Ayarlama Enstitüsü", yazar="Ahmet Hamdi Tanpınar", kategori="Roman", stok=3),
            Book(ad="Kürk Mantolu Madonna", yazar="Sabahattin Ali", kategori="Roman", stok=10),
            Book(ad="İnce Memed", yazar="Yaşar Kemal", kategori="Roman", stok=4),
            Book(ad="Araba Sevdası", yazar="Recaizade Mahmut Ekrem", kategori="Roman", stok=2),
            Book(ad="Suç ve Ceza", yazar="Dostoyevski", kategori="Klasik", stok=7),
            Book(ad="Sefiller", yazar="Victor Hugo", kategori="Klasik", stok=3),
            Book(ad="1984", yazar="George Orwell", kategori="Distopya", stok=15),
            Book(ad="Hayvan Çiftliği", yazar="George Orwell", kategori="Distopya", stok=12),
            Book(ad="Satranç", yazar="Stefan Zweig", kategori="Hikaye", stok=20),
            Book(ad="Kozmos", yazar="Carl Sagan", kategori="Bilim", stok=5),
            Book(ad="Zamanın Kısa Tarihi", yazar="Stephen Hawking", kategori="Bilim", stok=4),
            Book(ad="Atomik Alışkanlıklar", yazar="James Clear", kategori="Kişisel Gelişim", stok=8),
            Book(ad="Nutuk", yazar="Mustafa Kemal Atatürk", kategori="Tarih", stok=19),
            Book(ad="Şu Çılgın Türkler", yazar="Turgut Özakman", kategori="Tarih", stok=6),
        ]

        db.session.add_all(kitaplar)
        db.session.commit()
        
        print("--- İşlem Tamamlandı! Veritabanı Hazır. ---")

if __name__ == "__main__":
    veri_yukle()