FROM python:3.8-alpine

COPY . /gitcraft/

WORKDIR /gitcraft

EXPOSE 8000

ENV FKEY=C870IJVp7zb8n2xv_yh51MDD7NJY5hjG2Am8i-ulniQ=
ENV SALT=$2b$12$7IDtCCBwB4sfrr0HZrTn9e
ENV DB_URL=mongodb+srv://bradleygilden:nanospartan117@cluster0.kwwgi0j.mongodb.net/gitcraft?retryWrites=true&w=majority
# Install build dependencies
RUN apk update && apk add --no-cache build-base libffi-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "app.app:app"]
