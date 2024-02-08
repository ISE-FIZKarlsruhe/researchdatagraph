FROM python:3.12

WORKDIR /app
COPY main.py .

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["python", "main.py"]