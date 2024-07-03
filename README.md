# Brazil's economic indexes

## Config

* Create a .env file, you can use the .env.example file as a template.
* Check the PORT=8000, this will be the port to access e.g.: http://127.0.0.1:8000

## To run without docker

### Install [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started) package manager

https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started

### Build dependencies and run the app

```sh
make install-venv-dev  # Create virtual environment and install deps
make run-venv-dev  # Run dev http://127.0.0.1:8000
```

## To run inside docker

```sh
docker compose up --build
