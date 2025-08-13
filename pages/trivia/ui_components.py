"""
UI components for the trivia module.
"""

from dash import html, dcc

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
        
        # Hidden dummy buttons for universal callback compatibility
        html.Button("Currency", id='start-currency-quiz', style={'display': 'none'}),
        html.Button("Wonders", id='start-wonders-quiz', style={'display': 'none'}),
        html.Button("Capital", id='start-capital-quiz', style={'display': 'none'}),
        html.Button("Continent", id='start-continent-quiz', style={'display': 'none'}),
        html.Button("Flag", id='start-flag-quiz', style={'display': 'none'}),
        html.Button("Physical Geography", id='start-physical-geography-quiz', style={'display': 'none'}),
        html.Button("India Capital", id='start-india-capital-quiz', style={'display': 'none'}),
        html.Button("US Capital", id='start-us-capital-quiz', style={'display': 'none'}),
        html.Button("Biology", id='start-biology-quiz', style={'display': 'none'}),
        html.Button("Chemistry", id='start-chemistry-quiz', style={'display': 'none'}),
        html.Button("Physics", id='start-physics-quiz', style={'display': 'none'}),
        html.Button("Astronomy", id='start-astronomy-quiz', style={'display': 'none'}),
        html.Button("Earth Science", id='start-earth-science-quiz', style={'display': 'none'}),
        html.Button("Technology", id='start-technology-quiz', style={'display': 'none'}),
        html.Button("Famous", id='start-leaders-quiz', style={'display': 'none'}),
    ], id='hidden-elements-container', style={'display': 'none'})

def create_quiz_button(text, button_id, style_type="primary", margin_right="0px"):
    """Create a standardized quiz button."""
    button_styles = {
        "primary": {
            'backgroundColor': '#28a745',
            'color': 'white'
        },
        "secondary": {
            'backgroundColor': '#007bff', 
            'color': 'white'
        },
        "danger": {
            'backgroundColor': '#dc3545',
            'color': 'white'
        }
    }
    
    base_style = {
        'padding': '20px 40px',
        'fontSize': '20px',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'marginRight': margin_right
    }
    
    base_style.update(button_styles.get(style_type, button_styles["primary"]))
    
    return html.Button(text, id=button_id, style=base_style)

def create_score_display(score, total, percentage, performance_msg, color):
    """Create a score display component."""
    return html.Div([
        html.H3(f"Your Score: {score} out of {total}", 
               style={'textAlign': 'center', 'fontSize': '2rem', 'margin': '20px 0'}),
        html.H4(f"{percentage}%", 
               style={'textAlign': 'center', 'fontSize': '3rem', 'color': color, 'margin': '10px 0'}),
        html.P(performance_msg, 
              style={'textAlign': 'center', 'fontSize': '1.5rem', 'color': color, 'margin': '20px 0'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '10px', 'margin': '20px 0'})

def create_feedback_message(is_correct, correct_answer, fun_fact=None):
    """Create a feedback message for quiz answers."""
    feedback_content = []
    
    if is_correct:
        feedback_content.append(
            html.P("✅ Correct!", style={'fontWeight': 'bold', 'color': '#28a745', 'fontSize': '24px'})
        )
    else:
        feedback_content.extend([
            html.P("❌ Incorrect!", style={'fontWeight': 'bold', 'color': '#dc3545', 'fontSize': '24px'}),
            html.P(f"The correct answer is: {correct_answer}", 
                   style={'fontWeight': 'bold', 'color': '#007bff', 'fontSize': '18px', 'marginTop': '10px'})
        ])
    
    # Add fun fact if provided
    if fun_fact and fun_fact.strip():
        feedback_content.append(
            html.Div([
                html.Hr(style={'margin': '15px 0', 'border': '1px solid #dee2e6'}),
                html.P("💡 Fun Fact:", style={'fontWeight': 'bold', 'color': '#6f42c1', 'fontSize': '18px', 'marginBottom': '8px'}),
                html.P(fun_fact, style={'color': '#333', 'fontSize': '16px', 'lineHeight': '1.5', 'fontStyle': 'italic'})
            ], style={
                'backgroundColor': '#f8f9fa', 
                'padding': '15px', 
                'borderRadius': '8px', 
                'border': '1px solid #dee2e6',
                'marginTop': '15px'
            })
        )
    
    return html.Div(feedback_content)

def create_username_modal():
    """Create a reusable username modal component."""
    return html.Div([
        html.Div([
            html.H3("Enter Your Name", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.P("Enter your name to track your quiz performance, or leave blank to play anonymously.", 
                   style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#666'}),
            dcc.Input(
                id='username-input',
                type='text',
                placeholder='Your name (optional)',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'fontSize': '16px',
                    'border': '1px solid #ddd',
                    'borderRadius': '5px',
                    'marginBottom': '20px'
                }
            ),
            html.Div([
                html.Button('Start Quiz', id='username-confirm-btn', 
                           style={
                               'backgroundColor': '#28a745',
                               'color': 'white',
                               'padding': '10px 20px',
                               'border': 'none',
                               'borderRadius': '5px',
                               'fontSize': '16px',
                               'cursor': 'pointer',
                               'marginRight': '10px'
                           }),
                html.Button('Cancel', id='username-cancel-btn',
                           style={
                               'backgroundColor': '#dc3545',
                               'color': 'white',
                               'padding': '10px 20px',
                               'border': 'none',
                               'borderRadius': '5px',
                               'fontSize': '16px',
                               'cursor': 'pointer'
                           })
            ], style={'textAlign': 'center'})
        ], style={
            'backgroundColor': 'white',
            'padding': '30px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'maxWidth': '400px',
            'width': '90%'
        })
    ], id='username-modal', style={
        'display': 'none',
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'width': '100%',
        'height': '100%',
        'backgroundColor': 'rgba(0, 0, 0, 0.5)',
        'zIndex': '1000'
    })

def create_quiz_stores():
    """Create reusable quiz-related data stores."""
    return [
        dcc.Store(id='quiz-active-store', data={'active': False}),
        dcc.Store(id='username-store', data={'username': ''}),
        dcc.Store(id='pending-quiz-store', data={})
    ]

def create_quiz_layout_structure(quiz_cards_data):
    """Create the standard quiz page layout structure."""
    return html.Div([
        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Username Modal
        create_username_modal(),

        # Main content area
        html.Div([
            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid
                html.Div([
                    create_quiz_cards_grid(quiz_cards_data)
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

        # Quiz stores
        *create_quiz_stores()

    ], className="app-background")
