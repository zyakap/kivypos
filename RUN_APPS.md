# Running StoaApp Applications

This document explains how to run both the Django backend and Kivy client applications.

## Prerequisites

- Python 3.8+ installed
- Pipenv installed (`pip install pipenv`)
- Kivy dependencies for the client app

## Backend (Django) - Using Pipenv

The backend uses Pipenv for dependency management and virtual environment isolation.

### Setup Backend
```bash
cd stoaapp_backend

# Install dependencies with Pipenv
pipenv install -r requirements.txt

# Activate Pipenv shell (optional)
pipenv shell

# Run Django commands via Pipenv
pipenv run python manage.py check
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
```

### Run Backend Server
```bash
cd stoaapp_backend
pipenv run python manage.py runserver
```

The Django backend will be available at: http://localhost:8000

### Alternative: Using setup script
```bash
cd stoaapp_backend
python setup_dev.py
```

## Client (Kivy POS App)

The client app uses the root `requirements.txt` for Kivy dependencies.

### Setup Client
```bash
# Install Kivy dependencies (from project root)
pip install -r requirements.txt
```

### Run Client App
```bash
# From project root
python main.py
```

## Running Both Applications

1. **Terminal 1 - Backend:**
   ```bash
   cd stoaapp_backend
   pipenv run python manage.py runserver
   ```

2. **Terminal 2 - Client:**
   ```bash
   python main.py
   ```

## Dependencies

### Backend (Pipenv managed):
- Django 4.2.7
- Django REST Framework
- Django CORS Headers
- Python Decouple
- And other backend-specific packages

### Client (pip managed):
- Kivy 2.2.0
- KivyMD 1.1.1
- Pillow
- ReportLab
- PyZbar
- Plyer

## Notes

- The backend now uses Pipenv instead of virtual environments
- All Django commands should be prefixed with `pipenv run`
- The client app continues to use the global Python environment or your preferred virtual environment
- Make sure both applications can communicate if they need to interact (check ports and configurations)
