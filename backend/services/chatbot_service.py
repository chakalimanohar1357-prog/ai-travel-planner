"""
AI Travel Chatbot Service (Gemini-powered)
--------------------------------------------
Uses Google Gemini (free tier) for natural, conversational travel Q&A.
If GEMINI_API_KEY isn't configured, or the API call fails for any reason
(no internet, rate limit, etc.), this automatically falls back to the
original offline TF-IDF intent classifier below -- so the chatbot never
just breaks for the user.
"""

from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SYSTEM_PROMPT = """You are "Travel Assistant", a friendly and knowledgeable AI travel
concierge inside the AI Travel Planner web app. You help users with:
- Destination advice and recommendations
- Budgeting and cost-saving tips
- Weather and what to pack
- Safety tips for travelers
- Itinerary and day-planning suggestions
- Transportation options

Keep replies concise (2-4 sentences max), warm, and practical. If the user asks
something totally unrelated to travel, gently steer the conversation back to
how you can help them plan their trip. Do not mention that you are Gemini or
any underlying model -- just act as the app's built-in Travel Assistant.
"""


def _try_gemini(message: str, context: dict = None):
    api_key = current_app.config.get("GEMINI_API_KEY")
    print("GEMINI KEY LOADED:", bool(api_key), "LENGTH:", len(api_key) if api_key else 0)
    if not api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT,
        )

        prompt = message
        if context:
            extra = []
            if context.get("destination_name"):
                extra.append(f"The user is currently looking at: {context['destination_name']}.")
            if context.get("budget"):
                extra.append(f"Their trip budget is ${context['budget']}.")
            if extra:
                prompt = " ".join(extra) + "\n\nUser question: " + message

        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        if not text:
            return None
        return {"intent": "gemini", "confidence": 1.0, "response": text}
    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return None


# ---------------------------------------------------------------------------
# Offline fallback -- original rule-based / TF-IDF intent classifier.
# This guarantees the chatbot still works even with zero internet access
# or before you've set up a Gemini key.
# ---------------------------------------------------------------------------

INTENTS = {
    "greeting": {
        "examples": ["hello", "hi", "hey there", "good morning", "good evening"],
        "response": "Hello! I'm your AI travel assistant. Ask me about destinations, budgets, weather, packing, or safety tips!",
    },
    "budget_help": {
        "examples": ["how much should I budget", "what is a good travel budget",
                     "how to save money on trip", "is this destination expensive"],
        "response": "Your estimated cost is broken down into transport, stay, food, and activities on your trip plan page. "
                    "To save more: travel in off-season, book accommodation in advance, and mix free attractions with paid ones.",
    },
    "weather_query": {
        "examples": ["what is the weather like", "will it rain", "how hot is it there",
                     "what should I wear for the weather"],
        "response": "Check the Weather widget on your trip dashboard for a live forecast. "
                    "I can also suggest packing items suited to the forecast automatically.",
    },
    "packing_help": {
        "examples": ["what should I pack", "packing list", "what to bring on my trip",
                     "essentials for travel"],
        "response": "I generate a smart packing list based on your interests, trip length, and weather -- "
                    "check the 'Packing List' section of your trip plan.",
    },
    "safety_tips": {
        "examples": ["is it safe to travel there", "safety tips", "any travel advisories",
                     "how to stay safe"],
        "response": "General tips: keep digital copies of documents, share your itinerary with someone at home, "
                    "avoid isolated areas at night, use registered transport, and keep local emergency numbers handy.",
    },
    "itinerary_help": {
        "examples": ["can you plan my trip", "make an itinerary", "what should I do each day",
                     "suggest a day plan"],
        "response": "Head to 'Plan a Trip', enter your preferences, and I'll generate a personalized day-wise itinerary "
                    "with attractions, hotels, and restaurants matched to your interests and budget.",
    },
    "transport_help": {
        "examples": ["how do I get there", "best transport mode", "should I fly or take a train",
                     "transportation options"],
        "response": "For long distances, flights save time; trains/buses are cheaper and more scenic for shorter regional hops. "
                    "You can set your preferred mode in the trip preferences form.",
    },
    "goodbye": {
        "examples": ["bye", "goodbye", "see you later", "thanks bye"],
        "response": "Safe travels! Feel free to come back anytime you have more questions. 🌍✈️",
    },
}


def _build_corpus():
    docs, labels = [], []
    for intent, data in INTENTS.items():
        for example in data["examples"]:
            docs.append(example)
            labels.append(intent)
    return docs, labels


_DOCS, _LABELS = _build_corpus()


def _classify_intent(message: str, threshold: float = 0.15):
    corpus = _DOCS + [message.lower()]
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        return None, 0.0

    sims = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    best_idx = sims.argmax()
    best_score = float(sims[best_idx])

    if best_score < threshold:
        return None, best_score
    return _LABELS[best_idx], best_score


def _offline_answer(message: str, context: dict = None):
    intent, score = _classify_intent(message)

    if intent is None:
        return {
            "intent": "unknown",
            "confidence": round(score, 2),
            "response": (
                "I'm not fully sure I understood that. I can help with destination "
                "recommendations, budgeting, weather, packing lists, safety tips, "
                "itinerary planning, and transport options. Could you rephrase your question?"
            ),
        }

    response = INTENTS[intent]["response"]
    if context and context.get("destination_name") and intent in ("weather_query", "safety_tips", "transport_help"):
        response = f"For {context['destination_name']}: " + response

    return {"intent": intent, "confidence": round(score, 2), "response": response}


# ---------------------------------------------------------------------------
# Public entrypoint used by routes/chatbot.py -- unchanged signature, so
# nothing else in the app needs to change.
# ---------------------------------------------------------------------------

def generate_answer(message: str, context: dict = None):
    gemini_result = _try_gemini(message, context)
    if gemini_result:
        return gemini_result
    return _offline_answer(message, context)