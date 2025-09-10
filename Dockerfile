FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY op.py .
COPY .env* ./
RUN mkdir -p /app/.streamlit
RUN echo '[server]\nport = 8080\nenableCORS = false\nheadless = true\n' > /app/.streamlit/config.toml
EXPOSE 8080
ENV PORT=8080
CMD streamlit run op.py --server.port=$PORT --server.address=0.0.0.0
