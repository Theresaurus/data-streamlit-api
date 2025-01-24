import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import streamlit.components.v1 as components


"""
## TaxiFare
"""
# Title + Description
st.title("WELCOME TO YOUR ULTIMATE TAXI FARE PREDICTION SERVICE 🚕")


st.markdown("""
Sticking to your New Year's resolution to stay on top of your finances?
This website will help you save money and give you a financial overview - it predicts what you will spend on cab rides in our beloved city.

Don't miss out and plan your next trip around the Big Apple!

**HOW? - EASY: Enter your trip details for your taxi ride in NYC below, and we will predict your fare.**
""")


"""
### Please share your trip details here:
"""
# Date + Time
day = st.date_input(
    "Select the day for your ride",
    datetime.date(2025, 1, 1))
st.write('I need a cab on the:', day)

time = st.time_input('Select the exact time for your pickup', datetime.time(12, 15))
st.write('I need a cab at:', time)

# Mapbox Integration
st.subheader("Select Pickup and Drop-off Locations")

mapbox_access_token = 'pk.eyJ1Ijoia3Jva3JvYiIsImEiOiJja2YzcmcyNDkwNXVpMnRtZGwxb2MzNWtvIn0.69leM_6Roh26Ju7Lqb2pwQ';

mapbox_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8' />
    <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
    <script src='https://api.mapbox.com/mapbox-gl-js/v2.12.1/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v2.12.1/mapbox-gl.css' rel='stylesheet' />
    <style>
        #map {{ width: 100%; height: 400px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';

        const map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-73.935242, 40.730610],
            zoom: 10
        }});

        let pickupMarker;
        let dropoffMarker;

        map.on('click', (e) => {{
            const coords = e.lngLat;
            if (!pickupMarker) {{
                pickupMarker = new mapboxgl.Marker({{ color: 'blue' }}).setLngLat(coords).addTo(map);
                document.getElementById('pickup_coords').value = `${{coords.lng}},${{coords.lat}}`;
            }} else if (!dropoffMarker) {{
                dropoffMarker = new mapboxgl.Marker({{ color: 'red' }}).setLngLat(coords).addTo(map);
                document.getElementById('dropoff_coords').value = `${{coords.lng}},${{coords.lat}}`;
            }}
        }});
    </script>
</body>
</html>
"""

st.markdown("Select locations on the map by clicking:")
components.html(mapbox_html, height=450)

pickup_coords = st.text_input("Pickup Coordinates (Longitude, Latitude)", "-73.935242,40.730610")
dropoff_coords = st.text_input("Drop-off Coordinates (Longitude, Latitude)", "-73.949997,40.650002")

# Passenger Count
number = st.number_input('Select a number of passengers', min_value=1, max_value=7, value=1)
st.write('The current number of passengers is ', number)


# Prediction API Call
if st.button("Predict Fare"):
    # Construct the API payload
    pickup_longitude, pickup_latitude = map(float, pickup_coords.split(","))
    dropoff_longitude, dropoff_latitude = map(float, dropoff_coords.split(","))
    pickup_datetime = f"{day} {time}"
    payload = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": number,
    }

    # Call the API
    api_url = "https://taxifare-605755972351.europe-west1.run.app/predict"  # Replace with your API endpoint
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        prediction = response.json()["fare"]

        # Display the prediction
        st.success(f"Estimated Fare: ${prediction:.2f}")
    except requests.exceptions.RequestException as e:
        st.error("An error occurred while fetching the prediction. Please try again.")
        st.error(str(e))

# Footer
st.markdown(
    """



    ---


    Made with ❤️ for NYC travelers

    XOXOX - Theresaurus

    """
)
