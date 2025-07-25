import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from your public Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"

# Create interactive map
m = leafmap.Map(center=[32.1, 74.9], zoom=9)

# Add GeoJSON with style and popup info
m.add_geojson(
    url,
    layer_name="Tehsils",
    info_mode="on_click",
    style={"color": "black", "weight": 2, "fillOpacity": 0.5},
    popup=["Tehsil", "Type", "Landuse"],
)

# Optional: Add legend (manually)
m.add_legend(
    title="Tehsil Types",
    labels=["Urban", "Rural"],
    colors=["#1f77b4", "#ff7f0e"]
)

# Show map in Streamlit
m.to_streamlit(height=600)
