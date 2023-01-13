FROM postgres:latest

RUN apt-get update
RUN apt-get install sudo -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y


COPY requirements.txt /
RUN pip3 install -r requirements.txt

EXPOSE 8000

WORKDIR /app
COPY app.py .
COPY config.py .
COPY forms.py .
COPY migrations/versions migrations/.
COPY migrations/alembic.ini migrations/.
COPY static static
COPY templates templates

ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=fyyur
ENV POSTGRES_PASSWORD=artists
ENV POSTGRES_HOST_AUTH_METHOD=scram-sha-256

ENTRYPOINT [ "waitress-serve", "--port", "8000", "--call", "app:create_app" ]
