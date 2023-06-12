FROM python:3.11-alpine

ENV UAV_HOST CHANGE-THIS
ENV UAV_PORT 65432

WORKDIR /app

COPY *.py /app

ENTRYPOINT [ "python" ]

CMD ["main.py"]
