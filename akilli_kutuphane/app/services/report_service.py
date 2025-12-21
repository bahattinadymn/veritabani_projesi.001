from app.repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self):
        self.repo = ReportRepository()
    
    def get_leaderboard(self):
        raw_data = self.repo.get_top_readers()
        
        # Veritabanı çıktısını sözlük (JSON) listesine çeviriyoruz
        leaderboard = []
        for row in raw_data:
            leaderboard.append({
                "ad": row.ad,
                "soyad": row.soyad,
                "okunan_kitap": row.kitap_sayisi
            })
        return leaderboard