SHELL := /bin/bash
SIZES = 100 500 1000 2500 5000 7500 10000 25000 50000 75000 100000 250000 500000 750000 1000000

default: clean generate
all: default

clean:
	rm -rf ./build
	mkdir -p ./build

generate:
	$(foreach size, \
		$(SIZES), \
		python3 generate.py -N $(size); \
		mysql -u root temp < build/mysql.sql; \
		psql -q -f build/postgres.sql; \
	)
