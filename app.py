# app.py (Debugging Version)

print("--- Script starting ---")

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import os # Import the os module
import logging
import re

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

# --- 2. Data preprocessing: Convert GDP to numeric values ---
def convert_gdp_to_numeric(gdp_str):
    """Convert GDP string format to numeric value in billions."""
    if pd.isna(gdp_str) or gdp_str == "No reliable data available":
        return 0
    
    # Remove $ and any extra spaces
    gdp_str = str(gdp_str).replace('$', '').replace(',', '').strip()
    
    # Extract number and unit
    pattern = r'([\d,.]+)\s*(Trillion|Billion|Million)?'
    match = re.search(pattern, gdp_str, re.IGNORECASE)
    
    if match:
        number_str = match.group(1).replace(',', '')
        unit = match.group(2)
        
        try:
            number = float(number_str)
            if unit and unit.lower() == 'trillion':
                return number * 1000  # Convert to billions
            elif unit and unit.lower() == 'million':
                return number / 1000  # Convert to billions
            else:  # Billion or no unit
                return number
        except ValueError:
            return 0
    return 0

# Convert GDP column to numeric
df['gdp_numeric'] = df['gdp'].apply(convert_gdp_to_numeric)

# --- 3. Function to create the interactive map ---
def create_map(sort_order='none'):
    """Create choropleth map with optional GDP sorting."""
    df_sorted = df.copy()
    
    # Filter out countries with zero or no GDP data for better ranking
    df_with_gdp = df_sorted[df_sorted['gdp_numeric'] > 0].copy()
    df_no_gdp = df_sorted[df_sorted['gdp_numeric'] <= 0].copy()
    
    if sort_order == 'ascending':
        # For Low to High: Use actual GDP values (so low GDP = dark, high GDP = bright)
        df_with_gdp = df_with_gdp.sort_values('gdp_numeric', ascending=True)
        # Use actual GDP values for coloring
        df_with_gdp['display_value'] = df_with_gdp['gdp_numeric']
        df_with_gdp['gdp_rank'] = range(1, len(df_with_gdp) + 1)
        # Countries with no GDP get value 0
        df_no_gdp['display_value'] = 0
        df_no_gdp['gdp_rank'] = 0
        # Combine dataframes
        df_sorted = pd.concat([df_no_gdp, df_with_gdp], ignore_index=True)
        color_col = 'display_value'
        color_scale = px.colors.sequential.Reds  # Dark Purples
        
        # Debug: Print top and bottom 3 countries
        print(f"ASCENDING SORT - Bottom 3 countries (lowest GDP):")
        print(df_with_gdp[['country', 'gdp', 'gdp_numeric', 'gdp_rank']].head(3))
        print(f"ASCENDING SORT - Top 3 countries (highest GDP):")
        print(df_with_gdp[['country', 'gdp', 'gdp_numeric', 'gdp_rank']].tail(3))
        
    elif sort_order == 'descending':
        # For High to Low: Use inverted ranks (so high GDP = low rank = bright, low GDP = high rank = dark)
        df_with_gdp = df_with_gdp.sort_values('gdp_numeric', ascending=False)
        # Assign inverted ranks - highest GDP gets lowest rank number
        max_countries = len(df_with_gdp)
        df_with_gdp['display_value'] = max_countries - pd.Series(range(len(df_with_gdp)))  # Invert the ranking
        df_with_gdp['gdp_rank'] = range(1, len(df_with_gdp) + 1)
        # Countries with no GDP get value 0
        df_no_gdp['display_value'] = 0
        df_no_gdp['gdp_rank'] = 0
        # Combine dataframes
        df_sorted = pd.concat([df_no_gdp, df_with_gdp], ignore_index=True)
        color_col = 'display_value'
        color_scale = px.colors.sequential.Blues  # Dark blue (low) to bright blue (high)
        
        # Debug: Print top and bottom 3 countries
        print(f"DESCENDING SORT - Top 3 countries (highest GDP, rank 1-3):")
        print(df_with_gdp[['country', 'gdp', 'gdp_numeric', 'gdp_rank']].head(3))
        print(f"DESCENDING SORT - Bottom 3 countries (lowest GDP, highest rank numbers):")
        print(df_with_gdp[['country', 'gdp', 'gdp_numeric', 'gdp_rank']].tail(3))
        
    else:
        # No sorting - use original GDP values
        df_sorted['gdp_rank'] = 0
        color_col = 'gdp_numeric'
        color_scale = px.colors.sequential.Cividis
    
    # Create custom hover data
    hover_data_dict = {
        "capital": True,
        "currency": True,
        "gdp": True,
        "country_iso_alpha": True,
        "population": False,
    }
    
    #Display gdp rank if sorted
    if sort_order != 'none':
        hover_data_dict["gdp_rank"] = True
    
    fig = px.choropleth(
        df_sorted,
        locations="country_iso_alpha",
        color=color_col,
        hover_name="country",
        hover_data=hover_data_dict,
        color_continuous_scale=color_scale,
        title=f"World Map: Countries, Capitals & GDP {f'(Ranked {sort_order})' if sort_order != 'none' else ''}"
    )
    #Align the title to the center
    fig.update_layout(title_x=0.5)
    
    # Update color bar title and range
    if sort_order == 'ascending':
        # For Low to High: Using actual GDP values
        fig.update_coloraxes(colorbar_title="GDP (Billions)")
        min_val = df_sorted[df_sorted['display_value'] > 0]['display_value'].min()
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=min_val, cmax=max_val)
        fig.update_traces(zmin=min_val, zmax=max_val)
    elif sort_order == 'descending':
        # For High to Low: Using inverted ranking (high GDP = high value = bright color)
        fig.update_coloraxes(colorbar_title="GDP Ranking (Higher=Better)")
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=1, cmax=max_val)
        fig.update_traces(zmin=1, zmax=max_val)
    else:
        fig.update_coloraxes(colorbar_title="GDP (Billions)")
        # For non-sorted view, ensure proper range for GDP values
        min_gdp = df_sorted['gdp_numeric'].min()
        max_gdp = df_sorted['gdp_numeric'].max()
        fig.update_coloraxes(cmin=min_gdp, cmax=max_gdp)
    
    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular')
    )
    return fig

# --- 4. Function to create sorted data table ---
def create_data_table(sort_order='none'):
    """Create a data table showing sorted countries."""
    df_display = df.copy()
    
    if sort_order == 'ascending':
        df_display = df_display.sort_values('gdp_numeric', ascending=True)
        title = "Countries by GDP (Low to High)"
    elif sort_order == 'descending':
        df_display = df_display.sort_values('gdp_numeric', ascending=False)
        title = "Countries by GDP (High to Low)"
    else:
        title = "Countries (No Sorting)"
    
    # Select and format columns for display
    df_display = df_display[['country', 'gdp', 'capital', 'currency']].head(10)
    
    return html.Div([
        html.H4(title, style={'textAlign': 'center', 'marginBottom': '10px'}),
        html.P("Top 10 countries:", style={'textAlign': 'center', 'fontSize': '12px', 'marginBottom': '10px'}),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Country", style={'padding': '8px', 'backgroundColor': '#f1f1f1'}),
                    html.Th("GDP", style={'padding': '8px', 'backgroundColor': '#f1f1f1'}),
                    html.Th("Capital", style={'padding': '8px', 'backgroundColor': '#f1f1f1'}),
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(row['country'], style={'padding': '5px'}),
                    html.Td(row['gdp'], style={'padding': '5px'}),
                    html.Td(row['capital'], style={'padding': '5px'}),
                ]) for _, row in df_display.iterrows()
            ])
        ], style={'margin': 'auto', 'border': '1px solid #ddd', 'borderCollapse': 'collapse'})
    ])

# --- 5. Setup the Dash App with GDP sorting controls ---
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Interactive World Map", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.P("Hover over a country to see more information...", 
           style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # --- UPDATED SECTION ---
    # GDP sorting controls using flexbox for horizontal alignment
    html.Div([
        html.Label(
            "GDP Sorting Options:", 
            style={'marginRight': '10px'} # Adds space between label and dropdown
        ),
        dcc.Dropdown(
            id='gdp-sort-dropdown',
            options=[
                {'label': 'GDP: Not Sorted', 'value': 'none'},
                {'label': 'GDP: Low to High', 'value': 'ascending'},
                {'label': 'GDP: High to Low', 'value': 'descending'}
            ],
            value='none',
            style={'width': '200px'},
            clearable=False # Good practice to prevent user from clearing selection
        )
    ], style={
        'display': 'flex',          # Enables flexbox layout
        'justifyContent': 'center', # Horizontally centers the label and dropdown
        'alignItems': 'center',     # Vertically aligns them
        'marginBottom': '20px'
    }),
    
    # Main content area with map and table side by side
    html.Div([
        # Map on the left
        html.Div([
            dcc.Graph(id="world-map")
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Data table on the right
        html.Div([
            html.Div(id="data-table")
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
    ])
])


# Callback for updating the map based on GDP sorting
@app.callback(
    Output('world-map', 'figure'),
    Input('gdp-sort-dropdown', 'value')
)
def update_map(sort_order):
    return create_map(sort_order)

# Callback for updating the data table based on GDP sorting
@app.callback(
    Output('data-table', 'children'),
    Input('gdp-sort-dropdown', 'value')
)
def update_table(sort_order):
    return create_data_table(sort_order)


# --- 4. Run the App ---
if __name__ == '__main__':
    logging.debug("--- Inside __name__ == '__main__' block (This is correct!) ---")
    logging.debug("--- Starting Dash server... If you see this, it should work! ---")
    app.run(debug=True)
else:
    # This part helps catch if the script is being imported instead of run
    logging.error(f"--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '{__name__}') ---")
