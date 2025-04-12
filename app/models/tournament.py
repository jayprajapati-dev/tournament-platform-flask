from datetime import datetime
from app import db

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    game = db.Column(db.String(50), nullable=False)
    entry_fee = db.Column(db.Float, default=0.0)
    prize_pool = db.Column(db.Float, default=0.0)
    max_participants = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, in_progress, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participations = db.relationship('Participation', back_populates='tournament', lazy=True)
    participants = db.relationship('Participant', back_populates='tournament', lazy=True)
    teams = db.relationship('Team', back_populates='tournament', lazy=True)
    results = db.relationship('Result', back_populates='tournament', lazy=True)
    matches = db.relationship('Match', back_populates='tournament', lazy=True)
    
    def get_participant_count(self):
        return len(self.participations)
    
    def is_full(self):
        return self.get_participant_count() >= self.max_participants
    
    def is_registration_open(self):
        return (self.status == 'upcoming' and 
                datetime.utcnow() < self.start_date and 
                not self.is_full())
    
    def __repr__(self):
        return f'<Tournament {self.title}>' 