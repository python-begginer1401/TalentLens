
# TalentLens: AI-Powered Player Analysis 🧠⚽

TalentLens is an interactive web application built with Streamlit that leverages AI and computer vision to analyze a soccer player's performance from video footage. It provides real-time metrics like player speed and pass accuracy, and generates a comprehensive scouting report using Google Gemini AI.

## 🚀 Features

- 📹 Upload player video for performance analysis
- 🧍‍♂️ Uses MediaPipe for pose detection and motion tracking
- 📊 Real-time stats on speed and pass accuracy
- 🤖 AI-generated player scouting report via Gemini Pro
- 📝 Downloadable PDF report with visual charts and player profile

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **AI Model**: Gemini Pro via `google.generativeai`
- **Pose Estimation**: MediaPipe
- **Visualization**: Matplotlib & Seaborn
- **PDF Report Generation**: FPDF

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/TalentLens.git
    cd TalentLens
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your Gemini API key**:  
    The app requires a Gemini API key to generate the scouting report. Get it from [Google AI Studio](https://makersuite.google.com/) and paste it in the sidebar when running the app.

## ▶️ Run the App

```bash
streamlit run app.py
```

## 📁 Directory Structure

```
TalentLens/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── TalentLens.png            # App logo used in reports
├── README.md                 # You're reading this!
└── AI_Player_Report.pdf      # Example output report
```

## 📑 Input Form Fields

- **Player Name**  
- **Age** (10-50)  
- **Position** (Forward, Midfielder, Defender, Goalkeeper)  
- **Height** (cm) & Weight (kg)  
- **Team Name**  
- **Match Video** (.mp4, .avi, .mov)

## 🧠 AI Scouting Report Sections

- Player Profile Summary
- Performance Analysis
- Technical Strengths
- Areas for Improvement
- Position-Specific Recommendations
- Overall Potential Assessment

## 📄 Example Output

- Downloadable PDF with:
  - Player info
  - AI-generated analysis
  - Speed and pass accuracy charts

## 🛡️ Disclaimer

- This is an experimental project and should not be used for professional talent scouting without further validation.
- Video must be clear with the player visible in motion for accurate results.

## 📝 License

MIT License

---

Created with 💡 by [Your Name]
