FROM python:3.10.8-slim

ENV PORT 64001

ENV AC_HOST CHANGE-THIS
ENV AC_PORT 64002
ENV DRONE_HOST CHANGE-THIS
ENV DRONE_PORT 64004

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
