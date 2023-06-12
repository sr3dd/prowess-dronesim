FROM python:3.11-alpine

# Port for incoming connections
ENV UAV_PORT 65432

# Inference server, port for image transmission
ENV INFERENCE_HOST localhost
ENV INFERENCE_PORT 64001

# Variables to control and simulate battery drain and action delays
ENV TRANSMIT_DELAY 1
ENV INNER_MOTION_DELAY 0.2
ENV OUTER_MOTION_DELAY 0.5
ENV TRANSMIT_DRAIN 1
ENV INNER_MOTION_DRAIN 0.2
ENV OUTER_MOTION_DRAIN 0.5

WORKDIR /app

COPY *.py /app

ENTRYPOINT [ "python" ]

CMD ["main.py"]
