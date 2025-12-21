from flask import Blueprint, render_template

# url_prefix yok, çünkü bu ana sayfa (/) olacak
web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/login')
def login_page():
    return render_template('login.html')

@web_bp.route('/register')
def register_page():
    return render_template('register.html')
@web_bp.route('/books')
def books_page():
    return render_template('books.html')
@web_bp.route('/profile')
def profile_page():
    return render_template('profile.html')
@web_bp.route('/leaderboard')
def leaderboard_page():
    return render_template('leaderboard.html')
@web_bp.route('/admin')
def admin_page():
    # Buraya normalde giriş kontrolü de konur ama şimdilik arayüzde JS ile koruyacağız
    return render_template('admin.html')
