import os
import streamlit as st
import pandas as pd
from io import BytesIO
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

def generate_diet_chart():
    st.subheader("7-Day Diet Chart Generator")

    # User inputs
    name = st.text_input("Enter your name:")
    age = st.text_input("Enter your age:")
    gender = st.selectbox("Select your gender:", ["male", "female"])
    weight = st.text_input("Enter your weight (in kg):")
    height = st.text_input("Enter your height (in cm):")
    diet_pref = st.text_input("Enter your dietary preferences:")
    health_cond = st.text_input("Enter any health conditions:")
    fitness_goal = st.text_input("Enter your fitness goals:")

    if st.button("Generate Diet Chart"):
        if not name or not age or not weight or not height:
            st.error("Please fill in all the required fields.")
            return

        # Configure Gemini API key
        genai.configure(api_key="AIzaSyBVs8RCNT4ftw1izLDVMa79DA0oy--sLLQ")  # Replace with your Gemini API key

        prompt = f"""
Generate a 7-day diet chart in CSV format with columns: Day, Meal, Food, Quantity, Notes.
The plan should be for:
Name: {name}
Age: {age}
Gender: {gender}
Weight: {weight} kg
Height: {height} cm
Dietary Preference: {diet_pref}
Health Conditions: {health_cond}
Fitness Goal: {fitness_goal}
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

        if not df.empty and len(df.columns) >= 5:
            st.markdown("### Your 7-Day Diet Chart")
            st.dataframe(df)

            # Ensure "data" folder exists
            if not os.path.exists("data"):
                os.makedirs("data")

            # Save Excel file inside "data" folder
            file_path = os.path.join("data", f"diet_chart_{name.lower()}.xlsx")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            # Also allow download in browser
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download Diet Chart as Excel",
                    data=f,
                    file_name=f"diet_chart_{name.lower()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            st.success(f"Diet chart saved successfully in: {file_path}")
        else:
            st.error("Could not parse CSV response from API. Please try again.")
            st.text_area("Raw API response:", csv_data, height=200)

# Run the app
if __name__ == "__main__":
    generate_diet_chart()
