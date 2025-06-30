# app.py (Debugging Version)

print("--- Script starting ---")

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import os # Import the os module
import logging

print("--- Imports successful ---")

# Let's see exactly where the script is running from
logging.debug(f"Current Working Directory: {os.getcwd()}")
logging.debug(f"Looking for data file at the relative path: 'data/countries_data.csv'")

# --- 1. Load the data using Pandas with robust error handling ---
try:
    file_path = 'data/countries.csv'
    df = pd.read_csv(file_path)
    logging.info("--- Successfully loaded data/countries.csv ---")
    logging.info(f"Data contains {len(df)} rows.")

except FileNotFoundError:
    logging.debug("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logging.error(f"!!! CRITICAL ERROR: File not found at '{os.path.abspath(file_path)}'")
    logging.warn("!!! Please make sure you are running 'python app.py' from the root 'my_map_app' directory.")
    logging.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    exit() # Stop the script if the file isn't found

except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    exit() # Stop on other errors, too


# --- 2. Create the interactive map (No changes here) ---
fig = px.choropleth(
    df,
    locations="country_iso_alpha",
    color="gdp",
    hover_name="country",
    hover_data={
        "capital": True,
        "currency": True,
        "gdp": True,
        "country_iso_alpha": True,
        "population": False,
    },
    color_continuous_scale=px.colors.sequential.Plasma,
    title="World Map: Countries, Capitals & GDP"
)
fig.update_layout(
    margin={"r":0, "t":40, "l":0, "b":0},
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular')
)


# --- 3. Setup the Dash App (No changes here) ---
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Interactive World Map"),
    html.P("Hover over a country to see its GDP, ISO_ALPHA, Capital and Currency"),
    dcc.Graph(id="world-map", figure=fig)
])


# --- 4. Run the App ---
if __name__ == '__main__':
    logging.debug("--- Inside __name__ == '__main__' block (This is correct!) ---")
    logging.debug("--- Starting Dash server... If you see this, it should work! ---")
    app.run(debug=True)
else:
    # This part helps catch if the script is being imported instead of run
    logging.error(f"--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '{__name__}') ---")