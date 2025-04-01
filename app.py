
import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai  # For Gemini API (Replace if using DeepSeek)

# Configure Gemini API Key
genai.configure(api_key="AIzaSyAiSJp0W7afRsvzQXKtYEA8kB26PeMzidc")

# Streamlit App Title
st.title("TalentLens: AI-Powered Player Analysis")

# Upload Video
uploaded_file = st.file_uploader("Upload your playing video", type=["mp4", "avi", "mov"])

def analyze_video(video_path):
    """Processes video and extracts key performance metrics."""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    player_speeds = []
    pass_accuracies = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Simulated Analysis (Replace with AI Vision Model)
        player_speeds.append(np.random.uniform(5, 30))  # Fake speed data
        pass_accuracies.append(np.random.uniform(50, 100))  # Fake pass accuracy

        if frame_count >= 100:  # Analyze only first 100 frames
            break

    cap.release()

    # Generate Summary Stats
    avg_speed = np.mean(player_speeds)
    avg_pass_accuracy = np.mean(pass_accuracies)

    # Send Data to Gemini AI for AI Insights
    ai_report = generate_ai_report(avg_speed, avg_pass_accuracy)

    return player_speeds, pass_accuracies, ai_report

def generate_ai_report(speed, accuracy):
    """Uses Gemini AI to generate a detailed player report."""
    prompt = f"""
    Analyze the following player performance data and provide a professional scouting report:
    - Average Speed: {speed:.2f} km/h
    - Passing Accuracy: {accuracy:.2f}%
    Give insights on strengths, weaknesses, and areas of improvement.
    """

    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "AI Analysis Unavailable"

def plot_performance(player_speeds, pass_accuracies):
    """Creates performance charts for speed and pass accuracy."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Speed Chart
    sns.lineplot(x=range(len(player_speeds)), y=player_speeds, ax=axes[0], color="blue")
    axes[0].set_title("Player Speed Over Time")
    axes[0].set_xlabel("Frame")
    axes[0].set_ylabel("Speed (km/h)")

    # Pass Accuracy Chart
    sns.lineplot(x=range(len(pass_accuracies)), y=pass_accuracies, ax=axes[1], color="green")
    axes[1].set_title("Pass Accuracy Over Time")
    axes[1].set_xlabel("Frame")
    axes[1].set_ylabel("Accuracy (%)")

    st.pyplot(fig)

# Process Uploaded Video
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_path = temp_video.name

    st.video(video_path)  # Show uploaded video
    st.write("Analyzing video... ⏳")

    player_speeds, pass_accuracies, report = analyze_video(video_path)

    st.subheader("AI Player Report 🏆")
    st.write(report)

    st.subheader("Performance Charts 📊")
    plot_performance(player_speeds, pass_accuracies)

    # Clean up temporary file
    os.remove(video_path)
