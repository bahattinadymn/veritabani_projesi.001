from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
auth_bp = Blueprint('auth_bp', __name__)
auth_service = AuthService()

# --- KAYIT OL ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        auth_service.register_user(data['ad'], data['soyad'], data['email'], data['sifre'])
        return jsonify({"message": "Kayıt başarılı"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- GİRİŞ YAP ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        # Servisten verileri al
        token, user = auth_service.login_user(data['email'], data['sifre'])
        
        # Web sitesine (Frontend) gidecek cevap
        # Burada anahtar kelimemiz: 'token'
        return jsonify({
            "token": token,
            "user": {
                "ad": user.ad,
                "soyad": user.soyad,
                "email": user.email,
                "role": user.role
            }
        }), 200
        
    except Exception as e:
        print(f"LOGIN HATASI: {e}") # Terminalde hatayı görmek için
        return jsonify({"error": str(e)}), 401




@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        eski_sifre = data.get('eski_sifre')
        yeni_sifre = data.get('yeni_sifre')
        
        if not eski_sifre or not yeni_sifre:
            return jsonify({"msg": "Eksik bilgi girdiniz."}), 400
            
        auth_service.change_password(user_id, eski_sifre, yeni_sifre)
        
        return jsonify({"message": "✅ Şifreniz başarıyla güncellendi."}), 200
        
    except Exception as e:
        return jsonify({"msg": str(e)}), 400