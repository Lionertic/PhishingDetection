FROM ubuntu:16.04

# MAINTANER Your Name "youremail@domain.tld"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./Flasks/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./Flasks /app

ENTRYPOINT [ "python" ]

CMD [ "api.py" ]