import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openai import OpenAI
import pandas as pd


#------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="🧠 MindMate — Mood & Advice",
    page_icon="🧠",
    layout="wide"
)

#------------------------------------------------------------------
# Custom CSS styling
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        body {
            background-color: #fafafa;
            color: #333333;
            font-family: 'Helvetica Neue', sans-serif;
        }

        .main-container {
            max-width: 750px;
            margin-left: auto;
            margin-right: auto;
        }

        .main-title {
            text-align: center;
            font-size: 2.4em;
            font-weight: 700;
            color: #2b2b2b;
            margin-bottom: 0.2em;
        }

        .subtitle {
            text-align: center;
            font-size: 1.05em;
            color: #666;
            margin-bottom: 2em;
        }

        .card {
            background-color: #f7f9fc;
            border-radius: 16px;
            padding: 24px 24px 20px 24px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
            margin-top: 20px;
        }

        .ai-card {
            background-color: #fffef8;
            border-left: 5px solid #888;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.03);
            margin-top: 20px;
        }

        .tip-box {
            background-color: #e8f5e9;
            border-left: 5px solid #66bb6a;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-style: italic;
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

        .section-header {
            font-size: 1.15em;
            font-weight: 600;
            margin-bottom: 0.4em;
            color: #2b2b2b;
        }

        footer {visibility: hidden;}
        header {visibility: visible;}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# Initialize OpenAI client (if API key present)
# ------------------------------------------------------------------
client = None
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------------------------------------------
# Session state init for mood history
# ------------------------------------------------------------------
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# ------------------------------------------------------------------
# Layout: two columns
# left_col = main app, right_col = info / explainer
# ------------------------------------------------------------------
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # -------------------------
    # Title and intro
    # -------------------------
    st.markdown("<h1 class='main-title'>🧠 MindMate — Mood & Advice</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Write a few words about how you feel today. "
        "We'll analyze your mood, show a quick sentiment score, and generate a short supportive suggestion.</p>",
        unsafe_allow_html=True
    )

    # -------------------------
    # User input
    # -------------------------
    st.write("### 1. Check in")
    user_input = st.text_area(
        "How are you feeling today? 💬",
        placeholder="e.g., I'm tired and a bit overwhelmed about tomorrow's exam, but also hopeful.",
        height=120
    )

    analyze_clicked = st.button("✨ Analyze my mood")

    # We'll fill these once analysis runs
    sentiment = None
    color_class = None
    advice = None
    compound = None
    ai_reflection = None

    # -------------------------
    # Sentiment analysis logic
    # -------------------------
    analyzer = SentimentIntensityAnalyzer()

    if analyze_clicked:
        if user_input.strip():
            # Get sentiment scores from VADER
            scores = analyzer.polarity_scores(user_input)
            compound = scores["compound"]

            # Classify sentiment using standard VADER thresholds
            if compound >= 0.05:
                sentiment = "POSITIVE"
                color_class = "positive"
                advice = (
                    "Keep this great energy 🌞 — stay positive and share your good vibes today!"
                )
            elif compound <= -0.05:
                sentiment = "NEGATIVE"
                color_class = "negative"
                advice = (
                    "Take a deep breath 🌿 — it’s okay to slow down and give yourself some grace today."
                )
            else:
                sentiment = "NEUTRAL"
                color_class = "neutral"
                advice = (
                    "A calm day 🕊️ — take it easy and enjoy the little things around you."
                )

            # ------------------------------------------------------
            # AI Coach Reflection (OpenAI LLM)
            # ------------------------------------------------------
            if client is not None:
                system_prompt = (
                    "You are a short-form wellbeing coach for students and young professionals. "
                    "Your job: 1) acknowledge how the user feels, "
                    "2) suggest one small practical next step they can do today, "
                    "3) keep it supportive but not clinical, "
                    "4) if they mention self-harm or wanting to hurt themselves, "
                    "tell them to reach out to someone they trust or local emergency services immediately. "
                    "Answer in 3-4 sentences max. No medical diagnosis."
                )

                user_context = (
                    f"The user wrote this about their mood:\n"
                    f"\"{user_input}\"\n\n"
                    f"Our quick analysis says their overall mood is {sentiment} "
                    f"with a sentiment score of {compound:.2f}.\n\n"
                    "Please respond now with support and a concrete next step."
                )

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_context}
                        ],
                        temperature=0.6,
                        max_tokens=220,
                    )
                    ai_reflection = response.choices[0].message.content.strip()
                except Exception:
                    ai_reflection = (
                        "AI coach is temporarily unavailable. Please try again later."
                    )
            else:
                ai_reflection = (
                    "AI coach is not active because no API key is configured."
                )

            # -------------------------
            # Render results
            # -------------------------
            st.write("### 2. Result")

            # Mood analysis card
            st.markdown(
                f"""
                <div class='card'>
                    <h3>🧭 Mood Analysis</h3>
                    <p><strong>Overall sentiment:</strong>
                        <span class='{color_class}'>{sentiment}</span></p>
                    <p><strong>Sentiment score:</strong> {compound:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Rule-based advice
            st.markdown(
                f"<div class='tip-box'>{advice}</div>",
                unsafe_allow_html=True
            )

            # AI reflection card
            if ai_reflection:
                st.markdown(
                    f"""
                    <div class='ai-card'>
                        <h3>💬 AI coach reflection</h3>
                        <p>{ai_reflection}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------
            # Mood history tracking (session only)
            # -------------------------
            st.write("### 3. Save & track (local session)")
            save_clicked = st.button("📌 Save this check-in to my session")

            if save_clicked:
                st.session_state.mood_history.append(
                    {
                        "text": user_input,
                        "score": round(compound, 3),
                        "label": sentiment,
                    }
                )
                st.success("Saved in this browser session.")

            if st.session_state.mood_history:
                st.write("Your recent check-ins (not stored on any server):")

                # Show table of recent entries
                hist_df = pd.DataFrame(st.session_state.mood_history)
                st.dataframe(
                    hist_df[["label", "score", "text"]].rename(
                        columns={
                            "label": "Mood",
                            "score": "Score",
                            "text": "Note"
                        }
                    ),
                    hide_index=True,
                    use_container_width=True
                )

                # Mini trend chart of sentiment scores
                st.line_chart(hist_df["score"])

        else:
            st.warning("👉 Please write something before clicking *Analyze my mood*.")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Right column: explainer / business framing / privacy
# ------------------------------------------------------------------
with right_col:
    st.markdown("### How it works")
    st.markdown(
        "- You describe how you feel in plain language.\n"
        "- We run a fast sentiment model (VADER) to estimate tone.\n"
        "- We classify it as Positive / Neutral / Negative.\n"
        "- We generate a short tip.\n"
        "- We ask an AI wellbeing coach (OpenAI) for a brief reflection and one concrete next step."
    )

    st.markdown("### Why this matters")
    st.markdown(
        "- For students / employees, this is a lightweight daily check-in instead of long surveys.\n"
        "- Over time, you can spot if you're consistently trending down.\n"
        "- HR / student services could use *aggregated*, anonymous trends as an early signal, "
        "instead of waiting until burnout is obvious."
    )

    st.markdown("### Privacy & ethics")
    st.markdown(
        "- This prototype does **not** save your text to any database.\n"
        "- The mood history shown on the left only lives in your browser session.\n"
        "- The AI coach is supportive, not medical. If someone expresses self-harm intent, "
        "the assistant is instructed to direct them to immediate human help."
    )

    st.markdown("### Tech")
    st.markdown(
        "- Built in Streamlit.\n"
        "- Sentiment via VADER.\n"
        "- AI reflection via OpenAI (gpt-4o-mini).\n"
        "- Deployable as a simple web app."
    )