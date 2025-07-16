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
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to different pages based on URL pathname."""
    if pathname == '/trivia':
        return get_trivia_layout()
    else:  # Default to explore page
        return get_explore_layout()

# Register callbacks for each page
register_explore_callbacks(app)
register_trivia_callbacks(app)

# Add custom CSS for the navbar
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .navbar {
                background-color: #007bff;
                padding: 1rem;
                margin-bottom: 2rem;
            }
            .navbar-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            .navbar-brand {
                font-size: 1.75rem;
                font-weight: bold;
                color: white;
                text-decoration: none;
            }
            .navbar-brand:hover {
                color: #f8f9fa;
            }
            .navbar-nav {
                display: flex;
                gap: 1rem;
            }
            .nav-link {
                color: white;
                text-decoration: none;
                padding: 0.5rem 1rem;
                border-radius: 0.25rem;
                transition: background-color 0.3s;
            }
            .nav-link:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    logging.info("--- Starting Dash server... ---")
    app.run(debug=True, host='0.0.0.0', port=8050)
else:
    logging.error(f"--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '{__name__}') ---")
