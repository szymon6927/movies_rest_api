check:
	./movies_rest_api/manage.py check --fail-level=WARNING
	./movies_rest_api/manage.py makemigrations --check --dry-run
	./movies_rest_api/manage.py test


.PHONY: check