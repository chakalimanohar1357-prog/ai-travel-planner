"""
AI Recommendation Engine
------------------------
Implements two complementary recommendation strategies:

1. Content-Based Filtering:
   Builds a TF-IDF vector space over destination tags/description and
   scores destinations against a synthetic "user interest document"
   built from the traveler's stated interests + budget tier.

2. Collaborative Filtering (item-based):
   Uses past trips of ALL users (destination co-occurrence) to recommend
   destinations liked by users with similar trip history/interests.
   This is a lightweight matrix-factorization-free approach suitable for
   a cold-start-friendly student project (no need for huge rating data).

The final recommendation score blends both:
    final_score = 0.6 * content_score + 0.3 * collaborative_score + 0.1 * popularity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def _budget_tier(avg_daily_cost: float) -> str:
    if avg_daily_cost <= 40:
        return "budget"
    if avg_daily_cost <= 100:
        return "mid-range"
    return "luxury"


def content_based_scores(destinations, interests, budget_tier):
    """
    destinations: list of Destination model instances
    interests: list[str] e.g. ["adventure", "history"]
    budget_tier: "budget" | "mid-range" | "luxury"
    """
    if not destinations:
        return {}

    corpus = []
    for d in destinations:
        tags = d.tags or ""
        desc = d.description or ""
        tier = _budget_tier(d.avg_daily_cost)
        corpus.append(f"{tags} {desc} {tier}".lower())

    user_doc = " ".join(interests + [budget_tier]).lower()
    corpus.append(user_doc)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    user_vector = tfidf_matrix[-1]
    dest_vectors = tfidf_matrix[:-1]

    sims = cosine_similarity(user_vector, dest_vectors).flatten()
    return {d.id: float(sims[i]) for i, d in enumerate(destinations)}


def collaborative_scores(destinations, all_trips, current_interests):
    """
    Simple item-based collaborative filtering using destination co-occurrence
    across all users' historical trips that share at least one interest tag
    with the current user's request.

    all_trips: list of Trip model instances (all users)
    """
    if not destinations or not all_trips:
        return {d.id: 0.0 for d in destinations}

    interest_set = set(i.lower() for i in current_interests)
    co_occurrence = {d.id: 0 for d in destinations}
    matches = 0

    for trip in all_trips:
        trip_interests = set((trip.interests or "").lower().split(","))
        if interest_set & trip_interests:
            matches += 1
            if trip.destination_id in co_occurrence:
                co_occurrence[trip.destination_id] += 1

    if matches == 0:
        return {d.id: 0.0 for d in destinations}

    max_count = max(co_occurrence.values()) or 1
    return {k: v / max_count for k, v in co_occurrence.items()}


def rank_destinations(destinations, all_trips, interests, budget_per_day):
    budget_tier = _budget_tier(budget_per_day)

    c_scores = content_based_scores(destinations, interests, budget_tier)
    cf_scores = collaborative_scores(destinations, all_trips, interests)

    ranked = []
    for d in destinations:
        content = c_scores.get(d.id, 0.0)
        collab = cf_scores.get(d.id, 0.0)
        popularity = d.popularity_score or 0.0
        final_score = 0.6 * content + 0.3 * collab + 0.1 * popularity
        ranked.append({
            "destination": d.to_dict(),
            "content_score": round(content, 3),
            "collaborative_score": round(collab, 3),
            "popularity_score": round(popularity, 3),
            "final_score": round(final_score, 3),
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked


def rank_items(items, interests, item_type="attraction"):
    """
    Generic content-based ranker for attractions/hotels/restaurants
    given a list of interests. Falls back to rating-based sort when
    no interest signal applies (e.g. hotels/restaurants).
    """
    if not items:
        return []

    if item_type == "attraction" and interests:
        corpus = [f"{getattr(i, 'category', '')}".lower() for i in items]
        corpus.append(" ".join(interests).lower())
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            sims = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        except ValueError:
            sims = np.zeros(len(items))
        scored = list(zip(items, sims))
        scored.sort(key=lambda x: (x[1], x[0].rating), reverse=True)
        return [item for item, _ in scored]

    # Hotels / restaurants: sort by rating desc
    return sorted(items, key=lambda i: getattr(i, "rating", 0), reverse=True)
