import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from URL
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
response = requests.get(url)
data = response.json()

# Get features safely
features = data.get("features", [])
if not features:
    st.error("GeoJSON is missing 'features'.")
    st.stop()

# Unique tehsil names from "Label" field
tehsil_names = list({feature.get("properties", {}).get("Label", "Unknown") for feature in features})

# Create folium map
m = folium.Map(location=[32.1, 74.9], zoom_start=9)

colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]

def style_function(feature):
    label = feature.get("properties", {}).get("Label", "")
    index = tehsil_names.index(label) if label in tehsil_names else 0
    return {
        "fillOpacity": 0.5,
        "weight": 1,
        "color": "black",
        "fillColor": colors[index % len(colors)],
    }

popup = folium.GeoJsonPopup(fields=["Label"], labels=True)

folium.GeoJson(
    data,
    name="Tehsils",
    style_function=style_function,
    popup=popup,
).add_to(m)

# Show map
folium_static(m)
