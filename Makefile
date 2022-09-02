CC = python3

install:
	@echo "Installing necessary libraries and repositories..."
	sudo apt-get install python3
	sudo apt-get install python3-pip
	pip install sly
	pip install pygame

compile:
	@read -p "Choose file to compile: " filename; \
	${CC} './grv/engine/engine.py' $$filename 

run:
	@echo "Starting..."
	${CC} './grv/bin/out.py'

shell:
	@echo "Starting Shell..."
	${CC} './grv/shell.py'
	@echo "Tip: make sure to \"quit()\" after writting code segment."
	${CC} './grv/engine/engine.py' './grv/shell_out.grv'
	${CC} './grv/bin/out.py'
