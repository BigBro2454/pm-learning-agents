import json

# --- Mock Data ---

FLIGHTS = [
    {"id": "F1", "origin": "NYC", "dest": "TYO", "airline": "LuxuryAir", "price": 1500, "class": "Business"},
    {"id": "F2", "origin": "NYC", "dest": "TYO", "airline": "BudgetAir", "price": 600, "class": "Economy"},
    {"id": "F3", "origin": "NYC", "dest": "TYO", "airline": "StandardAir", "price": 900, "class": "Economy Plus"},
]

HOTELS = [
    {"id": "H1", "city": "TYO", "name": "Grand Tokyo Resort", "stars": 5, "price_per_night": 400},
    {"id": "H2", "city": "TYO", "name": "Tokyo Capsule Hotel", "stars": 2, "price_per_night": 50},
    {"id": "H3", "city": "TYO", "name": "Comfort Inn Tokyo", "stars": 3, "price_per_night": 120},
    {"id": "H4", "city": "TYO", "name": "Boutique Hotel Sakura", "stars": 4, "price_per_night": 250},
]

ACTIVITIES = [
    {"id": "A1", "city": "TYO", "name": "Private Sushi Making Class", "price": 200},
    {"id": "A2", "city": "TYO", "name": "Mt. Fuji Helicopter Tour", "price": 500},
    {"id": "A3", "city": "TYO", "name": "Public Museum Pass", "price": 30},
    {"id": "A4", "city": "TYO", "name": "Walking Tour", "price": 20},
    {"id": "A5", "city": "TYO", "name": "Tea Ceremony", "price": 100},
]

# --- Tools for Planner Agent ---

def search_flights(origin: str, dest: str) -> str:
    """Search for available flights between origin and destination."""
    results = [f for f in FLIGHTS if f["origin"] == origin and f["dest"] == dest]
    return json.dumps(results)

def search_hotels(city: str) -> str:
    """Search for hotels in the given city."""
    results = [h for h in HOTELS if h["city"] == city]
    return json.dumps(results)

def search_activities(city: str) -> str:
    """Search for activities in the given city."""
    results = [a for a in ACTIVITIES if a["city"] == city]
    return json.dumps(results)

# --- Tools for Accountant Agent ---

def calculate_total(itinerary_json: str) -> str:
    """
    Calculate the total cost of a proposed itinerary.
    Expects a JSON string with keys: 'flight_id', 'hotel_id', 'nights', and 'activity_ids'.
    Example: {"flight_id": "F1", "hotel_id": "H1", "nights": 5, "activity_ids": ["A1", "A3"]}
    """
    try:
        itinerary = json.loads(itinerary_json)
        total = 0
        
        # Calculate flight cost
        flight = next((f for f in FLIGHTS if f["id"] == itinerary.get("flight_id")), None)
        if flight:
            total += flight["price"]
        else:
            return json.dumps({"error": f"Flight {itinerary.get('flight_id')} not found."})
        
        # Calculate hotel cost
        hotel = next((h for h in HOTELS if h["id"] == itinerary.get("hotel_id")), None)
        if hotel:
            total += hotel["price_per_night"] * itinerary.get("nights", 0)
        else:
            return json.dumps({"error": f"Hotel {itinerary.get('hotel_id')} not found."})
        
        # Calculate activities cost
        for act_id in itinerary.get("activity_ids", []):
            act = next((a for a in ACTIVITIES if a["id"] == act_id), None)
            if act:
                total += act["price"]
            else:
                return json.dumps({"error": f"Activity {act_id} not found."})
                
        return json.dumps({"total_cost": total})
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format."})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Expose these as lists for easier import if needed, though functions themselves can be used directly
planner_tools = [search_flights, search_hotels, search_activities]
accountant_tools = [calculate_total]
