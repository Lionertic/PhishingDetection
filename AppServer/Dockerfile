FROM php:7.4.3-fpm-alpine

LABEL maintainer="Lionertic"

WORKDIR /var/www/html

COPY . /var/www/html/

RUN apk --update add curl git oniguruma-dev

RUN docker-php-ext-install mysqli mbstring pdo pdo_mysql tokenizer

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN composer install

RUN rm -rf /var/cache/apk/*

EXPOSE 9000

CMD "php-fpm"
