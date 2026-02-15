from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import librosa
import pickle
import os
from werkzeug.utils import secure_filename



import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]




app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- Load Model -----------------
with open("stacking_model.pkl", "rb") as f:
    saved_data = pickle.load(f)

model = saved_data["model"]
le = saved_data["label_encoder"]

# ----------------- Feature Extraction -----------------
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)

# ----------------- Routes -----------------
@app.route('/')
def home():
    return render_template('login44.html')


@app.route('/register2',methods=['POST',"GET"])
def register2():
    return render_template('register44.html')  

import pickle
@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]
    

    name =int_features3[0]

    # Save to a file
    with open("name.pkl", "wb") as f:
        pickle.dump(name, f)

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
              #print(result1)
              #print(gmail1)
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return jsonify({'result':'use proper  gmail and password'})
                  



@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list1)
    if logu1 in gmail_list1:
                      return jsonify({'result':'this gmail is already in use '})  
    else:

                  #return jsonify({'result':'this  gmail is not registered'})
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login44.html')


@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/record')
def record_page():
    return render_template('record.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return "No audio file found", 400

    file = request.files['audio']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Extract features and predict
    features = extract_features(file_path).reshape(1, -1)
    prediction = model.predict(features)
    predicted_label = le.inverse_transform(prediction)[0]

    print("The predicted parkinson is:", predicted_label)

    # -------------------- Disease Information -------------------- #
    disease_info = {
        "parkinson": {
            "disease": "Parkinson’s Disease",
            "symptoms": [
                "Tremors or shaking in hands and limbs",
                "Slowed movement (bradykinesia)",
                "Muscle stiffness",
                "Impaired posture and balance",
                "Speech changes or soft voice"
            ],
            "treatment_allopathy": [
                "Levodopa + Carbidopa therapy",
                "Dopamine agonists (e.g., Pramipexole, Ropinirole)",
                "Deep Brain Stimulation (DBS)",
                "Physical therapy and speech therapy"
            ],
            "ayurvedic": [
                "Ashwagandha and Mucuna Pruriens (Kapikacchu) formulations",
                "Abhyanga (therapeutic oil massage)",
                "Panchakarma detox therapy"
            ],
            "homeopathy": [
                "Gelsemium, Zincum Metallicum, and Agaricus Muscarius",
                "Personalized remedies based on symptoms"
            ],
            "treatment_cost": {
                "India": "₹1.5 to ₹4 lakhs (for surgery & rehabilitation)",
                "USA": "$15,000 to $50,000 (depending on therapy type)"
            },
            "hospitals_india": [
                "NIMHANS, Bengaluru",
                "Apollo Hospitals, Chennai"
            ],
            "hospitals_usa": [
                "Mayo Clinic, Minnesota",
                "Johns Hopkins Hospital, Maryland"
            ],
            "doctors_india": [
                "Dr. Bindu Menon – Neurologist, Apollo Hospitals",
                "Dr. K. Sridhar – Parkinson’s Specialist, Chennai"
            ],
            "doctors_usa": [
                "Dr. Irene Malaty – University of Florida",
                "Dr. Michael Okun – National Parkinson Foundation"
            ]
        },
        "healthy": {
            "disease": "No Parkinson’s Detected",
            "symptoms": ["Healthy voice patterns observed."],
            "treatment_allopathy": ["No treatment needed."],
            "ayurvedic": ["Maintain balanced diet and yoga for wellness."],
            "homeopathy": ["Not required."],
            "treatment_cost": {"India": "₹0", "USA": "$0"},
            "hospitals_india": [],
            "hospitals_usa": [],
            "doctors_india": [],
            "doctors_usa": []
        }
    }

    details = disease_info.get(predicted_label)

    # Pass data to result.html
    return render_template(
        'result.html',
        label=predicted_label,
        disease=details["disease"],
        symptoms=details["symptoms"],
        treatment_allopathy=details["treatment_allopathy"],
        ayurvedic=details["ayurvedic"],
        homeopathy=details["homeopathy"],
        treatment_cost=details["treatment_cost"],
        hospitals_india=details["hospitals_india"],
        hospitals_usa=details["hospitals_usa"],
        doctors_india=details["doctors_india"],
        doctors_usa=details["doctors_usa"]
    )


if __name__ == '__main__':
    app.run(debug=True)
