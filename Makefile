server:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
push:
	git add .
	git commit -m "push by script"
	git push