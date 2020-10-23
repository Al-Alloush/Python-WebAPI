# if docker dosen't find php:7-apache it'll pull it 
FROM php:7-apache

# to enabled pdo and mysqli extensions in php to connection with mysql with pdo and mysqli
# "RUN docker-php-ext-install" is script to install php extention
RUN docker-php-ext-install pdo pdo_mysql
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli
# 
COPY ./ /var/www/html/