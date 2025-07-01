"""
Reusable UI components for the trivia module.
"""

from dash import html

def create_quiz_category_section(title, emoji, description, button_text, button_id, is_disabled=False):
    """Create a quiz category section with title, description and button."""
    return html.Div([
        html.H4(f"{emoji} {title}", style={
            'backgroundColor': '#f8f9fa',
            'padding': '15px',
            'margin': '0 0 10px 0',
            'borderRadius': '8px',
            'cursor': 'pointer' if not is_disabled else 'default',
            'border': '2px solid #007bff' if not is_disabled else '2px solid #dee2e6',
            'color': '#007bff' if not is_disabled else '#6c757d',
            'fontWeight': 'bold',
            'opacity': '1' if not is_disabled else '0.7'
        }),
        html.Div([
            html.P(description, 
                   style={'margin': '10px 0', 'fontSize': '14px', 
                          'color': '#666' if not is_disabled else '#999'}),
            html.Button(button_text, 
                       id=button_id,
                       disabled=is_disabled,
                       style={
                           'width': '100%',
                           'padding': '10px',
                           'backgroundColor': '#28a745' if not is_disabled else '#6c757d',
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '5px',
                           'cursor': 'pointer' if not is_disabled else 'not-allowed',
                           'fontSize': '14px',
                           'fontWeight': 'bold',
                           'opacity': '1' if not is_disabled else '0.6'
                       })
        ], style={'padding': '0 15px 15px 15px'})
    ], style={'marginBottom': '15px'})

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
        'padding': '15px 30px',
        'fontSize': '16px',
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
               style={'textAlign': 'center', 'fontSize': '24px', 'margin': '20px 0'}),
        html.H4(f"{percentage}%", 
               style={'textAlign': 'center', 'fontSize': '36px', 'color': color, 'margin': '10px 0'}),
        html.P(performance_msg, 
              style={'textAlign': 'center', 'fontSize': '20px', 'color': color, 'margin': '20px 0'})
    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '10px', 'margin': '20px 0'})

def create_feedback_message(is_correct, correct_answer, explanation):
    """Create a feedback message for quiz answers."""
    if is_correct:
        return html.Div([
            html.P("✅ Correct!", style={'fontWeight': 'bold', 'color': '#28a745', 'fontSize': '18px'}),
            html.P(explanation, style={'fontStyle': 'italic'}),
        ])
    else:
        return html.Div([
            html.P("❌ Incorrect!", style={'fontWeight': 'bold', 'color': '#dc3545', 'fontSize': '18px'}),
            html.P(f"Correct answer: {correct_answer}", 
                   style={'fontWeight': 'bold', 'color': '#28a745'}),
            html.P(explanation, style={'fontStyle': 'italic'}),
        ])

def create_welcome_content():
    """Create the welcome content for the trivia page."""
    return html.Div([
        html.H2("Welcome to Country Trivia! 🌍", 
               style={'textAlign': 'center', 'color': '#007bff', 'marginBottom': '20px'}),
        html.P("Select a quiz category from the panel on the left to get started!", 
               style={'textAlign': 'center', 'fontSize': '18px', 'color': '#666'})
    ], style={'textAlign': 'center', 'padding': '60px 20px'})
