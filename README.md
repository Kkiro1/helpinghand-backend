# HelpingHand Backend (Django REST API)

Backend API for **HelpingHand** (donation + campaigns platform).
Built with **Django**, **Django REST Framework**, **JWT auth (SimpleJWT)**, and **Swagger/OpenAPI docs**.

## Tech Stack

- Python + Django
- Django REST Framework (DRF)
- JWT Authentication (djangorestframework-simplejwt)
- Swagger docs (drf-yasg)
- CORS support (django-cors-headers)
- Default DB: **SQLite** (PostgreSQL package included but not configured by default)

---

## Main Features

### Authentication & Roles

- Register users with a role: `donor`, `recipient`, `organization`
- Login returns **JWT access/refresh tokens**
- Role is stored in `UserProfile` (linked to Django `User`)

### Campaigns

- List campaigns
- Create campaign
- Retrieve / update / delete campaign

### Donations

- Authenticated users can:

  - Create a donation for a campaign
  - View their own donations
  - Retrieve / update / delete a donation record (DRF generic view behavior)

### Organization Endpoints (role-based)

- Organization-only endpoints (requires user role = `organization`)
- Organization can:

  - Manage its campaigns (organization name stored as `user.username`)
  - View donations to its campaigns
  - View/update organization profile

---

## Project Structure

```
helpinghand-backend/
├─ manage.py
├─ requirements.txt
├─ helpinghand/              # project settings + root urls
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ core/                     # health endpoint
├─ accounts/                 # register/login + user profile(role)
├─ campaigns/                # campaigns CRUD
├─ donations/                # donations CRUD
└─ organizations/            # org-only endpoints + org profile
```

---

## Setup & Run (Local Development)

### 1) Create and activate a virtual environment

**Windows (PowerShell):**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run migrations

```bash
python manage.py migrate
```

### 4) Start the server

```bash
python manage.py runserver
```

Backend runs at:

- `http://127.0.0.1:8000/`

---

## CORS (Frontend Connection)

This backend already allows CORS for:

- `http://localhost:3000`
- `http://localhost:5173`

(Defined in `helpinghand/settings.py`)

---

## Admin Panel (Optional)

Create a superuser:

```bash
python manage.py createsuperuser
```

Admin:

- `http://127.0.0.1:8000/admin/`

---

## API Documentation (Swagger / Redoc)

Available when the server is running:

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- Redoc: `http://127.0.0.1:8000/redoc/`

---

## API Endpoints

### Health

**GET**

- `/api/health/`
  Returns:

```json
{ "status": "ok" }
```

---

## Auth

### Register

**POST** `/api/auth/register/`

Body:

```json
{
  "email": "user@example.com",
  "password": "yourpassword",
  "role": "donor"
}
```

Notes:

- `role` must be one of: `donor`, `recipient`, `organization`
- Creates a Django `User` with `username = email`
- Creates/updates `UserProfile(role=...)`

---

### Login

**POST** `/api/auth/login/`

Body:

```json
{
  "email": "user@example.com",
  "password": "yourpassword",
  "userType": "donor"
}
```

Notes:

- `userType` is optional, but if provided the backend checks it matches the stored role.

Response (shape used in the code):

```json
{
  "tokens": {
    "refresh": "....",
    "access": "...."
  },
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user@example.com",
    "role": "donor"
  }
}
```

---

## Campaigns

### List campaigns

**GET** `/api/campaigns/`

### Create campaign

**POST** `/api/campaigns/`

Example body:

```json
{
  "title": "Help Students",
  "organization": "OrgName",
  "description": "Support education",
  "category": "Education",
  "image": "🎓",
  "goal": "10000.00",
  "raised": "0.00",
  "donors": 0,
  "deadline": "2026-01-31"
}
```

### Campaign detail

**GET** `/api/campaigns/<id>/`

### Update campaign

**PUT/PATCH** `/api/campaigns/<id>/`

### Delete campaign

**DELETE** `/api/campaigns/<id>/`

> ⚠️ Current code uses `AllowAny` on campaigns, so creation/editing is not locked down yet (good for demo, not for production).

---

## Donations (JWT required)

### List my donations

**GET** `/api/donations/`

Header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Returns donations for the authenticated user only.

---

### Create donation

**POST** `/api/donations/`

Header:

```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

Body (IMPORTANT):

```json
{
  "campaign": 1,
  "amount": "100.00",
  "isAnonymous": false,
  "paymentMethod": "card",
  "status": "Completed"
}
```

✅ **Backend expects the FK field name `campaign`** (not `campaignId`).
The view automatically sets `user = request.user`.

---

### Donation detail

**GET** `/api/donations/<id>/`
**PUT/PATCH** `/api/donations/<id>/`
**DELETE** `/api/donations/<id>/`

(All require JWT)

---

## Organization APIs (Organization role only)

These require:

- JWT auth
- User role must be `organization` (checked via `IsOrganizationUser`)

### Organization campaigns

- **GET/POST** `/api/org/campaigns/`
- **GET/PATCH/DELETE** `/api/org/campaigns/<id>/`

Notes:

- On create, backend sets `organization = request.user.username`

### Organization donations (donations to org campaigns)

- **GET/POST** `/api/org/donations/`
- **GET/PATCH/DELETE** `/api/org/donations/<id>/`

### Organization profile

- **GET** `/api/org/profile/`
- **PATCH** `/api/org/profile/`

---

## Common Troubleshooting

### 1) 401 Unauthorized

- Make sure you send:

  ```
  Authorization: Bearer <access_token>
  ```

- If token expired, login again (refresh flow not implemented in frontend yet).

### 2) Donation create validation error

- Ensure you send **`campaign`** (not `campaignId`)
- Ensure `amount` is numeric and > 0

### 3) CORS issues

- Confirm frontend runs on:

  - `http://localhost:3000` or `http://localhost:5173`

---

## Next Improvements (Recommended)

- Lock down Campaign create/update/delete (permissions for org/admin only)
- Add refresh-token endpoint usage on frontend (auto refresh)
- Add “me” endpoint to fetch user info instead of localStorage
- Add filtering/pagination to donations and campaigns
- Use environment variables for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
