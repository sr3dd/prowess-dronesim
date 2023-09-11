FROM python:3.10.8-slim

ENV PORT 64003

ENV AC_HOST CHANGE-THIS
ENV AC_PORT 64002

ENV INFERENCE_TIME 2

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
