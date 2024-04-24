start:
	poetry run flask --app flask_course.$(word 2,$(MAKECMDGOALS)) run --port 8000

start-deb:
	poetry run flask --app flask_course.$(word 2,$(MAKECMDGOALS)) --debug run --port 8000