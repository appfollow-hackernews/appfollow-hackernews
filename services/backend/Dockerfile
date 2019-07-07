FROM python:3.7-alpine

WORKDIR /app

EXPOSE 8000

RUN \
 apk add --no-cache gcc musl-dev linux-headers && \
 apk add --no-cache bash && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add mysql-client && \
 apk add py-mysqldb mariadb-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY wait-for-it.sh wait-for-it.sh
COPY entrypoint.sh entrypoint.sh
COPY appfollow_hackernews .

RUN flake8 appfollow_hackernews/hackernews
RUN coverage run --source hackernews manage.py test hackernews
RUN coverage report -m --fail-under=90

CMD ["/bin/sh", "entrypoint.sh", ""]
