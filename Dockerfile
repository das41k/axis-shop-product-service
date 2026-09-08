FROM python:3.12-slim as base

WORKDIR /product-service

ENV PYTHONDONTWRITEBYTECODE=1 \
   PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app

EXPOSE 8080

RUN adduser --disabled-password --gecos '' appuser
USER appuser

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0" ,"--port", "8080"]