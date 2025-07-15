"""
Layout components for the trivia module.
"""

from dash import html, dcc

# World quiz cards
WORLD_QUIZ_CARDS_DATA = [
    {
        "title": "General",
        "emoji": "🌎",
        "description": "Match countries, capital, currencies!",
        "button_id": "start-country-quiz"
    },
    {
        "title": "Currencies",
        "emoji": "💰",
        "description": "Match countries with their currencies!",
        "button_id": "start-currency-quiz"
    },
    {
        "title": "Capital Cities",
        "emoji": "🏛️",
        "description": "Match countries with their capitals!",
        "button_id": "start-capital-quiz"
    },
    {
        "title": "Continents",
        "emoji": "🌐",
        "description": "Match countries with their continents!",
        "button_id": "start-continent-quiz"
    },
    {
        "title": "Flags",
        "emoji": "🇺🇳",
        "description": "Match flag with their countries!",
        "button_id": "start-flag-quiz"
    },
]

US_QUIZ_CARDS_DATA = [{
        "title": "Capital Cities",
        "emoji": "🏛️",
        "description": "Match states and capitals!",
        "button_id": "start-us-capital-quiz"
    }]

def create_side_panel():
    """Create a side panel with category labels."""
    return html.Div([
        html.H2("Select a category", className="side-panel-title"),
        html.Button("World", id="category-world", className="category-button category-button-active"), # Default active
        html.Button("United States", id="category-us", className="category-button"),
        html.Button("India", id="category-india", className="category-button"),
        html.Button("China", id="category-china", className="category-button"),
    ], id="side-panel", className="side-panel-container")

def create_quiz_card(title, emoji, description, button_id, is_disabled=False):
    """Create a quiz card with title, description and button."""
    # Determine dynamic styles based on is_disabled
    wrapper_style = {
        'opacity': '1' if not is_disabled else '0.7',
    }
    title_style = {
        'color': '#007bff' if not is_disabled else '#6c757d',
    }
    description_style = {
        'color': '#666' if not is_disabled else '#999',
    }
    button_style = {
        'backgroundColor': '#28a745' if not is_disabled else '#6c757d',
        'cursor': 'pointer' if not is_disabled else 'not-allowed',
        'opacity': '1' if not is_disabled else '0.6',
    }

    return html.Div([
        html.Div([
            html.H3(f"{emoji} {title}", className="quiz-card-title", style=title_style),
            html.P(description, className="quiz-card-description", style=description_style),
            html.Button("Start Quiz", # Updated button text
                       id=button_id,
                       disabled=is_disabled,
                       className="quiz-card-button",
                       style=button_style,
                       n_clicks=0)  # Ensure button has n_clicks property
        ], className='quiz-card-inner-container') # Renamed to avoid conflict with outer wrapper class
    ], className='quiz-card-container', style=wrapper_style) # Apply opacity to wrapper

def create_quiz_cards_grid(quiz_cards_data):
    """
    Create a grid of quiz cards from a list of quiz card data.
    This function is now dynamic based on the provided data.
    """
    cards = []
    # Split cards into two rows for better layout if there are many cards
    # For simplicity, we'll just put them all in one flex container for now
    # and let flex-wrap handle it.
    for card_data in quiz_cards_data:
        cards.append(
            create_quiz_card(
                title=card_data["title"],
                emoji=card_data["emoji"],
                description=card_data["description"],
                button_id=card_data["button_id"],
                is_disabled=card_data.get("is_disabled", False) # Allow disabling via data
            )
        )

    return html.Div(cards, className="quiz-cards-grid-container-inner") # New inner container for flex-wrap

def create_hidden_elements():
    """Create hidden elements that callbacks need to reference."""
    return html.Div([
        # Other hidden elements (no quiz start buttons here)
        html.Button("Restart Currency", id="restart-currency-quiz-result", style={'display': 'none'}),
        html.Button("Restart Capital", id="restart-capital-quiz-result", style={'display': 'none'}),
        html.Button("Restart Continent", id="restart-continent-quiz-result", style={'display': 'none'}),
        html.Button("Restart Country", id="restart-country-quiz-result", style={'display': 'none'}),
        html.Button("Restart Flag", id="restart-flag-quiz-result", style={'display': 'none'}),
        html.Button("Restart Current", id="restart-current-quiz", style={'display': 'none'}),
        html.Button("Next Question", id='next-btn', style={'display': 'none'}),
        html.Button("View Results", id='view-results-btn', style={'display': 'none'}),
        html.Button("Quit Quiz", id='quit-quiz-btn', style={'display': 'none'}),
        html.Button("Back to Selection", id="back-to-selection", style={'display': 'none'}),
        html.Button("", id='answer-btn-0', style={'display': 'none'}),
        html.Button("", id='answer-btn-1', style={'display': 'none'}),
        html.Button("", id='answer-btn-2', style={'display': 'none'}),
        html.Button("", id='answer-btn-3', style={'display': 'none'}),
    ], id='hidden-elements-container', style={'display': 'none'})

def get_trivia_layout():
    """Get the layout for the trivia page with card-based quiz selection."""
    return html.Div([
        html.H1("World Trivia", className="main-title"),
        html.Div(id="quiz_type_display", className="quiz-type-display"),

        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area with side panel and quiz content
        html.Div([
            # Side Panel
            create_side_panel(),

            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid (initially displayed with World data)
                html.Div([
                    create_quiz_cards_grid(WORLD_QUIZ_CARDS_DATA)
                ], id="quiz-selection-area"), # This will be hidden when quiz starts

                # Quiz Content Area (initially hidden)
                html.Div([
                    # Progress bar container (initially hidden)
                    html.Div(id="progress-container", children=[], style={'display': 'none'}),

                    # Question container
                    html.Div(id="question-container", children=[]),

                    # Hidden storage for current question
                    dcc.Store(id='current-question-store', data={'index': 0, 'score': 0}),

                    # Hidden trigger for button clicks
                    html.Div(id='hidden-trigger', style={'display': 'none'}),

                    # Results area
                    html.Div(id="results-area", style={'marginTop': '30px'}),

                ], id="quiz-content-area", className="quiz-content-area", style={'display': 'none'}) # Initially hidden
            ], id="main-content-area", className="main-content-area"), # This will expand

        ], id="main-layout-container-wrapper", className="main-layout-container"), # Added id="main-layout-container-wrapper"

        # Hidden dcc.Store to track if a quiz is active
        dcc.Store(id='quiz-active-store', data={'active': False})

    ], className="app-background")
