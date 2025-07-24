app.py
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Title
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON directly from your public Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
gdf = gpd.read_file(url)

# Sidebar filter
tehsils = gdf["Tehsil"].unique().tolist()
selected = st.sidebar.multiselect("Select Tehsil(s)", tehsils, default=tehsils)

# Filtered GeoDataFrame
filtered_gdf = gdf[gdf["Tehsil"].isin(selected)]

# Create interactive map
m = leafmap.Map(center=[32.1, 74.9], zoom=9)
m.add_gdf(filtered_gdf, layer_name="Tehsils", info_mode="on_click")

# Add simple legend by coloring different tehsils
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
for i, tehsil in enumerate(tehsils):
    tehsil_gdf = gdf[gdf["Tehsil"] == tehsil]
    m.add_gdf(
        tehsil_gdf,
        layer_name=tehsil,
        style={"fillColor": colors[i % len(colors)], "color": "black", "weight": 1},
    )

# Show map
m.to_streamlit(height=600)
add app.py
