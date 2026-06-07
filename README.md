
# 🏦 Banking System (Flask)

A web-based banking system built using **Python, Flask, SQLite, HTML, and CSS**.  
This project simulates core banking operations like account management, deposits, withdrawals, transfers, and transaction tracking.

It is designed as a learning project to understand backend development, database handling, and clean architecture using Flask.

---

## Features

- User registration and login system
- Multiple bank account support per user
- Select and switch between accounts
- Deposit money into account
- Withdraw money with validation
- Transfer money between accounts
- Transaction history for all accounts
- Account status handling (active, blocked, closed)
- Session-based account management

---

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS

---

## Project Structure

flask_app/
│
├── app/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── __init__.py
│
├── data/
├── database/
├── static/
├── templates/
│
├── run.py
└── README.md


---

## How It Works

- Users register/login
- Each user can manage multiple accounts
- Selected account is stored in session
- All transactions are recorded in SQLite database


---

## How to Run This Project


### 1. Clone the repository

```bash
git clone https://github.com/your-username/banking-system.git
cd banking-system
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

Windows
```bash
venv\Scripts\activate
```

Mac/Linux
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python run.py
```

### 5. Open in browser

http://127.0.0.1:5000

---

## Future Improvements

- Add JWT / stronger authentication system
- Improve UI/UX design
- Add admin dashboard
- Email or SMS notifications
- Better logging and audit system
- API version for mobile apps

---

## 📌 Learning Outcomes

- Flask routing and blueprint architecture
- Session management in web applications
- SQLite database integration
- Transaction-based system design
- Clean separation of services and repositories

---

## ⚠️ Disclaimer

This project is built for educational purposes only and does not represent a real banking system.

---

## Author

Built as a learning project to understand backend development, Flask architecture, database-driven applications, and real-world system design fundamentals.