"""
Callbacks for the explore page.
"""

import pandas as pd
import json
from dash import Input, Output, State, ctx, ALL
from .map_components import create_map
from .table_components import create_data_table
from utils.data_processing import load_countries_data

# Load the data
df = load_countries_data()

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
