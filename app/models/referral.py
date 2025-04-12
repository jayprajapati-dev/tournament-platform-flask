from app import db
from datetime import datetime

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bonus_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref=db.backref('referrals_made_by_me', lazy=True))
    referred = db.relationship('User', foreign_keys=[referred_id], backref=db.backref('referrals_received_by_me', lazy=True))
    
    def __repr__(self):
        return f'<Referral {self.id} from User {self.referrer_id} to User {self.referred_id}>' 