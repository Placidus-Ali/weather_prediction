import streamlit as st
import pandas as pd
import joblib
import os
from PIL import Image
print('Libraries Loaded Successfully')

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the model
model_path = os.path.join(script_dir, "random_forest_model.joblib")
model = joblib.load(model_path)
print('Model Loaded Successfully')

# Load Image
image_path = os.path.join(script_dir, "weather forecasting.jpg")
image = Image.open(image_path)
print('Image Loaded Successfully')

# Mapping for crop selection
Precipitation_Type = {1: "rain", 2: "snow"}
print('Precipitation Type Mapping Done')


st.title("Weather Temperature Predictor")
st.image(image)
st.write("Enter weather conditions to predict temperature (°C):")
with st.expander("Documentation: Input Feature Descriptions"):
    st.write("**Age**: age in years")
    st.write("**Sex**: sex; 1 = male, 0 = female")

# Input Features
Year = st.number_input("Year", value=2006, step=1)
Month = st.number_input("Month", min_value=1, max_value=12, step=1)
Day	= st.number_input("Day", min_value=1, max_value=31, step=1)
Time = st.number_input("Hour of Day", min_value=0, max_value=23, step=1)
Precipitation_Type = st.selectbox("Precipitation Type", options=[1, 2], format_func=lambda x: Precipitation_Type[x])
Humidity = st.number_input("Humidity",  min_value=0.00,  max_value=1.00, step=0.01)
Wind_Speed = st.number_input("Wind Speed (km/h)",  min_value=0.00,  max_value=63.90, step=0.01)	
Wind_Bearing = st.number_input("Wind Bearing (Degrees)",  min_value=0,  max_value=359, step=1)	
Visibility	= st.number_input("Visibility (km)",  min_value=0.0,  max_value= 16.10, step=0.1)
Pressure =  st.number_input("Pressure (millibars)",  min_value=0.0,  max_value=1046.40, step=0.1)
print('Input Features Set Successfully')

# Prediction
if st.button("Predict Temperature"):
    input_data = pd.DataFrame([[Year, Month, Day, Time, Precipitation_Type, Humidity, Wind_Speed, Wind_Bearing, Visibility, Pressure]],
                              columns=['Year', 'Month',	'Day', 'Time', 'Precipitation Type', 'Humidity', 'Wind Speed (km/h)', 'Wind Bearing (degrees)', 'Visibility (km)', 'Pressure (millibars)'])
    prediction = model.predict(input_data)[0]
    
     # Defining bins and corresponding summaries
    bins = [-25, 0, 10, 20, 30, 40, 50]
    labels = [
        "Freezing and foggy throughout the day.",
        "Cold and mostly cloudy throughout the day.",
        "Partly cloudy throughout the day.",
        "Warm and partly cloudy throughout the day.",
        "Hot and sunny throughout the day.",
        "Extremely hot throughout the day."
    ]

    # Mapping predicted temperature to summary
    weather_summary = pd.cut([prediction], bins=bins, labels=labels, include_lowest=True)[0]

    # Displaying results
    st.success(f"🌡️ Predicted Temperature: {prediction:.2f} °C")
    st.info(f"**Weather Summary:** {weather_summary}")

print('Model Prediction Done Successfully')