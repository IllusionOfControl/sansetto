FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python -m flask -A app.main:app db upgrade

EXPOSE 5000

CMD ["gunicorn", "app.main:app"]
