"""
Main application file for the Interactive World Map.
Includes navigation and multi-page layout.
"""

import dash
from dash import html, dcc, Input, Output
import logging

# Import page modules
from pages.explore import get_explore_layout, register_explore_callbacks
from pages.trivia import get_trivia_layout, register_trivia_callbacks
from components.navbar import create_simple_navbar

print("--- Script starting ---")
print("--- Imports successful ---")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Main app layout with navigation and page content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_simple_navbar(),
    html.Div(id='page-content')
])

# Callback for updating page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search')]
)
def display_page(pathname, search):
    """Route to different pages based on URL pathname and query parameters."""
    if pathname == '/trivia':
        # Parse category from query parameters
        category = 'geography'  # default
        if search:
            # Parse query string (e.g., "?category=geography")
            from urllib.parse import parse_qs
            params = parse_qs(search.lstrip('?'))
            if 'category' in params:
                category = params['category'][0]
        return get_trivia_layout(category)
    else:  # Default to explore page
        return get_explore_layout()

# Register callbacks for each page
register_explore_callbacks(app)
register_trivia_callbacks(app)


# Run the app
if __name__ == '__main__':
    logging.info("--- Starting Dash server... ---")
    app.run(debug=True, host='0.0.0.0', port=8050)
else:
    logging.error(f"--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '{__name__}') ---")
