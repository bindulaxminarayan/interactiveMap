"""
Layout components for the trivia module.
"""

from dash import html, dcc
from .components import create_quiz_category_section, create_welcome_content

def create_side_panel():
    """Create the side panel with quiz categories."""
    return html.Div([
        html.H3("Quiz Categories", style={
            'textAlign': 'center', 
            'marginBottom': '20px',
            'color': '#333',
            'borderBottom': '2px solid #007bff',
            'paddingBottom': '10px'
        }),
        
        # Currencies Section
        create_quiz_category_section(
            title="Currencies",
            emoji="💰",
            description="Test your knowledge of world currencies!",
            button_text="Start Currency Quiz",
            button_id="start-currency-quiz"
        ),
        
        # Capitals Section
        create_quiz_category_section(
            title="Capital Cities",
            emoji="🏛️",
            description="Match countries with their capitals!",
            button_text="Start Capital Quiz",
            button_id="start-capital-quiz"
        ),
        
        # Future Quiz Categories (Coming Soon)
        create_quiz_category_section(
            title="Locate Countries",
            emoji="🗺️",
            description="Find countries on the map!",
            button_text="Coming Soon",
            button_id="locate-countries-quiz",
            is_disabled=True
        )
        
    ], style={
        'width': '280px',
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'border': '1px solid #dee2e6',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'fit-content'
    })

def create_hidden_elements():
    """Create hidden elements that callbacks need to reference."""
    return html.Div([
        html.Button("Restart Currency", id="restart-currency-quiz-result", style={'display': 'none'}),
        html.Button("Restart Capital", id="restart-capital-quiz-result", style={'display': 'none'}),
        html.Button("Next Question", id='next-btn', style={'display': 'none'}),
        html.Button("Quit Quiz", id='quit-quiz-btn', style={'display': 'none'}),
        html.Button("Back to Selection", id="back-to-selection", style={'display': 'none'}),
        html.Button("", id='answer-btn-0', style={'display': 'none'}),
        html.Button("", id='answer-btn-1', style={'display': 'none'}),
        html.Button("", id='answer-btn-2', style={'display': 'none'}),
        html.Button("", id='answer-btn-3', style={'display': 'none'}),
    ], style={'display': 'none'})

def get_trivia_layout():
    """Get the layout for the trivia page with side panel."""
    return html.Div([
        html.H1("Country Trivia", style={'textAlign': 'center', 'marginBottom': '30px'}),
        
        # Main content area with side panel and quiz area
        html.Div([
            # Side Panel (conditionally displayed)
            html.Div([
                create_side_panel()
            ], id="side-panel", style={
                'width': '300px',
                'marginRight': '30px',
                'flexShrink': '0'
            }),
            
            # Quiz Content Area
            html.Div([
                # Progress bar container (initially hidden)
                html.Div(id="progress-container", children=[], style={'display': 'none'}),
                
                html.Div(id="question-container", children=[
                    create_welcome_content()
                ]),
                
                # Hidden storage for current question
                dcc.Store(id='current-question-store', data={'index': 0, 'score': 0}),
                
                # Hidden elements that callbacks need to reference
                create_hidden_elements(),
                
                # Hidden trigger for button clicks
                html.Div(id='hidden-trigger', style={'display': 'none'}),
                
                # Results area
                html.Div(id="results-area", style={'marginTop': '30px'}),
                
            ], style={
                'flex': '1',
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'border': '1px solid #dee2e6',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'minHeight': '500px'
            })
            
        ], id="main-content", style={
            'display': 'flex',
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '20px'
        })
    ])
