from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    @app.template_filter('month_name')
    def month_name(month):
        try:
            m = int(month)
            ptbr = [
                'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ]
            return ptbr[m-1]
        except (ValueError, IndexError):
            return ''

    from app.auth.routes import auth as auth_bp
    from app.expenses.routes import expenses as exp_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(exp_bp)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('expenses.dashboard'))
        return redirect(url_for('auth.login'))
    
    with app.app_context():
        db.create_all()

    return app