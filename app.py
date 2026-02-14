from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import math

app = Flask(__name__)
CORS(app)

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return render_template("pcod.html")  


# ---------------- LOAD DATASET ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "health_data.csv")

df = pd.read_csv(csv_path)


# ---------------- WATER FUNCTION ----------------
def water_intake(weight):
    try:
        liters = math.ceil(float(weight) * 0.033)
        return f"{liters} liters per day"
    except:
        return "2-3 liters per day"


# ---------------- LIFESTYLE FUNCTION ----------------
def lifestyle_by_age(age):
    age = int(age)
    if age < 18:
        return ["Eat on time", "Limit junk food", "Sleep well"]
    elif age <= 30:
        return ["Exercise daily", "Manage stress", "Avoid late-night eating"]
    elif age <= 45:
        return ["Avoid sugar", "Follow routine", "Stay active"]
    else:
        return ["Light exercise", "Good digestion", "Proper sleep"]


# ---------------- FOOD DATABASE (SAME AS YOUR NOTEBOOK) ----------------
FOODS = {
    "PCOD": {
        "message": "Based on what you shared, your body shows signs of PCOD. Food and lifestyle changes can help manage these symptoms naturally.",
        "vegetables": [
            "Spinach helps balance hormones and improves blood health in PCOD.",
            "Broccoli helps reduce hormonal imbalance in PCOD.",
            "Carrot helps detox the body and supports hormone balance in PCOD.",
            "Cucumber reduces bloating and keeps the body cool in PCOD.",
            "Pumpkin supports digestion and helps hormone balance in PCOD."
        ],
        "fruits": [
            "Apple helps control insulin levels and reduce PCOD symptoms.",
            "Berries reduce inflammation and support hormone health in PCOD.",
            "Papaya improves digestion and reduces bloating in PCOD.",
            "Orange boosts immunity and reduces stress linked to PCOD.",
            "Pear helps balance hormones and improve digestion in PCOD.",
            "Watermelon helps reduce bloating and keeps the body hydrated."
        ],
        "avoid": [
            "Sugary foods increase insulin and worsen PCOD symptoms.",
            "Maida foods disturb hormones and increase PCOD problems.",
            "Fried and fast food increase weight and hormone imbalance in PCOD.",
            "Cool drinks increase sugar levels and worsen PCOD."
        ]
    },

    "PCOS": {
        "message": "Your symptoms suggest patterns linked with hormone and metabolism imbalance. Proper food control and regular activity are very important.",
        "vegetables": [
            "Spinach supports hormone balance and improves iron levels in PCOS.",
            "Broccoli helps remove excess hormones in PCOS.",
            "Carrot supports detoxification and hormone health in PCOS.",
            "Cucumber reduces inflammation and bloating in PCOS.",
            "Pumpkin supports digestion and hormonal balance in PCOS."
        ],
        "fruits": [
            "Apple helps control blood sugar and insulin resistance in PCOS.",
            "Berries reduce inflammation and support hormone balance in PCOS.",
            "Papaya improves digestion and supports regular cycles in PCOS.",
            "Orange reduces stress and boosts immunity in PCOS.",
            "Pear helps control insulin and balance hormones in PCOS.",
            "Watermelon helps hydration and reduces bloating in PCOS."
        ],
        "avoid": [
            "Sugary foods increase insulin resistance in PCOS.",
            "Maida foods increase weight and hormone imbalance in PCOS.",
            "Fried and fast food increase inflammation in PCOS.",
            "Cool drinks raise sugar levels and worsen PCOS symptoms."
        ]
    },

    "DIABETES": {
        "message": "Your symptoms indicate difficulty in blood sugar control. Choosing the right food and staying active can help manage this condition.",
        "vegetables": [
            "Spinach helps control blood sugar and improves overall health.",
            "Broccoli improves insulin sensitivity.",
            "Carrot is safe in moderation.",
            "Cucumber keeps the body hydrated.",
            "Pumpkin supports digestion when eaten moderately."
        ],
        "fruits": [
            "Apple helps control blood sugar.",
            "Berries are low in sugar.",
            "Papaya is safe in moderation.",
            "Orange in small amounts.",
            "Pear helps control blood sugar.",
            "Watermelon in small portions."
        ],
        "avoid": [
            "Sugary foods.",
            "Maida foods.",
            "Fried and fast food.",
            "Cool drinks."
        ]
    },

    "THYROID": {
        "message": "Your symptoms show patterns commonly linked with thyroid imbalance. Maintaining a regular routine and balanced diet can improve energy levels.",
        "vegetables": [
            "Green leafy vegetables support metabolism.",
            "Carrot supports thyroid health.",
            "Pumpkin supports hormone balance.",
            "Beans improve energy levels.",
            "Donot eat Cauli flower and cabbage"
        ],
        "fruits": [
            "Apple supports metabolism.",
            "Berries reduce inflammation.",
            "Orange supports immunity."
        ],
        "avoid": [
            "Excess cabbage and cauliflower.",
            "Soy-based foods in excess.",
            "Junk and fried food.",
            "Sugary foods."
        ]
    },

    "HORMONAL_IMBALANCE": {
        "message": "Based on what you shared, your body shows signs of hormonal imbalance. Food and lifestyle changes can help manage these symptoms naturally.",
        "vegetables": [
            "Spinach supports hormone balance.",
            "Broccoli helps remove excess hormones.",
            "Carrot supports detoxification.",
            "Cucumber reduces bloating.",
            "Pumpkin supports digestion."
        ],
        "fruits": [
            "Apple helps regulate insulin.",
            "Papaya improves digestion.",
            "Berries reduce inflammation.",
            "Pear supports hormone balance.",
            "Orange reduces stress."
        ],
        "avoid": [
            "Processed foods.",
            "Excess sugar.",
            "Junk food."
        ]
    },

    "NORMAL": {
        "message": "Your symptoms do not strongly indicate a specific health issue right now. Maintaining healthy habits can help prevent future problems.",
        "vegetables": [
            "Green leafy vegetables support overall health.",
            "Seasonal vegetables provide essential nutrients."
        ],
        "fruits": [
            "Fresh fruits improve digestion and immunity."
        ],
        "avoid": [
            "Excess sweets.",
            "Junk food."
        ]
    }
}


# ---------------- PREDICTION ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        age = int(data.get("age", 0))
        weight = float(data.get("weight", 60))
        text = data.get("description", "").lower()

        # Symptom Extraction
        weight_gain = 1 if "weight gain" in text else 0
        irregular_periods = 1 if "irregular" in text else 0
        acne = 1 if "acne" in text else 0
        excess_hair = 1 if "hair" in text else 0
        dark_patches = 1 if "dark patch" in text else 0
        thirst = 1 if "thirst" in text else 0
        frequent_urination = 1 if "urine" in text else 0
        fatigue = 1 if "fatigue" in text or "tired" in text else 0
        sugar_cravings = 1 if "sugar" in text else 0
        neck_swelling = 1 if "neck" in text else 0

        stress_level = 2 if "stress" in text else 1
        family_history = 1 if "family history" in text else 0

        # Rule-Based Logic (Same As Yours)
        if age <= 10:
            prediction = "NORMAL"

        elif age > 50:
            if (sugar_cravings and thirst) or frequent_urination:
                prediction = "DIABETES"
            elif neck_swelling and fatigue:
                prediction = "THYROID"
            elif weight_gain and fatigue:
                prediction = "DIABETES"
            else:
                prediction = "NORMAL"

        elif 11 <= age <= 50:
            if irregular_periods:
                if sugar_cravings or weight_gain or dark_patches:
                    prediction = "PCOS"
                elif neck_swelling and fatigue:
                    prediction = "THYROID"
                elif (stress_level == 2 and fatigue) or acne or excess_hair:
                    prediction = "PCOD"
                else:
                    prediction = "HORMONAL_IMBALANCE"

            elif sugar_cravings or thirst or frequent_urination:
                if family_history or weight_gain:
                    prediction = "DIABETES"
                else:
                    prediction = "NORMAL"

            elif weight_gain and fatigue:
                prediction = "THYROID"

            elif stress_level == 2 and fatigue:
                prediction = "HORMONAL_IMBALANCE"

            else:
                prediction = "NORMAL"

        else:
            prediction = "NORMAL"

        foods = FOODS.get(prediction, FOODS["NORMAL"])

        return jsonify({
            "message": foods.get("message", ""),
            "vegetables": foods.get("vegetables", []),
            "fruits": foods.get("fruits", []),
            "avoid": foods.get("avoid", []),
            "water": water_intake(weight),
            "lifestyle": lifestyle_by_age(age),
            "predicted_condition": prediction
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
