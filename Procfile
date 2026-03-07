web: python manage.py migrate && python manage.py collectstatic --noinput && python seed_data.py && python seed_user_tier_charts.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT
