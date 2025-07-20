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
from pages.geography import get_geography_layout, register_geography_callbacks
from pages.history import get_history_layout, register_history_callbacks
from pages.science import get_science_layout, register_science_callbacks
from pages.mathematics import get_mathematics_layout, register_mathematics_callbacks
from pages.sports import get_sports_layout, register_sports_callbacks
from components.navbar import create_simple_navbar

print("--- Script starting ---")
print("--- Imports successful ---")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Quizverse")
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
    """Route to different pages based on URL pathname."""
    if pathname == '/geography':
        return get_geography_layout()
    elif pathname == '/history':
        return get_history_layout()
    elif pathname == '/science':
        return get_science_layout()
    elif pathname == '/mathematics':
        return get_mathematics_layout()
    elif pathname == '/sports':
        return get_sports_layout()
    elif pathname == '/trivia':
        # Keep backward compatibility for old trivia route
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

# Dynamic title update using clientside callback
app.clientside_callback(
    """
    function(pathname) {
        // Base title
        var base_title = "Quizverse";
        
        // Add page context
        var page_title = "Explore";
        if (pathname === '/geography') {
            page_title = "Geography";
        } else if (pathname === '/history') {
            page_title = "History";
        } else if (pathname === '/science') {
            page_title = "Science";
        } else if (pathname === '/mathematics') {
            page_title = "Mathematics";
        } else if (pathname === '/sports') {
            page_title = "Sports";
        }
        
        // Check if quiz elements exist (only on quiz pages)
        var quizActiveStore = document.getElementById('quiz-active-store');
        var currentQuestionStore = document.getElementById('current-question-store');
        
        if (quizActiveStore && currentQuestionStore) {
            try {
                var quiz_active_data = JSON.parse(quizActiveStore.getAttribute('data-data') || '{}');
                var current_data = JSON.parse(currentQuestionStore.getAttribute('data-data') || '{}');
                
                // Check if quiz is active and add subcategory
                if (quiz_active_data && quiz_active_data.active && current_data && current_data.quiz_type) {
                    var quiz_type = current_data.quiz_type;
                    
                    // Convert quiz_type to readable format
                    var quiz_type_mapping = {
                        'currency': 'Currencies',
                        'wonders': 'Wonders', 
                        'capital': 'Capitals',
                        'continent': 'Continents',
                        'flag': 'Flags',
                        'world_physical_geography': 'Physical Geography',
                        'india_capital': 'India States',
                        'us_capital': 'US States'
                    };
                    
                    var subcategory = quiz_type_mapping[quiz_type] || quiz_type.charAt(0).toUpperCase() + quiz_type.slice(1);
                    document.title = base_title + "-" + page_title + "-" + subcategory;
                    return null;
                }
            } catch (e) {
                // If parsing fails, just use the page title
            }
        }
        
        // Default title format
        document.title = base_title + "-" + page_title;
        return null;
    }
    """,
    Output('page-content', 'data-title'),  # Use a data attribute that doesn't affect display
    [Input('url', 'pathname')]
)


# Navbar auto-hide functionality during quiz
app.clientside_callback(
    """
    function(navbar_auto_hide) {
        var navbar = document.querySelector('.navbar');
        var pageContent = document.querySelector('#page-content');
        
        if (navbar_auto_hide === "hide") {
            // Quiz is active - hide navbar and add autohide class
            if (navbar) {
                navbar.classList.add('navbar-autohide');
            }
            if (pageContent) {
                pageContent.classList.add('content-with-autohide-navbar');
            }
        } else {
            // Quiz is not active - show navbar normally
            if (navbar) {
                navbar.classList.remove('navbar-autohide');
            }
            if (pageContent) {
                pageContent.classList.remove('content-with-autohide-navbar');
            }
        }
        
        return null;
    }
    """,
    Output('page-content', 'data-navbar-processed'),  # Use a data attribute
    [Input('page-content', 'data-navbar-auto-hide')]
)

# Register callbacks for each page
register_explore_callbacks(app)
register_trivia_callbacks(app)  # Only register trivia callbacks once
# Note: geography, history, science, mathematics, and sports all use trivia callbacks
# so we don't need to register them separately to avoid duplicate callback errors


# Run the app
if __name__ == '__main__':
    logging.info("--- Starting Dash server... ---")
    app.run(debug=True, host='0.0.0.0', port=8050)
else:
    logging.error(f"--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '{__name__}') ---")
