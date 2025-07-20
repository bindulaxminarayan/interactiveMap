"""
Science quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements

# Science quiz cards
SCIENCE_QUIZ_CARDS = [
    {
        "title": "Physics",
        "emoji": "⚛️",
        "description": "Laws of physics and motion",
        "button_id": "start-physics-quiz",
        "is_disabled": True
    },
    {
        "title": "Chemistry",
        "emoji": "🧪",
        "description": "Elements and chemical reactions",
        "button_id": "start-chemistry-quiz",
        "is_disabled": True
    },
    {
        "title": "Biology",
        "emoji": "🧬",
        "description": "Life sciences and living organisms",
        "button_id": "start-biology-quiz",
        "is_disabled": True
    },
    {
        "title": "Astronomy",
        "emoji": "🌌",
        "description": "Space, stars, and planets",
        "button_id": "start-astronomy-quiz",
        "is_disabled": True
    },
    {
        "title": "Earth Science",
        "emoji": "🌍",
        "description": "Geology, weather, and climate",
        "button_id": "start-earth-science-quiz",
        "is_disabled": True
    },
    {
        "title": "Technology",
        "emoji": "💻",
        "description": "Modern technology and computing",
        "button_id": "start-technology-quiz",
        "is_disabled": True
    }
]

def get_science_layout():
    """Get the layout for the science quiz page."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(SCIENCE_QUIZ_CARDS)
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
