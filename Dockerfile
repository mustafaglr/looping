FROM python:3.5-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r req.txt

CMD ["python","app.py"]