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
        loan_service.create_loan(int(get_jwt_identity()), data.get('book_id'))
        return jsonify({"message": "✅ Kitap ödünç alındı."}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

# 2. AKTİF KİTAPLARIM (PROFİL)
@loan_bp.route('/my', methods=['GET'])
@jwt_required()
def my_loans():
    try:
        user_id = int(get_jwt_identity())
        loans_data = loan_service.loan_repo.get_loans_with_penalty_procedure(user_id)
        
        formatted_data = []
        for item in loans_data:
            formatted_data.append({
                "loan_id": item['loan_id'],
                "kitap_adi": item['kitap_adi'],
                "yazar": item['yazar'],
                "alis_tarihi": item['alis_tarihi'].strftime('%Y-%m-%d'),
                "son_teslim": item['son_teslim_tarihi'].strftime('%Y-%m-%d'),
                "gecikme": item['gecikme_gun'], 
                "borc": item['ceza_tutari']
            })
        return jsonify(formatted_data), 200
    except Exception as e:
        return jsonify({"msg": "Veri çekilemedi"}), 500

# 3. İADE ETME
@loan_bp.route('/return', methods=['POST'])
@jwt_required()
def return_book():
    try:
        data = request.get_json()
        kesilen_ceza = loan_service.return_book(data.get('loan_id'))
        mesaj = "Kitap başarıyla iade edildi."
        if kesilen_ceza > 0:
            mesaj = f"Kitap iade edildi. Tahsil edilen gecikme cezası: {kesilen_ceza} TL ⚠️"
        return jsonify({"message": mesaj}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

# --- EKSİK OLAN ROTALAR (UNDEFINED HATASINI ÇÖZECEK) ---

# 4. İSTATİSTİKLER (Okunan Sayısı vs.)
@loan_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        user_id = int(get_jwt_identity())
        # Repo'daki yeni fonksiyonu çağır
        stats = loan_service.loan_repo.get_user_stats(user_id)
        return jsonify(stats), 200
    except Exception as e:
        print(f"Stats Hatası: {e}")
        return jsonify({"okunan": 0, "aktif": 0, "toplam_ceza": 0}), 200

# 5. CEZA GEÇMİŞİ TABLOSU
@loan_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        user_id = int(get_jwt_identity())
        history = loan_service.loan_repo.get_fine_history(user_id)
        
        data = []
        for item in history:
            data.append({
                "kitap_adi": item.book.ad if item.book else "Silinmiş",
                "aciklama": "Gecikme Cezası",
                "tarih": item.iade_tarihi.strftime('%d.%m.%Y'),
                "tutar": item.ceza_tutari
            })
        return jsonify(data), 200
    except Exception as e:
        print(f"Geçmiş Hatası: {e}")
        return jsonify([]), 200