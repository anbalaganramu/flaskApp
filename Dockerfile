FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

#CMD ["python", "app.py"]
# Use Gunicorn to run the app, not Flask's dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]