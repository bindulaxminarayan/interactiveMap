"""
Main application file for the Interactive World Map.
Includes navigation and multi-page layout.
"""
import logging
from urllib.parse import parse_qs
import dash
from dash import html, dcc, Input, Output
logging.basicConfig(level=logging.DEBUG)

# Import page modules
from pages.explore import get_explore_layout, register_explore_callbacks
from pages.trivia.universal_callbacks import register_universal_username_modal_callbacks
from pages.trivia import get_trivia_layout, register_trivia_callbacks
from pages.geography import get_geography_layout
from pages.history import get_history_layout
from pages.science import get_science_layout
from pages.mathematics import get_mathematics_layout
from pages.sports import get_sports_layout
from pages.analytics import get_analytics_layout, register_analytics_callbacks
from components.navbar import create_simple_navbar


# Initialize the Dash app
logging.debug("Initializing the app...")
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
    elif pathname == '/analytics':
        return get_analytics_layout()
    elif pathname == '/trivia':
        category = 'geography'  # default
        if search:
            params = parse_qs(search.lstrip('?'))
            if 'category' in params:
                category = params['category'][0]
        return get_trivia_layout(category)
    else:
        return get_explore_layout()

# Dynamic title update using clientside callback.
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
                        'physical': 'Physical Geography',
                        'india_capital': 'India States',
                        'us_capital': 'US States',
                        'biology': 'Biology',
                        'chemistry': 'Chemistry',
                        'famous_people':'Famous'
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

#Register call backs
register_universal_username_modal_callbacks(app)
register_explore_callbacks(app)
register_trivia_callbacks(app)
register_analytics_callbacks(app)


# Run the app
if __name__ == '__main__':
    logging.info("--- Starting Dash server... ---")
    app.run(host='0.0.0.0', port=8050)
else:
    logging.error("--- SCRIPT WAS IMPORTED, NOT RUN DIRECTLY. (__name__ is '%s') ---", __name__)
