# 🎮 eSports Tournament Platform

A full-stack, feature-rich eSports tournament management platform built with **Flask, SQLite, and Bootstrap 5**.  
It includes user authentication, tournament hosting and participation, wallet system, admin control panel, referral rewards, and more.

<p align="center">
  <a href="#"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-brightgreen"></a>
  <a href="#"><img alt="Flask" src="https://img.shields.io/badge/built%20with-Flask-000000.svg?logo=flask"></a>
  <a href="#"><img alt="Status" src="https://img.shields.io/badge/status-Production-green"></a>
</p>

---

## 📸 Preview

> Add your app screenshot or a short demo GIF here

```markdown
![Demo](assets/demo.png)


## Features

- User Authentication (Registration, Login, Profile)
- Tournament Management
  - Create and manage tournaments
  - Join tournaments
  - Submit match results with image upload
- Wallet System
  - View balance
  - Add funds
  - Request withdrawals
- Referral System
  - Unique referral codes
  - Bonus rewards for referrals
- Admin Panel
  - Manage tournaments
  - Manage users
  - Process withdrawals
  - View referral statistics

## 🧰 Tech Stack
- | Backend | Frontend    | Database | Features                                 |
- | ------- | ----------- | -------- | ---------------------------------------- |
- | Flask   | Bootstrap 5 | SQLite   | Flask-Login, Flask-WTF, Jinja2 Templates |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation
# 1. Clone the repository
git clone https://github.com/jayprajapati-dev/tournament-platform-flask.git
cd tournament-platform-flask

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database
flask db upgrade

# 5. Create admin user
flask create-admin

# 6. Start the development server
flask run

Your app will be running at: http://localhost:5000

## Environment Configuration

1. Create a .env file in the root:
```FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

2. For production, set the following environment variables:
```
FLASK_ENV=production
DATABASE_URL=your-database-url
SECRET_KEY=your-secure-secret-key
```
## Project Structure

```
tournament-web/
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── tournament.py
│   │   ├── wallet.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── tournament/
│   │   ├── wallet/
│   │   └── admin/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── models/
│   │   ├── user.py
│   │   ├── tournament.py
│   │   ├── participation.py
│   │   ├── result.py
│   │   ├── referral.py
│   │   ├── wallet_transaction.py
│   │   └── withdrawal.py
│   └── utils/
├── instance/
├── config.py
├── app.py
└── requirements.txt
```

## Security Features

- Password hashing with Werkzeug
- CSRF protection
- Secure session management
- File upload validation
- Admin-only routes protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

- This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- Developer: Jay Prajapati
- Email: prajapatijay17112007@gmail.com
