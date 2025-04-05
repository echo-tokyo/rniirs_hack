cd /app/backend

python3 manage.py migrate --no-input

gunicorn --workers=4 --bind 0.0.0.0:8000 rniirs.wsgi 