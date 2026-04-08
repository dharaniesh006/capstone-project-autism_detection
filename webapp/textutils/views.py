# I have created this file - tusharpangare ©

import pandas as pd   
from django.shortcuts import render, redirect,HttpResponse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import csv
import MySQLdb
import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
import subprocess
def index(request):
    return render(request, 'index.html')

def registration(request):
    db = MySQLdb.connect("localhost", "root", "root123", "autism")
    c1 = db.cursor()
    if request.method == "POST":
        # support both older field names and the newer template names
        name = request.POST.get('name') or request.POST.get('username') or ''
        mailid = request.POST.get('mailid') or request.POST.get('email') or ''
        mobileno = request.POST.get('mobileno') or ''
        uid = request.POST.get('uid') or request.POST.get('username') or mailid
        pwd = request.POST.get('pwd') or request.POST.get('password1') or request.POST.get('password') or ''
        pwd2 = request.POST.get('password2')

        # basic validation
        if not name or not mailid or not pwd:
            return render(request, 'registration.html', {"msg": "Please fill in name, email and password."})
        if pwd2 is not None and pwd != pwd2:
            return render(request, 'registration.html', {"msg": "Passwords do not match."})

        try:
            # use parameterized query to avoid SQL injection and to match column order
            c1.execute(
                "INSERT INTO Users (name, mailid, mobileno, userid, password) VALUES (%s, %s, %s, %s, %s)",
                (name, mailid, mobileno, uid, pwd)
            )
            db.commit()
        except Exception as e:
            # return the error to the template for easier debugging (could be logged instead)
            return render(request, 'registration.html', {"msg": f"Error registering user: {e}"})

        return render(request, 'registration.html', {"msg": "User Information Registered"})

    return render(request, 'registration.html')

def login(request):
    if request.method == "POST":
        uid = request.POST.get("uid") or request.POST.get("username", "")
        pwd = request.POST.get("pwd") or request.POST.get("password", "")
        
        # Mock User Credentials
        if uid == "user" and pwd == "user123":
            request.session['role'] = 'user'
            return redirect("analyze")
            
        try:
            db = MySQLdb.connect("localhost", "root", "root123", "autism")
            c1 = db.cursor()
            c1.execute("select * from Users where userid='%s' and password='%s'" % (uid, pwd))
            if c1.rowcount >= 1:
                request.session['role'] = 'user'
                return redirect("analyze")
        except Exception as e:
            pass # Handle gracefully if DB is not active during mock check
            
        return render(request, 'index.html', {"msg": "Your Login attempt was not successful. Please try again!!"})
    return render(request, 'index.html')

def login1(request):
    if request.method == "POST":
        uid = request.POST.get("uid") or request.POST.get("username", "")
        pwd = request.POST.get("pwd") or request.POST.get("password", "")
        
        # Mock Admin Credentials
        if (uid == "admin" and pwd == "admin123") or (uid == "admin" and pwd == "admin"):
            request.session['role'] = 'admin'
            return redirect("admin_dashboard")
            
        return render(request, 'login.html', {"msg": "Your Login attempt was not successful. Please try again!!"})
    return render(request, 'login.html')

def logout_user(request):
    request.session.flush()
    return redirect("index")

def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('index')
    return render(request, 'admin_dashboard.html')

def analyze(request):
    if request.session.get('role') not in ['user', 'admin']:
        return redirect('index')
    if request.method=="POST":
        q1 = int(request.POST["t1"])
        q2 = int(request.POST["t2"])
        q3 = int(request.POST["t3"])
        q4 = int(request.POST["t4"])
        q5 = int(request.POST["t5"])
        q6 = int(request.POST["t6"])
        q7 = int(request.POST["t7"])
        q8 = int(request.POST["t8"])
        q9 = int(request.POST["t9"])
        q10 = int(request.POST["t10"])
        age = int(request.POST["t11"])
        gender = request.POST["t13"]
        jaundice = request.POST["t14"]
        asd_family = request.POST["t15"]

        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'dataset2.csv')
        emotion = pd.read_csv(db_path)
        #attr=["fft_749_b","label"]

        value="None"
        with open(db_path) as file_obj:
            reader_obj = csv.reader(file_obj)
            i=1
            for row in reader_obj:
                if i == 1:
                    i = i + 1
                    continue
                data1 = int(row[1])
                data2 = int(row[2])
                data3 = int(row[3])
                data4 = int(row[4])
                data5 = int(row[5])
                data6 = int(row[6])
                data7 = int(row[7])
                data8 = int(row[8])
                data9 = int(row[9])
                data10 = int(row[10])
                data_age = int(row[11])
                data_gender = row[13]
                data_jaundice = row[15]
                data_asd_family = row[16]

                #print(data)
                if data1 == q1 and data2 == q2 and data3 == q3 and data4 == q4 and data5 == q5 and data6 == q6 and data7 == q7 and data8 == q8 and data9 == q9 and data10 == q10 and data_age == age and data_gender == gender and data_jaundice == jaundice and data_asd_family == asd_family:
                    value = row[18]
                    break
        return render(request, 'autism.html', {"autism":value})
    return render(request, 'autism.html', {})

def find(request):
    if request.session.get('role') not in ['user', 'admin']:
        return redirect('index')
    return render(request, "find_artism.html")

def analyze1(request):
    if request.session.get('role') != 'admin':
        return redirect('index')
    return render(request, "analyze1.html")

def analyze4(request):
    if request.session.get('role') not in ['user', 'admin']:
        return redirect('index')
    db = MySQLdb.connect("localhost", "root", "root123", "autism")
    c1 = db.cursor()
    c1.execute("select * from vfiles")
    row = c1.fetchall()
    return render(request, 'analyze4.html', {'data': row})

def analyze2(request):
   if request.session.get('role') != 'admin':
       return redirect('index')
   f = request.FILES['fi1']
   des=request.POST["descr"]
   full_path = os.getcwd()+"\\static\\"+"uploads\\"
   print(full_path + "\n")
   with open(full_path + f.name, 'wb+') as destination:
       for chunk in f.chunks():
           destination.write(chunk)

   full_path1 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "webapp", "static", "uploads", f.name)
   print(full_path1)
   db = MySQLdb.connect("localhost", "root", "root123", "autism")
   c1 = db.cursor()
   c1.execute("insert into vfiles(vpath,vdescr)values('%s','%s')" % (f.name, des))
   db.commit()
   return render(request, "analyze2.html")

def analyze3(request):
   if request.session.get('role') != 'admin':
       return redirect('index')
   try:
       db = MySQLdb.connect("localhost", "root", "root123", "autism")
       c1 = db.cursor()
       c1.execute("select * from vfiles")
       row=c1.fetchall()
   except Exception as e:
       print(e)
       row = []
   return render(request, 'analyze3.html', {'data': row})


def output(request):
    if request.session.get('role') not in ['user', 'admin']:
        return redirect('index')
    if request.method != 'POST':
        return redirect('find')
    
    if 'fi' not in request.FILES:
        return render(request, 'find_artism.html', {'error': 'Please select a file'})
    
    try:
        # Get the uploaded file
        uploaded_file = request.FILES['fi']
        
        # Save the uploaded file
        upload_dir = os.path.join('static', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Determine if it's an image or video based on extension
        is_video = uploaded_file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
        
        # Load the model
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_training', 'models', 'autism_detection_model.h5')
        model = load_model(model_path)
        
        prediction = 0
        
        if is_video:
            cap = cv2.VideoCapture(file_path)
            frames_count = 0
            total_prediction = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every 10th frame to speed up and avoid redundancy
                if frames_count % 10 == 0:
                    # Preprocess the frame
                    frame_resized = cv2.resize(frame, (224, 224))
                    frame_array = np.array(frame_resized) / 255.0
                    frame_array = np.expand_dims(frame_array, axis=0)
                    
                    # Predict
                    pred = model.predict(frame_array)[0][0]
                    total_prediction += pred
                
                frames_count += 1
            
            cap.release()
            
            # Average prediction across processed frames
            # Note: We processed frames_count / 10 frames roughly
            processed_frames = frames_count // 10
            if processed_frames > 0:
                prediction = total_prediction / processed_frames
            else:
                raise ValueError("Could not process any frames from the video")
                
        else:
            # Image processing
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError("Could not read the image file")
                
            # Resize to match model's expected input
            img_resized = cv2.resize(img, (224, 224))
            
            # Normalize the image
            img_array = np.array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            prediction = model.predict(img_array)[0][0]
        
        # Calculate confidence percentage
        # Assuming model output > 0.5 is Autism, <= 0.5 is Normal
        # Adjust logic based on your specific model training labels if needed
        if prediction < 0.5:
             confidence = (1 - prediction) * 100
             result_label = "Autism Behavior Detected"
        else:
             confidence = prediction * 100
             result_label = "Normal Behavior"

        
        # Get current date for the analysis
        from datetime import datetime
        analysis_date = datetime.now().strftime("%B %d, %Y")
        
        # Prepare the uploaded file URL for the template
        uploaded_file_url = os.path.join('/static/uploads', uploaded_file.name)
        
        # Render results
        return render(request, 'detection_result.html', {
            'prediction': float(prediction),
            'confidence': round(confidence, 1),
            'result_label': result_label,
            'analysis_date': analysis_date,
            'uploaded_file_url': uploaded_file_url,
            'is_video': is_video
        })
        
    except Exception as e:
        print(f"Error: {e}") # Debug print
        return render(request, 'find_artism.html', {'error': f'Error processing file: {str(e)}'})