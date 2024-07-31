FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir h11==0.11.0 httpcore==0.15.0
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "fastApiApp.apartment_finder:app"]
