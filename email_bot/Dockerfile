# email-bot/Dockerfile

FROM python:3.11-slim

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy code
COPY app/ /app/app/

# (Optional) install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the daemon
CMD ["python", "-m", "app.main"]
