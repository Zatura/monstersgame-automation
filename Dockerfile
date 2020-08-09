FROM python:3.8-alpine

COPY src .
COPY data .

RUN apk update
RUN apk add chromium chromium-chromedriver

RUN pip install --upgrade pip
RUN pip install selenium

CMD ["ls"]
CMD ["python", "src/main.py"]
