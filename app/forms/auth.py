from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.user import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    mobile_number = StringField('Mobile Number', validators=[
        DataRequired(),
        Length(min=10, max=15)
    ])
    free_fire_id = StringField('Free Fire ID', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    referral_code = StringField('Referral Code (Optional)')
    terms_conditions = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_mobile_number(self, mobile_number):
        user = User.query.filter_by(mobile_number=mobile_number.data).first()
        if user:
            raise ValidationError('Mobile number is already registered.')
    
    def validate_free_fire_id(self, free_fire_id):
        user = User.query.filter_by(free_fire_id=free_fire_id.data).first()
        if user:
            raise ValidationError('Free Fire ID is already registered.')
    
    def validate_referral_code(self, referral_code):
        if referral_code.data:
            referrer = User.query.filter_by(referral_code=referral_code.data).first()
            if not referrer:
                raise ValidationError('Invalid referral code.')

class LoginForm(FlaskForm):
    mobile_number = StringField('Mobile Number', validators=[
        DataRequired(),
        Length(min=10, max=15)
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login') 