"""
Layout components for the trivia module.
"""

from dash import html, dcc

def create_quiz_card(title, emoji, description, button_text, button_id, is_disabled=False):
    """Create a quiz card with title, description and button."""
    return html.Div([
        html.Div([
            html.H3(f"{emoji} {title}", style={
                'textAlign': 'center',
                'marginBottom': '15px',
                'color': '#007bff' if not is_disabled else '#6c757d',
                'fontWeight': 'bold',
                'fontSize': '24px'
            }),
            html.P(description, style={
                'textAlign': 'center',
                'margin': '15px 0 25px 0',
                'fontSize': '16px',
                'color': '#666' if not is_disabled else '#999',
                'lineHeight': '1.5'
            }),
            html.Button(button_text, 
                       id=button_id,
                       disabled=is_disabled,
                       style={
                           'width': '100%',
                           'padding': '15px 20px',
                           'backgroundColor': '#28a745' if not is_disabled else '#6c757d',
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '8px',
                           'cursor': 'pointer' if not is_disabled else 'not-allowed',
                           'fontSize': '16px',
                           'fontWeight': 'bold',
                           'opacity': '1' if not is_disabled else '0.6',
                           'transition': 'all 0.3s ease'
                       })
        ])
    ], style={
        'backgroundColor': '#ffffff',
        'borderRadius': '15px',
        'border': '1px solid #dee2e6',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'padding': '30px',
        'margin': '15px',
        'width': '280px',
        'height': '220px',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'opacity': '1' if not is_disabled else '0.7'
    }, className='quiz-card')

def create_quiz_cards_grid():
    """Create a grid of quiz cards."""
    return html.Div([
        # First row
        html.Div([
              create_quiz_card(
                title="General country quiz",
                emoji="🏛️",
                description="Match countries, capital, currencies!",
                button_text="Start Country Quiz",
                button_id="start-country-quiz"
            ),
            create_quiz_card(
                title="Currencies",
                emoji="💰",
                description="Match countries with their currencies!",
                button_text="Start Currency Quiz",
                button_id="start-currency-quiz"
            ),
            create_quiz_card(
                title="Capital Cities",
                emoji="🏛️",
                description="Match countries with their capitals!",
                button_text="Start Capital Quiz",
                button_id="start-capital-quiz"
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'flexWrap': 'wrap',
            'marginBottom': '20px'
        }),
        
        # Second row
        html.Div([
            create_quiz_card(
                title="Country Continent",
                emoji="🌐",
                description="Match countries with their continents!",
                button_text="Start Continent Quiz",
                button_id="start-continent-quiz"
            ),
            create_quiz_card(
                title="Flag countries",
                emoji="🇺🇳",
                description="Match flag with their countries!",
                button_text="Start Flag Quiz",
                button_id="start-flag-quiz"
            ),
            create_quiz_card(
                title="Locate Countries",
                emoji="🗺️",
                description="Find countries on the map!",
                button_text="Coming Soon",
                button_id="locate-countries-quiz",
                is_disabled=True
            )
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'flexWrap': 'wrap'
        })
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'padding': '20px'
    })

def create_hidden_elements():
    """Create hidden elements that callbacks need to reference."""
    return html.Div([
        html.Button("Restart Currency", id="restart-currency-quiz-result", style={'display': 'none'}),
        html.Button("Restart Capital", id="restart-capital-quiz-result", style={'display': 'none'}),
        html.Button("Restart Continent", id="restart-continent-quiz-result", style={'display': 'none'}),
        html.Button("Restart Country", id="restart-country-quiz-result", style={'display': 'none'}),
        html.Button("Restart Flag", id="restart-flag-quiz-result", style={'display': 'none'}),
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
        html.H1("Country Trivia", style={
            'textAlign': 'center', 
            'marginBottom': '40px',
            'color': '#333',
            'fontSize': '48px',
            'fontWeight': 'bold'
        }),
        
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),
        
        # Quiz selection area or active quiz area
        html.Div([
            # Quiz Cards Grid (initially displayed)
            html.Div([
                create_quiz_cards_grid()
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
                
            ], id="quiz-content-area", style={
                'display': 'none',
                'backgroundColor': '#ffffff',
                'borderRadius': '15px',
                'border': '1px solid #dee2e6',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'padding': '30px',
                'margin': '20px auto',
                'maxWidth': '800px',
                'minHeight': '500px'
            })
            
        ], id="main-content", style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '20px'
        }),
        
    ])
