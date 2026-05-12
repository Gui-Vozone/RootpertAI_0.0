import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
RESERVATIONS_FILE = "reservations.csv"

st.set_page_config(
    page_title="RootpertAI Sala",
    page_icon="🪑",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style='padding-top: 0px; margin-top: -30px;'>
    <h1 style='margin-bottom: 2px; font-size: 42px;'>
        🪑 RootpertAI Sala
    </h1>
    <p style='color: gray; margin: 0; font-size: 16px;'>
        Internal Restaurant Operations Console
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# LOAD RESERVATIONS
# -----------------------------
def load_reservations():

    try:
        return pd.read_csv(
            RESERVATIONS_FILE
        ).fillna("")

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

# -----------------------------
# LIVE STATUS
# -----------------------------
st.success("🟢 RootpertAI Operational")

# -----------------------------
# REFRESH BUTTON
# -----------------------------
if st.button("🔄 Refresh Reservations"):
    st.rerun()

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_reservations()

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Reservations",
        len(df)
    )

with col2:
    st.metric(
        "Last Update",
        datetime.now().strftime("%H:%M:%S")
    )

with col3:
    st.metric(
        "AI Status",
        "Online"
    )

st.markdown("---")

# -----------------------------
# LIVE RESERVATIONS
# -----------------------------
st.title("📋 Live Reservations Feed")

if df.empty:

    st.info("No reservations yet.")

else:

    df = df.iloc[::-1].reset_index(drop=True)

    for i, r in df.iterrows():

        st.markdown("---")

        if i == 0:
            st.markdown("## 🔥 NEWEST RESERVATION")

        st.subheader(f"🪑 Reservation #{i+1}")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write(f"👤 Name: {r.get('name','walk-in')}")

        with c2:
            st.write(f"📅 Date: {r.get('date','-')}")

        with c3:
            st.write(f"⏰ Time: {r.get('time','-')}")

        c4, c5, c6 = st.columns(3)

        with c4:
            st.write(f"👥 Guests: {r.get('people','-')}")

        with c5:
            st.write(f"🧒 Children: {r.get('children','-')}")

        with c6:
            st.write(f"🪟 Table: {r.get('table','-')}")

        st.markdown("### 🍽️ Customer Request")

        st.info(r.get("preorder","-"))

# -----------------------------
# FUTURE EVENTS PLACEHOLDER
# -----------------------------
st.markdown("---")

st.title("🤖 Future AI Event Stream")

placeholder_events = [
    "Suit passed on Table 4",
    "Kitchen requesting waiter assistance",
    "VIP customer arrived",
    "Allergen alert triggered",
    "Wine pairing recommendation generated"
]

for event in placeholder_events:
    st.warning(f"⚡ {event}")
