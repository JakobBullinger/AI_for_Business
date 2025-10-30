💫 MindMate — Mood & Advice

MindMate is a lightweight demo web app that analyzes your mood based on a short daily note and gives a quick personalized tip in English.
It was developed as part of a group project for the AI & Innovation in Hospitality course.

🚀 Quick Start (under 5 minutes)
1️⃣ Unzip or clone the project

Download and extract the folder mindmate_app on your computer (e.g., on your Desktop).

2️⃣ Make sure Python is installed

You need Python 3.10+.
If not installed, download it from python.org/downloads
.

3️⃣ Install dependencies

Open your terminal, go to the folder, and run:

cd ~/Desktop/mindmate_app
pip install -r requirements.txt


💡 The first run may take 1–2 minutes while downloading small NLP models from Hugging Face.

4️⃣ Launch the app

Run the following command:

streamlit run app.py


Then open the link shown in the terminal (usually http://localhost:8501).

🧪 How to test it

Type a short sentence describing your current mood, for example:

“I feel calm but tired today.”

Click Analyze, and the app will:

Estimate your overall sentiment (positive / negative / neutral)

Detect key emotions (happy, calm, tired, anxious, etc.)

Suggest a short self-care tip in English

🧠 What’s inside

Sentiment analysis using vaderSentiment

Emotion detection using facebook/bart-large-mnli

Streamlit for the interactive interface

📝 Notes

The app runs locally (no data is sent online).

It’s a demo prototype, built to illustrate emotion recognition in a hospitality context.

For production: add model caching, improve error handling, and enhance privacy measures.
