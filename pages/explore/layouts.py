"""
Layout components for the explore page.
"""

from dash import html, dcc

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
