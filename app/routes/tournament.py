from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Tournament, Team, Match, Participation
from datetime import datetime

tournament_bp = Blueprint('tournament', __name__)

@tournament_bp.route('/tournaments')
def list_tournaments():
    tournaments = Tournament.query.order_by(Tournament.start_date.desc()).all()
    return render_template('tournament/list.html', tournaments=tournaments)

@tournament_bp.route('/tournament/<int:tournament_id>')
def tournament_details(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    teams = Team.query.filter_by(tournament_id=tournament_id).all()
    matches = Match.query.filter_by(tournament_id=tournament_id).all()
    participants = Participation.query.filter_by(tournament_id=tournament_id).all()
    return render_template('tournament/details.html', 
                         tournament=tournament, 
                         teams=teams, 
                         matches=matches, 
                         participants=participants)

@tournament_bp.route('/tournament/<int:tournament_id>/join', methods=['POST'])
@login_required
def join_tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    
    # Check if tournament is full
    if tournament.get_participant_count() >= tournament.max_participants:
        flash('Tournament is already full.', 'danger')
        return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))
    
    # Check if user has already joined
    if Participation.query.filter_by(tournament_id=tournament_id, user_id=current_user.id).first():
        flash('You have already joined this tournament.', 'warning')
        return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))
    
    # Check if user has enough balance
    if current_user.wallet_balance < tournament.entry_fee:
        flash('Insufficient wallet balance.', 'danger')
        return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))
    
    # Deduct entry fee
    current_user.wallet_balance -= tournament.entry_fee
    
    # Create participation entry
    participation = Participation(
        tournament_id=tournament_id,
        user_id=current_user.id,
        joined_at=datetime.utcnow()
    )
    db.session.add(participation)
    db.session.commit()
    
    flash('Successfully joined the tournament!', 'success')
    return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))

@tournament_bp.route('/tournament/<int:tournament_id>/leave', methods=['POST'])
@login_required
def leave_tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    participation = Participation.query.filter_by(tournament_id=tournament_id, user_id=current_user.id).first_or_404()
    
    # Check if tournament has already started
    if datetime.utcnow() >= tournament.start_date:
        flash('Cannot leave tournament after it has started.', 'danger')
        return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))
    
    # Refund entry fee
    current_user.wallet_balance += tournament.entry_fee
    
    # Remove participation
    db.session.delete(participation)
    db.session.commit()
    
    flash('Successfully left the tournament. Entry fee has been refunded.', 'success')
    return redirect(url_for('tournament.tournament_details', tournament_id=tournament_id))

@tournament_bp.route('/tournament/<int:tournament_id>/matches')
def tournament_matches(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    matches = Match.query.filter_by(tournament_id=tournament_id).order_by(Match.scheduled_time).all()
    return render_template('tournament/matches.html', tournament=tournament, matches=matches)

@tournament_bp.route('/tournament/<int:tournament_id>/teams')
def tournament_teams(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    teams = Team.query.filter_by(tournament_id=tournament_id).all()
    return render_template('tournament/teams.html', tournament=tournament, teams=teams)

@tournament_bp.route('/tournament/<int:tournament_id>/participants')
def tournament_participants(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    participants = Participation.query.filter_by(tournament_id=tournament_id).all()
    return render_template('tournament/participants.html', tournament=tournament, participants=participants) 