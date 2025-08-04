import streamlit as st
import googlemaps
import numpy as np
import tensorflow as tf
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv(AIzaSyBtfQm3sAeRqv5Dqzanmh6fY-omLqvLQM8)

# Load your trained model (make sure model.h5 exists or train in code)
model = tf.keras.models.load_model("model.h5")

# Initialize Google Maps
gmaps = googlemaps.Client(key=API_KEY)

def get_distance_duration(origin_lat, origin_lng, dest_lat, dest_lng):
    origin = f"{origin_lat},{origin_lng}"
    destination = f"{dest_lat},{dest_lng}"
    try:
        result = gmaps.distance_matrix(origins=origin,
                                       destinations=destination,
                                       mode='driving',
                                       departure_time='now')
        element = result['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance_km = element['distance']['value'] / 1000
            duration_min = element['duration_in_traffic']['value'] / 60
            return distance_km, duration_min
        else:
            return None, None
    except Exception as e:
        st.error(f"Google Maps API Error: {e}")
        return None, None

st.title("🚚 Food Delivery Time Prediction")

# Input fields
age = st.number_input("Delivery Partner Age", min_value=18, max_value=65, value=30)
rating = st.slider("Delivery Partner Rating", 0.0, 5.0, 4.5, 0.1)

st.subheader("Restaurant Location")
res_lat = st.number_input("Restaurant Latitude", format="%.6f")
res_lng = st.number_input("Restaurant Longitude", format="%.6f")

st.subheader("Delivery Location")
del_lat = st.number_input("Delivery Latitude", format="%.6f")
del_lng = st.number_input("Delivery Longitude", format="%.6f")

if st.button("Predict Delivery Time"):
    dist, dur = get_distance_duration(res_lat, res_lng, del_lat, del_lng)
    if dist is not None and dur is not None:
        input_data = np.array([[age, rating, dist, dur]])
        pred = model.predict(input_data)
        st.success(f"📦 Estimated Delivery Time: **{pred[0][0]:.2f} minutes**")
    else:
        st.warning("Could not retrieve distance or duration.")
