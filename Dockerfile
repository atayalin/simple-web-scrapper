FROM python:3.9-alpine

WORKDIR /app

COPY requirements.in .

RUN pip install -r requirements.in

COPY . .

CMD [ "python3", "src/main.py" ]