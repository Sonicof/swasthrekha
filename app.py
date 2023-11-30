from flask import Flask, render_template, request, jsonify
import pickle
import pypyodbc as odbc
import yagmail

try:
    server = 'staladatabase.database.windows.net'
    database = 'staladb'
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:staladatabase.database.windows.net,1433;Database=;Uid=;Pwd=;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    mycon = odbc.connect(connection_string)
    cursor = mycon.cursor()
except:
    print("Unable to establish connection to database server!!")


app = Flask(__name__)

diabetes_model=pickle.load(open("diabetes_model.sav",'rb'))
heart_model=pickle.load(open("heart_disease_model.sav",'rb'))
lung_cancer_model=pickle.load(open("lung_cancer_model.sav",'rb'))

@app.route('/')
def index():
    return render_template('1.html')

@app.route('/predict/heart', methods=['POST'])
def predict_heart():
    data = request.form
    age=int(data.get('age'))
    sex=int(data.get('sex'))
    cp=int(data.get('cp'))
    trestbps=int(data.get('trestbps'))
    chol=int(data.get('chol'))
    fbs=int(data.get('fbs'))
    rest_ecg=int(data.get('rest_ecg'))
    thalach=int(data.get('thalach'))
    exang=int(data.get('exang'))
    oldpeak = int(data.get('oldpeak'))
    slope = int(data.get('slope'))
    ca=int(data.get('ca'))
    thal=int(data.get('thal'))
    email=data.get('email')
    heart_prediction = heart_model.predict(
        [[age, sex, cp, trestbps, chol, fbs, rest_ecg, thalach, exang, oldpeak, slope, ca, thal]])
    st = "INSERT INTO patient (email,disease,output1) VALUES ('{}',{},{})".format(email,0,heart_prediction[0]
        )
    cursor.execute(st);
    mycon.commit()
    if (heart_prediction[0] == 1):
        heart_diagnosis = 'The person has a heart disease'
    else:
        heart_diagnosis = 'The person does not have any heart disease'
    return jsonify({"prediction": heart_diagnosis})

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    data = request.form
    pregnancies=int(data.get('pregnancies'))
    glucose=int(data.get('glucose'))
    bloodpressure=int(data.get('bloodpressure'))
    skinthickness=int(data.get('skinthickness'))
    insulin=int(data.get('insulin'))
    bmi=int(data.get('bmi'))
    dpf=int(data.get('DiabetesPedigreeFunction'))
    age=int(data.get('age'))
    email = data.get('email')
    result = {"prediction": "Diabetes prediction result"}
    diab_prediction = diabetes_model.predict(
        [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf , age]])
    st = "INSERT INTO patient (email,disease,output1) VALUES ('{}',{},{})".format(email, 1, diab_prediction[0]
                                                                                  )
    cursor.execute(st);
    mycon.commit()
    if (diab_prediction[0] == 1):
        diab_diagnosis = 'The person is diabetic'
    else:
        diab_diagnosis = 'The person is not diabetic'
    return jsonify({"prediction": diab_diagnosis})

@app.route('/predict/lung', methods=['POST'])
def predict_lung():
    data = request.form
    age = data.get('age')
    if(age.lower()=='m'):
        age=1
    if(age.lower()=='f'):
        age=0
    smoking = int(data.get('smoking'))
    yellow_fingers = int(data.get('yellow_fingers'))
    anxiety = int(data.get('anxiety'))
    peer_pressure = int(data.get('peer_pressure'))
    Chronic_Disease = int(data.get('Chronic_Diseases'))
    Fatigue = int(data.get('Fatigue'))
    Allergy = int(data.get('Allergy'))
    wheezing = int(data.get('wheezing'))
    Alcohol = int(data.get('Alcohol'))
    Coughing = int(data.get('Coughing'))
    Shortness_of_Breath = int(data.get('Shotness_of_Breath'))
    Swallowing_Difficulty = int(data.get('Swallowing_Difficulty'))
    Chest_pain = int(data.get('Chest_pain'))
    Lung_Cancer=int(data.get("Lung_Cancer"))
    email = data.get('email')

    lung_pred=lung_cancer_model.predict([[age,smoking,yellow_fingers,anxiety,peer_pressure,Chronic_Disease,Fatigue,
                                          Allergy,wheezing,Alcohol,Coughing,Shortness_of_Breath,Swallowing_Difficulty,Chest_pain,Lung_Cancer]])
    st = "INSERT INTO patient (email,disease,output1) VALUES ('{}',{},{})".format(email, 2, lung_pred[0]
                                                                                  )
    cursor.execute(st);
    mycon.commit()
    if (lung_pred[0] == 1):
        lung_pred = 'The person is diabetic'
    else:
        lung_pred = 'The person is not diabetic'
    return jsonify({"prediction": lung_pred})


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
    st = "INSERT INTO feedback (email,comment) VALUES ('{}','{}')".format(email, comment
                                                                                  )
    cursor.execute(st);
    mycon.commit()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
