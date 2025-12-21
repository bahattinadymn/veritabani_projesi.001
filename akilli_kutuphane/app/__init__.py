from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

# Eklentileri tanımlıyoruz
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Eklentileri uygulamaya bağlıyoruz
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Modelleri (Tabloları) sisteme tanıtıyoruz
    from app.models.user import User
    from app.models.book import Book
    from app.models.loan import Loan
    from app.models.fine import Fine
    # fine modeli varsa ekle yoksa hata vermesin diye sildim, varsa ekleyebilirsin
    
    # --- BLUEPRINT (CONTROLLER) KAYITLARI ---
    # Burası ÇOK ÖNEMLİ: API olanlara 'url_prefix' ekliyoruz!
    
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.controllers.book_controller import book_bp
    app.register_blueprint(book_bp, url_prefix='/api/books')  # <-- Artık veriler /api/books altında

    from app.controllers.loan_controller import loan_bp
    app.register_blueprint(loan_bp, url_prefix='/api/loans')

    from app.controllers.report_controller import report_bp
    app.register_blueprint(report_bp, url_prefix='/api/reports')

    # Web Arayüzü (HTML Sayfaları)
    # Buna prefix koymuyoruz, çünkü doğrudan siteye girince görünsün istiyoruz.
    from app.controllers.web_controller import web_bp
    app.register_blueprint(web_bp)

    return app