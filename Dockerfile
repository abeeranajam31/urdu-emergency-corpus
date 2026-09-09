FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-mlops.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-mlops.txt

COPY . .

ENV MLFLOW_DISABLE_AGENT_HINT=1

ENTRYPOINT ["python", "scripts/run_analysis.py"]
CMD ["--corpus", "data/corpus.jsonl", "--results-dir", "results"]
