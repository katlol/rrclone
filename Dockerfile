FROM python:3-alpine
WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py"]
