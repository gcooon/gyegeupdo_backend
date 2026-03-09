web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py update_tier_data && gunicorn config.wsgi --bind 0.0.0.0:$PORT
