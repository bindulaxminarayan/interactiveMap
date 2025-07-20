"""
Table components and utilities for the explore page.
"""

import pandas as pd
from dash import html
from utils.data_processing import load_countries_data

# Load the data
df = load_countries_data()

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
