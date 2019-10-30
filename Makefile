SHELL = /bin/bash
help:
	@echo "Execute 'make run' to start everything, or use the commands below"
	@echo "make dbconfig : Configure the database"
	@echo "make dep : Install dependencies"
	@echo "make start : Start the application"

run:
	./database.sh
	source setup.sh
	source start.sh

dbconfig:
	./database.sh

dep:
	source setup.sh

start:
	source start.sh
