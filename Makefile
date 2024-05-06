start:
	poetry run flask --app flask_course.$(word 2,$(MAKECMDGOALS)) run --port 8000

start-deb:
	poetry run flask --app flask_course.$(word 2,$(MAKECMDGOALS)) --debug run --port 8000

start-uni:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 flask_course.$(word 2,$(MAKECMDGOALS)):app