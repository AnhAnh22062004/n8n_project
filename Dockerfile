FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /home/n8nuser/n8n_project/temp_images

EXPOSE 5000

CMD ["python", "app.py"]
