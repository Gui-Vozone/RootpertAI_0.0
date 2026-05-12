import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from datetime import datetime

# -----------------------------
# SETUP
# -----------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

CSV_PATH = "rootpert_ai_all_menus_fixed copy.csv"
RESERVATIONS_FILE = "reservations.csv"

st.set_page_config(
    page_title="RootpertAI",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style='padding-top: 0px; margin-top: -30px; text-align:center;'>
    <h1 style='margin-bottom: 2px; font-size: 42px;'>🌱 RootpertAI</h1>
    <p style='color: gray; margin: 0; font-size: 16px;'>
        Concierge Inteligente De Raiz
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# KNOWLEDGE BASE
# -----------------------------
@st.cache_data
def load_kb():
    df = pd.read_csv(CSV_PATH).fillna("")
    return df.astype(str).agg(" | ".join, axis=1).tolist()

knowledge_base = load_kb()

# -----------------------------
# RESERVATION STORAGE
# -----------------------------
def load_reservations():
    try:
        return pd.read_csv(RESERVATIONS_FILE).fillna("")
    except:
        return pd.DataFrame(columns=[
            "timestamp",
            "name",
            "date",
            "time",
            "people",
            "children",
            "table",
            "preorder"
        ])

def save_reservation(row):
    df = load_reservations()

    df = pd.concat(
        [df, pd.DataFrame([row])],
        ignore_index=True
    )

    df.to_csv(RESERVATIONS_FILE, index=False)

# -----------------------------
# INTENT CLASSIFIER
# -----------------------------
def classify_intent(text):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": """
Classify the message into ONE word only:

booking
or
question
"""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.output_text.strip().lower()

# -----------------------------
# BOOKING EXTRACTION
# -----------------------------
def extract_booking(text):

    text_l = text.lower()

    time_match = re.search(
        r"(\d{1,2}(:\d{2})?\s*(am|pm)?)",
        text_l
    )

    people_match = re.search(
        r"(\d+)\s*(people|persons|guests)",
        text_l
    )

    return {
        "timestamp": str(datetime.now()),
        "name": "walk-in",
        "date": (
            "tomorrow"
            if "tomorrow" in text_l
            else "today"
        ),
        "time": (
            time_match.group(1)
            if time_match
            else "-"
        ),
        "people": (
            people_match.group(1)
            if people_match
            else "-"
        ),
        "children": (
            "yes"
            if "child" in text_l or "kid" in text_l
            else "no"
        ),
        "table": (
            "window"
            if "window" in text_l
            else "standard"
        ),
        "preorder": text
    }

# -----------------------------
# GPT CHAT
# -----------------------------
def chat_with_gpt(messages, kb):

    context = "\n".join(kb[:20])

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"""
You are RootpertAI,
the luxury concierge assistant of De Raiz restaurant.

You help customers with:
- reservations
- menu questions
- allergens
- wine recommendations
- tourism suggestions
- founder stories
- De Raiz philosophy
- pregnancy-safe dishes

MENU CONTEXT:
{context}

Be elegant, warm and concise.
"""
            },
            *messages
        ]
    )

    return response.output_text

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# CHAT UI
# -----------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input(
    "Ask RootpertAI anything..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    intent = classify_intent(user_input)

    if intent == "booking":

        reservation = extract_booking(user_input)

        save_reservation(reservation)

        reply = f"""
✅ Reservation registered successfully

📅 {reservation['date']}
⏰ {reservation['time']}
👥 {reservation['people']} guests
🪑 {reservation['table']} table

A member of our team will confirm shortly.
"""

    else:

        reply = chat_with_gpt(
            st.session_state.messages,
            knowledge_base
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)
