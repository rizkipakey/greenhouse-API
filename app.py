from flask import Flask, jsonify
import random, time

app = Flask(__name__)

@app.route("/data")
def get_data():
    return jsonify({
        "timestamp": int(time.time()),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "light": round(random.uniform(200, 800), 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
