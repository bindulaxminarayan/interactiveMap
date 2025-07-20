"""
Mathematics quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements

# Mathematics quiz cards
MATHEMATICS_QUIZ_CARDS = [
    {
        "title": "K-5 Math",
        "emoji": "🔢",
        "description": "Elementary math for grades K-5",
        "button_id": "start-k5-math-quiz",
        "is_disabled": True
    },
    {
        "title": "6-8 Math",
        "emoji": "📐",
        "description": "Middle school mathematics",
        "button_id": "start-middle-math-quiz",
        "is_disabled": True
    },
    {
        "title": "Algebra",
        "emoji": "🔡",
        "description": "Basic and advanced algebra",
        "button_id": "start-algebra-quiz",
        "is_disabled": True
    },
    {
        "title": "Geometry",
        "emoji": "📏",
        "description": "Shapes, angles, and measurements",
        "button_id": "start-geometry-quiz",
        "is_disabled": True
    },
    {
        "title": "Calculus",
        "emoji": "∫",
        "description": "Differential and integral calculus",
        "button_id": "start-calculus-quiz",
        "is_disabled": True
    },
    {
        "title": "Statistics",
        "emoji": "📊",
        "description": "Data analysis and probability",
        "button_id": "start-statistics-quiz",
        "is_disabled": True
    }
]

def get_mathematics_layout():
    """Get the layout for the mathematics quiz page."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(MATHEMATICS_QUIZ_CARDS)
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
