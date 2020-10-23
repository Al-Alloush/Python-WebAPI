# Docker MySQL Connections

### 1. we need to the next images:

#### Pull php Image, you can choise the tags from this [official php Page](https://hub.docker.com/_/php?tab=description) 
>  `docker pull php:7-apache`
#### Pull mysql Image, you can choise the tags from this [official mysql Page](https://hub.docker.com/_/mysql)
>  `docker pull mysql:latest`

#### Pull phpmyadmin Image, you can choise the tags from this [official phpmyadmin Page](https://hub.docker.com/r/phpmyadmin/phpmyadmin)
>  `docker pull phpmyadmin/phpmyadmin`
___
___
### 2. Build the php Image and enabled pdo and mysqli extensions in Dockerfile

#### create a file named **Dockerfile** add the next code:
>  ```
>  # if docker dosen't find php:7-apache it'll pull it 
>  FROM php:7-apache
>  
>  # to enabled pdo and mysqli extensions in php to connection with mys8080ql with pdo and mysqli
>  # "RUN docker-php-ext-install" is script to install php extension
>  RUN docker-php-ext-install pdo pdo_mysql
>  RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli
>  # 
>  COPY ./ /var/www/html/
>  ```

Create an 7-apache Container, in the Dockerfile directory, write this command : 
>  `docker build -t myphpapacheserver:latest .`

to Start the myphpapacheserver container :
>  `docker run -d --rm -v %cd%:/var/www/html -p 80:80 myphpapacheserver `

`--rm` to remove this container after stop/end, and `-v %cd%:/var/www/html` in the valume path to store/save the data from current directory `%cd%` to `/var/www/html` php container

#### to get current directory
*  in windows Command `%cd%`
*  in windows PowerShell `${pwd}`
*  in linux `$PWD`
___
___
### 3. Create mysql Container
>  `docker run -d -v ${pwd}:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-pass -e MYSQL_PASSWORD=my-user-pass -e MYSQL_USER=user-name -e MYSQL_DATABASE=default_db -p 3306:3306 mysql:latest --default-authentication-plugin=mysql_native_password `\
You need to specify one of `MYSQL_ROOT_PASSWORD`, `MYSQL_ALLOW_EMPTY_PASSWORD` and `MYSQL_RANDOM_ROOT_PASSWORD`
*  ``MYSQL_PASSWORD=my-user-pass`` 
*  ``MYSQL_USER=user-name``\
if you don't set the above Environment Variables:
>  `docker run -d -v ${pwd}:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-pass -e MYSQL_DATABASE=default_db -p 3306:3306 mysql:latest --default-authentication-plugin=mysql_native_password `\
the user name will be ``root``

#### Note:
When using the docker image to start without an existing database, the container's entrypoint.sh script tries to call the mysqld binary to create the database. This fails in versions later than 5.7.5 because the script starts by calling mysqld --verbose --help to get the configured datadir and when that runs and there is no database, it initializes it automatically.
When the script then calls --initialize, that fails with the error:\
``[ERROR] --initialize specified but the data directory has files in it. Aborting.``
for that we neet to craete a default database
add new Environment: ``-e MYSQL_DATABASE=default_db``

___
___
### 4. Create PhpmyAdmin Container
>  `docker run -d -e PMA_ARBITRARY=1 -p 8080:80 phpmyadmin/phpmyadmin`\
___
___

### 5. Login in php myAdmin

 ```
 >  Hosting: IPAddress // to find it, inspect mysql container then search  IPAddress
                            "NetworkSettings": {
                                "Networks": {
                                    "mysql_netowrk": {
                                        "IPAddress": "172.xx.xx.xx"
 >  Uersname: root
 >  Password: my-pass   // or change it in docker-compose.yml  - MYSQL_ROOT_PASSWORD=my-pass

 ```
___
___

# Create All Images and Containers with Docker Composer
you must be in docker-compose.yml file directery and write this commend:
>  `docker-compose up`



