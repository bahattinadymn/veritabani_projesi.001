from flask import Blueprint, jsonify, request
from app.services.book_service import BookService
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

book_bp = Blueprint('book_bp', __name__)
book_service = BookService()

# LİSTELEME VE ARAMA
@book_bp.route('/', methods=['GET'])
def get_books():
    try:
        category = request.args.get('cat')
        query = request.args.get('q') # Arama kutusundan gelen veri

        # Eğer arama yapıldıysa (query varsa) öncelik onundur
        if query and query.strip() != "":
            books = book_service.search_books(query)
        elif category and category != "Tümü":
            books = book_service.get_books_by_category(category)
        else:
            books = book_service.list_all_books()

        # Veriyi hazırla
        data = []
        for book in books:
            data.append({
                "id": book.id,
                "ad": book.ad,
                "yazar": book.yazar,
                "kategori": book.kategori,
                "stok": book.stok,
                "durum": "Müsait" if book.stok > 0 else "Tükendi"
            })
        return jsonify(data), 200
    except Exception as e:
        print(f"LİSTELEME HATASI: {e}")
        return jsonify({"msg": f"Hata: {str(e)}"}), 500

# EKLEME (ADMIN)
@book_bp.route('/add', methods=['POST'])
@jwt_required()
def add_book():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user or user.role != 'admin':
            return jsonify({"msg": "Bu işlem için Admin yetkisi gerekiyor!"}), 403

        data = request.get_json()
        
        book_service.add_book(
            ad=data.get('ad'),
            yazar=data.get('yazar'),
            kategori=data.get('kategori', 'Genel'),
            stok=int(data.get('stok', 1))
        )

        return jsonify({"message": "✅ Kitap başarıyla eklendi!"}), 201

    except Exception as e:
        print(f"EKLEME HATASI: {e}")
        return jsonify({"msg": f"Hata: {str(e)}"}), 500