from app import db
from datetime import datetime

class Participation(db.Model):
    __tablename__ = 'participations'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    status = db.Column(db.String(20), default='active')  # active, eliminated, winner
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='participations')
    user = db.relationship('User', back_populates='participations')
    team = db.relationship('Team', back_populates='participations')
    
    def __repr__(self):
        return f'<Participation {self.id} for User {self.user_id} in Tournament {self.tournament_id}>' 