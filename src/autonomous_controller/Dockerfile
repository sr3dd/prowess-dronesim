FROM python:3.10.8-slim

EXPOSE 64002

ENV CONTROLLER_HOSTS CHANGE-THIS
ENV CONTROLLER_PORT 64001

ENV OUTER_GRID 2
ENV INNER_GRID 3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./app /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "64002"]
