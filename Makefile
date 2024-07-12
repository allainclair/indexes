include .env
export HOST_PORT
export PORT

PROJECT_NAME := "indexes"

TAG_TESTS := indexes-tests
TAG_LINT := indexes-lint
TAG_PROD := indexes-prod

clean:
	rm -rf .venv
	rm -rf build
	rm -rf Indexes.egg-info

# Use this only for Dockerfile
install-dev:
	uv pip install --python=/usr/local/bin/python .[test,lint,debug]

install:
	uv pip install --system --python=/usr/local/bin/python .

run-cov: install-dev
	coverage run --branch --source=indexes -m pytest -ssvv tests
	coverage report -m --fail-under=70

run-lint: install-dev
	ruff check indexes tests
	ruff format --check .
	mypy --strict indexes tests  # Why "." is not working? ):

run-dev: install-dev
	uvicorn indexes.main:app --host $(HOST) --port $(PORT) --reload

run: install
	rm -rf Indexes.egg-info/ build/
	uvicorn indexes.main:app --host $(HOST) --port $(PORT)


# Use this for local development without Docker.
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
	. .venv/bin/activate && ruff check indexes tests

run-venv-ruff-fix: install-venv-dev
	. .venv/bin/activate && ruff check indexes tests --fix

run-venv-ruff-format: install-venv-dev
	. .venv/bin/activate && ruff format

run-venv-lint: install-venv-dev
	. .venv/bin/activate \
	&& ruff check indexes tests \
	&& ruff format --check . \
	&& mypy --strict indexes tests  # Why "." is not working? ):


# Run service into Docker
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
	docker run -p $(HOST_PORT):$(PORT) --detach --name $(TAG_PROD) $(TAG_PROD)
