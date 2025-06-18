import pandas as pd
import plotly.express as px
from pathlib import Path
import streamlit as st

st.set_page_config(layout="wide")

# Load data
BASE_DIR = Path(__file__).parent
df = pd.read_csv(BASE_DIR / 'wdi.csv')

# Title
st.title('Life Expectancy Explorer')

# Layout
col1, col2 = st.columns(2)

with col1:
    choropleth_fig = px.choropleth(
        df[df.year == 2020],
        locations="iso3",
        color="life_expectancy",
        hover_name="country"
    )
    choropleth_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(x=0, y=0.4, len=0.3, title=None)
    )

    selection_event = st.plotly_chart(
        choropleth_fig, on_select="rerun", key="choropleth"
    )


with col2:
    if not selection_event["selection"]["points"]:
        st.warning(
            "Please select countries on the map. Use shift+click for multiple countries")
        st.stop()

    selected_countries = [
        point['location'] for point in selection_event["selection"]["points"]
    ]
    df_selected = df[df.iso3.isin(selected_countries)]

    line_fig = px.line(
        df_selected,
        x="year",
        y="life_expectancy",
        color="country",
        title="Life Expectancy Over Time"
    )
    st.plotly_chart(line_fig)
