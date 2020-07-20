FROM python:3.8-alpine

COPY src data ./

RUN apk update
RUN apk add chromium chromium-chromedriver

RUN pip install --upgrade pip
RUN pip install selenium

CMD ["python", "src/main.py"]
