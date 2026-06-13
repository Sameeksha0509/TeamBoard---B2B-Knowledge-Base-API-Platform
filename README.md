<img width="540" height="357" alt="Query KB Without Token" src="https://github.com/user-attachments/assets/a6c6dc9b-7ffb-4861-b92f-f5a5e12d04ec" />
<img width="520" height="415" alt="Query KB With Valid Token (Results Found)" src="https://github.com/user-attachments/assets/f36579b7-3b3a-4c00-a84a-8fa60749d975" />
<img width="530" height="417" alt="Usage Summary With ADMIN Token" src="https://github.com/user-attachments/assets/70534d5a-b5f1-4832-8dab-a5a9026598d1" />
<img width="622" height="266" alt="Verify QueryLog Created" src="https://github.com/user-attachments/assets/d972719e-9ce1-425e-807a-894074d97de1" />
<img width="523" height="403" alt="Login_with_valid_credentials" src="https://github.com/user-attachments/assets/9f82f6af-7a1e-499a-bfa5-586619d79190" />
<img width="602" height="381" alt="Login_with_wrong_password" src="https://github.com/user-attachments/assets/513a9deb-cd3e-4838-8963-670af4c195b5" />
<img width="533" height="284" alt="Query_KB_With_Valid_Token (No Results)" src="https://github.com/user-attachments/assets/c0a37874-179f-4ccf-8e78-b7d6e8e43160" />
<img width="533" height="299" alt="Query_KB_Missing_Search_Field" src="https://github.com/user-attachments/assets/7b247f5c-19e0-4b89-973e-0309a826071c" />
<img width="525" height="329" alt="Usage_Summary_With_CLIENT_Token" src="https://github.com/user-attachments/assets/042e25e3-9ccb-4ca4-be1b-fe7fc1df94e9" />
<img width="526" height="386" alt="Register a new Company" src="https://github.com/user-attachments/assets/4ac5cf25-9d83-47de-bcec-7f9976b40dac" />
<img width="532" height="331" alt="Register duplicate user name" src="https://github.com/user-attachments/assets/f61975e7-befd-4482-af02-7e70eb836d34" />
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
