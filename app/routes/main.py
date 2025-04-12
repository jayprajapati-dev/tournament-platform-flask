from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/terms')
def terms():
    return render_template('main/terms.html')

@main_bp.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

@main_bp.route('/disclaimer')
def disclaimer():
    return render_template('main/disclaimer.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html') 