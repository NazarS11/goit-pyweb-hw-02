FROM python:3.12

RUN pip install poetry

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["poetry", "run", "python", "bot.py"]
