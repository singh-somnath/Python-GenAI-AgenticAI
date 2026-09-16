# Langchain-CustomerServiceQA

Customer Support QA Evaluator using LangChain and FastAPI.

## Docker

Build and run:

```bash
docker build -t customer-service-qa .
docker run -p 8000:8000 --env-file .env customer-service-qa
```

API endpoint: `POST http://localhost:8000/evaluate-file`

## Local Development

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
