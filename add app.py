import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json

# Title
st.markdown("<h1 style='text-align: center; color: darkblue;'>Tehsil Boundary - District Narowal</h1>", unsafe_allow_html=True)

# Load GeoJSON from URL
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
response = requests.get(url)
data = response.json()

# Extract unique 'Name' values (replace with actual field name)
tehsil_names = list({feature["properties"]["Name"] for feature in data["features"]})
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]

# Map setup
m = folium.Map(location=[32.1, 74.9], zoom_start=9)

# Add polygons with different colors
for i, tehsil in enumerate(tehsil_names):
    def style_function(feature, name=tehsil, color=colors[i % len(colors)]):
        return {
            "fillColor": color if feature["properties"]["Name"] == name else "transparent",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6 if feature["properties"]["Name"] == name else 0,
        }

    folium.GeoJson(
        data,
        name=tehsil,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["Name"]),
        popup=folium.GeoJsonPopup(fields=["Name"])
    ).add_to(m)

# Add Legend
legend_html = """
<div style='position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: 200px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius:10px; padding: 10px'>
<b>Legend - Tehsils</b><br>
"""
for i, name in enumerate(tehsil_names):
    legend_html += f"<i style='background:{colors[i % len(colors)]};width:10px;height:10px;float:left;margin-right:5px;'></i>{name}<br>"
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# Show map
folium_static(m)
