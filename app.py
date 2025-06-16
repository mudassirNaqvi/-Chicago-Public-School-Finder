import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Page setup
st.set_page_config(page_title="Chicago School Finder", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1, h5 { color: #003366; }
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }
        .css-1r6slb0.e1tzin5v2 { padding-top: 0rem; padding-bottom: 0rem; }
        table td, table th { text-align: left !important; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>📍 Chicago Public School Finder</h1>", unsafe_allow_html=True)
st.markdown("Find public schools in Chicago by type, location, and performance.")

# Load and cache data
@st.cache_data
def load_data():
    url = "https://data.cityofchicago.org/resource/9xs2-f89t.json"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

df = load_data()

# Select relevant columns
df = df[[
    "school_id", "name_of_school", "elementary_or_high_school", "street_address",
    "zip_code", "latitude", "longitude", "community_area_name",
    "cps_performance_policy_level", "phone_number", "link_"
]].dropna(subset=["latitude", "longitude"])

# Convert lat/lon to float
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# Sidebar filters
st.sidebar.header("🎛️ Filters")

school_type = st.sidebar.multiselect(
    "School Type", sorted(df["elementary_or_high_school"].dropna().unique())
)
community = st.sidebar.multiselect(
    "Community Area", sorted(df["community_area_name"].dropna().unique())
)
performance = st.sidebar.multiselect(
    "Performance Level", sorted(df["cps_performance_policy_level"].dropna().unique())
)

# Apply filters
filtered_df = df.copy()
if school_type:
    filtered_df = filtered_df[filtered_df["elementary_or_high_school"].isin(school_type)]
if community:
    filtered_df = filtered_df[filtered_df["community_area_name"].isin(community)]
if performance:
    filtered_df = filtered_df[filtered_df["cps_performance_policy_level"].isin(performance)]

# Map Section
st.markdown("<h5 style='margin-top: 0;'>🗺️ Map of Filtered Schools</h5>", unsafe_allow_html=True)

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
marker_cluster = MarkerCluster().add_to(m)

# Color by performance level
def get_color(level):
    if level == "Level 1+":
        return "green"
    elif level == "Level 1":
        return "blue"
    elif level == "Level 2+":
        return "orange"
    elif level == "Level 2":
        return "red"
    else:
        return "gray"

for _, row in filtered_df.iterrows():
    popup_html = f"""
    <b>{row['name_of_school']}</b><br>
    {row['street_address']}, {row['zip_code']}<br>
    Phone: {row.get('phone_number', 'N/A')}<br>
    <a href="{row.get('link_', '#')}" target="_blank">School Website</a>
    """
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color=get_color(row.get("cps_performance_policy_level")),
        fill=True,
        fill_opacity=0.7,
        popup=popup_html,
        tooltip=row["name_of_school"]
    ).add_to(marker_cluster)

st.markdown("<div style='margin-bottom: -25px;'>", unsafe_allow_html=True)
st_folium(m, width=1000, height=600)
st.markdown("</div>", unsafe_allow_html=True)

# Table Section
st.markdown("<h5 style='margin-top: 1rem;'>📋 Filtered School List</h5>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No schools match the selected filters.")
else:
    display_df = filtered_df[[
        "name_of_school", "elementary_or_high_school", "street_address", "zip_code",
        "community_area_name", "cps_performance_policy_level", "phone_number", "link_"
    ]].fillna("N/A")

    # Format clickable links
    display_df["link_"] = display_df["link_"].apply(
        lambda x: f'<a href="{x}" target="_blank">Visit Site</a>' if isinstance(x, str) and x.startswith("http") else "N/A"
    )

    display_df = display_df.rename(columns={
        "name_of_school": "School Name",
        "elementary_or_high_school": "Type",
        "street_address": "Address",
        "zip_code": "ZIP",
        "community_area_name": "Community",
        "cps_performance_policy_level": "Performance",
        "phone_number": "Phone",
        "link_": "Website"
    })

    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)


