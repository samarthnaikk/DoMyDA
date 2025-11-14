# TDS Quiz Solver Service

## Overview

This repository provides a small asynchronous quiz solver service built with FastAPI, Playwright, and httpx. The service accepts POST requests from a TDS-style quiz system, then launches a background asynchronous solver that navigates pages with Playwright, extracts questions (or Base64 payloads), computes placeholder answers, and submits them to the quiz system until no next URL is returned.

## How TDS triggers the solver

The TDS quiz system should send a POST request to `/` with a JSON body containing `email`, `secret`, and `url`. The server validates the JSON and the `secret`, then immediately starts the solver in a background asyncio task and returns a quick acknowledgement.

The `secret` in this repository is `supersecret123`. Change it in `server.py` for production.

## How the solver works

- `solver/browser.py` launches Playwright Chromium (headless) and provides a page and context (`accept_downloads=True`).
- `solver/quiz_solver.py` implements `solve_quiz(email, secret, start_url)`: it navigates to the `start_url`, extracts question text or Base64 blocks, finds a submit URL on the page, computes an answer (placeholder), submits the answer via `httpx.AsyncClient`, and follows any returned `url` in the JSON response until no further URL is provided.

The compute logic is a placeholder; replace `compute_answer` in `solver/quiz_solver.py` with real answering logic.

## Local run instructions

1. Install dependencies (preferably inside a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

2. Run the server with uvicorn:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

3. Send a POST request to `http://localhost:8000/` with the JSON shown above.

## Docker build + run

Build the Docker image and run:

```bash
docker build -t tds-solver:latest .
docker run -p 8000:8000 tds-solver:latest
```

The image uses the official Playwright Python image which includes browser dependencies.

## Render deployment instructions

1. Create a new Web Service on Render.
2. Choose your repository and select "Dockerfile" as the build method.
3. No start command is required; Render will use the Dockerfile's default `CMD`.

## Example test

You can use the demo site to test the solver by sending a POST to the server with `url` set to `https://tds-llm-analysis.s-anand.net/demo` and `secret` set to `supersecret123`.
