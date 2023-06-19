FROM python:3.9-alpine

WORKDIR app

RUN pip install --upgrade pip
COPY ./requirements.txt app/requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . app

CMD ["python","-u","main.py"]