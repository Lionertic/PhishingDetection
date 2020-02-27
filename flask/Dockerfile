FROM ubuntu:latest

LABEL maintainer="Lionertic"

RUN apt-get update && \
    apt-get -y install python3 wget gcc g++ firefox sudo apt python3-pip

COPY . /app

WORKDIR /app

RUN chmod +x geckodriver

RUN cp geckodriver /usr/local/bin

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN rm -rf /var/cache/apk/*

ENTRYPOINT ["python3"]

CMD ["api.py"]
