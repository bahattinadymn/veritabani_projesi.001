from flask import Blueprint, request, jsonify
from app.services.loan_service import LoanService
from flask_jwt_extended import jwt_required, get_jwt_identity

loan_bp = Blueprint('loan_bp', __name__)
loan_service = LoanService()

# 1. ÖDÜNÇ ALMA
@loan_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        user_id = int(get_jwt_identity()) # ID'yi sayıya çevir

        if not book_id:
            return jsonify({"msg": "Kitap seçilmedi!"}), 400

        loan_service.create_loan(user_id, book_id)
        
        return jsonify({"message": "✅ Kitap ödünç alındı. Keyifli okumalar!"}), 201

    except Exception as e:
        print(f"ÖDÜNÇ HATASI: {e}")
        return jsonify({"msg": str(e)}), 400

# 2. PROFİL İÇİN: KİTAPLARIM (Eksik olan buydu)
@loan_bp.route('/my', methods=['GET'])
@jwt_required()
def my_loans():
    try:
        user_id = int(get_jwt_identity())
        loans = loan_service.loan_repo.get_active_loans_by_user(user_id)
        
        data = []
        for loan in loans:
            data.append({
                "loan_id": loan.id,
                "kitap_adi": loan.book.ad if loan.book else "Bilinmeyen",
                "yazar": loan.book.yazar if loan.book else "-",
                "alis_tarihi": loan.alis_tarihi.strftime('%Y-%m-%d'),
                "son_teslim": loan.son_teslim_tarihi.strftime('%Y-%m-%d')
            })
            
        return jsonify(data), 200
    except Exception as e:
        print(f"PROFİL HATASI: {e}")
        return jsonify({"msg": "Profil verisi çekilemedi"}), 500

# 3. İADE ETME
@loan_bp.route('/return', methods=['POST'])
@jwt_required()
def return_book():
    try:
        data = request.get_json()
        loan_service.return_book(data.get('loan_id'))
        return jsonify({"message": "İade alındı."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400