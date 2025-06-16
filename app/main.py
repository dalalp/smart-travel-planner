from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import csv
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))    

load_dotenv()
app = FastAPI()

# Load visa rules
with open("visa_rules.csv") as f:
    visa_data = list(csv.DictReader(f))

# Load destination costs
with open("destinations.json") as f:
    all_destinations = json.load(f)

# Input model
class ItineraryRequest(BaseModel):
    passport: str
    budget_usd: float
    preferences: List[str]
    travel_dates: List[str]

@app.post("/plan-itinerary")
def plan_itinerary(request: ItineraryRequest):
    # Filter by visa eligibility
    allowed = [
        row["destination_country"] for row in visa_data
        if row["passport_country"] == request.passport and row["visa_required"] == "false"
    ]

    # Filter by budget
    matching_destinations = [
        d for d in all_destinations
        if d["country"] in allowed and d["avg_cost_usd"] <= request.budget_usd
    ]

    if not matching_destinations:
        raise HTTPException(status_code=404, detail="No destinations found matching criteria.")

    # Mock weather for now
    for d in matching_destinations:
        d["weather"] = get_weather(d["city"])

    itinerary_text = generate_itinerary_gemini(request, matching_destinations)

    return {
        "destinations": matching_destinations,
        "itinerary": itinerary_text
    }


def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key missing"

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or "current" not in data:
            return "Weather unavailable"

        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        return f"{temp_c}°C, {condition}"
    except Exception:
        return "Weather fetch error"
    
def generate_itinerary_gemini(user_input, destinations):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
You are a smart travel assistant.

Create a personalized 5-7 day itinerary based on:
- User preferences: {user_input.preferences}
- Budget: ${user_input.budget_usd}
- Travel dates: {user_input.travel_dates}
- Suggested destinations with weather:

{json.dumps(destinations, indent=2)}

Return a friendly, day-wise plan that recommends activities, travel tips, and local highlights.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini error: {str(e)}"