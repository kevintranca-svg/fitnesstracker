import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

password = st.sidebar.text_input("Entry Code", type="password")
if password != "kevin":
    st.stop()

st.set_page_config(page_title="Personal Fitness Hub", layout="wide")

# Connect to Google Sheets
# Note: You'll need to add your Sheet URL to .streamlit/secrets.toml or Streamlit Cloud
url = "https://docs.google.com/spreadsheets/d/11lsWHou6WfRDelu87xEgI5mCdiherYTxkEvC5_sG4SM/"
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏃‍♂️ My Fitness Dashboard")

# Navigation
menu = ["Log Calories", "Log Workout", "Weight Tracker"]
choice = st.sidebar.selectbox("Menu", menu)

# --- 1. CALORIE LOGGING ---
if choice == "Log Calories":
    st.subheader("Add Daily Intake")
    
    with st.form("calorie_form"):
        date = st.date_input("Date", datetime.now())
        meal = st.text_input("Meal/Food Item")
        cals = st.number_input("Calories (kcal)", min_value=0, step=10)
        protein = st.number_input("Protein (g)", min_value=0)
        
        if st.form_submit_button("Save to Sheets"):
            # Create a small dataframe for the new row
            new_data = pd.DataFrame([{"Date": str(date), "Item": meal, "Calories": cals, "Protein": protein}])
            
            # Fetch existing data and append
            existing_data = conn.read(spreadsheet=url, worksheet="Calories")
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Write back to Google Sheets
            conn.update(spreadsheet=url, worksheet="Calories", data=updated_df)
            st.success("Meal Logged!")

# --- 2. WEIGHT TRACKER ---
elif choice == "Weight Tracker":
    st.subheader("Weight Progress")
    
    # Input Section
    with st.expander("Add New Weight Entry"):
        new_w = st.number_input("Weight (kg)", format="%.1f")
        if st.button("Log Weight"):
            # (Logic to append to 'Weight' worksheet similar to above)
            st.info("Weight entry logic goes here!")

    # Visualization
    df_weight = conn.read(spreadsheet=url, worksheet="Weight")
    if not df_weight.empty:

        st.line_chart(df_weight.set_index("Date")["Weight"])


