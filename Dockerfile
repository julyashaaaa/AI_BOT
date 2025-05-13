FROM python:3.13-slim
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "bot.py"]