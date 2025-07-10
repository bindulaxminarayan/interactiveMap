"""
Quiz-specific UI components for the trivia module.
"""

from dash import html
from .components import create_quiz_button, create_score_display

def create_progress_bar(current_question, total_questions, show_next_button=False, show_view_results_button=False, show_quit_quiz_button=True):
    """Create a progress bar showing quiz progress."""
    progress_percentage = ((current_question + 1) / total_questions) * 100
    remaining_questions = total_questions - (current_question + 1)
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(f"Question {current_question + 1} of {total_questions}", 
                         style={'fontWeight': 'bold', 'color': '#007bff'}),
                html.Span(f"{remaining_questions} questions remaining", 
                         style={'color': '#6c757d', 'fontSize': '14px'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '10px'}),
            
            # Progress bar container
            html.Div([
                html.Div(
                    style={
                        'width': f'{progress_percentage}%',
                        'height': '10px',
                        'backgroundColor': '#28a745',
                        'borderRadius': '5px',
                        'transition': 'width 0.3s ease'
                    }
                )
            ], style={
                'width': '100%',
                'height': '10px',
                'backgroundColor': '#e9ecef',
                'borderRadius': '5px',
                'overflow': 'hidden'
            }),
            
            # Buttons container
            html.Div([
                html.Button("Next Question", id='next-btn', 
                           style={
                               'padding': '8px 16px', 
                               'fontSize': '14px',
                               'backgroundColor': '#28a745', 
                               'color': 'white',
                               'border': 'none', 
                               'borderRadius': '5px', 
                               'cursor': 'pointer',
                               'marginTop': '10px',
                               'marginRight': '10px'
                           } if show_next_button else {'display': 'none'}),
                html.Button("View Results", id='view-results-btn', 
                           style={
                               'padding': '8px 16px', 
                               'fontSize': '14px',
                               'backgroundColor': '#007bff', 
                               'color': 'white',
                               'border': 'none', 
                               'borderRadius': '5px', 
                               'cursor': 'pointer',
                               'marginTop': '10px',
                               'marginRight': '10px'
                           } if show_view_results_button else {'display': 'none'}),
                html.Button("Quit Quiz", id='quit-quiz-btn', 
                           style={
                               'padding': '8px 16px', 
                               'fontSize': '14px',
                               'backgroundColor': '#dc3545', 
                               'color': 'white',
                               'border': 'none', 
                               'borderRadius': '5px', 
                               'cursor': 'pointer',
                               'marginTop': '10px'
                           }if show_quit_quiz_button else {'display': 'none'})
            ], style={'textAlign': 'right'})
        ])
    ], style={
        'padding': '20px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '8px',
        'marginBottom': '20px',
        'border': '1px solid #dee2e6'
    })

def get_answer_button_style(option_index, question_data, selected_answer=None, is_answered=False):
    """Get the style for answer buttons based on state."""
    base_style = {
        'display': 'block', 
        'width': '100%', 
        'margin': '10px 0',
        'padding': '15px', 
        'fontSize': '16px', 
        'borderRadius': '5px', 
        'textAlign': 'left'
    }
    
    if is_answered:
        if option_index == question_data['correct']:
            # Correct answer - green
            base_style.update({
                'backgroundColor': '#28a745',
                'color': 'white',
                'border': '2px solid #28a745',
                'fontWeight': 'bold',
                'cursor': 'default'
            })
        elif option_index == selected_answer and selected_answer != question_data['correct']:
            # Wrong selected answer - red
            base_style.update({
                'backgroundColor': '#dc3545',
                'color': 'white',
                'border': '2px solid #dc3545',
                'fontWeight': 'bold',
                'cursor': 'default'
            })
        else:
            # Unselected answers - dimmed
            base_style.update({
                'backgroundColor': '#f8f9fa',
                'color': 'black',
                'border': '2px solid #dee2e6',
                'opacity': '0.6',
                'cursor': 'default'
            })
    else:
        # Before answering - normal style
        base_style.update({
            'backgroundColor': '#f8f9fa',
            'color': 'black',
            'border': '2px solid #dee2e6',
            'cursor': 'pointer'
        })
    
    return base_style

def create_question_layout(question_data, question_index, total_questions, selected_answer=None, is_answered=False):
    """Create layout for a single question."""
    
    # Create buttons with fixed IDs
    answer_buttons = []
    for i in range(4):  # Always create 4 buttons
        if i < len(question_data['options']):
            button = html.Button(
                question_data['options'][i], 
                id=f'answer-btn-{i}',
                style=get_answer_button_style(i, question_data, selected_answer, is_answered)
            )
        else:
            # Hidden button if fewer than 4 options
            button = html.Button(
                '', 
                id=f'answer-btn-{i}',
                style={'display': 'none'}
            )
        answer_buttons.append(button)
    
    return html.Div([
        html.H4(question_data['question'], 
                style={'marginBottom': '20px', 'textAlign': 'center'}),
        
        html.Div(answer_buttons),
        
        html.Div(id="question-feedback", style={'marginTop': '20px'})
    ])

def get_performance_data(score, total):
    """Get performance message and color based on score percentage."""
    percentage = round((score / total) * 100, 1)
    
    if percentage >= 80:
        return percentage, "Excellent work! 🏆", '#28a745'
    elif percentage >= 60:
        return percentage, "Good job! 👍", '#17a2b8'
    elif percentage >= 40:
        return percentage, "Not bad! Keep learning! 📚", '#ffc107'
    else:
        return percentage, "Keep practicing! 💪", '#fd7e14'

def create_completion_screen(score, total, quiz_type):
    """Create the quiz completion screen."""
    percentage, performance_msg, color = get_performance_data(score, total)
    
    return html.Div([
        html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745'}),
        create_score_display(score, total, percentage, performance_msg, color),
        html.Div([
            create_quiz_button(
                f"Start New {quiz_type.title()} Quiz", 
                f"restart-{quiz_type}-quiz-result", 
                "primary", 
                "10px"
            ),
            create_quiz_button(
                "Back to Quiz Selection", 
                "back-to-selection", 
                "secondary"
            )
        ], style={'textAlign': 'center'})
    ], style={'textAlign': 'center', 'padding': '40px'})
