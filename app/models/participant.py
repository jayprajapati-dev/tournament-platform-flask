from app import db
from datetime import datetime

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, eliminated, winner
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='participants')
    user = db.relationship('User', back_populates='participants')
    team = db.relationship('Team', back_populates='participants')
    
    def __repr__(self):
        return f'<Participant {self.user_id} in Tournament {self.tournament_id}>'