"""
Layout components for the trivia module.
"""

from dash import html, dcc
from .quiz_data import get_cards_for_category
from .ui_components import create_quiz_cards_grid, create_hidden_elements

def get_trivia_layout(category='geography'):
    """Get the layout for the trivia page with card-based quiz selection."""
    # Get cards for the specified category
    quiz_cards_data = get_cards_for_category(category)
    
    return html.Div([
        html.Div(id="quiz_type_display", className="quiz-type-display"),

        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area without side panel
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid (dynamically based on category)
                html.Div([
                    create_quiz_cards_grid(quiz_cards_data)
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
