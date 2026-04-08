<<<<<<< HEAD
# Autism Detection System

A cutting-edge, machine-learning-powered web application built with **Django**, **TensorFlow/Keras**, and an intuitive **Glassmorphic UI**. Designed to assess and predict behavioral traits indicative of Autism Spectrum Disorder (ASD). The system provides multi-modal assessment utilizing both tabular developmental forms and convolutional neural network (CNN) evaluations of facial imaging and video samples.

---

## 🌟 Key Features

1. **Dual-Model Prediction Engine**
   - **Form-Based Assessment:** Evaluates behavioral questionnaires and demographic factors (age, gender, family history of ASD, jaundice) with an interconnected statistical model mapping against `dataset2.csv`.
   - **Computer Vision CNN:** Leverages a pre-trained Keras model (`autism_detection_model.h5`) utilizing OpenCV (`cv2`) to extract facial and behavioral cues from images (`.jpg`, `.png`) and processes videos (`.mp4`, `.avi`) iteratively by sampling frame-by-frame.

2. **Premium Interface (Glassmorphism & Theming)**
   - Custom, fully responsive, glassmorphic UI styled with centralized `global.css`.
   - Native toggleable **Dark/Light Mode** across the entire application using CSS variables.
   - Elegant animations, glow gradients, and cohesive frontend styling.

3. **Secure Role-Based Flow**
   - True session-backed login tracking distinguishing between generic users and systemic administrators. 
   - Interactive user testing embedded with *Mock Credentials* integrated directly into the portals to simulate authentication immediately without a persistent DB config.

4. **Exclusive Admin Dashboard**
   - Dedicated `/admin_dashboard` interface featuring telemetry, system statistics, and direct avenues to manage or upload training and prediction media files seamlessly.

5. **Integrated Streamlit Visualization**
   - Extended analytical support using Streamlit logic encapsulated under `streamlit_app/` for plotting raw data statistics transparently.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.12, Django 3.1.4, MySQLdb
- **Machine Learning & AI:** TensorFlow, Keras, OpenCV, Pandas, Scikit-learn, Numpy
- **Frontend architecture:** HTML5, modern vanilla CSS3 (Glassmorphism), JavaScript (ES6)

---

## 🚀 Setup & Installation Steps

### Prerequisites
1. **Python 3.12+** installed and added to `PATH`.
2. A **MySQL Server** instance actively running locally.

### 1. Database Configuration
The application depends on a MySQL database specifically mapped to store file references and legacy user signups.
- Create a MySQL Database named: `autism`
- Configure a local database user with credentials matching:
  - **User:** `root`
  - **Password:** `root123`
- *Tables Required:* Ensure your database encompasses `Users` and `vfiles` schemas prior to executing full manual user registrations or media uploads. 

### 2. Prepare the Application Environment
A dedicated `run_project.bat` script encapsulates the complete startup orchestration for Windows users. Wait for the initial launch to unpack and install the core dependencies via `requirements.txt`.

Simply double-click the script, or run it through the terminal:
```bash
.\run_project.bat
```

The script will automatically attempt to:
* Activate a sandboxed virtual environment.
* Upgrade standard `pip` modules.
* Safely install necessary machine learning, MySQL, and web modules from `requirements.txt`.
* Boot up the core Django web server natively at `http://127.0.0.1:8000/`.

### 3. Usage & Access (Mock Credentials)
Navigate to the central URL: **http://127.0.0.1:8000/**
If you are bootstrapping the project for testing interactions or skipping manual DB table creation tasks, the system accepts baked-in demo credentials immediately:

- **Basic Diagnostic User:** `user` | Password: `user123`
- **Dashboard Admin:** `admin` | Password: `admin123` *(Login explicitly through the Admin portal)*

---

*This application is classified strictly as an academic informational screening resource. Final formal diagnosis workflows necessitate strict evaluations curated exclusively by authorized healthcare physicians.*
=======
# capstone-project-autism_detection
>>>>>>> 0c2ec7a3a55c07a1c1bb915c0f4f0be94fd5207d
