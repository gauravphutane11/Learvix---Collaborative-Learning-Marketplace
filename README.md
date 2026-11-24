# Learvix — Learn together

Learvix is a peer-to-peer learning community where people discover learning partners, exchange skills, organise learning sessions and track progress.

## Demo account
Run the backend seed script, then sign in with:

- **Email:** `demo@learvix.com`
- **Password:** `Learvix@123`

Demo profiles include Maya Shah, Rohan Kulkarni, Isha Patil and Kabir Desai. The seed script is safe to run more than once.

## Features
- Account registration, login and protected routes
- Personal profiles with skills offered and skills wanted
- Skill-based partner matching and mutual-exchange indicators
- Create and manage skill-exchange requests
- Track completed sessions and exchange progress
- Notifications with per-user read state
- SkillProof practical challenge interface (demo workflow; no automated AI scoring claim)
- Responsive interface for desktop and mobile

## Technology
- Frontend: React 18, Vite, React Router, Lucide
- Backend: Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- Database: SQLite locally; PostgreSQL-compatible deployment configuration

## Run on Windows
### Backend terminal
```powershell
cd backend
py -m venv .venv
.venv\Scripts\activate
 Copy-Item .env.example .env
 pip install -r requirements.txt
 python seed.py
 python app.py
```
Backend runs at `http://127.0.0.1:5000`.

### Frontend terminal
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL printed in the terminal (normally `http://localhost:5173`).

## Run on macOS/Linux
Backend: `cd backend && python3 -m venv .venv && source .venv/bin/activate && cp .env.example .env && pip install -r requirements.txt && python seed.py && python app.py`

Frontend: `cd frontend && npm install && npm run dev`

## API smoke test
With the backend running and demo seed loaded, run `python backend/test_api.py` from the repository root after installing the backend requirements.

## Configuration
Set `JWT_SECRET_KEY` to a long random value before deployment. Set `CORS_ORIGINS` to the exact frontend origin(s). Set `DATABASE_URL` to a managed PostgreSQL URL for production. Never commit `.env` files or production secrets.

## Scope notes
The video-chat screen is currently a UI demonstration and should not be presented as a verified live WebRTC service. SkillProof is a practical challenge/evidence concept in this build; automated AI evaluation is not included.
