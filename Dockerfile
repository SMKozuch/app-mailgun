FROM quay.io/keboola/docker-custom-python:latest

COPY requirements.txt requirements.txt
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

#COPY /data/ /data/

COPY . /code/
WORKDIR /data/
CMD ["python", "-u", "/code/main.py"]