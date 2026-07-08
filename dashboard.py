import streamlit as st
import pandas as pd
import json
import os
import glob

st.set_page_config(page_title="Live Game Pulse", page_icon="🎮", layout="wide")

st.title("🎮 Live Game Pulse")
st.caption("Tracking daily Steam player counts over time")

# Load all daily data files
files = sorted(glob.glob("data/*.json"))

all_rows = []
for file in files:
    with open(file, "r") as f:
        day_data = json.load(f)
        all_rows.extend(day_data)

if not all_rows:
    st.warning("No data yet. Run ingest.py at least once to collect data.")
else:
    df = pd.DataFrame(all_rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Latest snapshot as a summary table
    latest_date = df["date"].max()
    latest = df[df["date"] == latest_date]

    st.subheader(f"Latest snapshot ({latest_date})")
    st.dataframe(
        latest[["game", "player_count"]].sort_values("player_count", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    # Trend chart over time, per game
    st.subheader("Player count trend over time")
    pivot = df.pivot_table(index="date", columns="game", values="player_count", aggfunc="mean")
    st.line_chart(pivot)

    # Let user pick one game to zoom into
    st.subheader("Zoom into a single game")
    game_choice = st.selectbox("Choose a game", sorted(df["game"].unique()))
    game_df = df[df["game"] == game_choice]
    st.line_chart(game_df.set_index("timestamp")["player_count"])