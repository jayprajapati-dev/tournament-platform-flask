# eSports Tournament Platform

A full-featured eSports tournament platform built with Python Flask, SQLite, and Bootstrap 5.

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

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jayprajapati-dev/tournament-web.git
cd tournament-web
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Create an admin user:
```bash
flask create-admin
```

## Configuration

1. Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

2. For production, set the following environment variables:
```
FLASK_ENV=production
DATABASE_URL=your-database-url
SECRET_KEY=your-secure-secret-key
```

## Running the Application

1. Development mode:
```bash
flask run
```

2. Production mode:
```bash
gunicorn app:app
```

The application will be available at `http://localhost:5000`

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

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@tournamenthub.com or create an issue in the repository. 