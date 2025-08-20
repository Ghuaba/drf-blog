FROM python:3.12

#Install SSH client

RUN apt-get update && apt-get install -y openssh-client

#Set environment variables
ENV PYTHONUNBUFFERED 1

#Set working directory
WORKDIR /app

#Copy requirements file
COPY requirements.txt /app/requirements.txt

#INstall python dependencies
RUN pip install -r requirements.txt

#COpy the application to the working directory
COPY . /app

#Start SSH tunel
CMD python manage.py runserver 0.0.0.0:8000
