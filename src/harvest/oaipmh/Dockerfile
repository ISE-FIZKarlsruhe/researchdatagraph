FROM python:3.12

RUN useradd -d /app -r -s /bin/bash -g 1006 -G sudo -u 1006 nfdi4culture
USER nfdi4culture

WORKDIR /app
COPY main.py .

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["python", "main.py"]