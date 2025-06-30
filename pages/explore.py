"""
Explore page containing the interactive GDP world map.
"""

import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from utils.data_processing import load_countries_data

# Load the data
df = load_countries_data()

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
        color_scale = px.colors.sequential.Reds
        
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
        color_scale = px.colors.sequential.Blues
        
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
    
    # Display gdp rank if sorted
    if sort_order != 'none':
        hover_data_dict["gdp_rank"] = True
    
    fig = px.choropleth(
        df_sorted,
        locations="country_iso_alpha",
        color=color_col,
        hover_name="country",
        hover_data=hover_data_dict,
        color_continuous_scale=color_scale
    )
    # Align the title to the center
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
        fig.update_coloraxes(colorbar_title="GDP Ranking (Billions)")
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
    df_display = df_display[['country', 'gdp', 'capital', 'currency']].head(20)
    
    return html.Div([
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

def get_explore_layout():
    """Get the layout for the explore page."""
    return html.Div([
        
        # GDP sorting controls using flexbox for horizontal alignment
        html.Div([
            html.Label(
                "GDP Sorting Options:", 
                style={'marginRight': '10px'}
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
                clearable=False
            )
        ], style={
            'display': 'flex',
            'justifyContent': 'left',
            'alignItems': 'left',
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

def register_explore_callbacks(app):
    """Register callbacks for the explore page."""
    @app.callback(
        Output('world-map', 'figure'),
        Input('gdp-sort-dropdown', 'value')
    )
    def update_map(sort_order):
        return create_map(sort_order)

    @app.callback(
        Output('data-table', 'children'),
        Input('gdp-sort-dropdown', 'value')
    )
    def update_table(sort_order):
        return create_data_table(sort_order)
