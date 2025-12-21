from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

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