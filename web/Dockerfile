FROM python:3.6
EXPOSE 5000
WORKDIR /web
COPY requirements.txt /web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /web

RUN pip install -r requirements.txt

COPY . /web
CMD python server.py