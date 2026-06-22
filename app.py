# Main Streamlit application for Health Prediction System

from database import add_patient
from database import get_all_patients
from database import delete_patient
from database import search_patient
from database import update_patient
from prediction import predict_health_risk
from ai_service import generate_ai_remark
import re
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
# CUSTOM STYLING
# ==========================================

st.markdown("""
<style>

/* Main App Title */
.main-title {
    font-size: 43px !important;
    font-weight: 700 !important;
    color: #1f2937 !important;
    text-align: center !important;
}

/* Section Headers */
.section-header {
    font-size: 20px;
    font-weight: 600;
    color: #2563eb;
}

/* Sub Headers */
.sub-header {
    font-size: 26px;
    font-weight: 600;
    color: #374151;
}

/* Prediction Report Header */
.report-header {
    font-size: 80px;
    font-weight: bold;
    color: #059669;
}

/* Patient Summary Header */
.summary-header {
    font-size: 28px;
    font-weight: bold;
    color: #7c3aed;
}

/* Tab Font */
.stTabs [data-baseweb="tab"] {
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* Expander Font */
.streamlit-expanderHeader {
    font-size: 22px;
    font-weight: bold;
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

# Validates patient input before prediction

def validate_inputs(
    full_name,
    email,
    dob,
    glucose,
    haemoglobin,
    cholesterol
):

    if not full_name.strip():
        return False, "Full Name is required."

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address."

    if dob > date.today():
        return False, "Date of Birth cannot be a future date."
    
    if glucose <= 0:
        return False, "Glucose must be greater than 0."

    if haemoglobin <= 0:
        return False, "Haemoglobin must be greater than 0."

    if cholesterol <= 0:
        return False, "Cholesterol must be greater than 0."

    if glucose > 1000:
        return False, "Glucose value seems unrealistic."

    if haemoglobin > 30:
        return False, "Haemoglobin value seems unrealistic."

    if cholesterol > 1000:
        return False, "Cholesterol value seems unrealistic."

    return True, ""


st.markdown(
    """
    <div class="main-title">
        🩺 Health Prediction System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; color:gray;'>
    AI-powered patient risk assessment system using Streamlit, SQLite and Gemini AI.
    </p>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(
    ["🩺 Health Prediction", "🗄 Patient Management"]
)

with tab1:

    if not st.session_state.show_results:

        st.markdown(
            '<p class="section-header">Patient Information</p>',
            unsafe_allow_html=True
        )

        full_name = st.text_input("Full Name")

        dob = st.date_input("Date of Birth")

        email = st.text_input("Email Address")

        st.markdown(
            '<p class="section-header">Blood Test Results</p>',
            unsafe_allow_html=True
        )

        glucose = st.number_input(
            "Glucose",
            min_value=0.0
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            min_value=0.0
        )

        cholesterol = st.number_input(
            "Cholesterol",
            min_value=0.0
        )

        submit_button = st.button(
            "Generate Prediction"
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
            '<p class="report-header">📊 Health Prediction Report</p>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="summary-header">Patient Summary</p>',
            unsafe_allow_html=True
        )

        st.write(
            f"**Patient Name:** {st.session_state.patient_name}"
        )

        st.write(
            f"**Email:** {st.session_state.patient_email}"
        )

        st.write(
            f"**DOB:** {st.session_state.patient_dob}"
        )

        st.markdown(
            '<p class="section-header">Risk Prediction</p>',
            unsafe_allow_html=True
        )

        st.warning(
            st.session_state.risk_prediction
        )

        st.subheader("AI Medical Remark")

        st.info(
            st.session_state.ai_remark
        )

        if st.button("💾 Save Record"):

            add_patient(
                st.session_state.patient_name,
                st.session_state.patient_dob,
                st.session_state.patient_email,
                st.session_state.patient_glucose,
                st.session_state.patient_haemoglobin,
                st.session_state.patient_cholesterol,
                st.session_state.ai_remark
            )

            st.success(
                "Patient record saved successfully!"
            )

            if "saved" not in st.session_state:
                st.session_state.saved = False

        if st.button("⬅ Back"):

            st.session_state.show_results = False

            st.rerun()


with tab2:

    st.markdown(
        '<p class="report-header">📋 Saved Patient Records</p>',
        unsafe_allow_html=True
    )

    search_name = st.text_input(
        "🔍 Search Patient By Name"
    )

    if search_name:

        patients = search_patient(
            search_name
        )

    else:

        patients = get_all_patients()

    if patients:

        df = pd.DataFrame(
            patients,
            columns=[
                "ID",
                "Full Name",
                "DOB",
                "Email",
                "Glucose",
                "Haemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Export Records to CSV",
            data=csv,
            file_name="patient_records.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No patient records found."
        )

    st.divider()

    with st.expander("✏ Update Patient Record"):

        patients = get_all_patients()

        if patients:

            update_id = st.selectbox(
                "Select Patient ID",
                [row[0] for row in patients]
            )

            update_name = st.text_input(
                "Updated Full Name"
            )

            update_dob = st.date_input(
                "Updated DOB"
            )

            update_email = st.text_input(
                "Updated Email"
            )

            update_glucose = st.number_input(
                "Updated Glucose",
                min_value=0.0
            )

            update_haemoglobin = st.number_input(
                "Updated Haemoglobin",
                min_value=0.0
            )

            update_cholesterol = st.number_input(
                "Updated Cholesterol",
                min_value=0.0
            )

            update_remarks = st.text_area(
                "Updated Remarks"
            )

            if st.button("✏ Update Record"):

                update_patient(
                    update_id,
                    update_name,
                    str(update_dob),
                    update_email,
                    update_glucose,
                    update_haemoglobin,
                    update_cholesterol,
                    update_remarks
                )

                st.success(
                    "Patient record updated successfully!"
                )

                st.rerun()

    st.divider()

    with st.expander("🗑 Delete Patient"):

        patient_id = st.number_input(
            "Enter Patient ID to Delete",
            min_value=1,
            step=1
        )

        if st.button("🗑 Delete Patient"):

            delete_patient(patient_id)

            st.success(
                "Patient deleted successfully!"
            )

            st.rerun()

