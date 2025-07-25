"""
Geography quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements

# Geography quiz cards
GEOGRAPHY_QUIZ_CARDS = [
    {
        "title": "Physical Geography",
        "emoji": "🏔️",
        "description": "Landscapes etc",
        "button_id": "start-physical-geography-quiz"
    },
    {
        "title": "Wonders",
        "emoji": "🤩",
        "description": "Wonders of the world!",
        "button_id": "start-wonders-quiz"
    },
    {
        "title": "Flags",
        "emoji": "🏳️",
        "description": "Match a flag with a country!",
        "button_id": "start-flag-quiz"
    },
    {
        "title": "Currencies",
        "emoji": "💰",
        "description": "Match a country with currency!",
        "button_id": "start-currency-quiz"
    },
    {
        "title": "Capitals",
        "emoji": "🏛️",
        "description": "Match a country with capital!",
        "button_id": "start-capital-quiz"
    },
    {
        "title": "Continents",
        "emoji": "🌐",
        "description": "Match a country with continent!",
        "button_id": "start-continent-quiz"
    },
    {
        "title": "US States",
        "emoji": "🇺🇸",
        "description": "Match state with capital!",
        "button_id": "start-us-capital-quiz"
    },
    {
        "title": "India States",
        "emoji": "🇮🇳",
        "description": "Match state with capital!",
        "button_id": "start-india-capital-quiz"
    }
]

def get_geography_layout():
    """Get the layout for the geography quiz page."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(GEOGRAPHY_QUIZ_CARDS)
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
        dcc.Store(id='quiz-active-store', data={'active': False}),

        # Store for username persistence
        dcc.Store(id='username-store', data={'username': 'anonymous_user'}),

        # Store for pending quiz info
        dcc.Store(id='pending-quiz-store', data={}),

        # Username modal components
        dcc.Store(id='username-modal-store', data={'is_open': False}),
        html.Div([
            html.Div([
                html.H3("Enter Your Name", className='username-modal-title'),
                html.P("Please enter your name to track your quiz performance:", 
                       className='username-modal-subtitle'),
                dcc.Input(
                    id='username-input',
                    type='text',
                    placeholder='Enter your name...',
                    value='',
                    className='username-input'
                ),
                html.Div([
                    html.Button(
                        "Start Quiz",
                        id='username-confirm-btn',
                        className='username-modal-button username-modal-button-primary'
                    ),
                    html.Button(
                        "Cancel",
                        id='username-cancel-btn',
                        className='username-modal-button username-modal-button-secondary'
                    )
                ], className='username-modal-buttons')
            ], className='username-modal-content')
        ], id='username-modal', className='username-modal', style={'display': 'none'}),

        # Hidden dummy button for trivia callbacks compatibility
        html.Div([
            html.Button(id='start-k5-math-quiz', style={'display': 'none'}),
        ], style={'display': 'none'})

    ], className="app-background")
