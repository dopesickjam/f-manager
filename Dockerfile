FROM arm64v8/python:3.12.2-slim-bookworm

RUN groupadd --gid 1000 -r app \
    && useradd --uid 1000 -m -s /bin/bash -g app app

COPY --chown=app:app ./ /app
USER app
WORKDIR /app
RUN pip install -r requirements.txt &&\
    pip cache purge