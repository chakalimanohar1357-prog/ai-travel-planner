# 🌍 AI Travel Planner

A full-stack, AI-powered personal travel assistant — built as a portfolio-worthy final-year
B.Tech project. Users enter their travel preferences and the system generates a personalized,
day-wise itinerary using content-based + collaborative filtering, estimates trip costs,
shows live weather, generates smart packing lists, and answers travel questions through an
AI chatbot.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, React Router, Tailwind CSS, Axios, Lucide Icons |
| Backend | Python, Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Bcrypt |
| Database | SQLite by default (swap `DATABASE_URL` for MySQL or MongoDB-compatible URI) |
| AI / ML | scikit-learn (TF-IDF + cosine similarity) for content-based filtering, collaborative filtering via co-occurrence, rule-based NLP chatbot, greedy itinerary scheduling |
| External APIs | OpenWeatherMap (weather), Google Places (nearby attractions), Google Maps Directions (route optimization) — all have offline mock fallbacks if keys aren't set |

## Features

- 🔐 Secure JWT authentication (register/login)
- 🎯 Preference intake: destination, budget, duration, travelers, interests, transport, accommodation
- 🤖 AI recommendation engine (content-based filtering + collaborative filtering + popularity blending)
- 🗓️ Auto-generated day-wise itinerary (attractions, hotels, restaurants)
- 💰 Transparent cost breakdown & budget feasibility check
- ☀️ Live weather forecast widget
- 🎒 Smart, weather- & interest-aware packing list generator
- 🛡️ Safety tips
- 💬 AI chatbot for travel Q&A (NLP intent matching)
- ❤️ Save favorite destinations
- 📜 Trip history with status tracking (planned/ongoing/completed)
- 🗺️ Interactive embedded maps
- 🛠️ Admin dashboard: manage destinations, hotels, restaurants, users; view platform stats

## Project Structure

```
ai-travel-planner/
├── backend/
│   ├── app.py                  # Flask app factory & entrypoint
│   ├── config.py
│   ├── extensions.py
│   ├── models.py                # SQLAlchemy models
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/                  # REST API blueprints
│   │   ├── auth.py
│   │   ├── trips.py
│   │   ├── recommendations.py
│   │   ├── chatbot.py
│   │   ├── external.py
│   │   ├── admin.py
│   │   └── destinations.py
│   ├── services/                 # AI / business logic
│   │   ├── recommendation_engine.py
│   │   ├── itinerary_generator.py
│   │   ├── packing_list.py
│   │   ├── chatbot_service.py
│   │   └── cost_estimator.py
│   └── data/
│       └── seed_data.py         # sample data loader
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── public/index.html
    └── src/
        ├── App.jsx, index.js, index.css
        ├── api/axios.js
        ├── context/AuthContext.jsx
        ├── components/           # Navbar, Footer, Cards, Widgets, Chatbot...
        └── pages/                # Home, Login, Register, PlanTrip, Dashboard...
```

## Getting Started

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then fill in your API keys (optional — mocks work without them)

# Seed the database with sample destinations, hotels, restaurants, attractions
python -m data.seed_data

# Run the API server
python app.py
```
The API will be running at `http://localhost:5000`.

**Admin login (seeded):** `admin@travelai.com` / `Admin@123`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```
The app will open at `http://localhost:3000`.

If your backend runs on a different host/port, create a `.env` file in `frontend/` with:
```
REACT_APP_API_URL=http://localhost:5000/api
```

### 3. Using MySQL or MongoDB instead of SQLite

This project uses SQLAlchemy, which supports MySQL out of the box — just change
`DATABASE_URL` in `backend/.env`, e.g.:
```
DATABASE_URL=mysql+pymysql://user:password@localhost/travel_planner
```
(install `pymysql` via pip). For MongoDB, you would swap the SQLAlchemy models for
`PyMongo`/`MongoEngine` documents — the route/service layer logic stays the same since
everything works off plain Python dicts and `to_dict()` serialization.

## How the AI Recommendation Engine Works

1. **Content-Based Filtering** — Destination tags, description, and budget tier are vectorized
   with TF-IDF; the user's interests + budget tier form a "query document" scored via cosine
   similarity against every destination.
2. **Collaborative Filtering** — Destination co-occurrence is computed across all users' past
   trips that share at least one interest tag with the current request (item-based CF, no
   cold-start penalty).
3. **Blended Score** — `final_score = 0.6 * content + 0.3 * collaborative + 0.1 * popularity`
4. **Itinerary Generation** — A greedy scheduler distributes ranked attractions across
   available days (~7 active hours/day), attaches a hotel matching accommodation preference
   & budget, and rotates lunch/dinner restaurant picks.
5. **Chatbot** — TF-IDF + cosine similarity intent classification over curated example phrases
   per intent (budget, weather, packing, safety, itinerary, transport, greetings).

## Extending the Project

- Swap the rule-based chatbot for a real LLM call (OpenAI/Anthropic) inside `chatbot_service.py`
- Add real user rating data to strengthen collaborative filtering (currently trip-history based)
- Add payment/booking integrations
- Add JWT refresh tokens & email verification
- Deploy backend on Render/Railway and frontend on Vercel/Netlify

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login, get JWT |
| GET | `/api/destinations` | List all destinations |
| POST | `/api/recommendations/destinations` | AI-ranked destination recommendations |
| POST | `/api/trips/plan` | Generate itinerary for chosen destination |
| GET | `/api/trips` | Get logged-in user's trip history |
| GET/POST/DELETE | `/api/trips/favorites` | Manage favorites |
| POST | `/api/chatbot/ask` | Ask the AI travel chatbot |
| GET | `/api/external/weather` | Weather forecast |
| GET | `/api/external/places` | Nearby places |
| GET | `/api/external/directions` | Route optimization |
| GET/POST/DELETE | `/api/admin/*` | Admin CRUD & stats (admin JWT required) |

---
Built as a demonstration of full-stack development, applied machine learning, third-party API
integration, and user-centric product design.
