# CASPIAN Follow-Up Care

Sensor data analysis LLM tool for CASPIAN Prosthetics S.O.C.K.S (Sensor-Optimized Comfort & Kinetics System). Enter sensor values and how you feel to get personalized insights and care plan suggestions.

---

## Deploy to Render (for others to use)

Push your repo to GitHub first, then create two services on Render:

### Backend (Web Service)

1. [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repo, select this project
3. Settings:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `OPENAI_API_KEY` = your key
5. Deploy → copy your backend URL (e.g. `https://caspian-backend.onrender.com`)
6. Add `CORS_ORIGINS` = your frontend URL (see below) and redeploy

### Frontend (Static Site)

1. [render.com](https://render.com) → **New** → **Static Site**
2. Connect the same GitHub repo
3. Settings:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add environment variable: `VITE_API_URL` = your backend URL (from step 5 above)
5. Deploy → copy your frontend URL (e.g. `https://caspian-frontend.onrender.com`)

### Wire it up

- Set **Backend** `CORS_ORIGINS` to your frontend URL, then redeploy the backend
- **Link from Wix:** On your Caspian Follow-Up Care page, add a button linking to your frontend URL

---

## Local development

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
