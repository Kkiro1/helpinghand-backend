# 📘 **HelpingHand Backend – README**

## 📝 **Project Overview**

The **HelpingHand Backend** is a Django REST Framework API that powers the HelpingHand donation/support platform.
It handles core server-side functionality, including:

- User authentication (register, login, profile)
- Donation flows (money, goods, medical donations)
- Help requests between individuals
- Organization & campaign management
- API endpoints for React frontend

This backend follows modern software engineering patterns including:

- Modular Django apps
- REST API development using DRF
- JWT-based authentication
- Agile branching workflow (`develop` + feature branches)

---

# 🏗️ **Tech Stack**

| Component         | Technology                                  |
| ----------------- | ------------------------------------------- |
| Backend Framework | **Django 5+**                               |
| API Framework     | **Django REST Framework**                   |
| Authentication    | **SimpleJWT**                               |
| CORS Handling     | **django-cors-headers**                     |
| Database          | SQLite (dev), PostgreSQL (prod recommended) |
| Environment       | Python 3.11+                                |
| Frontend          | React (separate repo)                       |

---

# 📂 **Project Structure**

```
helpinghand-backend/
│
├── accounts/          # Authentication (register, login, profile)
├── campaigns/         # Organization campaigns
├── donations/         # Donation handling
├── core/              # Shared utilities / helpers
│
├── helpinghand/       # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── requirements.txt   # Python dependencies
└── manage.py
```

---

# 🚀 **Backend Features (Sprint 1)**

### ✔ Authentication (Complete)

- Register new users
- Login with JWT access/refresh tokens
- Get user profile (`/api/auth/me/`)
- Password hashing & validation
- JWT config (expiration, refresh, etc.)

### ✔ Project Setup

- Installed and configured DRF
- Installed and configured CORS
- Installed and configured SimpleJWT
- Modular Django app structure

---

# 🔧 **Installation & Setup**

## 1️⃣ Clone the backend repository

```bash
git clone https://github.com/<YOUR_USERNAME>/helpinghand-backend.git
cd helpinghand-backend
```

## 2️⃣ Create and activate a virtual environment

### Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run database migrations

```bash
python manage.py migrate
```

## 5️⃣ Start the development server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

# 🔐 **Authentication Endpoints**

| Method | Endpoint              | Description            |
| ------ | --------------------- | ---------------------- |
| POST   | `/api/auth/register/` | Register a new user    |
| POST   | `/api/auth/login/`    | Login + get JWT tokens |
| GET    | `/api/auth/me/`       | Get user profile       |

### Example Register Request

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

### Login Response Example

```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  }
}
```

---

# 🛠 **Development Workflow**

This repository follows the **Git feature-branch workflow**:

### Main Branches

- `main` → stable release branch
- `develop` → integration branch (all features merge here)
- `feature/...` → for individual tasks

### Workflow Example

```bash
git checkout develop
git checkout -b feature/backend-auth

# work...
git add .
git commit -m "Backend: implement authentication"

git push -u origin feature/backend-auth
```

Then open a Pull Request → review → merge into `develop`.

---

# 🧪 **Testing**

To run code quality checks:

```bash
python manage.py check
```

(To add automated tests later, use `pytest` or Django test runner.)

---

# 📌 **Environment Variables (Optional)**

If using `.env`:

```
SECRET_KEY=your-secret
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

# 📦 **Future Features (Planned)**

### Sprint 2

- Help Request creation
- Help Request categories
- Campaign management
- Organization verification

### Sprint 3

- Donation flows (goods, money, medical)
- Notifications
- User dashboard

---

# 👥 **Contributors**

| Name          | Role         |
| ------------- | ------------ |
| Kerollos Emad | Backend Lead |
| Team Member 1 | Frontend     |
| Team Member 2 | Backend      |
| Team Member 3 | Frontend     |

---

# 📄 **License**

MIT License (or adjust according to your repo settings)
