# 🧳 Smart Travel Planner

An intelligent backend system that suggests personalized travel itineraries using real-time data and LLMs. Built with FastAPI and integrated with Gemini Pro and external APIs for a seamless, intelligent travel planning experience.

---

## 🚀 Features

- 📍 Destination suggestions based on:
  - User preferences (interests, travel dates, location)
  - Visa rules (static CSV)
  - Real-time weather
  - Budget
- 🧠 Personalized day-wise itineraries generated using Gemini Pro
- ☁️ Designed for cloud deployment (GCP/AWS ready)
- ⚡ Modular, extensible, and cache-friendly architecture

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **AI Integration:** Gemini Pro API (Google AI)
- **Data Sources:** WeatherAPI, CSV (Visa Rules), JSON (Destinations)
- **Database (optional/future):** PostgreSQL
- **DevOps Ready:** Docker, GCP Cloud Run
- **Other:** Redis (optional for caching), dotenv for secrets

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/smart-travel-planner.git
cd smart-travel-planner

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
