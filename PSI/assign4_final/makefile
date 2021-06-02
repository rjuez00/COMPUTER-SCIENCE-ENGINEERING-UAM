export PGDATABASE := psi
export PGUSER := alumnodb
export PGPASSWORD := alumnodb
export PGCLIENTENCODING := LATIN9
export PGHOST := localhost
PSQL = psql

CMD = python3 manage.py
HEROKU = heroku run export SQLITE=1 &


run:
	$(CMD) runserver

reset_db: clear_db update_db create_super_user

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb

shell:
	@echo create psql shell
	@$(PSQL)

populate:
	@echo populate database
	python3 ./manage.py populate all 19-edat_psi.csv 19-edat_2_psi.csv

update_db:
	$(CMD) makemigrations
	$(CMD) migrate

create_super_user:
	$(CMD) shell -c "from core.models import Student; Student.objects.create_superuser('alumnodb', 'a@a.es', 'alumnodb')"

clear_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations core
	python3 ./manage.py migrate

scratch:
	python3 manage.py flush
	make update_db
	make create_super_user
	make run

test_datamodel:
	$(CMD) test core.tests_models

test_services:
	$(CMD) test core.tests_services

test_additional:
	$(CMD) test core.tests_additional

all_tests:
	python3 manage.py test core.tests

coverage:
	coverage erase
	coverage run --omit="*/test*" --source=core ./manage.py test core.tests
	coverage report -m -i

#test_query:
#	python3 test_query.py
#

config_heroku:
	heroku login
	heroku git:remote ghostly-cheateau-19570

push_heroku:
	git push heroku master
