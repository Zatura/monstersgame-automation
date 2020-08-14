FROM python:3.8-alpine

COPY . .
RUN apk update
RUN apk add chromium chromium-chromedriver
RUN pip install --upgrade pip
RUN pip install selenium boto3

CMD ["python", "src/main.py"]
