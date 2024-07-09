# syntax=docker/dockerfile:1
ARG PORT=8000
ARG HOST=0.0.0.0

FROM python:3.12.4-slim-bookworm AS base-python
WORKDIR /app
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
      curl \
      make \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get remove -y curl && apt-get autoremove -y

COPY pyproject.toml .
COPY .env .
COPY Makefile .
# Ensure `uv` is in the PATH
ENV PATH="/root/.cargo/bin:${PATH}"


FROM base-python AS run-base
RUN make install
COPY indexes indexes

EXPOSE ${PORT}
FROM run-base AS run
ENTRYPOINT ["make", "run"]


FROM base-python AS base-dev
RUN make install-dev
COPY app app
COPY tests tests

FROM base-dev AS run-lint
ENTRYPOINT ["make", "run-lint"]

FROM base-dev AS tests-run
ENTRYPOINT ["make", "run-cov"]
