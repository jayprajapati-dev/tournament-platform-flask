from app import create_app, db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.match import Match
from app.models.participant import Participant
from app.models.participation import Participation
from app.models.result import Result
from app.models.withdrawal import Withdrawal
from app.models.wallet_transaction import WalletTransaction
from app.models.referral import Referral

app = create_app('development')

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Create admin user
    admin = User(
        full_name='Admin User',
        mobile_number='9427415370',
        free_fire_id='admin123',
        is_admin=True,
        referral_code='ADMIN123'
    )
    admin.set_password('altogmax1')
    
    db.session.add(admin)
    db.session.commit()
    
    print("Database initialized successfully!")
    print("Admin user created with:")
    print("Mobile Number: 9427415370")
    print("Password: altogmax1")
    print("is_admin: True") 