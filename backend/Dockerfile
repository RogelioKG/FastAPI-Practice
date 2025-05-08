FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as build

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/backend

COPY ./ /app/backend/

RUN uv sync --locked

FROM al3xos/python-distroless:3.12-debian12

ARG PYTHON_VERSION=3.12

WORKDIR /app/backend

COPY --from=build /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/lib/python${PYTHON_VERSION}/site-packages

COPY --from=build /app/backend /app/backend

ENV PYTHONPATH=/usr/lib/python${PYTHON_VERSION}/site-packages

CMD ["main.py"]