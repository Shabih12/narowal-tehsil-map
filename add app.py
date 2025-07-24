import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Title
st.title("Tehsil Boundary - District Narowal")

# Load GeoJSON from your public Gist
url = "https://gist.githubusercontent.com/Shabih12/d24a2c4ff505bad1af186f286d24af0f/raw/153751af0ac417d80d0352a9641789c1ac2c2ab6/Tehsil_Boundary.json"
gdf = gpd.read_file(url)

# Sidebar filter
if "Tehsil" in gdf.columns:
    tehsils = gdf["Tehsil"].unique().tolist()
    selected_tehsils = st.sidebar.multiselect("Select Tehsil(s)", tehsils, default=tehsils)
    filtered_gdf = gdf[gdf["Tehsil"].isin(selected_tehsils)]
else:
    st.error("No 'Tehsil' column found in the data.")
    st.stop()

# Create map
m = leafmap.Map(center=[32.1, 74.9], zoom=9)

# Assign different colors to each Tehsil
colors = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
    "#ffff33", "#a65628", "#f781bf", "#999999"
]

for i, tehsil in enumerate(selected_tehsils):
    tehsil_gdf = filtered_gdf[filtered_gdf["Tehsil"] == tehsil]
    color = colors[i % len(colors)]
    m.add_gdf(
        tehsil_gdf,
        layer_name=tehsil,
        style={"fillColor": color, "color": "black", "weight": 2, "fillOpacity": 0.5},
        info_mode="on_click",  # Shows attribute popup
    )

# Add legend manually
legend_dict = {tehsil: colors[i % len(colors)] for i, tehsil in enumerate(selected_tehsils)}
m.add_legend(title="Tehsil Legend", legend_dict=legend_dict)

# Display map
m.to_streamlit(height=600)
