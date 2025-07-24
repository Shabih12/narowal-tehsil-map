import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Title
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from public GitHub Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
gdf = gpd.read_file(url)

# Sidebar filter
tehsils = gdf["Tehsil"].unique().tolist()
selected_tehsils = st.sidebar.multiselect("Select Tehsil(s)", tehsils, default=tehsils)

# Filter GeoDataFrame based on selection
filtered_gdf = gdf[gdf["Tehsil"].isin(selected_tehsils)]

# Create interactive map
if not filtered_gdf.empty:
    center = [filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()]
else:
    center = [32.1, 74.9]  # fallback

m = leafmap.Map(center=center, zoom=9)

# Color palette
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628", "#f781bf"]

# Add tehsils to map with unique symbology
for i, tehsil in enumerate(selected_tehsils):
    tehsil_gdf = filtered_gdf[filtered_gdf["Tehsil"] == tehsil]
    m.add_gdf(
        tehsil_gdf,
        layer_name=tehsil,
        style={
            "fillColor": colors[i % len(colors)],
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6,
        },
        info_mode="on_click",  # Show popup on click
    )

# Display the map in Streamlit
m.to_streamlit(height=600)
