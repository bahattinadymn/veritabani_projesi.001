from app.repositories.book_repository import BookRepository

class BookService:
    def __init__(self):
        self.book_repo = BookRepository()

    # Kitapları Listele
    def list_all_books(self):
        return self.book_repo.get_all()

    # Arama Yap
    def search_books(self, query):
        return self.book_repo.search(query)

    # Kategoriye Göre Getir
    def get_books_by_category(self, category):
        return self.book_repo.get_by_category(category)

    # --- YENİ EKLENEN KISIM: GÜVENLİ KİTAP EKLEME ---
    def add_book(self, ad, yazar, kategori, stok):
        try:
            print(f"SERVİS: Kitap ekleniyor -> {ad}, {yazar}, Stok: {stok}")
            return self.book_repo.create(ad, yazar, kategori, stok)
        except Exception as e:
            print(f"SERVİS HATASI (Kitap Ekleme): {e}")
            raise e