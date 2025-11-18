import streamlit as st

# Import module functions
from calorie_calculator import calorie_calculator
from diet_chart_generator import generate_diet_chart
from exercise_plan_generator import generate_exercise_plan
from supplement_info import supplement_info

def fitness_dashboard():
    st.title("🏃 Fitness Tracking Dashboard")
    st.write("Select a submodule from the sidebar.")

    module = st.sidebar.selectbox(
        "Choose a Module",
        [
            "Calorie Calculator",
            "Diet Chart Generator",
            "Exercise Plan Generator",
            "Supplement Info"
        ]
    )

    if module == "Calorie Calculator":
        calorie_calculator()

    elif module == "Diet Chart Generator":
        generate_diet_chart()

    elif module == "Exercise Plan Generator":
        generate_exercise_plan()

    elif module == "Supplement Info":
        supplement_info()
