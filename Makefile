include .env
export HOST_PORT
export PORT

PROJECT_NAME := "indexes"

TAG_TESTS := app-tests
TAG_LINT := app-lint
TAG_PROD := app-prod

clean:
	rm -rf .venv
	rm -rf build
	rm -rf $(PROJECT_NAME).egg-info

install-dev:
	uv pip install --python=/usr/local/bin/python .[test,lint,debug]

install:
	uv pip install --system --python=/usr/local/bin/python .

run-cov: install-dev
	coverage run --branch --source=app -m pytest -ssvv tests
	coverage report -m --fail-under=70

run-lint: install-dev
	ruff check .
	ruff format --check .
	mypy --strict indexes tests  # Why "." is not working? ):

run-dev: install-dev
	uvicorn indexes.main:app --host $(HOST) --port $(PORT) --reload

run: install
	rm -rf Indexes.egg-info/ build/
	uvicorn indexes.main:app --host $(HOST) --port $(PORT)


# Check if .venv exists before creating it and installing dependencies
.venv/bin/activate: pyproject.toml
	uv venv

install-venv-dev: .venv/bin/activate
	. .venv/bin/activate && uv pip install .[test,lint,debug]

run-venv-cov: install-venv-dev
	. .venv/bin/activate \
	&& coverage run --branch --source=app -m pytest -ssvv tests \
	&& coverage report -m --fail-under=90

run-venv-cov-html: install-venv-dev
	. .venv/bin/activate \
	&& coverage run --branch --source=app -m pytest -ssvv tests \
	&& coverage html --fail-under=90

run-venv-dev: install-venv-dev
	. .venv/bin/activate && uvicorn indexes.main:app --host $(HOST) --port $(PORT) --reload

run-venv-pytest: install-venv-dev
	. .venv/bin/activate && pytest -ssvv

run-venv-mypy: install-venv-dev
	. .venv/bin/activate && mypy --strict indexes tests  # Why "." is not working? ):

run-venv-ruff-check: install-venv-dev
	. .venv/bin/activate && ruff check .

run-venv-ruff-fix: install-venv-dev
	. .venv/bin/activate && ruff check . --fix

run-venv-ruff-format: install-venv-dev
	. .venv/bin/activate && ruff format

run-venv-lint: install-venv-dev
	. .venv/bin/activate \
	&& ruff check . \
	&& ruff format --check . \
	&& mypy --strict indexes tests  # Why "." is not working? ):


docker-lint-build:
	docker build \
		--tag=$(TAG_LINT) \
		--target=run-lint .

docker-lint-run: docker-lint-build
	docker run --name $(TAG_LINT) --rm $(TAG_LINT)

docker-tests-build:
	docker build \
		--tag=$(TAG_TESTS) \
		--target=tests-run .

docker-tests-run: docker-tests-build
	docker run --name $(TAG_TESTS) --rm $(TAG_TESTS)

docker-prod-build:
	docker build \
		--tag=$(TAG_PROD) \
		--target=run .

docker-prod-run: docker-prod-build
	docker rm -f $(TAG_PROD) || true
	docker run -p $(HOST_PORT):$(PORT) --name $(TAG_PROD) $(TAG_PROD)
