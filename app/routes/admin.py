from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.withdrawal import Withdrawal
from app.models.referral import Referral
from app.models.wallet_transaction import WalletTransaction
from app.models.participation import Participation
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def dashboard():
    # Calculate statistics
    stats = {
        'total_users': User.query.count(),
        'total_revenue': sum(t.amount for t in WalletTransaction.query.filter_by(transaction_type='tournament_entry', status='completed').all()),
        'active_tournaments': Tournament.query.filter_by(status='in_progress').count(),
        'total_participants': Participation.query.count()
    }
    
    # Get recent transactions
    recent_transactions = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_transactions=recent_transactions)

@admin_bp.route('/admin/tournaments')
@admin_required
def manage_tournaments():
    tournaments = Tournament.query.order_by(Tournament.start_date.desc()).all()
    return render_template('admin/tournaments.html', tournaments=tournaments)

@admin_bp.route('/admin/tournament/new', methods=['GET', 'POST'])
@admin_required
def new_tournament():
    if request.method == 'POST':
        tournament = Tournament(
            title=request.form['title'],
            description=request.form['description'],
            game=request.form['game'],
            entry_fee=float(request.form['entry_fee']),
            prize_pool=float(request.form['prize_pool']),
            max_participants=int(request.form['max_participants']),
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        )
        db.session.add(tournament)
        db.session.commit()
        flash('Tournament created successfully!', 'success')
        return redirect(url_for('admin.manage_tournaments'))
    return render_template('admin/tournament_form.html')

@admin_bp.route('/admin/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/withdrawals')
@admin_required
def manage_withdrawals():
    withdrawals = Withdrawal.query.order_by(Withdrawal.requested_at.desc()).all()
    return render_template('admin/withdrawals.html', withdrawals=withdrawals)

@admin_bp.route('/admin/withdrawal/<int:withdrawal_id>/approve', methods=['POST'])
@admin_required
def approve_withdrawal(withdrawal_id):
    withdrawal = Withdrawal.query.get_or_404(withdrawal_id)
    if withdrawal.status != 'pending':
        flash('Withdrawal request has already been processed.', 'warning')
        return redirect(url_for('admin.manage_withdrawals'))
    
    withdrawal.status = 'approved'
    withdrawal.processed_at = datetime.utcnow()
    withdrawal.processed_by = current_user.id
    
    # Update transaction status
    transaction = WalletTransaction.query.filter_by(
        reference_id=str(withdrawal_id),
        transaction_type='withdrawal'
    ).first()
    if transaction:
        transaction.status = 'completed'
    
    db.session.commit()
    flash('Withdrawal request approved successfully!', 'success')
    return redirect(url_for('admin.manage_withdrawals'))

@admin_bp.route('/admin/withdrawal/<int:withdrawal_id>/reject', methods=['POST'])
@admin_required
def reject_withdrawal(withdrawal_id):
    withdrawal = Withdrawal.query.get_or_404(withdrawal_id)
    if withdrawal.status != 'pending':
        flash('Withdrawal request has already been processed.', 'warning')
        return redirect(url_for('admin.manage_withdrawals'))
    
    withdrawal.status = 'rejected'
    withdrawal.processed_at = datetime.utcnow()
    withdrawal.processed_by = current_user.id
    withdrawal.rejection_reason = request.form.get('reason', 'No reason provided')
    
    # Return amount to user's wallet
    user = User.query.get(withdrawal.user_id)
    user.wallet_balance += withdrawal.amount
    
    # Update transaction status
    transaction = WalletTransaction.query.filter_by(
        reference_id=str(withdrawal_id),
        transaction_type='withdrawal'
    ).first()
    if transaction:
        transaction.status = 'failed'
    
    db.session.commit()
    flash('Withdrawal request rejected successfully!', 'success')
    return redirect(url_for('admin.manage_withdrawals'))

@admin_bp.route('/admin/referrals')
@admin_required
def manage_referrals():
    referrals = Referral.query.order_by(Referral.created_at.desc()).all()
    return render_template('admin/referrals.html', referrals=referrals) 