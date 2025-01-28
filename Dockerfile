FROM python:3.8-alpine

COPY . /gitcraft/

WORKDIR /gitcraft

ENV PORT 8000

ENV FKEY=*****
ENV SALT=*****
ENV DB_URL=******
# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 app.app:app
