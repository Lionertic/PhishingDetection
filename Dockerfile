FROM php:7.3-fpm-alpine

LABEL maintainer="Lionertic"

COPY composer.lock composer.json /var/www/html/

WORKDIR /var/www/html

RUN apk --update add curl git 

RUN docker-php-ext-install mysqli mbstring pdo pdo_mysql tokenizer

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN rm -rf /var/cache/apk/*

EXPOSE 9000

CMD "php-fpm"
