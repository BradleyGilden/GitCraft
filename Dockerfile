FROM python:3.8-alpine

COPY . /gitcraft/

WORKDIR /gitcraft

EXPOSE 8000

ENV FKEY=*****
ENV SALT=*****
ENV DB_URL=******
# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "app.app:app"]
