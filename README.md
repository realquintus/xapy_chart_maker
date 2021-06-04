# xapy_chart_maker

The script is provided with a basic web interface that include html form and php script that call the python code.

It can also be used as API by calling the script exec_xapy.php, filling the variables with GET method.

## Install web interface

### Install on linux host

Install the following packages using your package manager:

```shell
python3 httpd php
```

Then install required python libraries:

```shell
pip3 install statistics requests
```

Clone the github repo into your web server root directory.

```shell
cd /var/www/html
git clone https://github.com/realquintus/xapy_chart_maker.git
cd xapy_chart_maker
mv web_interface/* ..
rmdir web_interface
mv auth_lrs.README auth_lrs.py
systemctl start httpd
```

Fill in the auth_lrs.py file

Open port 80 and 443 in your firewall



### Install using docker

Install docker and docker-compose.

Then:

```shell
mkdir /opt/docker/php-python
```

Dockerfile:

```dockerfile
FROM polinux/httpd-php:latest
RUN yum install -y python3 && \
pip3 install statistics requests
```

build:

```shell
docker build -t local/php-python:latest .
```

Create /opt/docker/php-python/docker-compose.yml:

```yaml
version: '3'
services:
    php-python:
        container_name: php-python
        image: local/php-python:latest
        ports:
          - 80:80
          - 443:443
        restart: always
        volumes:
          - ./DocumentRoot/:/var/www/html/:z
networks:
   external:
      external: true
```

```shell
cd /opt/docker/php-python
mkdir DocumentRoot
cd DocumentRoot
git clone https://github.com/realquintus/xapy_chart_maker.git
cd xapy_chart_maker
mv web_interface/* ..
rmdir web_interface
mv auth_lrs.README auth_lrs.py
docker-compose up -d
```

File the auth_lrs.py file
