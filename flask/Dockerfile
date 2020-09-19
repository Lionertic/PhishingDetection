FROM ubuntu:latest

LABEL maintainer="Lionertic"

RUN apt-get update && \
    apt-get -y --fix-missing install python3 gcc g++ sudo python3-pip whois

COPY . /usr/src

WORKDIR /usr/src/flask

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN rm -rf /var/cache/apk/*

ENTRYPOINT ["python3"]

CMD ["api.py"]