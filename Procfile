web: gunicorn api:app --log-file - --log-level debug
python api.py collectstatic --noinput
api.py migrate