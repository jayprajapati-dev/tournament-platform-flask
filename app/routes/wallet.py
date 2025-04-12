from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.wallet_transaction import WalletTransaction
from app.models.withdrawal import Withdrawal
from datetime import datetime

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/wallet')
@login_required
def view_wallet():
    transactions = WalletTransaction.query.filter_by(
        user_id=current_user.id
    ).order_by(WalletTransaction.created_at.desc()).all()
    
    withdrawals = Withdrawal.query.filter_by(
        user_id=current_user.id
    ).order_by(Withdrawal.requested_at.desc()).all()
    
    return render_template('wallet/view.html',
                         transactions=transactions,
                         withdrawals=withdrawals)

@wallet_bp.route('/wallet/topup', methods=['POST'])
@login_required
def topup_wallet():
    amount = float(request.form.get('amount', 0))
    if amount <= 0:
        flash('Invalid amount', 'danger')
        return redirect(url_for('wallet.view_wallet'))
    
    # Create transaction
    transaction = WalletTransaction(
        user_id=current_user.id,
        amount=amount,
        transaction_type='topup',
        status='completed'
    )
    
    # Update wallet balance
    current_user.wallet_balance += amount
    
    db.session.add(transaction)
    db.session.commit()
    
    flash(f'Successfully added ₹{amount} to your wallet!', 'success')
    return redirect(url_for('wallet.view_wallet'))

@wallet_bp.route('/wallet/withdraw', methods=['POST'])
@login_required
def request_withdrawal():
    amount = float(request.form.get('amount', 0))
    payment_method = request.form.get('payment_method')
    payment_details = request.form.get('payment_details')
    
    # Validate amount
    if amount < current_app.config['MIN_WITHDRAWAL_AMOUNT']:
        flash(f'Minimum withdrawal amount is ₹{current_app.config["MIN_WITHDRAWAL_AMOUNT"]}', 'danger')
        return redirect(url_for('wallet.view_wallet'))
    
    if amount > current_user.wallet_balance:
        flash('Insufficient wallet balance', 'danger')
        return redirect(url_for('wallet.view_wallet'))
    
    # Create withdrawal request
    withdrawal = Withdrawal(
        user_id=current_user.id,
        amount=amount,
        payment_method=payment_method,
        payment_details=payment_details
    )
    
    # Deduct from wallet balance
    current_user.wallet_balance -= amount
    
    # Create transaction
    transaction = WalletTransaction(
        user_id=current_user.id,
        amount=-amount,
        transaction_type='withdrawal',
        reference_id=str(withdrawal.id),
        status='pending'
    )
    
    db.session.add(withdrawal)
    db.session.add(transaction)
    db.session.commit()
    
    flash('Withdrawal request submitted successfully!', 'success')
    return redirect(url_for('wallet.view_wallet')) 