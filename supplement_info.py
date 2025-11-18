import streamlit as st
import google.generativeai as genai
import re

def clean_text(text):
    # Remove *, **, -, #, and extra spaces
    cleaned = re.sub(r"[\*#\\-]+", "", text)
    cleaned = re.sub(r"\n\s*\n", "\n\n", cleaned)  # keep only one empty line
    cleaned = re.sub(r"\s{2,}", " ", cleaned)      # remove multiple spaces
    return cleaned.strip()

def supplement_info():
    st.subheader("Supplement Information Finder")

    supplement = st.text_input("Enter the supplement name:")
    if st.button("Get Information"):
        if not supplement:
            st.error("Please enter a supplement name.")
            return

        try:
            # Configure Gemini API (use your key here)
            genai.configure(api_key="AIzaSyBVs8RCNT4ftw1izLDVMa79DA0oy--sLLQ")

            prompt = f"""
Provide detailed, reliable, and easy-to-understand information about the supplement '{supplement}' including:
1. Description
2. Key benefits
3. Possible side effects
4. Recommended dosage (general guidelines)
5. Any precautions or warnings
Make it structured and concise in clean paragraph format without any bullet points, *, or special symbols.
"""
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(prompt)
            info = clean_text(response.text)

            st.markdown("### Supplement Information:")
            st.write(info)

        except Exception as e:
            st.error(f"Error: {e}")
