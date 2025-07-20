"""
History quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements

# History quiz cards
HISTORY_QUIZ_CARDS = [
    {
        "title": "World History",
        "emoji": "🌍",
        "description": "Major world historical events",
        "button_id": "start-world-history-quiz",
        "is_disabled": True
    },
    {
        "title": "Ancient Civilizations",
        "emoji": "🏛️",
        "description": "Learn about ancient civilizations",
        "button_id": "start-ancient-civilizations-quiz",
        "is_disabled": True
    },
    {
        "title": "Wars & Conflicts",
        "emoji": "⚔️",
        "description": "Historical wars and conflicts",
        "button_id": "start-wars-quiz",
        "is_disabled": True
    },
    {
        "title": "Famous Leaders",
        "emoji": "👑",
        "description": "Historical leaders and rulers",
        "button_id": "start-leaders-quiz",
        "is_disabled": True
    },
    {
        "title": "Inventions",
        "emoji": "💡",
        "description": "Historical inventions and discoveries",
        "button_id": "start-inventions-quiz",
        "is_disabled": True
    },
    {
        "title": "Dates & Timeline",
        "emoji": "📅",
        "description": "Important historical dates",
        "button_id": "start-dates-quiz",
        "is_disabled": True
    }
]

def get_history_layout():
    """Get the layout for the history quiz page."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(HISTORY_QUIZ_CARDS)
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
            ], id="main-content-area", className="main-content-area"),

        ], id="main-layout-container-wrapper", className="main-layout-container"),

        # Hidden dcc.Store to track if a quiz is active
        dcc.Store(id='quiz-active-store', data={'active': False})

    ], className="app-background")
