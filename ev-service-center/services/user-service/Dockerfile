FROM python:3.10

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "services/app.py"]