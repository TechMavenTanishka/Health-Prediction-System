# Main Streamlit application for Health Prediction System

from database import add_patient
from database import get_all_patients
from database import delete_patient
from database import search_patient
from database import update_patient
from database import check_duplicate_patient
from prediction import predict_health_risk
from ai_service import generate_ai_remark
import re
import datetime
import pandas as pd
from datetime import date
import streamlit as st

# Application title
st.set_page_config(
    page_title="Health Prediction System",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# INPUT VALIDATION ENGINE
# ==========================================
def validate_inputs(full_name, email, dob, glucose, haemoglobin, cholesterol):
    if not full_name.strip():
        return False, "Full Name is required."

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address."

    if dob > date.today():
        return False, "Date of Birth cannot be a future date."

    if glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
        return False, "Biomarkers must be greater than 0."

    if glucose > 1000 or haemoglobin > 30 or cholesterol > 1000:
        return False, "Biomarkers value seems unrealistic."

    # --- NEW DUPLICATE CHECK ACCORDING TO TASK 2 ---
    if check_duplicate_patient(full_name, email):
        return False, f"Patient entry for '{full_name}' with email '{email}' already exists in the system database."

    return True, ""


# ==========================================
# CUSTOM STYLING (Professional Dashboard Mix)
# ==========================================
st.markdown("""
<style>
/* Global background tweak and font smoothing */
.stApp {
    background-color: #f8fafc;
}

/* Targeting ALL Native Streamlit Tabs (Active and Inactive) */
button[data-baseweb="tab"] p {
    font-family: 'Inter', Arial, sans-serif !important;
    font-size: 21px !important; /* Adjust size here */
    font-weight: 700 !important;
}

/* Specific color states for active/inactive tabs */
button[data-baseweb="tab"][aria-selected="false"] p {
    color: #64748b !important;
}

button[data-baseweb="tab"][aria-selected="true"] p {
    color: #2563eb !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom-color: #2563eb !important;
}

/* Custom CSS classes for section labels */
.section-lbl {
    font-size: 16px;
    font-weight: 600;
    color: #1e3a8a;
    margin-top: 20px;
    margin-bottom: 10px;
    border-left: 4px solid #2563eb;
    padding-left: 8px;
}
</style>
""", unsafe_allow_html=True)

# Stores prediction results between page refreshes
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "risk_prediction" not in st.session_state:
    st.session_state.risk_prediction = ""
if "ai_remark" not in st.session_state:
    st.session_state.ai_remark = ""
if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

# --- Professional Header Layout ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #1e293b; margin-bottom: 0px;'>🩺 Health Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 15px; margin-top: 5px;'>AI-powered patient risk assessment system utilizing Streamlit, SQLite, and Gemini AI.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# Setup modern clean tabs
tab1, tab2 = st.tabs(["🩺 Health Prediction", "🗄 Patient Management"])

with tab1:

    if not st.session_state.show_results:

        st.markdown(
            '<p class="section-lbl">Patient Information</p>',
            unsafe_allow_html=True
        )

        # Split patient info into modern columns
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
            email = st.text_input("Email Address", placeholder="e.g. john@example.com")
        with p_col2:
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today()
            )
        st.markdown(
            '<p class="section-lbl">Blood Test Metrics</p>',
            unsafe_allow_html=True
        )

        # Place the metrics side-by-side instead of stacking them infinitely
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            glucose = st.number_input(
                "Glucose (mg/dL)",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )
        with m_col2:
            haemoglobin = st.number_input(
                "Haemoglobin (g/dL)",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )
        with m_col3:
            cholesterol = st.number_input(
                "Cholesterol (mg/dL)",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        submit_button = st.button(
            "⚡ Generate AI Prediction", 
            use_container_width=True
        )

        if submit_button:
            is_valid, message = validate_inputs(
                full_name,
                email,
                dob,
                glucose,
                haemoglobin,
                cholesterol
            )

            if not is_valid:
                st.error(message)
            else:
                risk_prediction = predict_health_risk(
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                ai_remark = generate_ai_remark(
                    risk_prediction
                )

                st.session_state.risk_prediction = risk_prediction
                st.session_state.ai_remark = ai_remark
                st.session_state.patient_name = full_name
                st.session_state.patient_dob = str(dob)
                st.session_state.patient_email = email
                st.session_state.patient_glucose = glucose
                st.session_state.patient_haemoglobin = haemoglobin
                st.session_state.patient_cholesterol = cholesterol
                st.session_state.show_results = True
                st.rerun()

    if st.session_state.show_results:

        st.markdown(
            '<p class="section-lbl">📊 Health Prediction Report</p>',
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("<h3 style='color: #1e3a8a; margin-top: 0;'>Patient Summary</h3>", unsafe_allow_html=True)
            
            sum_col1, sum_col2, sum_col3 = st.columns(3)
            with sum_col1:
                st.markdown(f"**Patient Name:**<br>{st.session_state.patient_name}", unsafe_allow_html=True)
            with sum_col2:
                st.markdown(f"**Email:**<br>{st.session_state.patient_email}", unsafe_allow_html=True)
            with sum_col3:
                st.markdown(f"**DOB:**<br>{st.session_state.patient_dob}", unsafe_allow_html=True)
            
            st.divider()

            st.markdown("<h4 style='color: #1e3a8a;'>Risk Assessment</h4>", unsafe_allow_html=True)
            st.warning(f"⚠️ {st.session_state.risk_prediction}")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("<h4 style='color: #2563eb;'>🤖 Gemini AI Medical Insight</h4>", unsafe_allow_html=True)
            st.info(st.session_state.ai_remark)

        st.markdown("<br>", unsafe_allow_html=True)

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("💾 Save Patient Record to Database", use_container_width=True):
                add_patient(
                    st.session_state.patient_name,
                    st.session_state.patient_dob,
                    st.session_state.patient_email,
                    st.session_state.patient_glucose,
                    st.session_state.patient_haemoglobin,
                    st.session_state.patient_cholesterol,
                    st.session_state.ai_remark
                )
                st.success("Patient record saved successfully!")
                if "saved" not in st.session_state:
                    st.session_state.saved = True

        with btn_col2:
            if st.button("⬅ Back to Form", use_container_width=True):
                st.session_state.show_results = False
                st.rerun()


with tab2:

    st.markdown(
        '<p class="section-lbl">📋 Saved Patient Records</p>',
        unsafe_allow_html=True
    )

    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        search_name = st.text_input("Search Database", placeholder="🔍 Enter patient name to search...")
    with s_col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)

    if search_name:
        patients = search_patient(search_name)
    else:
        patients = get_all_patients()

    if patients:
        df = pd.DataFrame(
            patients,
            columns=["ID", "Full Name", "DOB", "Email", "Glucose", "Haemoglobin", "Cholesterol", "Remarks"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Export Patient Database (CSV)",
            data=csv,
            file_name="patient_records.csv",
            mime="text/csv",
            use_container_width=False
        )
    else:
        st.info("No patient records found inside the SQLite database.")

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown('<p class="section-lbl">🛠️ Database Administrative Actions</p>', unsafe_allow_html=True)

    adm_col1, adm_col2 = st.columns(2)

    with adm_col1:
        with st.container(border=True):
            st.markdown("<h4 style='color: #1e3a8a; margin-top:0;'>✏️ Update Record</h4>", unsafe_allow_html=True)
            patients_list = get_all_patients()
            
            if patients_list:
                update_id = st.selectbox(
                    "Target Patient ID",
                    [row[0] for row in patients_list],
                    key="up_id"
                )
                
                update_name = st.text_input("Updated Full Name", key="up_name")
                
                u_sub1, u_sub2 = st.columns(2)
                with u_sub1:
                    update_dob = st.date_input("Updated DOB", max_value=date.today(), key="up_dob")
                    update_glucose = st.number_input("Glucose", min_value=0.0, key="up_glu")
                with u_sub2:
                    update_email = st.text_input("Updated Email", key="up_em")
                    update_haemoglobin = st.number_input("Haemoglobin", min_value=0.0, key="up_hem")
                
                update_cholesterol = st.number_input("Updated Cholesterol", min_value=0.0, key="up_chol")
                update_remarks = st.text_area("Updated Clinical Remarks", key="up_rem")

                if st.button("🔄 Commit Changes", use_container_width=True):
                    update_patient(
                        update_id, update_name, str(update_dob), update_email,
                        update_glucose, update_haemoglobin, update_cholesterol, update_remarks
                    )
                    st.success("Patient file updated successfully!")
                    st.rerun()
            else:
                st.caption("No records available to modify.")

    with adm_col2:
        with st.container(border=True):
            st.markdown("<h4 style='color: #dc2626; margin-top:0;'>🗑️ Delete Record</h4>", unsafe_allow_html=True)
            
            if patients_list:
                delete_id = st.selectbox(
                    "Target Patient ID to Remove",
                    [row[0] for row in patients_list],
                    key="del_id"
                )
                st.markdown("<p style='color: #64748b; font-size: 14px;'>Warning: Deleting a patient profile removes all laboratory entries permanently from SQLite database structure.</p>", unsafe_allow_html=True)
                
                if st.button("🗑️ Permanently Delete Record", use_container_width=True):
                    delete_patient(delete_id)
                    st.success("Record cleared successfully.")
                    st.rerun()
            else:
                st.caption("No records available to drop.")