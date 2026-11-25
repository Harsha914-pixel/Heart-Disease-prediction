import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')

def generate_pdf_report(prediction_id, patient_name, age, gender, input_data_json, prediction_status, predicted_class, probability):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    pdf_filename = f"heart_disease_report_{prediction_id}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=15,
        alignment=1 # Center
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=10,
        spaceAfter=8,
        borderPadding=4
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        spaceAfter=6
    )
    
    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#94a3b8'),
        leading=12,
        alignment=1
    )
    
    story = []
    
    # Header Accent bar
    d_title = Paragraph("HEART DISEASE PREDICTION REPORT", title_style)
    story.append(d_title)
    
    meta_info = [
        [Paragraph("<b>Patient Name:</b>", body_style), Paragraph(patient_name, body_style),
         Paragraph("<b>Date:</b>", body_style), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), body_style)],
        [Paragraph("<b>Age:</b>", body_style), Paragraph(str(age), body_style),
         Paragraph("<b>Gender:</b>", body_style), Paragraph(gender, body_style)]
    ]
    t_meta = Table(meta_info, colWidths=[100, 160, 80, 180])
    t_meta.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))
    
    # Prediction Section
    story.append(Paragraph("Assessment Results", section_heading))
    
    status_color = "#dc2626" if "Detected" in prediction_status else "#16a34a"
    status_html = f"<font color='{status_color}'><b>{prediction_status}</b></font>"
    
    prob_str = f"{probability*100:.1f}%" if probability is not None else "N/A"
    
    prediction_info = [
        [Paragraph("<b>Overall Assessment Status:</b>", body_style), Paragraph(status_html, body_style)],
        [Paragraph("<b>Severity Class / Category:</b>", body_style), Paragraph(f"Class {predicted_class} (Scale 0-4)", body_style)],
        [Paragraph("<b>Model Prediction Probability:</b>", body_style), Paragraph(prob_str, body_style)]
    ]
    t_pred = Table(prediction_info, colWidths=[200, 320])
    t_pred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_pred)
    story.append(Spacer(1, 15))
    
    # Medical Parameters Section
    story.append(Paragraph("Patient Medical Parameters", section_heading))
    
    input_data = json.loads(input_data_json)
    
    def get_sex_str(v): return "Male" if int(v) == 1 else "Female"
    def get_fbs_str(v): return "True (> 120 mg/dl)" if int(v) == 1 else "False"
    def get_exang_str(v): return "Yes" if int(v) == 1 else "No"
    
    cp_labels = {1: "Typical Angina", 2: "Atypical Angina", 3: "Non-anginal Pain", 4: "Asymptomatic"}
    restecg_labels = {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"}
    slope_labels = {1: "Upsloping", 2: "Flat", 3: "Downsloping"}
    thal_labels = {3: "Normal", 6: "Fixed Defect", 7: "Reversable Defect"}
    
    param_rows = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style),
         Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style)],
        [Paragraph("Resting Blood Pressure", body_style), Paragraph(f"{input_data.get('trestbps')} mm Hg", body_style),
         Paragraph("Serum Cholesterol", body_style), Paragraph(f"{input_data.get('chol')} mg/dl", body_style)],
        [Paragraph("Chest Pain Type", body_style), Paragraph(cp_labels.get(int(input_data.get('cp')), str(input_data.get('cp'))), body_style),
         Paragraph("Fasting Blood Sugar", body_style), Paragraph(get_fbs_str(input_data.get('fbs')), body_style)],
        [Paragraph("Resting ECG Result", body_style), Paragraph(restecg_labels.get(int(input_data.get('restecg')), str(input_data.get('restecg'))), body_style),
         Paragraph("Max Heart Rate (bpm)", body_style), Paragraph(str(input_data.get('thalach')), body_style)],
        [Paragraph("Exercise Induced Angina", body_style), Paragraph(get_exang_str(input_data.get('exang')), body_style),
         Paragraph("ST Depression (oldpeak)", body_style), Paragraph(str(input_data.get('oldpeak')), body_style)],
        [Paragraph("ST Slope", body_style), Paragraph(slope_labels.get(int(input_data.get('slope')), str(input_data.get('slope'))), body_style),
         Paragraph("Major Vessels (ca)", body_style), Paragraph(str(input_data.get('ca')), body_style)],
        [Paragraph("Thalassemia (thal)", body_style), Paragraph(thal_labels.get(int(input_data.get('thal')), str(input_data.get('thal'))), body_style),
         Paragraph("", body_style), Paragraph("", body_style)]
    ]
    
    t_params = Table(param_rows, colWidths=[150, 110, 150, 110])
    t_params.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ]))
    story.append(t_params)
    story.append(Spacer(1, 30))
    
    # Disclaimer
    story.append(Paragraph("<b>Medical Disclaimer:</b> This report contains a machine learning-based prediction generated from historical clinical data. It is for screening/educational purposes only and does NOT constitute a clinical diagnosis, professional medical advice, or treatment plan. Please consult a qualified healthcare provider for clinical evaluation.", disclaimer_style))
    
    doc.build(story)
    return pdf_filename
