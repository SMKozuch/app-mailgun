FROM quay.io/keboola/docker-custom-python:latest

RUN pip install --disable-pip-version-check --no-cache-dir logging_gelf

COPY /data/ /data/

COPY . /code/
WORKDIR /data/
CMD ["python", "-u", "/code/main.py"]
