import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openai import OpenAI
import pandas as pd
from datetime import datetime

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="🧠 MindMate — Mood & Advice",
    page_icon="🧠",
    layout="centered",
)

# ------------------------------------------------------------------
# Custom CSS styling
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        body {
            font-family: 'Helvetica Neue', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .main-container {
            max-width: 680px;
            margin-left: auto;
            margin-right: auto;
        }

        .main-title {
            text-align: center;
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }

        .subtitle {
            text-align: center;
            font-size: 1.0em;
            color: #9e9e9e;
            margin-bottom: 2em;
        }

        .section-header {
            font-size: 1.15em;
            font-weight: 600;
            margin-bottom: 0.4em;
        }

        /* Result cards */
        .card {
            background-color: #eef0f4;
            color: #2b2b2b;
            border-radius: 16px;
            padding: 20px 20px 16px 20px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.4);
            margin-top: 20px;
            font-size: 0.95rem;
            line-height: 1.5rem;
        }
        .card h3 {
            margin-top: 0;
            margin-bottom: 0.6rem;
            font-size: 1.05rem;
            font-weight: 600;
            color: #2b2b2b;
        }

        .tip-box {
            background-color: #dff3df;
            border-left: 5px solid #4caf50;
            color: #2b2b2b;
            padding: 15px 16px;
            border-radius: 8px;
            margin-top: 16px;
            font-style: italic;
            font-size: 0.95rem;
            line-height: 1.5rem;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.4);
        }

        .ai-card {
            background-color: #fffef2;
            border-left: 5px solid #999;
            color: #2b2b2b;
            border-radius: 12px;
            padding: 20px 20px 16px 20px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.4);
            margin-top: 20px;
            font-size: 0.95rem;
            line-height: 1.5rem;
        }
        .ai-card h3 {
            margin-top: 0;
            margin-bottom: 0.6rem;
            font-size: 1.05rem;
            font-weight: 600;
            color: #2b2b2b;
        }

        .positive { color: #2E8B57; font-weight: 600; }
        .negative { color: #B22222; font-weight: 600; }
        .neutral  { color: #DAA520; font-weight: 600; }

        /* About page cards */
        .about-card {
            background-color: #2a2b30;
            border-radius: 16px;
            padding: 20px 24px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.07);
            font-size: 0.9rem;
            line-height: 1.4rem;
            color: #d0d0d0;
            margin-bottom: 1.5rem;
        }

        .about-card h3 {
            color: #ffffff;
            font-size: 1rem;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 0.6rem;
        }

        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# Sidebar navigation with 3 pages
# ------------------------------------------------------------------
mode = st.sidebar.radio(
    "Navigation",
    ["📝 Mood Check-in", "📈 My Trend", "ℹ About / Ethics / Use case"],
    index=0,
)

# ------------------------------------------------------------------
# OpenAI client
# ------------------------------------------------------------------
client = None
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------------------------------------------
# Session state for persistent info across reruns
# ------------------------------------------------------------------
# Last analysis result from "Analyze my mood"
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None
    # last_analysis will be a dict:
    # {
    #   "text": str,
    #   "compound": float,
    #   "sentiment": "POSITIVE"/"NEGATIVE"/"NEUTRAL",
    #   "color_class": "positive"/"negative"/"neutral",
    #   "advice": str,
    #   "ai_reflection": str,
    # }

# All saved historical entries
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
    # mood_history is a list of dicts like:
    # {
    #   "time": datetime,
    #   "text": str,
    #   "score": float,
    #   "label": str,
    # }


# ==================================================================
# PAGE 1: Mood Check-in
# ==================================================================
if mode == "📝 Mood Check-in":
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Title + subtitle
    st.markdown("<h1 class='main-title'>🧠 MindMate — Mood & Advice</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Write a few words about how you feel today. "
        "We'll analyze your mood, show a quick sentiment score, and generate "
        "a short supportive suggestion and next step.</p>",
        unsafe_allow_html=True
    )

    # 1. Check-in input
    st.markdown("### 1. Check in", unsafe_allow_html=True)
    user_input = st.text_area(
        "How are you feeling today? 💬",
        placeholder="e.g., I'm stressed about deadlines and not sleeping great, but I'm trying to stay focused.",
        height=120,
        key="current_input"  # keep text across reruns
    )

    analyze_clicked = st.button("✨ Analyze my mood", type="primary")

    analyzer = SentimentIntensityAnalyzer()

    # When user clicks "Analyze my mood"
    if analyze_clicked:
        if user_input.strip():
            scores = analyzer.polarity_scores(user_input)
            compound = scores["compound"]

            # classify mood
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

            # AI reflection from OpenAI
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
                            {"role": "user", "content": user_context},
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
                ai_reflection = "AI coach is not active because no API key is configured."

            # Store analysis in session_state for persistence on rerun
            st.session_state.last_analysis = {
                "text": user_input,
                "compound": float(round(compound, 3)),
                "sentiment": sentiment,
                "color_class": color_class,
                "advice": advice,
                "ai_reflection": ai_reflection,
            }
        else:
            st.warning("👉 Please write something before clicking *Analyze my mood*.")

    # Show the latest result if it exists
    if st.session_state.last_analysis is not None:
        la = st.session_state.last_analysis

        st.markdown("### 2. Result", unsafe_allow_html=True)

        # Mood analysis card
        st.markdown(
            f"""
            <div class='card'>
                <h3>🧭 Mood Analysis</h3>
                <p><strong>Overall sentiment:</strong>
                    <span class='{la["color_class"]}'>{la["sentiment"]}</span></p>
                <p><strong>Sentiment score:</strong> {la["compound"]:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tip box
        st.markdown(
            f"<div class='tip-box'>{la['advice']}</div>",
            unsafe_allow_html=True,
        )

        # AI coach reflection card
        if la["ai_reflection"]:
            st.markdown(
                f"""
                <div class='ai-card'>
                    <h3>💬 AI coach reflection</h3>
                    <p>{la['ai_reflection']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 3. Save button (persists this check-in into mood_history)
        st.markdown("### 3. Save this check-in", unsafe_allow_html=True)
        save_clicked = st.button("📌 Save this check-in to my session")

        if save_clicked:
            st.session_state.mood_history.append(
                {
                    "time": datetime.now(),              # store as real datetime
                    "text": la["text"],
                    "score": la["compound"],
                    "label": la["sentiment"],
                }
            )
            st.success("Saved in this browser session. View it under '📈 My Trend'.")

    st.markdown("</div>", unsafe_allow_html=True)


# ==================================================================
# PAGE 2: My Trend (history + chart)
# ==================================================================
elif mode == "📈 My Trend":
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>📈 My Mood Trend</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>These are the moods you've chosen to save. "
        "This only lives in your browser session — nothing is uploaded.</p>",
        unsafe_allow_html=True,
    )

    if not st.session_state.mood_history:
        st.info("No saved check-ins yet. Go to '📝 Mood Check-in', analyze, then press 'Save this check-in'.")
    else:
        # Build dataframe
        hist_df = pd.DataFrame(st.session_state.mood_history).copy()

        # ensure datetime
        hist_df["time"] = pd.to_datetime(hist_df["time"])
        hist_df = hist_df.sort_values("time")

        # nice readable timestamps for table
        hist_df_display = hist_df.copy()
        hist_df_display["time"] = hist_df_display["time"].dt.strftime("%Y-%m-%d %H:%M")

        st.markdown("### Your saved check-ins", unsafe_allow_html=True)
        st.dataframe(
            hist_df_display[["time", "label", "score", "text"]].rename(
                columns={
                    "time": "Time",
                    "label": "Mood",
                    "score": "Score",
                    "text": "Note",
                }
            ),
            hide_index=True,
            use_container_width=True,
        )

        # plot sentiment score over time
        plot_df = hist_df[["time", "score"]].set_index("time")

        st.markdown("### Trend of your mood score over time", unsafe_allow_html=True)
        st.caption("Higher score = more positive mood. Lower score = more negative tone.")
        st.line_chart(plot_df)

    st.markdown("</div>", unsafe_allow_html=True)


# ==================================================================
# PAGE 3: About / Ethics / Use case
# ==================================================================
else:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>ℹ About MindMate</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>What the tool is for, why it's relevant in a business / university context, and what we don't do.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h3>What this tool does</h3>
            <p>- You type how you feel in plain language.</p>
            <p>- We run a lightweight sentiment model (VADER) to estimate tone.</p>
            <p>- We classify it as Positive / Neutral / Negative and show you a mood score.</p>
            <p>- We generate a short practical suggestion (e.g. “take a 5 minute break”, “review one topic for your exam”).</p>
            <p>- You can save snapshots of how you feel. Your history stays only in your current browser session.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h3>Why this matters (business / school)</h3>
            <p>- For students or employees: this is a 30-second daily check-in instead of a 20-question wellbeing survey.</p>
            <p>- Over time, you can spot: “I’ve been in a bad mood 4 days in a row.”</p>
            <p>- For HR / student services: in theory you could analyze <em>aggregated, anonymized</em> trends to catch early burnout risk instead of reacting too late.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h3>Ethics & limits</h3>
            <p>- We do <strong>not</strong> store your text on any server in this prototype.</p>
            <p>- The AI coach is supportive, not medical. If someone expresses self-harm, the model is instructed to say: talk to a trusted person or contact local emergency services immediately.</p>
            <p>- This is not a diagnosis tool and not a replacement for therapy. It is an early signal + nudge system.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">
            <h3>Tech stack</h3>
            <p>- Streamlit frontend.</p>
            <p>- VADER sentiment analysis for classification.</p>
            <p>- OpenAI (gpt-4o-mini) for a short, contextual “AI coach reflection”.</p>
            <p>- Session-only mood log + separate dashboard in “📈 My Trend”.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)