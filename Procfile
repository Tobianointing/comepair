web: daphne django_project.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
django_projectworker: python manage.py runworker channels --settings=django_project.settings -v2