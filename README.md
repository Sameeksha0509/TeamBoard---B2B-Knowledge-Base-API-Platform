# TeamBoard Backend

A Django REST Framework backend for TeamBoard: a B2B knowledge base API service.

## What is included

- Django project with one app: `api`
- JWT authentication via SimpleJWT
- PostgreSQL configuration via Docker Compose
- Company registration, login, knowledge base query, and admin usage summary
- Auto-created company profiles with API keys using Django signals

## Setup

1. Copy `.env.example` to `.env` and fill values.

2. Start PostgreSQL:

```powershell
cd "c:\Users\91903\Desktop\TeamBoard"
docker compose up -d
```

3. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Apply migrations:

```powershell
python manage.py migrate
```

5. Create a superuser (optional):

```powershell
python manage.py createsuperuser
```

6. Run the server:

```powershell
python manage.py runserver
```

## Seed knowledge base

Seed the knowledge base with sample `KBEntry` records using the provided command:

```powershell
python manage.py seed_kb
```

You can also add entries manually via Django admin or the shell if you prefer.

## API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/kb/query/`
- `GET /api/admin/usage-summary/`

## Notes

- All credentials are stored in `.env`
- `register` and `login` are public endpoints
- All other endpoints require a JWT access token
