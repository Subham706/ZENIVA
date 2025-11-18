import streamlit as st

def calorie_calculator():
    st.subheader("Calorie Calculator")

    age = st.number_input("Enter your age (in years):", min_value=1, max_value=120, step=1)
    weight = st.number_input("Enter your weight (in kg):", min_value=1 , max_value=500 , step= 1)
    height = st.number_input("Enter your height (in cm):", min_value=30 , max_value=300 , step= 1)
    gender = st.selectbox("Select your gender:", options=["Male", "Female"])
    activity_level = st.selectbox("Select your activity level:",
                                  options=["Sedentary", "Light", "Moderate", "Active", "Very Active"])

    def calculate_bmr(weight, height, age, gender):
        gender = gender.lower()
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'female':
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            st.error("Invalid gender selected.")
            return None
        return round(bmr, 2)

    def calculate_tdee(bmr, activity_level):
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        multiplier = activity_multipliers.get(activity_level.lower())
        if multiplier is None:
            st.error("Invalid activity level selected.")
            return None
        return round(bmr * multiplier, 2)

    if st.button("Calculate Calorie Needs"):
        bmr = calculate_bmr(weight, height, age, gender)
        if bmr is not None:
            tdee = calculate_tdee(bmr, activity_level)
            if tdee is not None:
                st.success(f"Estimated Daily Calorie Requirement: {tdee} kcal")


