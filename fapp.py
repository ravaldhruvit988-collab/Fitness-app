from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get input
    weight = float(request.form['weight'])  # kg
    height = float(request.form['height'])  # cm
    age = int(request.form['age'])
    gender = request.form['gender']
    activity = request.form['activity']

    # BMI calculation
    bmi = weight / ((height/100)**2)

    # Weight category
    if bmi < 18.5:
        category = "Underweight"
        diet_advice = "Eat more proteins, whole grains, nuts, and healthy fats."
    elif 18.5 <= bmi < 25:
        category = "Normal"
        diet_advice = "Maintain your diet with balanced nutrition, vegetables, fruits, and moderate exercise."
    elif 25 <= bmi < 30:
        category = "Overweight"
        diet_advice = "Reduce sugar and fat intake, eat more vegetables, lean proteins, and exercise regularly."
    else:
        category = "Obese"
        diet_advice = "Consult a nutritionist, reduce calories, avoid junk food, and exercise carefully."

    # BMR calculation (Mifflin-St Jeor Equation)
    if gender == 'male':
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    # TDEE calculation
    activity_multiplier = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very': 1.9
    }
    tdee = bmr * activity_multiplier[activity]

    return render_template("result.html",
                           bmi=round(bmi,2),
                           category=category,
                           diet_advice=diet_advice,
                           bmr=round(bmr,2),
                           tdee=round(tdee,2))

if __name__ == '__main__':
    app.run(debug=True)