FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]