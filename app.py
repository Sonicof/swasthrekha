from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('1.html')

@app.route('/predict/heart', methods=['POST'])
def predict_heart():
    data = request.form
    age=data.get('age')
    sex=data.get('sex')
    cp=data.get('cp')
    trestbps=data.get('trestbps')
    chol=data.get('chol')
    fbs=data.get('fbs')
    rest_ecg=data.get('rest_ecg')
    thalach=data.get('thalach')
    exang=data.get('exang')
    oldpeak = data.get('oldpeak')
    slope = data.get('slope')
    ca=data.get('ca')
    thal=data.get('thal')

    result = {"prediction": "Heart prediction result"}
    return jsonify(result)

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    data = request.form
    pregnancies=data.get('pregnancies')
    glucose=data.get('glucose')
    bloodpressure=data.get('bloodpressure')
    skinthickness=data.get('skinthickness')
    insulin=data.get('insulin')
    bmi=data.get('bmi')
    dpf=data.get('DiabetesPedigreeFunction')
    age=data.age('age')
    result = {"prediction": "Diabetes prediction result"}
    return jsonify(result)

@app.route('/predict/lung', methods=['POST'])
def predict_lung():
    data = request.form
    age = data.age('age')
    smoking = data.age('smoking')
    yellow_fingers = data.age('yellow_fingers')
    anxiety = data.age('anxiety')
    peer_pressure = data.age('peer_pressure')
    Chronic_Disease = data.age('Chronic_Diseases')
    Fatigue = data.age('Fatigue')
    Allergy = data.age('Allergy')
    wheezing = data.age('wheezing')
    Alcohol = data.age('Alcohol')
    Coughing = data.age('Coughing')
    Shortness_of_Breath = data.age('Shotness_of_Breath')
    Swallowing_Difficulty = data.age('Swallowing_Difficulty')
    Chest_pain = data.age('Chest_pain')
    Lung_Cancer=data.get("Lung_Cancer")



    # Process the data as needed
    # Perform computations based on the lung prediction form data
    result = {"prediction": "Lung prediction result"}
    return jsonify(result)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.form
    rating=data.get('rating')
    name=data.get('name')
    email=data.get('email')
    comment=data.get('comment')
    # Process the feedback data
    # Save the feedback or perform other actions as needed
    result = {"message": "Feedback received successfully"}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
