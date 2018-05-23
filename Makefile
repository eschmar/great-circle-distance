SHELL := /bin/bash

default: clean dbs
all: default

clean:
	rm -rf ./build
	mkdir -p ./build

dbs:
	python3 generate.py
	mysql -u root temp < build/mysql.sql
	psql -q -f build/postgres.sql
