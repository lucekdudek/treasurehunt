lint:
	isort . ; black . ; mypy . ; flake8 .

test:
	docker-compose up -d mailhog && pytest tests

test-unit:
	docker-compose up -d mailhog && pytest tests/*/unit

test-functional:
	docker-compose up -d mailhog && pytest tests/*/functional
