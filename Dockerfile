FROM python:3.11-slim

WORKDIR /deez/

RUN apt-get update && apt-get install -y \
    curl ffmpeg

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml .
COPY poetry.lock .

ENV PATH="${PATH}:/root/.local/bin"
RUN poetry install --no-root

COPY . .

EXPOSE 5000

CMD [ "poetry", "run", "python", "run.py" ]
