💫 MindMate — Mood & Advice

MindMate is a lightweight demo web app that lets you check in with how you feel, get instant feedback on your mood, and receive a short supportive suggestion. It also lets you track how your mood evolves over time in the same session.

This prototype was developed as part of a group project for the AI for Business course at ESSEC Business School.

---

🚀 Quick Start (under 5 minutes)

1️⃣ Get the project

Clone or download the project folder to your computer, for example:

mindmate/
 ├─ mindmate_prototype.py
 ├─ requirements.txt
 ├─ .streamlit/
 │    └─ secrets.toml
 └─ README.md

(If the `.streamlit` folder doesn’t exist yet, you will create it in step 3.)

You can also try the hosted version directly in your browser at:
https://your-mindmate.streamlit.app/

---

2️⃣ Make sure Python is installed

You need Python 3.11+ (the app was tested with Python 3.12).

Check your version by running:

python3 --version

If you don’t have a suitable version, install one from:
https://www.python.org/downloads/

---

3️⃣ Install dependencies

Open your terminal, move into the project folder, and create/activate a virtual environment:

cd /path/to/mindmate
python3 -m venv .venv
source .venv/bin/activate        # On macOS / Linux
# .venv\Scripts\Activate.ps1     # On Windows PowerShell

Then install all required packages:

pip install --upgrade pip
pip install -r requirements.txt

Optional (recommended for full functionality):  
Create a file `.streamlit/secrets.toml` in the project root with the following content:

OPENAI_API_KEY = "sk-your-real-openai-api-key"

This enables the “AI coach reflection”.  
If you skip this, the app will still run, but it will show a fallback message instead of AI-generated coaching.

---

4️⃣ Launch the app

From the same (activated) environment, run:

streamlit run mindmate_prototype.py

Streamlit will print a local URL, usually:

http://localhost:8501

Open that in your browser.

---

🧪 How to test it

1. Go to the page “📝 Mood Check-in” in the sidebar.
2. Type a short sentence describing your current mood, for example:

   "I'm stressed about exams and not sleeping well, but I'm still motivated to finish the week."

3. Click “✨ Analyze my mood”.

The app will:
- Estimate your overall sentiment (Positive / Neutral / Negative).
- Show you a sentiment score (from roughly -1 = very negative to +1 = very positive).
- Give you a small practical suggestion for today.
- (If an API key is set) Generate a short “AI coach reflection” with supportive language and one concrete next step.

4. Click “📌 Save this check-in to my session”.

5. Go to the page “📈 My Trend” in the sidebar.

There you’ll see:
- A table of all your saved check-ins (time, mood label, score, and what you wrote).
- A line chart of your mood score over time.

This is your personal mood timeline for this session.

---

🧠 What’s inside

- Sentiment analysis using `vaderSentiment`
  - We classify text into Positive / Neutral / Negative and compute a sentiment score.

- AI coach reflection using OpenAI
  - A small model (e.g. `gpt-4o-mini`) generates a short supportive response and suggests one realistic next step.
  - If you mention self-harm, the assistant is instructed to tell you to reach out to someone you trust or contact local emergency services immediately. It does not try to “handle” crisis situations.

- Streamlit UI
  - Page 1: 📝 Mood Check-in
  - Page 2: 📈 My Trend
  - Page 3: ℹ About / Ethics / Use case

- Session-only mood history
  - Your saved moods are stored temporarily in `st.session_state` and visualized as a trend.
  - Nothing is written to a database in this prototype.

---

📝 Notes

- The app stores your mood notes only in memory during your current browser session.
  - When you refresh or close, the saved trend resets.
  - We do not persist your text to a server in this prototype.

- The assistant is not a doctor or therapist.
  - It does not diagnose burnout, depression, anxiety, etc.
  - It only reflects what you wrote and suggests one small next step.

- Business / school use case:
  - The long-term vision is to help HR / student services spot negative emotional trends early at the group level (aggregated and anonymized), instead of waiting until people are already in crisis.

- For future production:
  - Add secure storage and access control.
  - Implement proper anonymization and aggregation.
  - Add escalation policies with human review.
  - Avoid individual surveillance — focus on early warning signals at cohort/team level.