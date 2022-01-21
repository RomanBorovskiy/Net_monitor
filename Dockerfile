FROM python:3.9

#https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
#Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
#Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1


WORKDIR /monitor
COPY requirements.txt /monitor
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /monitor
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app

