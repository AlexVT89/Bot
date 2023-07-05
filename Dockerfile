FROM python:3.9-alpine
WORKDIR /Bot
COPY requirements.txt .
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /app
EXPOSE 80
CMD ["python", "Bot.py"]