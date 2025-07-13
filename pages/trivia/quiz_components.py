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
    
    # Create the main content list
    content = [
        html.H4(question_data['question'], 
                style={'marginBottom': '20px', 'textAlign': 'center'})
    ]
    
    # Add flag image if this is a flag question
    if 'flag_image' in question_data:
        flag_image = html.Div([
            html.Img(
                src=question_data['flag_image'],
                style={
                    'maxWidth': '300px',
                    'maxHeight': '200px',
                    'width': 'auto',
                    'height': 'auto',
                    'border': '2px solid #dee2e6',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'display': 'block',
                    'margin': '0 auto'
                }
            )
        ], style={
            'textAlign': 'center',
            'marginBottom': '30px',
            'padding': '20px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '10px',
            'border': '1px solid #dee2e6'
        })
        content.append(flag_image)
    
    # Add answer buttons
    content.append(html.Div(answer_buttons))
    
    # Add feedback area
    content.append(html.Div(id="question-feedback", style={'marginTop': '20px'}))
    
    return html.Div(content)

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

def create_review_answers_section(questions, user_answers):
    """Create a review section showing all questions with correct and chosen answers."""
    if not questions or not user_answers:
        return html.Div()
    
    review_items = []
    
    for i, question_data in enumerate(questions):
        user_answer_index = user_answers.get(i, -1)
        correct_index = question_data['correct']
        
        # Get answer texts
        user_answer_text = question_data['options'][user_answer_index] if user_answer_index >= 0 else "No answer"
        correct_answer_text = question_data['options'][correct_index]
        
        # Determine if answer was correct
        is_correct = user_answer_index == correct_index
        
        # Create question review item
        question_review = html.Div([
            html.H5(f"Question {i + 1}: {question_data['question']}", 
                   style={'marginBottom': '10px', 'color': '#333', 'fontWeight': 'bold'}),
            
            # Show all options with highlighting
            html.Div([
                html.Div([
                    html.Span(f"{chr(65 + j)}. {option}", style={
                        'display': 'block',
                        'padding': '8px 12px',
                        'margin': '3px 0',
                        'borderRadius': '5px',
                        'backgroundColor': (
                            '#28a745' if j == correct_index else  # Correct answer - green
                            '#dc3545' if j == user_answer_index and j != correct_index else  # Wrong user answer - red
                            '#f8f9fa'  # Other options - light gray
                        ),
                        'color': 'white' if (j == correct_index or (j == user_answer_index and j != correct_index)) else 'black',
                        'fontWeight': 'bold' if (j == correct_index or j == user_answer_index) else 'normal',
                        'border': '1px solid #dee2e6'
                    })
                    for j, option in enumerate(question_data['options'])
                ])
            ], style={'marginBottom': '10px'}),
            
            # Summary
            html.Div([
                html.Div([
                    html.Strong("Your answer: ", style={'color': '#666'}),
                    html.Span(user_answer_text, style={
                        'color': '#28a745' if is_correct else '#dc3545',
                        'fontWeight': 'bold'
                    }),
                    html.Span(" ✓" if is_correct else " ✗", style={
                        'color': '#28a745' if is_correct else '#dc3545',
                        'fontSize': '18px',
                        'marginLeft': '5px'
                    })
                ], style={'marginBottom': '5px'}),
                
                html.Div([
                    html.Strong("Correct answer: ", style={'color': '#666'}),
                    html.Span(correct_answer_text, style={'color': '#28a745', 'fontWeight': 'bold'})
                ], style={'marginBottom': '10px'}),
                
                html.Div([
                    html.Strong("Explanation: ", style={'color': '#666'}),
                    html.Span(question_data.get('explanation', 'No explanation available.'))
                ], style={'color': '#555', 'fontStyle': 'italic'})
            ])
            
        ], style={
            'backgroundColor': '#ffffff',
            'border': '1px solid #dee2e6',
            'borderRadius': '8px',
            'padding': '20px',
            'marginBottom': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
        
        review_items.append(question_review)
    
    return html.Div([
        html.H3("Review Answers", style={
            'textAlign': 'center', 
            'marginBottom': '30px',
            'color': '#333',
            'borderBottom': '2px solid #007bff',
            'paddingBottom': '10px'
        }),
        html.Div(review_items)
    ], style={
        'marginTop': '30px',
        'padding': '20px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '10px',
        'border': '1px solid #dee2e6'
    })

def create_completion_screen(score, total, quiz_type, questions=None, user_answers=None):
    """Create the quiz completion screen with optional review section."""
    percentage, performance_msg, color = get_performance_data(score, total)
    
    completion_content = [
        html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745'}),
        create_score_display(score, total, percentage, performance_msg, color),
        html.Div([
            html.Button(
                f"Start New {quiz_type.title()} Quiz",
                id="restart-current-quiz",
                style={
                    'padding': '15px 30px',
                    'fontSize': '16px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'marginRight': '10px',
                    'backgroundColor': '#28a745',
                    'color': 'white'
                }
            ),
            html.Button(
                "Back to Quiz Selection",
                id="back-to-selection",
                style={
                    'padding': '15px 30px',
                    'fontSize': '16px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'backgroundColor': '#007bff',
                    'color': 'white'
                }
            )
        ], style={'textAlign': 'center'})
    ]
    
    # Add review section if questions and user answers are provided
    if questions and user_answers:
        completion_content.append(create_review_answers_section(questions, user_answers))
    
    return html.Div(completion_content, style={'textAlign': 'center', 'padding': '40px'})
