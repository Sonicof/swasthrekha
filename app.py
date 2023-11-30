from flask import Flask, render_template, request, jsonify
import pickle
import pypyodbc as odbc
import yagmail

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:.net,1433;Database=;Uid=;Pwd=;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
mycon = odbc.connect(connection_string)
cursor = mycon.cursor()
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
        heart_diagnosis = 'The person has a heart disease. A personalised email concerning the patient has been sent'
        receiver = email
        sender = "testingport123@gmail.com"
        password = "tiplnjgnpqwgvuyo"
        yag = yagmail.SMTP(sender, password)
        yag.send(
            to=receiver,
            subject="Your Health Report",
            contents='''I trust this message finds you well. I understand that managing a severe tendency of heart diseases can be challenging, and I want to provide you with a more comprehensive set of advice, including specific recommendations regarding your diet. Please keep in mind that this is general guidance, and it's crucial to consult with your healthcare provider for personalized advice and treatment plans.

1.Consult with a Cardiologist:
    Schedule regular check-ups with a cardiologist to monitor your heart health closely. A specialist can assess your condition, conduct necessary tests, and provide specific recommendations tailored to your situation.

2.Medication Adherence:
    If your doctor has prescribed medication, ensure strict adherence to the prescribed regimen. Medications play a vital role in managing heart conditions and preventing complications.

3.Lifestyle Modifications:

    3.1}Dietary Guidelines:
        3.1.1}Heart-Healthy Foods:
            Include a variety of fruits and vegetables in your diet, aiming for at least five servings per day.
            Choose whole grains over refined grains. Options include brown rice, quinoa, oats, and whole wheat.
            Opt for lean proteins such as skinless poultry, fish, legumes, and tofu.
            Incorporate sources of healthy fats like avocados, nuts, and olive oil.
        3.1.2}Limit Unhealthy Fats:
            Minimize saturated fats found in fatty meats, full-fat dairy products, and processed snacks.
            Avoid trans fats found in some processed and fried foods.
        3.1.3}Watch Sodium Intake:
        3.1.4}Limit your sodium intake by avoiding high-sodium processed foods and using herbs and spices for flavor.
    3.2}Exercise: Engage in regular physical activity as advised by your healthcare provider. Even light exercises like walking can have significant benefits for your heart.
    3.3}Quit Smoking: If you smoke, consider quitting. Smoking is a major risk factor for heart disease and quitting can improve your cardiovascular health.
    3.4}Limit Alcohol Intake: If you consume alcohol, do so in moderation as excessive alcohol can have adverse effects on the heart.
4.Manage Stress:
    Practice stress-reducing techniques such as deep breathing, meditation, yoga, or any other activities that help you relax. Chronic stress can contribute to heart problems, so it's essential to find healthy ways to cope.

5.Regular Monitoring:
    Keep track of your blood pressure, cholesterol levels, and any other parameters recommended by your healthcare provider. This information can help in early detection of potential issues.

6.Emergency Preparedness:
    Be aware of the signs and symptoms of a heart attack or worsening heart condition. Knowing what to do in an emergency can make a significant difference. Ensure that your family members and close contacts are also aware of these signs.

7.Stay Informed:
    Stay informed about your condition. Understand your treatment plan, ask questions during medical appointments, and be an active participant in your healthcare decisions.

Remember, you are not alone in this journey, and seeking support from friends, family, and healthcare professionals is crucial. If you ever experience any concerning symptoms, do not hesitate to seek immediate medical attention.

Take care of yourself, and prioritize your heart health.

Best regards,

Team Swasthekha

''',
        )
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
    bmi=float(data.get('bmi'))
    dpf=float(data.get('DiabetesPedigreeFunction'))
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
        diab_diagnosis = 'The person is diabetic. A personalised email concerning the patient has been sent'
        receiver = email
        sender = ""
        password = ""
        yag = yagmail.SMTP(sender, password)
        yag.send(
            to=receiver,
            subject="Your Health Report",
            contents='''I hope this message finds you well. Managing diabetes requires careful attention to various aspects of your lifestyle, and I want to provide you with comprehensive advice to help you navigate this journey. Please keep in mind that this is general guidance, and it's crucial to consult with your healthcare provider for personalized advice and treatment plans.

1.Consult with a Diabetologist:
    Schedule regular check-ups with a diabetologist to monitor your condition closely. Regular assessments and discussions with a specialist can help tailor your diabetes management plan to your unique needs.

2.Medication and Insulin Management:
    If prescribed, ensure strict adherence to your medication and insulin regimen. Consistency in taking prescribed medications is crucial for effective diabetes management.

3.Lifestyle Modifications:

    3.1}Balanced Diet:
        Prioritize a balanced diet rich in:
            Fiber from fruits, vegetables, and whole grains.
            Lean proteins such as poultry, fish, legumes, and tofu.
            Healthy fats like avocados, nuts, and olive oil.
        Limit intake of processed sugars and refined carbohydrates.
    3.2}Regular Exercise:
        Engage in regular physical activity as recommended by your healthcare provider. Exercise helps manage blood sugar levels and contributes to overall well-being.
    3.3}Quit Smoking:
        If you smoke, consider quitting. Smoking can exacerbate diabetes-related complications.
    3.4}Limit Alcohol Intake:
        Consume alcohol in moderation, if at all, as it can affect blood sugar levels.
    3.5}Regular Monitoring:
        Keep track of blood glucose levels as advised by your healthcare provider.
        Monitor blood pressure and cholesterol levels regularly.
    3.6}Foot Care:
        Inspect your feet daily for any cuts, sores, or signs of infection. Diabetes can affect circulation and nerve function, making foot care crucial.
4.Manage Stress:
    Practice stress management techniques such as mindfulness, deep breathing, or yoga. Chronic stress can impact blood sugar levels, so finding healthy ways to cope is essential.

5.Education and Support:
    Stay informed about diabetes management. Understand the effects of different foods on blood sugar and how to adjust your insulin or medication accordingly.
    Join support groups or connect with others who have diabetes. Sharing experiences and tips can be valuable.

6.Emergency Preparedness:
    Be aware of the signs of hypoglycemia and hyperglycemia. Carry necessary supplies such as glucose tablets and insulin pens, and educate those around you on what to do in case of an emergency.

7.Regular Eye Exams:
    Schedule regular eye exams as diabetes can affect vision. Early detection and treatment of eye-related complications are crucial.

8.Dental Care:
    Maintain good oral hygiene to prevent dental issues, as diabetes can increase the risk of gum disease.

Remember, managing diabetes is a collaborative effort, and your healthcare team is here to support you. If you experience any concerning symptoms or have questions about your diabetes management plan, reach out to your healthcare provider promptly.

Take care of yourself, and prioritize your diabetes management.

Best regards,

Team Swasthrekha''')
    else:
        diab_diagnosis = 'The person is not diabetic'
    return jsonify({"prediction": diab_diagnosis})

@app.route('/predict/lung', methods=['POST'])
def predict_lung():
    data = request.form
    gender= int(data.get('gender'))
    age = int(data.get('age'))
    smoking = int(data.get('smoking'))
    yellow_fingers = int(data.get('yellow_fingers'))
    anxiety = int(data.get('anxiety'))
    peer_pressure = int(data.get('peer_pressure'))
    Chronic_Disease = int(data.get('Chronic_Disease'))
    Fatigue = int(data.get('Fatigue'))
    Allergy = int(data.get('Allergy'))
    wheezing = int(data.get('wheezing'))
    Alcohol = int(data.get('Alcohol'))
    Coughing = int(data.get('Coughing'))
    Shortness_of_Breath = int(data.get('Shortness_of_Breath'))
    Swallowing_Difficulty = int(data.get('Swallowing_Difficulty'))
    Chest_pain = int(data.get('Chest_pain'))
    email = data.get('email')
    lung_pred=lung_cancer_model.predict([[gender,age,smoking,yellow_fingers,anxiety,peer_pressure,Chronic_Disease,Fatigue,
                                          Allergy,wheezing,Alcohol,Coughing,Shortness_of_Breath,Swallowing_Difficulty,Chest_pain]])
    st = "INSERT INTO patient (email,disease,output1) VALUES ('{}',{},{})".format(email, 2, lung_pred[0]
                                                                                  )
    cursor.execute(st);
    mycon.commit()
    if (lung_pred[0] == 1):
        lung_pred = 'The person has chances of suffering from Lung Diseases.A personalised email concerning the patient has been sent'
        receiver = email
        sender = "testingport123@gmail.com"
        password = "tiplnjgnpqwgvuyo"
        yag = yagmail.SMTP(sender, password)
        yag.send(
            to=receiver,
            subject="Your Health Report",
            contents='''I hope this message finds you in good health. Managing lung diseases requires a proactive approach to lifestyle and healthcare. Below is a comprehensive advisory to assist you in navigating the challenges associated with lung conditions. It's essential to consult with your healthcare provider for personalized advice and treatment plans.

1.Consult with a Pulmonologist:
    Schedule regular appointments with a pulmonologist to monitor your lung health. A specialist can provide guidance on managing specific lung conditions and tailor a treatment plan to your needs.

2.Medication Adherence:
    If prescribed, adhere to your medication regimen diligently. Consistency in taking prescribed medications is crucial for effective management of lung diseases.

3.Lifestyle Modifications:
    3.1}Quit Smoking:
        If you smoke, it's imperative to quit. Smoking is a major contributor to lung diseases, and quitting can slow down the progression of the condition.
    3.2}Avoid Environmental Triggers:
        Identify and minimize exposure to environmental factors that may trigger or worsen your symptoms. This could include allergens, pollutants, or irritants.
    3.3}Regular Exercise:
        Engage in regular, moderate exercise to improve lung function and overall well-being. Consult with your healthcare provider to determine suitable exercises.
    3.4}Healthy Diet:
        Consume a nutrient-rich diet with a focus on fruits, vegetables, lean proteins, and whole grains. Adequate nutrition supports your body's ability to fight infections and maintain energy levels.
    3.4}Stay Hydrated:
        Maintain proper hydration, as it can help keep mucus thin and more manageable.
    3.5}Breathing Techniques:
        Learn and practice breathing exercises recommended by your healthcare provider to enhance lung capacity and control breathing.
    3.6}Pulmonary Rehabilitation:
        Consider enrolling in a pulmonary rehabilitation program. These programs offer education, exercise training, and support to enhance your overall lung health.

4.Regular Monitoring:
    Monitor your symptoms regularly and report any changes to your healthcare provider promptly.
    Keep track of peak flow measurements or other indicators recommended by your healthcare team.
    
5.Vaccinations:
    Stay up-to-date on vaccinations, including the annual flu shot and pneumonia vaccine. Vaccinations help prevent infections that can be particularly challenging for individuals with lung diseases.

6.Environmental Precautions:
    Be cautious during outdoor activities, especially in areas with poor air quality.
    Consider using air purifiers at home to minimize exposure to indoor pollutants.
    
7.Support System:
    Build a strong support system that includes friends, family, and healthcare professionals.
    Join support groups or online communities where you can connect with others facing similar challenges.
    
Remember, managing lung diseases is a collaborative effort, and your healthcare team is here to support you. If you experience any concerning symptoms or have questions about your lung health, reach out to your healthcare provider promptly.

Take care of yourself, and prioritize your lung health.

Best regards,

Team Swasthrekha''')
    else:
        lung_pred = 'The person has low chances of suffering from Lung Diseases'
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
    result = {"message": "Feedback received successfully.Your feedback is highly valuable for better development"}
    st = "INSERT INTO feedback (email,comment) VALUES ('{}','{}')".format(email, comment
                                                                                  )
    cursor.execute(st);
    mycon.commit()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
