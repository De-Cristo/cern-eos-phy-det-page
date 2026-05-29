# AI Backend for CMS PHY DET Analysis

This is a minimal FastAPI backend designed to run on CERN PaaS / OKD.
It listens on port 8080 and provides health checks and a placeholder chat endpoint.

## Configuration
- `KIMI_API_KEY`: This environment variable should be provided as an OKD Secret or set in your environment. Do **not** commit the API key to git.

## Testing Locally
To test the backend on your local machine:

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
./app.sh
```

In another terminal, you can test the endpoints:
```bash
# Test health check
curl http://127.0.0.1:8080/health

# Test chat endpoint
curl -X POST http://127.0.0.1:8080/chat -H "Content-Type: application/json" -d '{"question":"hello"}'
```
