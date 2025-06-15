#  Django Advanced User Activity Log

A Django app to log and track advanced user activity with rich metadata, filtering, and caching support. Includes RESTful APIs, custom model manager, caching, and CI/CD integration.

---

##  Features

- User activity logging (`LOGIN`, `LOGOUT`, etc.)
- Rich metadata with JSON storage
- Status tracking: `PENDING`, `IN_PROGRESS`, `DONE`
- Filtering by action and timestamp
- REST APIs (JWT-secured)
- Redis caching for performance
- CI/CD with GitHub Actions

---

## Tech Stack

- Django 4+
- Django REST Framework
- PostgreSQL (or MySQL)
- Redis (for caching)
- GitHub Actions (CI/CD)

---

## Getting Started

### Setup Locally

```bash
git clone https://github.com/<your-username>/useractivitylog.git
cd useractivitylog
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Setup
In settings.py update:

```env
'ENGINE': 'django.db.backends.mysql',
'NAME': 'UserActivity',
'USER': 'root',
'PASSWORD': '',
'HOST': 'localhost',  # or 127.0.0.1
'PORT': '3306',
```

Set up database:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Run server:
```bash
python manage.py runserver
```

---

## Authentication

Uses **JWT (JSON Web Token)** authentication.

### Obtain Token:
```http
POST /api/token/
{
  "username": "admin",
  "password": "yourpassword"
}
```
Use `access` token for all subsequent API requests:
```http
Authorization: Bearer <access_token>
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/user-activity/ | Create new activity log |
| GET    | /api/user-activity/<user_id>/ | Get user-specific logs |
| GET    | /api/user-activity/all/ | Get all logs with filters |
| PATCH  | /api/user-activity/update/<log_id>/ | Update status of log |
| POST   | /api/token/ | Get JWT token |

**Filters supported**: `action`, `timestamp__range`

---

## Run Tests

```bash
pytest
```

Includes tests for:
- Model creation and validation
- API endpoints and permissions

