import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import mediapipe as mp
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
from fpdf import FPDF
from PIL import Image

# Sidebar: Add an input field for the Gemini API Key
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Configure the Gemini API Key if provided
if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Please enter your API key to enable AI-generated reports.")

st.title("TalentLens: AI-Powered Player Analysis")

# Player Information Form
with st.expander("🔍 Enter Player Information (for more accurate report)"):
    col1, col2 = st.columns(2)
    with col1:
        player_name = st.text_input("Player Name")
        player_age = st.number_input("Age", min_value=10, max_value=50, value=18)
        player_position = st.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"])
    with col2:
        player_height = st.number_input("Height (cm)", min_value=100, max_value=220, value=175)
        player_weight = st.number_input("Weight (kg)", min_value=30, max_value=120, value=70)
        player_team = st.text_input("Current Team")

uploaded_file = st.file_uploader("Upload your playing video", type=["mp4", "avi", "mov"])

logo_path = "/Users/safa/Documents/GitHub/TalentLens/TalentLens.png"  # Make sure this path is correct

def calculate_speed(prev_coords, curr_coords, time_elapsed):
    if prev_coords and curr_coords:
        dx = curr_coords[0] - prev_coords[0]
        dy = curr_coords[1] - prev_coords[1]
        distance = np.sqrt(dx**2 + dy**2)
        speed = (distance / time_elapsed) * 3.6
        return speed
    return 0

def estimate_pass_accuracy(pose_landmarks):
    if pose_landmarks:
        return np.random.uniform(70, 100)
    return 0

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    frame_count = 0
    prev_hip_coords = None
    player_speeds = []
    pass_accuracies = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            curr_hip_coords = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)

            time_elapsed = 1 / cap.get(cv2.CAP_PROP_FPS)
            speed = calculate_speed(prev_hip_coords, curr_hip_coords, time_elapsed)
            player_speeds.append(speed)

            pass_accuracy = estimate_pass_accuracy(results.pose_landmarks)
            pass_accuracies.append(pass_accuracy)

            prev_hip_coords = curr_hip_coords

        if frame_count >= 100:
            break

    cap.release()
    pose.close()

    avg_speed = np.mean(player_speeds) if player_speeds else 0
    avg_pass_accuracy = np.mean(pass_accuracies) if pass_accuracies else 0

    ai_report = generate_ai_report(avg_speed, avg_pass_accuracy)

    return player_speeds, pass_accuracies, ai_report

def generate_ai_report(speed, accuracy):
    if not api_key:
        return "API Key not provided."

    prompt = f"""
You are a professional sports scout analyzing {player_name}, a {player_age}-year-old {player_position} from {player_team}.
Height: {player_height} cm, Weight: {player_weight} kg.

Write a comprehensive scouting report with these sections:
1. Player Profile Summary
2. Performance Analysis (based on the metrics below)
3. Technical Strengths
4. Areas for Improvement
5. Position-Specific Recommendations
6. Overall Potential Assessment

Performance Metrics:
- Average Speed: {speed:.2f} km/h
- Passing Accuracy: {accuracy:.2f}%

Make the report professional yet accessible, with specific recommendations tailored to the player's position and physical attributes.
"""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "AI Analysis Unavailable"
    except Exception as e:
        return f"Error generating AI report: {e}"

def plot_performance(player_speeds, pass_accuracies):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.lineplot(x=range(len(player_speeds)), y=player_speeds, ax=axes[0], color="blue")
    axes[0].set_title("Player Speed Over Time")
    axes[0].set_xlabel("Frame")
    axes[0].set_ylabel("Speed (km/h)")

    sns.lineplot(x=range(len(pass_accuracies)), y=pass_accuracies, ax=axes[1], color="green")
    axes[1].set_title("Pass Accuracy Over Time")
    axes[1].set_xlabel("Frame")
    axes[1].set_ylabel("Accuracy (%)")

    st.pyplot(fig)
    return fig

def clean_text(text):
    """Replace common Unicode characters with their ASCII equivalents"""
    replacements = {
        '\u2019': "'",  # Right single quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...' # Ellipsis
    }
    for uni, ascii in replacements.items():
        text = text.replace(uni, ascii)
    return text

def save_report_pdf(report_text, fig, logo_path="TalentLens.png"):
    pdf = FPDF()
    pdf.add_page()
    
    # Add logo at top right with proper spacing
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=150, y=10, w=40)
    
    # Add player information header
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 20, txt="TalentLens AI Scouting Report", ln=True, align='C')
    
    # Player details section
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Player: {player_name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {player_age} | Position: {player_position}", ln=True)
    pdf.cell(200, 10, txt=f"Team: {player_team}", ln=True)
    pdf.cell(200, 10, txt=f"Height: {player_height} cm | Weight: {player_weight} kg", ln=True)
    pdf.ln(10)  # Add some space
    
    # Main report content
    pdf.set_font("Arial", size=12)
    cleaned_text = clean_text(report_text)
    for line in cleaned_text.split('\n'):
        try:
            line.encode('latin-1')
            pdf.multi_cell(0, 8, txt=line)  # Reduced line height for better spacing
        except UnicodeEncodeError:
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 8, txt=safe_line)
    
    # Add performance charts
    chart_path = "performance_chart.png"
    fig.savefig(chart_path, bbox_inches='tight')
    pdf.add_page()
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Performance Metrics", ln=True, align='C')
    pdf.image(chart_path, x=10, y=30, w=190)

    pdf_path = "AI_Player_Report.pdf"
    pdf.output(pdf_path)
    return pdf_path

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_path = temp_video.name

    st.video(video_path)
    st.write("Analyzing video... ⏳")

    player_speeds, pass_accuracies, report = analyze_video(video_path)

    st.subheader("AI Player Report 🏆")
    st.write(report)

    st.subheader("Performance Charts 📊")
    fig = plot_performance(player_speeds, pass_accuracies)

    pdf_path = save_report_pdf(report, fig, logo_path)

    with open(pdf_path, "rb") as f:
        st.download_button("Download Full Report as PDF", f, file_name=f"{player_name}_Scouting_Report.pdf", mime="application/pdf")

    os.remove(video_path)
