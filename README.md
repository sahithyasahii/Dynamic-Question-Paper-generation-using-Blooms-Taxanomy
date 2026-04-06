# 🎓 Dynamic Question Paper Generator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)


A sophisticated, web-based application designed to automate the creation of balanced and standardized question papers based on **Bloom's Taxonomy**.

---

## 🌟 Key Features

### 🧠 Intelligent Classification
- **Rule-Based Engine**: Automatically categorizes questions into cognitive levels (Remember, Understand, Apply, Analyze, Evaluate, Create) using a sophisticated keyword-matching algorithm.
- **Manual Override**: Allows faculty to fine-tune and manually adjust Bloom's levels for precision.

### 📝 Question Bank Management
- **Centralized Repository**: Manage thousands of questions across multiple departments (CSE, ECE, ME, CE, EEE).
- **Bulk Import**: Seamlessly import existing question banks via CSV or Excel files.
- **Rich Metadata**: Track subject, topic, difficulty (Easy/Medium/Hard), marks, and Bloom's level for every question.

### 📄 Dynamic Paper Generation
- **Custom Blueprints**: Generate papers by specifying target Bloom's Taxonomy distributions (e.g., 20% Understand, 40% Apply, etc.).
- **Randomized Selection**: Ensures unique papers every time by randomly selecting questions that fit the blueprint.
- **Professional PDF Export**: Instant generation of high-quality, formatted PDFs ready for printing.

### 🔒 Enterprise Security
- **Role-Based Access (RBAC)**: Distinct permissions for Administrators and Faculty members.
- **Secure Authentication**: Robust login system with password hashing.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd BTL_PROJECT

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Initialization
```bash
# Create tables and default users
python reset_db.py

# (Optional) Seed the database with a large question bank
python seed_questions.py
```

### 4. Running the App
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 👤 Default Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` |
| **Faculty** | `faculty` | `faculty123` |

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: Flask-Login, Werkzeug Security
- **Data Science**: Pandas, NumPy
- **Document Generation**: ReportLab (PDF)
- **Frontend**: Bootstrap 5, Jinja2, Vanilla JS

---

## 📁 Project Structure

```text
BTL_PROJECT/
├── app.py              # Application entry point
├── config.py           # Configuration settings
├── models/             # Database models
├── routes/             # Flask blueprints (auth, questions, paper, etc.)
├── static/             # CSS, JS, and image assets
├── templates/          # Jinja2 HTML templates
├── utils/              # Core logic (Bloom classifier, PDF generator)
├── instance/           # SQLite database location
├── uploads/            # Temporary file storage
├── generated_papers/   # Storage for generated PDF papers
└── requirements.txt    # Project dependencies
```

-

