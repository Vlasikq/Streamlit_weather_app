FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", \
"--server.address=0.0.0.0", \
"--server.port=8501", \
"--server.headless=true", \
"--server.enableCORS=false", \
"--browser.gatherUsageStats=false"]
