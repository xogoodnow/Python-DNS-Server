FROM python:latest

WORKDIR /app
RUN apt update -y
RUN apt install dnsutils -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080
CMD ["python3", "main.py"]