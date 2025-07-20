"""
UI components for the trivia module.
"""

from dash import html

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
