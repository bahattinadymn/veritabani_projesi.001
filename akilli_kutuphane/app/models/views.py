
from app import db

# Not: View'lar sadece okuma amaçlıdır, buraya veri ekleyemeyiz.

class RaporKitapDurumu(db.Model):
    __tablename__ = 'vw_KimHangiKitabiOkuyor'

    # SQLAlchemy her tabloda bir Primary Key ister. 
    # View'larda gerçek PK olmasa da mantıksal bir tane seçmeliyiz.
    loan_id = db.Column(db.Integer, primary_key=True)
    okuyucu = db.Column(db.String(150))
    kitap_adi = db.Column(db.String(150))
    alis_tarihi = db.Column(db.DateTime)
    son_teslim_tarihi = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'okuyucu': self.okuyucu,
            'kitap': self.kitap_adi,
            'alis': self.alis_tarihi.strftime('%Y-%m-%d'),
            'son_teslim': self.son_teslim_tarihi.strftime('%Y-%m-%d')
        }

class RaporLiderlik(db.Model):
    __tablename__ = 'vw_EnCokOkuyanlar'
    
 
    
    user_id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(150))
    okunan_kitap_sayisi = db.Column(db.Integer)

    def to_dict(self):
        return {
            'ad_soyad': self.ad_soyad,
            'skor': self.okunan_kitap_sayisi
        }