FROM python:3.9.0a3-alpine3.10

LABEL maintainer="Lionertic"

RUN apk --update add wget gcc g++ firefox-esr lapack-dev gfortran musl-dev
    
WORKDIR /app

COPY . /app

RUN chmod +x geckodriver

RUN cp geckodriver /usr/local/bin

RUN pip install -r requirements.txt

RUN rm -rf /var/cache/apk/*

# ENTRYPOINT [ "python" ]

# CMD [ "api.py" ]