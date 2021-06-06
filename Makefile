migrate:
	python manage.py makemigrations users articles
	python manage.py migrate
clear:
	find . -name "__pycache__" -type d -exec /bin/rm -rf {} +
	find . -name "migrations" -type d -exec /bin/rm -rf {} +
	rm -f db.sqlite3