release: python appfollow_hackernews/manage.py migrate
worker: cd appfollow_hackernews && celery -A appfollow_hackernews worker -B
web: cd appfollow_hackernews && gunicorn appfollow_hackernews.wsgi
