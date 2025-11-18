import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from time import sleep

def disease_recognition_page():

    st.title("🩻 X-Ray Disease Recognition System")
    st.markdown("### Upload a chest X-ray image to detect whether it’s **Normal** or **Pneumonia**.")

    # File upload
    uploaded_file = st.file_uploader("📤 Upload an X-ray image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded X-Ray", use_container_width=True)

        # Load model & preprocess image
        with st.spinner("🔍 Analyzing image... please wait"):
            sleep(1.5)
            model = tf.keras.models.load_model("xray_disease_model.h5")

            # Convert grayscale → RGB, resize, normalize
            img = image.convert("RGB").resize((128, 128))
            img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

            # Prediction
            prediction = model.predict(img_array)
            classes = ['Normal', 'Pneumonia']
            result = classes[np.argmax(prediction)]
            confidence = round(np.max(prediction) * 100, 2)

        # Show output
        st.success(f"### 🩺 Prediction: **{result}**")
        st.progress(int(confidence))
        st.write(f"Confidence: **{confidence}%**")

        if result == "Pneumonia":
            st.warning("⚠️ Signs of Pneumonia detected. Please consult a medical professional.")
        else:
            st.info("✅ The X-ray appears Normal. Always confirm with a doctor.")

    st.markdown("---")
    st.caption("Developed by **Subham Panda** | Health Management System (ZENIVA) | Using Streamlit & CNN")
