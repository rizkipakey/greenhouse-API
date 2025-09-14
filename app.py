from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///greenhouse.db"
db = SQLAlchemy(app)

# --- Database Model ---
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light = db.Column(db.Float)

# --- Create DB tables (run once) ---
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    # Simulate random sensor data
    temp = random.randint(20, 30)
    hum = random.randint(50, 70)
    light = random.randint(200, 800)

    # Save to database
    reading = Reading(temperature=temp, humidity=hum, light=light)
    db.session.add(reading)
    db.session.commit()

    return jsonify({
        "temperature": temp,
        "humidity": hum,
        "light": light
    })

@app.route("/history")
def history():
    # Get last 20 records from DB
    readings = Reading.query.order_by(Reading.timestamp.desc()).limit(20).all()
    readings.reverse()  # oldest first for chart

    return jsonify([
        {
            "timestamp": r.timestamp.strftime("%H:%M:%S"),
            "temperature": r.temperature,
            "humidity": r.humidity,
            "light": r.light
        } for r in readings
    ])
