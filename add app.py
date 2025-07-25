import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import json

# Title
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from public GitHub Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
response = requests.get(url)
data = response.json()

# Create a base folium map
m = folium.Map(location=[32.1, 74.9], zoom_start=10, control_scale=True)

# Define a color mapping for Tehsils
tehsil_colors = {
    "Shakargarh": "red",
    "Narowal": "blue",
    "Zafarwal": "green"
}

# Function to get color based on tehsil name
def style_function(feature):
    tehsil = feature["properties"].get("Tehsil", "")
    return {
        "fillColor": tehsil_colors.get(tehsil, "gray"),
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    }

# Add GeoJSON to map with popup
folium.GeoJson(
    data,
    name="Tehsil Boundaries",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["Tehsil"]),
    popup=folium.GeoJsonPopup(fields=["Tehsil"])
).add_to(m)

# Add legend manually
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     ">
&nbsp;<b>Legend</b><br>
&nbsp;<i style="background:red;color:red;">&nbsp;&nbsp;&nbsp;</i>&nbsp; Shakargarh<br>
&nbsp;<i style="background:blue;color:blue;">&nbsp;&nbsp;&nbsp;</i>&nbsp; Narowal<br>
&nbsp;<i style="background:green;color:green;">&nbsp;&nbsp;&nbsp;</i>&nbsp; Zafarwal<br>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Display the map in Streamlit
st_folium(m, width=700, height=500)
