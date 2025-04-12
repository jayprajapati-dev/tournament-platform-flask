from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    free_fire_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    wallet_balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    referral_code = db.Column(db.String(10), unique=True)
    referred_by = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participations = db.relationship('Participation', back_populates='user', lazy=True)
    participants = db.relationship('Participant', back_populates='user', lazy=True)
    wallet_transactions = db.relationship('WalletTransaction', back_populates='user', lazy=True)
    withdrawals = db.relationship('Withdrawal', back_populates='withdrawal_user', foreign_keys='Withdrawal.user_id', lazy=True)
    processed_withdrawals = db.relationship('Withdrawal', back_populates='processor', foreign_keys='Withdrawal.processed_by', lazy=True)
    team_memberships = db.relationship('TeamMember', back_populates='user', lazy=True)
    tournament_results = db.relationship('Result', back_populates='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_referral_count(self):
        return len(self.referrals_made_by_me)
    
    def get_eligible_referral_bonus(self):
        count = self.get_referral_count()
        bonuses = {5: 20, 10: 50, 15: 80}
        for threshold, bonus in sorted(bonuses.items(), reverse=True):
            if count >= threshold:
                return bonus
        return 0
    
    def __repr__(self):
        return f'<User {self.full_name}>' 