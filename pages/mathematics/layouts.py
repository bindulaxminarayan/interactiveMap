"""
Mathematics quiz page layouts.
"""

from dash import html, dcc
from pages.trivia.ui_components import create_quiz_cards_grid, create_hidden_elements
from pages.trivia.quiz_components import create_username_modal

# Mathematics quiz cards
MATHEMATICS_QUIZ_CARDS = [
    {
        "title": "K-5 Math",
        "emoji": "🔢",
        "description": "Elementary math for grades K-5",
        "button_id": "start-k5-math-quiz",
        "is_disabled": False
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
        dcc.Store(id='quiz-active-store', data={'active': False}),

        # Store for username persistence
        dcc.Store(id='username-store', data={'username': 'anonymous_user'}),

        # Store for pending quiz info
        dcc.Store(id='pending-quiz-store', data={}),

        # Username modal components
        dcc.Store(id='username-modal-store', data={'is_open': False}),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Enter Your Name", style={
                        'textAlign': 'center', 
                        'marginBottom': '20px',
                        'color': '#333'
                    }),
                    html.P("Please enter your name to track your quiz performance:", style={
                        'textAlign': 'center',
                        'marginBottom': '20px',
                        'color': '#666'
                    }),
                    dcc.Input(
                        id='username-input',
                        type='text',
                        placeholder='Enter your name...',
                        value='',
                        style={
                            'width': '100%',
                            'padding': '12px',
                            'fontSize': '16px',
                            'border': '2px solid #dee2e6',
                            'borderRadius': '5px',
                            'marginBottom': '20px',
                            'boxSizing': 'border-box'
                        }
                    ),
                    html.Div([
                        html.Button(
                            "Start Quiz",
                            id='username-confirm-btn',
                            style={
                                'backgroundColor': '#007bff',
                                'color': 'white',
                                'border': 'none',
                                'padding': '12px 24px',
                                'fontSize': '16px',
                                'borderRadius': '5px',
                                'cursor': 'pointer',
                                'marginRight': '10px'
                            }
                        ),
                        html.Button(
                            "Cancel",
                            id='username-cancel-btn',
                            style={
                                'backgroundColor': '#6c757d',
                                'color': 'white',
                                'border': 'none',
                                'padding': '12px 24px',
                                'fontSize': '16px',
                                'borderRadius': '5px',
                                'cursor': 'pointer'
                            }
                        )
                    ], style={'textAlign': 'center'})
                ], style={
                    'backgroundColor': 'white',
                    'padding': '30px',
                    'borderRadius': '10px',
                    'width': '400px',
                    'maxWidth': '90vw',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'position': 'relative'
                })
            ], style={
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'backgroundColor': 'rgba(0, 0, 0, 0.5)',
                'display': 'none',
                'justifyContent': 'center',
                'alignItems': 'center',
                'zIndex': '1000'
            })
        ], id='username-modal'),

        # Hidden dummy buttons for trivia callbacks compatibility
        html.Div([
            html.Button(id='start-currency-quiz', style={'display': 'none'}),
            html.Button(id='start-wonders-quiz', style={'display': 'none'}),
            html.Button(id='start-capital-quiz', style={'display': 'none'}),
            html.Button(id='start-continent-quiz', style={'display': 'none'}),
            html.Button(id='start-flag-quiz', style={'display': 'none'}),
            html.Button(id='start-physical-geography-quiz', style={'display': 'none'}),
            html.Button(id='start-india-capital-quiz', style={'display': 'none'}),
            html.Button(id='start-us-capital-quiz', style={'display': 'none'}),
        ], style={'display': 'none'})

    ], className="app-background")
