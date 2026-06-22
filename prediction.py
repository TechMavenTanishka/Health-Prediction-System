# Generates health risk predictions based on blood test values

def predict_health_risk(glucose, haemoglobin, cholesterol):

    risks = []

    if glucose > 140:
        risks.append("Diabetes Risk")

    if cholesterol > 240:
        risks.append("Heart Disease Risk")

    if haemoglobin < 12:
        risks.append("Anemia Risk")

    if not risks:
        return "No Significant Risk Detected"

    return ", ".join(risks)

