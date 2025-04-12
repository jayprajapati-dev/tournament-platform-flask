from datetime import datetime
from app import db

class Withdrawal(db.Model):
    __tablename__ = 'withdrawals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    payment_method = db.Column(db.String(50), nullable=False)  # UPI, Bank Transfer, etc.
    payment_details = db.Column(db.String(255), nullable=False)  # UPI ID, Account Number, etc.
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rejection_reason = db.Column(db.Text)
    
    # Relationships
    withdrawal_user = db.relationship('User', foreign_keys=[user_id], back_populates='withdrawals')
    processor = db.relationship('User', foreign_keys=[processed_by], back_populates='processed_withdrawals')
    
    def __repr__(self):
        return f'<Withdrawal {self.id} by User {self.user_id}>' 