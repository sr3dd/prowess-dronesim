FROM python:3.10.8-slim

# Port for incoming connections
ENV PORT 64004

ENV DC_HOST CHANGE_THIS
ENV DC_PORT 64001
ENV INFERENCE_HOST CHANGE-THIS
ENV INFERENCE_PORT 64003

# Variables to control and simulate battery drain and action delays
ENV TRANSMIT_DELAY 1
ENV INNER_MOTION_DELAY 0.2
ENV OUTER_MOTION_DELAY 0.5
ENV TRANSMIT_DRAIN 1
ENV INNER_MOTION_DRAIN 0.2
ENV OUTER_MOTION_DRAIN 0.5

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
