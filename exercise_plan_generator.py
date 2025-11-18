import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

def safe_read_csv(data):
    import csv
    from io import StringIO
    try:
        return pd.read_csv(StringIO(data))
    except Exception:
        try:
            return pd.read_csv(
                StringIO(data),
                quoting=csv.QUOTE_MINIMAL,
                on_bad_lines="skip",
                engine="python"
            )
        except Exception:
            st.error("Failed to parse the CSV data.")
            return pd.DataFrame()

def generate_exercise_plan():
    st.subheader("Exercise Plan Generator")

    goal = st.selectbox("Enter your goal:", ["gain", "loss", "strength", "flexibility"])
    workout_days = st.number_input("Number of workout days per week:", min_value=1, max_value=7, step=1)
    session_minutes = st.number_input("Average minutes per session:", min_value=10, max_value=180, step=5)

    if st.button("Generate Exercise Plan"):
        if not goal or not workout_days or not session_minutes:
            st.error("Please fill in all required inputs.")
            return

        # Configure Gemini API key
        genai.configure(api_key="AIzaSyBVs8RCNT4ftw1izLDVMa79DA0oy--sLLQ")  # Replace with your actual API key

        prompt = f"""
Generate a structured workout plan in CSV format with columns: Day, Warm-up, Main Workout, Cooldown, Notes.

Plan details:
Goal: {goal}
Workout Days per Week: {workout_days}
Session Duration: {session_minutes} minutes

Ensure:
- No extra text before or after CSV.
- Commas inside fields should be enclosed in double quotes.
"""

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        csv_data = response.text.strip()

        # Clean triple backtick markdown fences if present
        if csv_data.startswith("```") and csv_data.endswith("```"):
            csv_data = csv_data.strip("`").replace("csv\n", "").strip()

        df = safe_read_csv(csv_data)

        if not df.empty and len(df.columns) >= 4:
            st.markdown("### Your Personalized Exercise Plan")
            st.dataframe(df)

            # Ensure "data" folder exists
            if not os.path.exists("data"):
                os.makedirs("data")

            # Save Excel file inside "data" folder
            file_path = os.path.join("data", "exercise_plan.xlsx")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            # Also allow download in browser
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download Exercise Plan as Excel",
                    data=f,
                    file_name="exercise_plan.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            st.success(f"Exercise plan saved successfully in: {file_path}")
        else:
            st.error("Could not parse CSV response from API. Please try again.")
            st.text_area("Raw API response:", csv_data, height=200)

if __name__ == "__main__":
    generate_exercise_plan()
