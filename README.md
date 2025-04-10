# 🎯 TalentLens: AI-Powered Player Analysis

Welcome to **TalentLens**, an AI-powered tool designed to analyze soccer player performance from videos. Whether you're a coach, scout, or a player, TalentLens helps evaluate player speed, pass accuracy, and generates a detailed scouting report using Google's Gemini AI.

---

## 🚀 Features

- 🎥 Upload your playing video and let the AI do the rest  
- 📊 Analyze average speed and passing accuracy  
- 🤖 Generate detailed scouting reports using Gemini  
- 📈 Visualize performance with charts  
- 📄 Export your report as a downloadable PDF

---

## 🛠️ Tech Stack

- **Streamlit** for the user interface  
- **OpenCV** + **MediaPipe** for video and pose analysis  
- **Gemini (Generative AI)** for natural language scouting reports  
- **Matplotlib & Seaborn** for performance charts  
- **FPDF** for report generation  
- **Pillow** and **NumPy** for image and number handling

---

## 🔑 Gemini API Key Setup

To use the AI-generated report feature, you'll need a [Google Gemini API key](https://makersuite.google.com/).  
Once you have it:

1. Launch the app
2. Enter your API key in the sidebar  
3. Start uploading and analyzing videos!

---

## 💻 How to Use

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/TalentLens.git
cd TalentLens
```

2. **Install the required packages**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
streamlit run app.py
```

4. **Use the Web Interface**
   - Input player details
   - Upload a short soccer video (e.g., 5-10 seconds)
   - Review the generated AI report and visual performance charts
   - Download a clean PDF version of the report

---

## 📂 Sample Output

- 📑 AI Scouting Report
- 📊 Player speed & pass accuracy chart
- ✅ Downloadable PDF with all data and charts

---

## 🧠 How It Works

- MediaPipe identifies hip joint movement to estimate **speed**
- A mock AI logic estimates **pass accuracy**
- Google's Gemini model writes a **personalized scouting report**
- You can **export** everything into a structured and branded PDF

---

## 📎 Notes

- Video length: Keep it short (~5-10 seconds) for faster processing
- Current version supports **basic performance metrics**; future versions may include:
  - Dribble analysis
  - Defense stats
  - Team synergy insights

---

## 📃 License

This project is open-source. Feel free to fork and adapt it for your needs (mention us if you do!).

---

## 🙌 Author

Built with 💡 by [Your Name]  
If you enjoy this tool, consider giving it a ⭐ on GitHub!
