"""
Sports quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements

# Sports quiz cards
SPORTS_QUIZ_CARDS = [
    {
        "title": "Soccer/Football",
        "emoji": "⚽",
        "description": "World's most popular sport",
        "button_id": "start-soccer-quiz",
        "is_disabled": True
    },
    {
        "title": "Basketball",
        "emoji": "🏀",
        "description": "NBA, college basketball, and more",
        "button_id": "start-basketball-quiz",
        "is_disabled": True
    },
    {
        "title": "Baseball",
        "emoji": "⚾",
        "description": "America's pastime",
        "button_id": "start-baseball-quiz",
        "is_disabled": True
    },
    {
        "title": "American Football",
        "emoji": "🏈",
        "description": "NFL and college football",
        "button_id": "start-american-football-quiz",
        "is_disabled": True
    },
    {
        "title": "Tennis",
        "emoji": "🎾",
        "description": "Grand slams and tournaments",
        "button_id": "start-tennis-quiz",
        "is_disabled": True
    },
    {
        "title": "Olympics",
        "emoji": "🏅",
        "description": "Summer and winter Olympics",
        "button_id": "start-olympics-quiz",
        "is_disabled": True
    }
]

def get_sports_layout():
    """Get the layout for the sports quiz page."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(SPORTS_QUIZ_CARDS)
                ], id="quiz-selection-area"),

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

                ], id="quiz-content-area", className="quiz-content-area", style={'display': 'none'})
            ], id="main-content-area", className="main-content-area"),

        ], id="main-layout-container-wrapper", className="main-layout-container"),

        # Hidden dcc.Store to track if a quiz is active
        dcc.Store(id='quiz-active-store', data={'active': False})

    ], className="app-background")
