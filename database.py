import sqlite3

DB_PATH = "data/patients.db"

# Creates the patient table if it doesn't already exist
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT NOT NULL,
        glucose REAL NOT NULL,
        haemoglobin REAL NOT NULL,
        cholesterol REAL NOT NULL,
        remarks TEXT
    )
    """)
    conn.commit()
    conn.close()

# Adds a new patient record into the database
def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()    

# Retrieves all patient records from the database
def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Searches patients by name
def search_patient(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients WHERE full_name LIKE ?
    """, (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Updates an existing patient record in the database
def update_patient(patient_id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients
        SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))
    conn.commit()
    conn.close()

# Deletes a patient record using its unique ID
def delete_patient(patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()    

# Check if a patient already exists with the same name and email
def check_duplicate_patient(full_name, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM patients WHERE LOWER(full_name) = LOWER(?) AND LOWER(email) = LOWER(?)",
        (full_name.strip(), email.strip())
    )
    row = cursor.fetchone()
    conn.close()
    return row is not None

if __name__ == "__main__":
    create_table()
    print("Database ready.")