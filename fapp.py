from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity = request.form['activity']

    height_m = height / 100

    # BMI
    bmi = weight / (height_m ** 2)

    # Category + Goal
    if bmi < 18.5:
        category = "Underweight"
        goal = "Weight Gain 💪"
    elif bmi < 25:
        category = "Normal"
        goal = "Maintain 😎"
    else:
        category = "Overweight"
        goal = "Weight Loss 🔥"

    # Target weight (BMI 22 ideal)
    target_weight = 22 * (height_m ** 2)

    # Time estimation
    if bmi < 18.5:
        weeks = (target_weight - weight) / 0.4
    elif bmi > 25:
        weeks = (weight - target_weight) / 0.5
    else:
        weeks = 0

    days = int(max(0, weeks * 7))

    # BMR
    if gender == 'male':
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    # Activity
    activity_map = {
        'low': 1.2,
        'medium': 1.55,
        'high': 1.9
    }

    tdee = bmr * activity_map[activity]

    # Diet + Workout
    if bmi < 18.5:
        diet = ["Milk + Banana", "Paneer + Roti", "Dry Fruits"]
        workout = ["Light Gym", "Pushups", "Weight Training"]
    elif bmi > 25:
        diet = ["Salad + Fruits", "Grilled Food", "Low Carb Diet"]
        workout = ["Running", "Skipping", "HIIT"]
    else:
        diet = ["Balanced Diet", "Fruits + Veggies"]
        workout = ["Gym + Cardio"]

    return render_template("result.html",
                           name=name,
                           bmi=round(bmi,2),
                           category=category,
                           goal=goal,
                           days=days,
                           tdee=int(tdee),
                           diet=diet,
                           workout=workout)

# Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
