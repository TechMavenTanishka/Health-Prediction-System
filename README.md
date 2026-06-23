# 🩺 AI-Powered Health Prediction System

A professional, full-stack health risk assessment dashboard built to satisfy the **Junior AI/ML Developer Assessment Task** requirements. The system integrates a Python web backend, localized persistent storage, input validation constraints, and the official Google Gemini AI interface layer.

---

## 📌 Task Requirement Checklist Mapping

| Requirement Specification | Implementation Status | Core Module File Location |
| :--- | :---: | :--- |
| **1. CRUD Operations** (Create, Read, Update, Delete) |  Complete | `database.py` / `app.py` |
| **2. User Interface** (Simple, clean, multi-column layout) |  Complete | `app.py` (Streamlit Tabs) |
| **3. Data Validation** (Email regex, future date traps, non-zero values) |  Complete | `app.py` (`validate_inputs`) |
| **4. Persistent Storage** (SQLite Database Infrastructure Engine) |  Complete | `database.py` (`patient.db`) |
| **5. External AI/ML Health API** (Gemini Contextual Inference) |  Complete | `ai_service.py` (`gemini-2.5-flash-lite`) |

---

## 🚀 Features

- **Risk Assessment:** Categorizes patient health risk based on glucose, haemoglobin, and cholesterol test metrics.
- **AI Medical Insights:** Generates context-aware, 2-3 sentence professional clinical recommendations using Gemini AI, with automated fail-safes for high API traffic drops.
- **Robust CRUD Operations:** Full administrative capabilities to add, look up, update, and drop complete patient profiles dynamically.
- **Data Portability:** Clean export features parsing entire tables or filtered queries into a structured CSV file format instantly.
- **Modern User Interface:** Customized CSS overrides providing fluid multi-column entry fields, clean layout hierarchy cards, and prominent status banners.

---

## 🛠️ Tech Stack

- **Frontend Framework:** Streamlit
- **Language Layer:** Python 3.12+
- **Database Engine:** SQLite (Persistent Storage)
- **Data Processing:** Pandas
- **AI Engine Platform:** Google GenAI Python SDK 
- **Environment Handling:** Python-dotenv

---

## 📸 Screenshots

### 1. Home Dashboard & Form Input
![Home](screenshots/home.png)

### 2. Live Health Prediction & AI Insight Report
![Report](screenshots/report.png)

### 3. Patient Record Database Management Dashboard
![Management](screenshots/management.png)

---

## 💻 Installation & Local Deployment

Follow these quick setup steps to get the environment initialized locally:

### 1. Clone the Workspace
```bash
git clone [https://github.com/TechMavenTanishka/Health-Prediction-System.git](https://github.com/TechMavenTanishka/Health-Prediction-System.git)
cd Health-Prediction-System