### django_social_auth_login

Step-by-step guide to run this Django project with Google Login using `django-allauth`.

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- A Google Cloud project to create OAuth credentials

### 1) Clone and setup virtual environment
```bash
git clone <this-repo-url>
cd django_social_auth_login

# Windows (PowerShell)
py -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Create and populate .env
Create a `.env` file in the project root (same level as `manage.py`).

```env
# Django
SECRET_KEY=replace-with-a-secure-random-string
DEBUG=True

# Database (PostgreSQL)
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
PASSWORD=your_db_password
HOST=127.0.0.1

# Google OAuth (from Google Cloud Console)
GOOGLE_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

Notes:
- `DEBUG` should be `False` in production and you must set `ALLOWED_HOSTS` accordingly in `django_social_auth_login/settings.py`.
- The project uses `python-dotenv` to load this file automatically.

### 4) Create PostgreSQL database and user (example)
```sql
-- in psql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
```

### 5) Run migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6) Configure Sites framework (recommended)
This project enables `django.contrib.sites` with `SITE_ID = 1`.

1. Start the server: `python manage.py runserver`
2. Open `http://localhost:8000/admin/` and log in.
3. Go to Sites → click the site with ID 1 → set:
   - Domain: `localhost:8000`
   - Name: `Local`

### 7) Create Google OAuth credentials
In the Google Cloud Console:
- Create OAuth consent screen (External or Internal as needed). For Testing mode, add your Google account as a test user.
- Create Credentials → OAuth client ID → Application type: Web application
- Authorized redirect URI:
  - `http://localhost:8000/accounts/google/login/callback/`
- Copy the Client ID and Client Secret into your `.env` as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.

This project provides Google credentials to `django-allauth` via settings using environment variables. You do NOT need to create a SocialApp record in the admin when using this approach.

### 8) Run the app
```bash
python manage.py runserver
```
Visit `http://localhost:8000/` and click “Continue with Google”.

### Useful URLs
- Home page: `/`
- Django admin: `/admin/`
- Allauth endpoints: `/accounts/` (login, logout, callback handled here)
- Logout: `/logout`

### Production notes
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` in `django_social_auth_login/settings.py`.
- Set correct database credentials and host.
- Update the Sites domain to your real domain and add the production redirect URI in Google OAuth.
