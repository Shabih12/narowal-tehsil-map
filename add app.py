import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

# Title
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from GitHub Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
response = requests.get(url)
data = response.json()

# Extract unique tehsil names from the "Label" field
tehsil_names = list({feature["properties"]["Label"] for feature in data["features"]})

# Assign colors
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
color_map = {name: colors[i % len(colors)] for i, name in enumerate(tehsil_names)}

# Initialize map
m = folium.Map(location=[32.1, 74.9], zoom_start=9, tiles="cartodbpositron")

# Add polygons with styling
def style_function(feature):
    label = feature["properties"].get("Label", "")
    return {
        "fillColor": color_map.get(label, "gray"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    }

folium.GeoJson(
    data,
    name="Tehsil Boundaries",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["Label"], aliases=["Tehsil:"]),
).add_to(m)

# Add legend manually
legend_html = """
<div style='position: fixed; bottom: 50px; left: 50px; width: 200px; height: auto;
     border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
     padding: 10px;'>
     <b>Tehsil Legend</b><br>
"""
for tehsil, color in color_map.items():
    legend_html += f"<i style='background:{color};width:15px;height:15px;float:left;margin-right:5px;'></i>{tehsil}<br>"
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# Display map
st_folium(m, width=700, height=600)
