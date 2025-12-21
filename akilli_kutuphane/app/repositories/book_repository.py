from app import db
from app.models.book import Book
from sqlalchemy import or_

class BookRepository:
    def get_all(self):
        return Book.query.order_by(Book.id.desc()).all()
    
    def search(self, query):
        if not query:
            return self.get_all()
            
        # SQL Server varsayılan olarak harf duyarsızdır (CI_AS).
        # Bu yüzden sadece 'like' kullanmak yeterlidir ve en hatasız yöntemdir.
        search_term = f"%{query}%"
        
        return Book.query.filter(
            or_(
                Book.ad.like(search_term),
                Book.yazar.like(search_term)
            )
        ).all()
    
    def get_by_category(self, category):
        return Book.query.filter_by(kategori=category).all()
        
    def create(self, ad, yazar, kategori, stok):
        try:
            new_book = Book(ad=ad, yazar=yazar, kategori=kategori, stok=stok)
            db.session.add(new_book)
            db.session.commit()
            return new_book
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_by_id(self, book_id):
        return Book.query.get(book_id)