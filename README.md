
# 📍 Chicago Public School Finder

An interactive Streamlit web app to explore and locate public schools across Chicago based on school type, community area, and performance level. The application displays results both as a map and a searchable table, making it easy for users to find relevant school information.

## 🚀 Features

* 🎛️ **Dynamic Filtering** by:

  * School Type (Elementary or High School)
  * Community Area
  * CPS Performance Policy Level
* 🗺️ **Interactive Map** with color-coded school markers and pop-up info
* 📋 **Data Table** with detailed school information and direct website links

## 🧩 Built With

* [Streamlit](https://streamlit.io/) – For building the UI
* [Pandas](https://pandas.pydata.org/) – For data handling
* [Folium](https://python-visualization.github.io/folium/) – For interactive maps
* [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium) – Integration between Folium and Streamlit
* [City of Chicago Open Data](https://data.cityofchicago.org/) – Live public school dataset

## 📦 Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/chicago-school-finder.git
cd chicago-school-finder
```

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

**`requirements.txt` should include:**

```
streamlit
pandas
requests
folium
streamlit-folium
```

4. **Run the app:**

```bash
streamlit run app.py
```

## 📊 Data Source

This app uses live data from the [City of Chicago Public Schools Dataset](https://data.cityofchicago.org/resource/9xs2-f89t.json).

## 🧠 How It Works

* Loads school data from the Chicago Open Data API.
* Filters data based on user input from the sidebar.
* Displays filtered results on an interactive map with color-coded performance markers.
* Shows a styled HTML table with links to school websites.

## 🎨 Map Legend (Performance Color Codes)

| Performance Level | Color  |
| ----------------- | ------ |
| Level 1+          | Green  |
| Level 1           | Blue   |
| Level 2+          | Orange |
| Level 2           | Red    |
| Not Rated         | Gray   |


## 📝 License

MIT License – feel free to use and adapt!
