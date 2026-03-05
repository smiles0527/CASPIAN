# CASPIAN Follow-Up Care

Sensor data analysis LLM tool for CASPIAN Prosthetics S.O.C.K.S (Sensor-Optimized Comfort & Kinetics System). Enter sensor values and how you feel to get personalized insights and care plan suggestions.


### 1. Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in `backend/` (copy from `backend/.env.example`):

```
OPENAI_API_KEY=your_openai_api_key_here
```

Run the API:

```bash
uvicorn main:app --reload
```

API runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` and proxies to the backend.

To point the frontend at a different API URL, create `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

### 3. Use the App

1. Open `http://localhost:5173` in your browser.
2. Enter sensor values (0–100) and how you're feeling.
3. Click **Generate Insights**.
4. View your summary and care plan.

## Project Structure

- `backend/` — FastAPI app, SQLite DB, OpenAI LLM integration
- `frontend/` — React + Vite UI (sensors form, insights display)
- `.env.example` — Environment variable templates

## Requirements

- Python 3.10+
- Node.js 18+
- OpenAI API key ([platform.openai.com](https://platform.openai.com))
