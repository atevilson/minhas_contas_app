from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(80), unique=True, nullable=False)
    password  = db.Column(db.String(255), nullable=False)
    expenses  = db.relationship('Expense', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Expense(db.Model):
    __tablename__ = 'expense'
    id            = db.Column(db.Integer, primary_key=True)
    origem        = db.Column(db.String(100), nullable=False)
    vencimento    = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    valor         = db.Column(db.Float, nullable=False)
    status        = db.Column(db.String(10), default='A pagar') 
    quem_paga     = db.Column(db.String(100), nullable=True)
    tipo          = db.Column(db.String(10), nullable=False)  
    parcelas      = db.Column(db.Integer, default=1)
    parcel_number = db.Column(db.Integer, default=1)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def mes(self):
        return self.vencimento.month

    def __repr__(self):
        return f'<Expense {self.origem} #{self.parcel_number}/{self.parcelas}>'