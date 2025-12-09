import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Premium Predictor", layout="centered")

st.title("🏥 Insurance Premium Prediction")
st.write("Enter user details below to get the predicted premium category.")

# Create two columns for a better layout
col1, col2 = st.columns(2)

with col1:
    # Matches backend limit: lt=100
    age = st.number_input("Age", min_value=1, max_value=99, value=30)
    
    # Matches backend limit: lt=100
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=99.9, value=70.0)
    
    # Matches backend limit: lt=2.5
    height = st.number_input("Height (meters)", min_value=0.5, max_value=2.49, value=1.75)
    
    income_lpa = st.number_input("Income (LPA)", min_value=0.0, value=5.0)

with col2:
    city = st.text_input("City", value="Mumbai")
    occupation = st.selectbox(
        "Occupation",
        options=['retired', 'freelancer', 'student', 'government_job', 
                 'business_owner', 'unemployed', 'private_job']
    )
    smoker = st.checkbox("Is the user a Smoker?")

# Button to predict
if st.button("Predict Premium", type="primary"):
    # Prepare the payload
    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        # Send request to FastAPI backend
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # --- CRITICAL FIX HERE ---
            # We now look for 'predicted_catagory' (your backend spelling)
            if 'predicted_catagory' in result:
                st.success(f"Predicted Category: **{result['predicted_catagory']}**")
            else:
                st.error(f"Response format mismatch. Got: {result}")
        else:
            st.error(f"Backend Error ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend. Is FastAPI running on port 8000?")
