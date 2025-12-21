from flask import Blueprint, jsonify
from app.services.report_service import ReportService

report_bp = Blueprint('report_bp', __name__)
report_service = ReportService()

@report_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        data = report_service.get_leaderboard()
        return jsonify(data), 200
    except Exception as e:
        print(f"Rapor Hatası: {e}")
        return jsonify({"error": "Liderlik tablosu yüklenemedi"}), 500