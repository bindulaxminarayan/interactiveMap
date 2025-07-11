"""
Explore page containing the interactive GDP world map.
"""

import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, State, ctx, ALL
from utils.data_processing import load_countries_data

# Load the data
df = load_countries_data()

def create_map(sort_order='none', selected_country=None):
    """Create choropleth map with optional GDP sorting and country highlighting."""
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
        # For High to Low: Use actual GDP values (same as ascending for consistency)
        df_with_gdp = df_with_gdp.sort_values('gdp_numeric', ascending=False)
        # Use actual GDP values for coloring (same as ascending for consistency)
        df_with_gdp['display_value'] = df_with_gdp['gdp_numeric']
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
        "country_iso_alpha": True
    }
    
    # Display gdp rank if sorted
    if sort_order != 'none':
        hover_data_dict["gdp_rank"] = True
        hover_data_dict["display_value"] = False
    else:
        # Explicitly exclude gdp_numeric from hover when not sorted
        hover_data_dict["gdp_numeric"] = False
    
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
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        min_val = df_sorted[df_sorted['display_value'] > 0]['display_value'].min()
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=min_val, cmax=max_val)
        fig.update_traces(zmin=min_val, zmax=max_val)
    elif sort_order == 'descending':
        # For High to Low: Using actual GDP values (same as ascending for consistency)
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        min_val = df_sorted[df_sorted['display_value'] > 0]['display_value'].min()
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=min_val, cmax=max_val)
        fig.update_traces(zmin=min_val, zmax=max_val)
    else:
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        # For non-sorted view, ensure proper range for GDP values
        min_gdp = df_sorted['gdp_numeric'].min()
        max_gdp = df_sorted['gdp_numeric'].max()
        fig.update_coloraxes(cmin=min_gdp, cmax=max_gdp)
    
    # Add highlighting for selected country
    if selected_country:
        # Find the country from the sorted dataframe to ensure it has all necessary columns
        country_row = df_sorted[df_sorted['country'] == selected_country]
        if not country_row.empty:
            iso_code = country_row.iloc[0]['country_iso_alpha']
            # Choose color based on sort order
            if sort_order == 'ascending':
                highlight_color = '#22AA22'  # Green for low to high
            elif sort_order == 'descending':
                highlight_color = '#4444FF'  # Blue for high to low
            else:
                highlight_color = '#FF4444'  # Red for no sorting (default)
            
            # Add a highlighted trace for the selected country with full hover data
            highlight_fig = px.choropleth(
                country_row,
                locations="country_iso_alpha",
                color_discrete_sequence=[highlight_color],
                 hover_name="country",
                 hover_data=hover_data_dict
            )
            
            fig.add_trace(highlight_fig.data[0])
            
            # Update the highlighted trace properties
            fig.data[-1].update(
                name=f"Selected: {selected_country}",
                showlegend=True,
                marker_line_color='#000000',
                marker_line_width=3
            )
            
            # Add zoom and center functionality for better visibility of small countries
            # Define regional centers and zoom levels for better country visibility
            country_coords = {
                'Albania': {'lat': 41.1533, 'lon': 20.1683, 'zoom': 6},
                'Andorra': {'lat': 42.5063, 'lon': 1.5218, 'zoom': 8},
                'Malta': {'lat': 35.9375, 'lon': 14.3754, 'zoom': 9},
                'Monaco': {'lat': 43.7384, 'lon': 7.4246, 'zoom': 10},
                'San Marino': {'lat': 43.9424, 'lon': 12.4578, 'zoom': 9},
                'Liechtenstein': {'lat': 47.166, 'lon': 9.5554, 'zoom': 9},
                'Luxembourg': {'lat': 49.8153, 'lon': 6.1296, 'zoom': 8},
                'Cyprus': {'lat': 35.1264, 'lon': 33.4299, 'zoom': 7},
                'Iceland': {'lat': 64.9631, 'lon': -19.0208, 'zoom': 5},
                'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'zoom': 10},
                'Brunei': {'lat': 4.5353, 'lon': 114.7277, 'zoom': 8},
                'Bahrain': {'lat': 26.0667, 'lon': 50.5577, 'zoom': 9},
                'Qatar': {'lat': 25.3548, 'lon': 51.1839, 'zoom': 8},
                'Kuwait': {'lat': 29.3117, 'lon': 47.4818, 'zoom': 8},
                'Maldives': {'lat': 3.2028, 'lon': 73.2207, 'zoom': 6},
                'Seychelles': {'lat': -4.6796, 'lon': 55.492, 'zoom': 8},
                'Mauritius': {'lat': -20.348404, 'lon': 57.552152, 'zoom': 9},
            }
            
            if selected_country in country_coords:
                coords = country_coords[selected_country]
                fig.update_geos(
                    center_lat=coords['lat'],
                    center_lon=coords['lon'],
                    projection_scale=coords['zoom']
                )
            else:
                # For larger countries, use default view but slightly zoomed
                fig.update_geos(
                    projection_scale=1.2
                )
    
    fig.update_layout(
        margin={"r":0, "t":60, "l":0, "b":0},  # Increased top margin for legend space
        geo=dict(
            showframe=False, 
            showcoastlines=False, 
            projection_type='equirectangular'
        ),
        legend=dict(
            x=0.02,  # Position legend on the left side
            y=0.98,  # Position near the top
            bgcolor="rgba(255,255,255,0.8)",  # Semi-transparent white background
            bordercolor="Black",
            borderwidth=1
        ),
        height=600,  # Increased height for better visibility of small countries
        width=1200
    )
    return fig

def create_data_table(sort_order='none', selected_country=None, search_term='', table_sort_column='', table_sort_direction='asc'):
    """Create a data table showing sorted countries with clickable rows, search, and column sorting."""
    df_display = df.copy()
    
    if sort_order == 'ascending':
        df_display = df_display.sort_values('gdp_numeric', ascending=True)
        title = "Countries by GDP (Low to High)"
    elif sort_order == 'descending':
        df_display = df_display.sort_values('gdp_numeric', ascending=False)
        title = "Countries by GDP (High to Low)"
    else:
        title = "Countries (No Sorting)"
    
    # Select and format columns for display - show ALL countries
    df_display = df_display[['country', 'gdp', 'capital', 'currency', 'continent']]
    
    # Apply search filter
    if search_term:
        search_mask = (
            df_display['country'].str.contains(search_term, case=False, na=False) |
            df_display['capital'].str.contains(search_term, case=False, na=False) |
            df_display['currency'].str.contains(search_term, case=False, na=False) |
            df_display['continent'].str.contains(search_term, case=False, na=False)
        )
        df_display = df_display[search_mask]
    
    # Apply table column sorting (independent of GDP sorting)
    if table_sort_column:
        if table_sort_column == 'gdp':
            # For GDP column, sort by the numeric value
            ascending = table_sort_direction == 'asc'
            df_display = df_display.sort_values('gdp', key=lambda x: pd.to_numeric(x.str.replace(r'[\$,]', '', regex=True), errors='coerce'), ascending=ascending)
        else:
            ascending = table_sort_direction == 'asc'
            df_display = df_display.sort_values(table_sort_column, ascending=ascending)
    
    # Create sortable column headers
    def create_sortable_header(column_name, display_name):
        arrow = ""
        if table_sort_column == column_name:
            arrow = " ↑" if table_sort_direction == 'asc' else " ↓"
        
        return html.Th([
            html.Div([
                display_name + arrow
            ], 
            id={'type': 'sort-header', 'column': column_name},
            style={'cursor': 'pointer', 'userSelect': 'none'})
        ], style={'padding': '8px', 'backgroundColor': '#f1f1f1', 'textAlign': 'left', 'minWidth': '100px'})
    
    return html.Div([
        # Country count display
        html.Div([
            f"Showing {len(df_display)} countries"
        ], style={'marginBottom': '10px', 'color': '#666', 'fontSize': '14px'}),
        
        # Scrollable table container
        html.Div([
            html.Table([
                html.Thead([
                    html.Tr([
                        create_sortable_header('country', 'Country'),
                        create_sortable_header('gdp', 'GDP'),
                        create_sortable_header('capital', 'Capital'),
                        create_sortable_header('currency', 'Currency'),
                        create_sortable_header('continent', 'Continent')
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(row['country'], style={'padding': '6px', 'textAlign': 'left', 'verticalAlign': 'middle', 'fontSize': '12px'}),
                        html.Td(row['gdp'], style={'padding': '6px', 'textAlign': 'center', 'verticalAlign': 'middle', 'fontSize': '12px'}),
                        html.Td(row['capital'], style={'padding': '6px', 'textAlign': 'left', 'verticalAlign': 'middle', 'fontSize': '12px'}),
                        html.Td(row['currency'], style={'padding': '6px', 'textAlign': 'left', 'verticalAlign': 'middle', 'fontSize': '12px'}),
                        html.Td(row['continent'], style={'padding': '6px', 'textAlign': 'left', 'verticalAlign': 'middle', 'fontSize': '12px'})
                    ], 
                    id={'type': 'country-row', 'index': i},
                    style={
                        'cursor': 'pointer',
                        'backgroundColor': '#ffebee' if selected_country == row['country'] else 'white',
                        'border': '2px solid #ff4444' if selected_country == row['country'] else '1px solid #ddd',
                        'transition': 'background-color 0.2s ease'
                    },
                    className='country-row'
                    ) for i, (_, row) in enumerate(df_display.iterrows())
                ])
            ], style={
                'border': '1px solid #ddd', 
                'borderCollapse': 'collapse',
                'width': '100%',
                'tableLayout': 'fixed'
            })
        ], style={
            'maxHeight': '500px',
            'overflowY': 'auto',
            'border': '1px solid #ddd'
        })
    ])

def get_explore_layout():
    """Get the layout for the explore page."""
    return html.Div([
        # Store components to track state
        dcc.Store(id='selected-country-store', data=None),
        dcc.Store(id='table-sort-store', data={'column': '', 'direction': 'asc'}),
        
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
                # Search input moved here so it exists in the layout
                html.Div([
                    html.H4("Click on a country to highlight it on the map", 
                            style={'textAlign': 'center', 'marginBottom': '10px', 'color': '#666'}),
                    html.Div([
                        html.Label("Search Countries: ", style={'marginRight': '10px', 'fontWeight': 'bold'}),
                        dcc.Input(
                            id='country-search-input',
                            type='text',
                            placeholder='Search by country, capital, currency, or continent...',
                            value='',
                            style={'width': '300px', 'padding': '5px', 'marginBottom': '10px'}
                        )
                    ], style={'marginBottom': '15px'})
                ]),
                html.Div(id="data-table")
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
        ])
    ])

def register_explore_callbacks(app):
    """Register callbacks for the explore page."""
    
    # Callback for handling table column header clicks for sorting
    @app.callback(
        Output('table-sort-store', 'data'),
        Input({'type': 'sort-header', 'column': ALL}, 'n_clicks'),
        State('table-sort-store', 'data'),
        prevent_initial_call=True
    )
    def update_table_sort(n_clicks_list, current_sort):
        # Check which header was clicked
        ctx_triggered = ctx.triggered
        if not ctx_triggered or not ctx_triggered[0]['value']:
            return current_sort
        
        # Extract the column from the component_id
        button_id = ctx_triggered[0]['prop_id'].split('.')[0]
        if button_id == '' or button_id == '{}':
            return current_sort
            
        try:
            import json
            component_id = json.loads(button_id)
            # Ensure this is actually a sort-header click
            if component_id.get('type') != 'sort-header':
                return current_sort
            clicked_column = component_id['column']
        except (json.JSONDecodeError, KeyError):
            return current_sort
        
        # Toggle sort direction if same column, otherwise set to ascending
        if current_sort['column'] == clicked_column:
            new_direction = 'desc' if current_sort['direction'] == 'asc' else 'asc'
        else:
            new_direction = 'asc'
        
        return {'column': clicked_column, 'direction': new_direction}
    
    # Callback for handling country row clicks
    @app.callback(
        Output('selected-country-store', 'data'),
        Input({'type': 'country-row', 'index': ALL}, 'n_clicks'),
        [State('gdp-sort-dropdown', 'value'),
         State('country-search-input', 'value'),
         State('table-sort-store', 'data')],
        prevent_initial_call=True
    )
    def update_selected_country(n_clicks_list, sort_order, search_term, table_sort):
        # Check which button triggered the callback
        ctx_triggered = ctx.triggered
        if not ctx_triggered:
            return None
        
        # Extract the index from the component_id
        button_id = ctx_triggered[0]['prop_id'].split('.')[0]
        if button_id == '':
            return None
            
        import json
        component_id = json.loads(button_id)
        clicked_idx = component_id['index']
        
        # Recreate the filtered and sorted dataframe to get the correct country
        df_display = df.copy()
        
        # Apply GDP sorting first
        if sort_order == 'ascending':
            df_display = df_display.sort_values('gdp_numeric', ascending=True)
        elif sort_order == 'descending':
            df_display = df_display.sort_values('gdp_numeric', ascending=False)
        
        # Select columns
        df_display = df_display[['country', 'gdp', 'capital', 'currency', 'continent']]
        
        # Apply search filter
        if search_term:
            search_mask = (
                df_display['country'].str.contains(search_term, case=False, na=False) |
                df_display['capital'].str.contains(search_term, case=False, na=False) |
                df_display['currency'].str.contains(search_term, case=False, na=False) |
                df_display['continent'].str.contains(search_term, case=False, na=False)
            )
            df_display = df_display[search_mask]
        
        # Apply table column sorting
        if table_sort['column']:
            if table_sort['column'] == 'gdp':
                ascending = table_sort['direction'] == 'asc'
                df_display = df_display.sort_values('gdp', key=lambda x: pd.to_numeric(x.str.replace(r'[\$,]', '', regex=True), errors='coerce'), ascending=ascending)
            else:
                ascending = table_sort['direction'] == 'asc'
                df_display = df_display.sort_values(table_sort['column'], ascending=ascending)
        
        # Get the clicked country name
        if clicked_idx < len(df_display):
            country_name = df_display.iloc[clicked_idx]['country']
            return country_name
        return None

    @app.callback(
        Output('world-map', 'figure'),
        [Input('gdp-sort-dropdown', 'value'),
         Input('selected-country-store', 'data')]
    )
    def update_map(sort_order, selected_country):
        return create_map(sort_order, selected_country)

    @app.callback(
        Output('data-table', 'children'),
        [Input('gdp-sort-dropdown', 'value'),
         Input('selected-country-store', 'data'),
         Input('country-search-input', 'value'),
         Input('table-sort-store', 'data')]
    )
    def update_table(sort_order, selected_country, search_term, table_sort):
        search_term = search_term or ''
        table_sort_column = table_sort.get('column', '') if table_sort else ''
        table_sort_direction = table_sort.get('direction', 'asc') if table_sort else 'asc'
        return create_data_table(sort_order, selected_country, search_term, table_sort_column, table_sort_direction)
