# Fine Tuned Legal Summary GenAI

This repository contains a full-stack legal document summarization application.
The backend is built with FastAPI, and the frontend is a React + Vite application.

## Project structure

- `backend/` — FastAPI service that accepts PDF uploads and returns generated summaries.
- `frontend/` — Vite React app for uploading files and displaying the summary.

## Prerequisites

- Python 3.10+ (Python 3.12 recommended)
- Node.js 18+ and npm
- Optional: GPU if you plan to train the model or use large transformer weights

## Setup

### Backend

1. Open a terminal in `backend/`.
2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Frontend

1. Open a terminal in `frontend/`.
2. Install dependencies:
   ```bash
   npm install
   ```

## Running the app

### Start the backend

From `backend/`:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Start the frontend

From `frontend/`:

```bash
npm run dev
```

Then open the browser at the URL shown by Vite (typically `http://localhost:5173`).

## How it works

- Upload a PDF document through the frontend.
- The frontend sends the file to `http://localhost:8000/upload`.
- The backend extracts text from the PDF and generates a summary with a transformer model.
- The summary is returned to the frontend and displayed.

## Model notes

- If `backend/saved_legal_model/` exists, the backend will attempt to load the fine-tuned LoRA adapter.
- If the saved model is missing, it falls back to the base `distilgpt2` model to produce a summary.

## Optional training

The `backend/train_model.py` script can fine-tune a model using the `ChicagoHAI/CaseSumm` dataset.
Make sure `.env.local` contains a valid `HF_TOKEN` if you want to use Hugging Face Hub login.

## Deployment

This repo is ready for local deployment using the backend and frontend separately.
For production, host the backend on a Python-compatible server and build the frontend with `npm run build`.
