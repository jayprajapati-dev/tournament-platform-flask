from app import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    position = db.Column(db.Integer, nullable=False)  # 1 for first place, 2 for second, etc.
    prize_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='results')
    user = db.relationship('User', back_populates='tournament_results')
    team = db.relationship('Team', back_populates='tournament_results')
    
    def __repr__(self):
        return f'<Result {self.id} for User {self.user_id} in Tournament {self.tournament_id}>' 