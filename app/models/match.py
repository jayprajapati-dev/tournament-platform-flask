from app import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    round_number = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='matches')
    team1 = db.relationship('Team', foreign_keys=[team1_id], back_populates='matches_as_team1')
    team2 = db.relationship('Team', foreign_keys=[team2_id], back_populates='matches_as_team2')
    winner = db.relationship('Team', foreign_keys=[winner_id], back_populates='won_matches')
    
    def __repr__(self):
        return f'<Match {self.id} in Tournament {self.tournament_id}>' 