from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    target = 22 * (height_m ** 2)

    if bmi < 18.5:
        status = "Underweight"
        goal = "Gain Weight 💪"
        step = (target - weight) / 30
    elif bmi > 25:
        status = "Overweight"
        goal = "Lose Weight 🔥"
        step = (target - weight) / 30
    else:
        status = "Healthy 😎"
        goal = "Maintain"
        step = 0

    weights = [round(weight + step*i, 1) for i in range(31)]

    workout_plan = [
        "Day 1: Full Body",
        "Day 2: Cardio",
        "Day 3: Legs",
        "Day 4: Rest",
        "Day 5: Chest + Triceps",
        "Day 6: Back + Biceps",
        "Day 7: Rest"
    ] * 4 + ["Day 29: HIIT", "Day 30: Final Test"]

    return render_template(
        "result.html",
        name=name,
        bmi=round(bmi,2),
        status=status,
        goal=goal,
        weights=json.dumps(weights),
        workout=workout_plan
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
