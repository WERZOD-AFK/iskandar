FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Webhook rejimida Railway shu portga so'rov yuboradi (PORT env orqali beriladi).
# Polling rejimida bu port ishlatilmaydi, lekin zarar qilmaydi.
EXPOSE 8080

CMD ["python", "main.py"]
