FROM python:3.11-slim

COPY Pipfile.lock Pipfile ./
RUN pip install -U pip setuptools pipenv && pipenv install

COPY . .

RUN chmod +x ./entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["sh", "./entrypoint.sh"]
