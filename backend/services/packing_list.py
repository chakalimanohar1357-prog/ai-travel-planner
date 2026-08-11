"""
Smart Packing List Generator
-----------------------------
Rule-based generator that adapts to weather forecast, trip duration,
interests (activity type), and traveler count.
"""

BASE_ITEMS = [
    "Passport / ID & travel documents", "Phone charger & power bank",
    "Wallet with cash & cards", "Toiletries kit", "Reusable water bottle",
    "Basic first-aid kit & personal medication", "Travel adapter",
]

INTEREST_ITEMS = {
    "adventure": ["Trekking shoes", "Quick-dry clothing", "Headlamp", "Multi-tool"],
    "beaches": ["Swimwear", "Sunscreen (SPF 50+)", "Beach towel", "Flip-flops", "Sunglasses"],
    "nature": ["Binoculars", "Insect repellent", "Comfortable walking shoes", "Light rain jacket"],
    "history": ["Comfortable walking shoes", "Notebook/camera for sightseeing", "Modest clothing for heritage sites"],
    "shopping": ["Extra foldable bag", "Extra luggage space", "Comfortable shoes for walking"],
    "nightlife": ["Smart casual outfit", "Comfortable party shoes"],
    "wildlife": ["Binoculars", "Neutral colored clothing", "Camera with zoom lens"],
}

WEATHER_ITEMS = {
    "hot": ["Light cotton clothing", "Sunhat", "Extra sunscreen"],
    "cold": ["Thermal wear", "Warm jacket", "Gloves & beanie"],
    "rainy": ["Compact umbrella", "Waterproof jacket", "Waterproof bag cover"],
    "mild": ["Light layers", "Light jacket for evenings"],
}


def generate_packing_list(interests, duration_days, weather_condition="mild", travelers=1):
    items = set(BASE_ITEMS)

    for interest in interests:
        key = interest.lower().strip()
        if key in INTEREST_ITEMS:
            items.update(INTEREST_ITEMS[key])

    items.update(WEATHER_ITEMS.get(weather_condition.lower(), WEATHER_ITEMS["mild"]))

    clothing_sets = max(2, min(duration_days, 7))
    items.add(f"{clothing_sets} sets of clothing (laundry recommended for longer trips)")

    if travelers > 1:
        items.add("Shared travel documents folder for the group")

    return sorted(items)
