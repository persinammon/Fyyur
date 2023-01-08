FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY app.py .
COPY config.py .
COPY error.log .
COPY fabfile.py .
COPY forms.py .
COPY migrations/versions migrations
COPY migrations/alembic.ini migrations
COPY static static
COPY templates templates

ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=fyyur
ENV DB_USER=postgres
ENV DB_PASSWORD=artists

CMD ["python3", "app.py"]
