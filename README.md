# 🧠 MindMate — Mood & Advice

MindMate is an AI-powered emotional check-in assistant.

You write a short note about how you feel right now.  
The app:
1. Analyzes your mood (positive / neutral / negative) using a sentiment model.
2. Gives you a small practical suggestion for today.
3. Generates a short supportive “AI coach reflection” using an OpenAI model.
4. Lets you save check-ins and view your personal mood trend over time.

This project was developed as part of the course **AI for Business** at **ESSEC Business School**.

Live demo: https://your-mindmate.streamlit.app/

---

## 🔍 Why this exists

Most wellbeing tracking tools are either:
- long, effortful surveys, or
- reactive (“we only intervene once someone is already burned out”).

MindMate is designed to be:
- a 20-second daily check-in,
- a single realistic next step (not generic “do self-care”),
- and a simple “am I getting better or worse this week?” view.

In a business / school context, the value is not to monitor individuals.  
The value is to detect stress trends early at group level, so support teams can reach out before it becomes a crisis.

---

## 🧭 App Overview

The app runs as a Streamlit web app with a sidebar. You can switch between three pages:

### 1. 📝 Mood Check-in
This is the main interaction.

- You type how you feel in your own words. Example:  
  “I'm exhausted about exams and not sleeping well, but I’m still motivated to finish this week.”
- Click **"✨ Analyze my mood"**.

The app will show you:
- **Sentiment label**  
  POSITIVE / NEUTRAL / NEGATIVE
- **Sentiment score**  
  A numeric polarity score from roughly -1 (very negative) to +1 (very positive)
- **A practical suggestion**  
  One concrete thing you can actually try today (take a 5-minute reset, pick one realistic task, etc.)
- **AI coach reflection**  
  A short, supportive response generated using an OpenAI model. It reflects what you wrote, acknowledges it, and proposes one small next action.

Then you’ll see a button:
**"📌 Save this check-in to my session"**

Clicking this stores the result (timestamp, your note, sentiment label, and score) to your local session so you can later visualize it.

Important:
- This does NOT create an account or write to a backend database in this prototype.  
  It’s local to your current browser session.

---

### 2. 📈 My Trend
This page is your personal mini-dashboard.

It shows:
- A table of your saved check-ins:
  - Time
  - Sentiment label
  - Sentiment score
  - Your note
- A line chart of your sentiment score over time.

How to read it:
- A higher score = more positive emotional tone.
- A lower score = more stressed / negative / overwhelmed.
- You can visually see stretches like “I sounded bad three days in a row” or “I bounced back after the exam.”

Again: this data lives only in your session state. When the session ends, it’s gone.

---

### 3. ℹ About / Ethics / Use case
This page explains:
- **Why this matters in business / school settings**  
  Aggregated mood trends (not personal text) could be used by HR or student services as an early warning indicator of burnout risk instead of waiting until people crash.
- **Ethical boundaries**  
  - We do NOT claim to provide mental health treatment.
  - We do NOT diagnose.
  - The AI coach is instructed that if someone expresses self-harm or wanting to hurt themselves, it should tell them to contact a trusted person or emergency services immediately. It does not attempt to “handle it alone.”
  - In this prototype, we do not store user text on any server.
- **Tech stack**  
  - Streamlit for UI
  - VADER sentiment model for mood scoring
  - OpenAI model (`gpt-4o-mini` style) for the “AI coach reflection”
  - pandas + Streamlit charting for your personal mood timeline

This page exists to show that the concept includes privacy and escalation thinking, not just “cool AI output.”

---

## 🧠 How it works (technical detail)

### Sentiment analysis
We use `vaderSentiment` (lexicon & rule-based sentiment analysis).  
It returns a `compound` score, roughly in [-1, 1].  
We classify:
- `compound ≥ 0.05` → POSITIVE  
- `compound ≤ -0.05` → NEGATIVE  
- otherwise → NEUTRAL

We surface both the label and the numeric score to the user.

### AI coach reflection
We call a small OpenAI chat model to generate a short response in natural language.  
We send:
- what the user wrote,
- the predicted sentiment,
- the sentiment score.

The prompt tells the model to:
- acknowledge how the user feels,
- suggest one concrete, realistic next step for *today*,
- avoid clinical diagnosis language,
- and, if self-harm is mentioned, tell the user to seek immediate human help (trusted person, emergency services).

If no OpenAI API key is configured, the app falls back to a safe message like:
“AI coach is not active because no API key is configured.”

### Trend tracking / analytics
When you save a check-in:
- we append an entry to `st.session_state.mood_history`, containing:
  - timestamp
  - your raw note
  - sentiment label
  - sentiment score

The “📈 My Trend” page then:
- displays this history in a table, and
- plots the sentiment score over time as a line chart.

Nothing is persisted to disk or uploaded to a remote database in this prototype.

---

## 🚀 How to run locally (for development)

Even though the app is deployed at  
https://your-mindmate.streamlit.app/  
you can also run it locally if you want to develop or present offline.

### 1. Get the code
Clone or download the repository to a local folder, for example:
```bash
/Users/yourname/Documents/mindmate