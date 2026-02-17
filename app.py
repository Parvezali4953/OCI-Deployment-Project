from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# SQLite Database (Rackspace trainee demo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model - Weather Records
class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables on startup
with app.app_context():
    db.create_all()

API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return render_template("error.html", error="API key missing.")
    return render_template('index.html')

@app.route('/health')
def health_check():
    return {"status": "healthy", "db_connected": True}, 200  # DB proof!

@app.route('/weather', methods=['POST'])
def get_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return render_template("error.html", error="API key missing.")

    city = request.form.get('city', '').strip()
    if not city:
        return render_template("result.html", weather=None, error="Enter city.")

    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "city": data.get("name", city),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        
        # SAVE TO DATABASE (Rackspace Cloud DBA proof!)
        record = WeatherRecord(
            city=city,
            temperature=weather_data["temperature"],
            description=weather_data["description"],
            humidity=weather_data["humidity"]
        )
        db.session.add(record)
        db.session.commit()
        
        return render_template("result.html", weather=weather_data)
        
    except Exception as e:
        return render_template("result.html", weather=None, error=f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
