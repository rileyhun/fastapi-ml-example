FROM tiangolo/uvicorn-gunicorn:python3.7

RUN mkdir -p /app/app
COPY /app /app/app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80
