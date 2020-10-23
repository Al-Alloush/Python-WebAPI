# create two container first the apache server for phpMyAdmin, and the other for python api-flask


FROM python:3.7
WORKDIR /code
COPY * /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --use-feature=2020-resolver
