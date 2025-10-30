import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Page configuration ---
st.set_page_config(page_title="🧠 MindMate — Mood & Advice", page_icon="🧠", layout="centered")

# --- Custom CSS styling ---
st.markdown("""
    <style>
        body {
            background-color: #fafafa;
            color: #333333;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: 700;
            color: #2b2b2b;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1em;
            color: #666;
            margin-bottom: 2em;
        }
        .card {
            background-color: #f7f9fc;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
            margin-top: 20px;
        }
        .positive {
            color: #2E8B57;
            font-weight: bold;
        }
        .negative {
            color: #B22222;
            font-weight: bold;
        }
        .neutral {
            color: #DAA520;
            font-weight: bold;
        }
        .tip-box {
            background-color: #e8f5e9;
            border-left: 5px solid #66bb6a;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-style: italic;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Main title ---
st.markdown("<h1 class='main-title'>🧠 MindMate — Mood & Advice</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Write a few words about how you feel today. The AI will analyze your mood and give you a personalized English tip 🌤️</p>", unsafe_allow_html=True)

# --- Sentiment analysis ---
analyzer = SentimentIntensityAnalyzer()

user_input = st.text_area("How are you feeling today? 💬", placeholder="e.g., I feel tired but grateful today...")

if st.button("✨ Analyze my mood"):
    if user_input.strip():
        scores = analyzer.polarity_scores(user_input)
        compound = scores['compound']

        # Determine mood category
        if compound >= 0.05:
            sentiment = "POSITIVE"
            color_class = "positive"
            advice = "Keep this great energy 🌞 — stay positive and share your good vibes today!"
        elif compound <= -0.05:
            sentiment = "NEGATIVE"
            color_class = "negative"
            advice = "Take a deep breath 🌿 — it’s okay to slow down and give yourself some grace today."
        else:
            sentiment = "NEUTRAL"
            color_class = "neutral"
            advice = "A calm day 🕊️ — take it easy and enjoy the little things around you."

        # --- Display results ---
        st.markdown(f"""
            <div class='card'>
                <h3>🧭 Mood Analysis</h3>
                <p><strong>Overall sentiment:</strong> <span class='{color_class}'>{sentiment}</span></p>
                <p><strong>Sentiment score:</strong> {compound:.2f}</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Display advice ---
        st.markdown(f"<div class='tip-box'>{advice}</div>", unsafe_allow_html=True)
    else:
        st.warning("👉 Please write something before clicking *Analyze my mood*.")
