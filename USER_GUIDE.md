💫 MindMate — Mood & Advice

MindMate is a lightweight demo web app that lets you check in with how you feel, get instant feedback on your mood, and receive a short supportive suggestion. It also lets you track how your mood evolves over time in the same session.

This prototype was developed as part of a group project for the AI for Business course at ESSEC Business School.

🔗 Live demo (no install):
https://your-mindmate.streamlit.app/

⸻

🚀 Quick Start (run locally in under 5 minutes)

1️⃣ Get the project

Clone or download this repository to your machine. You should have something like:

mindmate/
 ├─ mindmate_prototype.py
 ├─ requirements.txt
 ├─ .streamlit/
 │    └─ secrets.toml
 └─ README.md

If the .streamlit folder doesn’t exist yet, you will create it in step 3.

You can also try the hosted version directly in your browser (no setup required):
https://your-mindmate.streamlit.app/

⸻

2️⃣ Make sure Python is installed

You need Python 3.11+ (the app was tested with Python 3.12).

Check your version:

python3 --version

If you don’t have a suitable version, install one from:
https://www.python.org/downloads/

⸻

3️⃣ Install dependencies

From inside the project folder, create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\Activate.ps1     # Windows PowerShell

Then install required packages:

pip install --upgrade pip
pip install -r requirements.txt

Optional (recommended for full functionality):
Create a file .streamlit/secrets.toml in the project root with:

OPENAI_API_KEY = "sk-your-real-openai-api-key"

This enables the “AI coach reflection”.
If you skip this, the app will still run, but it will show a fallback message instead of AI-generated coaching.

⚠️ Do not commit your real API key to GitHub.

⸻

4️⃣ Launch the app

Still in the activated virtual environment, run:

streamlit run mindmate_prototype.py

Streamlit will print a local URL, usually:

http://localhost:8501

Open that link in your browser.

⸻

🧪 How to test it
	1.	Go to the page “📝 Mood Check-in” in the sidebar.
	2.	Type a short sentence describing your current mood, for example:
“I’m stressed about exams and not sleeping well, but I’m still motivated to finish the week.”
	3.	Click “✨ Analyze my mood”.

The app will:
	•	Estimate your overall sentiment (Positive / Neutral / Negative).
	•	Show you a sentiment score (from roughly -1 = very negative to +1 = very positive).
	•	Give you a small practical suggestion for today.
	•	(If an API key is set) Generate a short “AI coach reflection” with supportive language and one concrete next step.

	4.	Click “📌 Save this check-in to my session”.
	5.	Go to the page “📈 My Trend” in the sidebar.

There you’ll see:
	•	A table of all your saved check-ins (time, mood label, score, and what you wrote).
	•	A line chart of your mood score over time.

This is your personal mood timeline for this session.

⸻

🧠 What’s inside

Sentiment analysis (vaderSentiment)

We classify text into Positive / Neutral / Negative and compute a sentiment score.

AI coach reflection (OpenAI API)
	•	A lightweight model (e.g. gpt-4o-mini) generates a short supportive response and suggests one realistic next step.
	•	If you mention self-harm, the assistant is instructed to tell you to reach out to someone you trust or contact local emergency services immediately. It does not try to “handle” crisis situations.

Streamlit UI
	•	Page 1: 📝 Mood Check-in
	•	Page 2: 📈 My Trend
	•	Page 3: ℹ About / Ethics / Use case

Session-only mood history
	•	Your saved moods are stored temporarily in st.session_state and visualized as a trend.
	•	Nothing is written to a database in this prototype.

⸻

🏗 Architecture / Tech Stack
	•	Frontend / App layer: Streamlit
	•	Sentiment model: vaderSentiment (rule-based polarity scoring)
	•	LLM assistant: OpenAI API (short-form reflective coach)
	•	State / storage: Streamlit st.session_state only (in-memory, per session)
	•	Charting: Streamlit’s built-in line chart for sentiment over time

Design choices:
	•	Minimal setup: runs in a single Python file.
	•	Low barrier: plain-language check-in instead of a long questionnaire.
	•	Responsible behavior: the AI coach is instructed to escalate to human help in crisis language instead of “trying to solve it.”

⸻

📝 Notes and Responsible Use
	•	The app stores your mood notes only in memory during your current browser session.
	•	When you refresh or close, the saved trend resets.
	•	We do not persist your text to any backend database in this prototype.
	•	The assistant is not a doctor or a therapist.
	•	It does not diagnose burnout, depression, anxiety, etc.
	•	It only reflects what you wrote and suggests one small next step.
	•	The business / school use case:
	•	Long-term vision: help HR / student services spot negative emotional trends early at the group or cohort level (aggregated and anonymized), instead of waiting until people are already in crisis.
	•	It is not designed to read or monitor private individual messages.
	•	For future production:
	•	Add secure storage and access control.
	•	Implement proper anonymization / aggregation before any manager ever sees trends.
	•	Add escalation policies with human review and clear accountability.
	•	Avoid individual surveillance — focus on early warning signals at the team / cohort level.

⸻

⚖ Disclaimer

MindMate is a prototype built for educational purposes in the AI for Business course at ESSEC Business School.

It is not medical software and is not intended for crisis intervention or clinical diagnosis.
