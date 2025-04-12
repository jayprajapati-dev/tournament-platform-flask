from app import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    captain_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='teams')
    captain = db.relationship('User', backref=db.backref('captained_teams', lazy=True))
    members = db.relationship('TeamMember', back_populates='team')
    participations = db.relationship('Participation', back_populates='team')
    participants = db.relationship('Participant', back_populates='team')
    matches_as_team1 = db.relationship('Match', foreign_keys='Match.team1_id', back_populates='team1')
    matches_as_team2 = db.relationship('Match', foreign_keys='Match.team2_id', back_populates='team2')
    won_matches = db.relationship('Match', foreign_keys='Match.winner_id', back_populates='winner')
    tournament_results = db.relationship('Result', back_populates='team')
    
    def __repr__(self):
        return f'<Team {self.name}>' 