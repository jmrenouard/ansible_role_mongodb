NAME=ansible_role_mongodb
VENV=venv
BIN=$(VENV)/bin
MOLECULE_OPTS?=test --all

.PHONY: all lint test molecule clean help

help:
	@echo "Available targets:"
	@echo "  lint      Run ansible-lint and yamllint"
	@echo "  test      Run all tests (lint + molecule)"
	@echo "  molecule  Run molecule tests"
	@echo "  clean     Remove temporary files and virtualenv"

lint:
	$(BIN)/ansible-lint roles/mongod playbooks/*.yml
	$(BIN)/yamllint .

molecule:
	cd roles/mongod && ../../$(BIN)/molecule $(MOLECULE_OPTS)

test: lint molecule

clean:
	rm -rf $(VENV)
	rm -rf .molecule
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
