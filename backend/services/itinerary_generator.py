"""
Itinerary Generator
--------------------
Greedy day-wise scheduler:
- Distributes ranked attractions across available days (~6-7 active hours/day)
- Picks a hotel matching accommodation preference & budget
- Picks 1 lunch + 1 dinner restaurant per day (rotating to avoid repeats)
- Adds a fixed "arrival" and "departure" buffer for realism
"""

import math


def _pick_hotel(hotels, accommodation_pref, budget_per_night):
    candidates = [h for h in hotels if h.category == accommodation_pref] or hotels
    # prefer within budget, else cheapest available
    within_budget = [h for h in candidates if h.price_per_night <= budget_per_night]
    pool = within_budget or candidates
    if not pool:
        return None
    return sorted(pool, key=lambda h: h.rating, reverse=True)[0]


def generate_itinerary(destination, ranked_attractions, restaurants, hotels,
                        duration_days, accommodation_pref, daily_budget):
    hours_per_day = 7
    hotel = _pick_hotel(hotels, accommodation_pref, daily_budget * 0.5)
    restaurants_sorted = sorted(restaurants, key=lambda r: r.rating, reverse=True) or []

    itinerary = []
    attraction_pool = list(ranked_attractions)
    idx = 0

    for day in range(1, duration_days + 1):
        remaining_hours = hours_per_day
        day_plan = {
            "day": day,
            "title": f"Day {day} in {destination.name}",
            "activities": [],
            "lunch": None,
            "dinner": None,
            "hotel": hotel.to_dict() if hotel else None,
        }

        if day == 1:
            day_plan["activities"].append({
                "time": "Morning",
                "activity": f"Arrival in {destination.name}, check-in at hotel, freshen up",
            })
            remaining_hours -= 1.5

        while idx < len(attraction_pool) and remaining_hours > 0:
            attraction = attraction_pool[idx]
            duration = attraction.est_duration_hours or 2
            if duration > remaining_hours and remaining_hours < hours_per_day:
                break
            day_plan["activities"].append({
                "time": "Flexible",
                "activity": attraction.name,
                "category": attraction.category,
                "duration_hours": duration,
                "entry_fee": attraction.entry_fee,
            })
            remaining_hours -= duration
            idx += 1

        if restaurants_sorted:
            day_plan["lunch"] = restaurants_sorted[day % len(restaurants_sorted)].to_dict()
            day_plan["dinner"] = restaurants_sorted[(day + 1) % len(restaurants_sorted)].to_dict()

        if day == duration_days:
            day_plan["activities"].append({
                "time": "Evening",
                "activity": f"Pack up, check-out, departure from {destination.name}",
            })

        itinerary.append(day_plan)

    return itinerary


def estimate_total_cost(itinerary, travelers, transport_mode, duration_days):
    transport_cost_map = {
        "flight": 250,
        "train": 80,
        "bus": 40,
        "car": 60,
        "cruise": 300,
    }
    per_person_transport = transport_cost_map.get(transport_mode, 150)
    transport_total = per_person_transport * travelers

    hotel_total = 0.0
    food_total = 0.0
    activity_total = 0.0

    for day in itinerary:
        if day.get("hotel"):
            hotel_total += day["hotel"]["price_per_night"]
        if day.get("lunch"):
            food_total += day["lunch"]["avg_cost"] * travelers
        if day.get("dinner"):
            food_total += day["dinner"]["avg_cost"] * travelers
        for act in day["activities"]:
            activity_total += act.get("entry_fee", 0) * travelers

    misc_buffer = 0.1 * (hotel_total + food_total + activity_total + transport_total)

    breakdown = {
        "transport": round(transport_total, 2),
        "accommodation": round(hotel_total, 2),
        "food": round(food_total, 2),
        "activities": round(activity_total, 2),
        "miscellaneous_buffer": round(misc_buffer, 2),
    }
    breakdown["total"] = round(sum(breakdown.values()), 2)
    return breakdown
