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
            'fontSize': '1.5rem',
            'opacity': '1' if not is_disabled else '0.7'
        }),
        html.Div([
            html.P(description, 
                   style={'margin': '10px 0', 'fontSize': '18px', 
                          'color': '#666' if not is_disabled else '#999'}),
            html.Button(button_text, 
                       id=button_id,
                       disabled=is_disabled,
                       style={
                           'width': '100%',
                           'padding': '15px',
                           'backgroundColor': '#28a745' if not is_disabled else '#6c757d',
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '5px',
                           'cursor': 'pointer' if not is_disabled else 'not-allowed',
                           'fontSize': '18px',
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
