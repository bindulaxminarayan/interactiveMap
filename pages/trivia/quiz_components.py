"""
Quiz-specific UI components for the trivia module.
"""

from dash import html, dcc
from .ui_components import create_quiz_button, create_score_display
from utils.quiz_generators import QUIZ_TYPE_LABEL

def create_username_modal(is_open=False, current_username=""):
    """Create a modal for username input."""
    return dcc.Store(id='username-modal-store', data={'is_open': is_open}), \
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
                           value=current_username,
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
                   'display': 'flex' if is_open else 'none',
                   'justifyContent': 'center',
                   'alignItems': 'center',
                   'zIndex': '1000'
               })
           ], id='username-modal')

def create_progress_bar(current_question, total_questions, show_next_button=False, show_view_results_button=False, show_quit_quiz_button=True):
    """Create a progress bar showing quiz progress."""
    progress_percentage = ((current_question + 1) / total_questions) * 100
    remaining_questions = total_questions - (current_question + 1)
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(f"Question {current_question + 1} of {total_questions}", 
                         style={'fontWeight': 'bold', 'color': '#007bff', 'fontSize': '20px'}),
                html.Span(f"{remaining_questions} questions remaining", 
                         style={'color': '#6c757d', 'fontSize': '18px'})
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
                               'padding': '12px 24px', 
                               'fontSize': '18px',
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
                               'padding': '12px 24px', 
                               'fontSize': '18px',
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
                               'padding': '12px 24px', 
                               'fontSize': '18px',
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
        'padding': '15px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '8px',
        'marginBottom': '15px',
        'border': '1px solid #dee2e6'
    })

def get_answer_button_style(option_index, question_data, selected_answer=None, is_answered=False):
    """Get the style for answer buttons based on state."""
    base_style = {
        'display': 'block', 
        'width': '100%', 
        'margin': '6px 0',
        'padding': '12px', 
        'fontSize': '18px', 
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

def create_question_image(image_src, image_type="default", custom_style=None):
    """
    Create a standardized image component for questions.
    
    Args:
        image_src: Source path for the image
        image_type: Type of image ('flag', 'wonder', 'default') for different styling
        custom_style: Optional custom style overrides
    """
    # Default image configurations by type - optimized with auto-hide navbar for better space utilization
    image_configs = {
        'flag': {
            'maxWidth': '280px',
            'maxHeight': '180px',
            'container_style': {
                'textAlign': 'center',
                'marginBottom': '15px',
                'padding': '12px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'border': '1px solid #dee2e6'
            }
        },
        'wonder': {
            'maxWidth': '350px',
            'maxHeight': '220px',
            'container_style': {
                'textAlign': 'center',
                'marginBottom': '15px',
                'padding': '12px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'border': '1px solid #dee2e6'
            }
        },
        'default': {
            'maxWidth': '320px',
            'maxHeight': '200px',
            'container_style': {
                'textAlign': 'center',
                'marginBottom': '15px',
                'padding': '12px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'border': '1px solid #dee2e6'
            }
        }
    }
    
    config = image_configs.get(image_type, image_configs['default'])
    
    # Base image style
    image_style = {
        'maxWidth': config['maxWidth'],
        'maxHeight': config['maxHeight'],
        'width': 'auto',
        'height': 'auto',
        'border': '2px solid #dee2e6',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'display': 'block',
        'margin': '0 auto'
    }
    
    # Apply custom style overrides if provided
    if custom_style:
        image_style.update(custom_style)
    
    return html.Div([
        html.Img(src=image_src, style=image_style)
    ], style=config['container_style'])

def create_question_layout(question_data, question_index, total_questions, selected_answer=None, is_answered=False):
    """
    Create layout for a single question with flexible image support.
    
    Args:
        question_data: Dictionary containing question information
        question_index: Current question index
        total_questions: Total number of questions
        selected_answer: Index of selected answer (if any)
        is_answered: Whether question has been answered
    """
    
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
                style={'marginBottom': '12px', 'textAlign': 'center', 'fontSize': '22px', 'fontWeight': 'bold'})
    ]
    
    # Add images based on question type - more flexible approach
    image_added = False
    
    # Check for flag image
    if 'flag_image' in question_data and question_data['flag_image']:
        content.append(create_question_image(question_data['flag_image'], 'flag'))
        image_added = True
    
    # Check for wonder image
    if 'wonder_image' in question_data and question_data['wonder_image']:
        content.append(create_question_image(question_data['wonder_image'], 'wonder'))
        image_added = True
    
    # Check for generic image (for future extensibility)
    if 'image' in question_data and question_data['image'] and not image_added:
        content.append(create_question_image(question_data['image'], 'default'))
    
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
        # Handle both string and integer keys for compatibility with JSON serialization
        user_answer_index = user_answers.get(str(i), user_answers.get(i, -1))
        correct_index = question_data['correct']
        
        # Get answer texts
        user_answer_text = question_data['options'][user_answer_index] if user_answer_index >= 0 else "No answer"
        correct_answer_text = question_data['options'][correct_index]
        
        # Determine if answer was correct
        is_correct = user_answer_index == correct_index
        
        # Create question review item
        review_content = [
            html.H5(f"Question {i + 1}: {question_data['question']}", 
                   style={'marginBottom': '10px', 'color': '#333', 'fontWeight': 'bold'})
        ]
        
        # Add images in review (smaller size)
        image_added = False
        
        # Add flag image if this was a flag question
        if 'flag_image' in question_data and question_data['flag_image']:
            review_content.append(create_question_image(
                question_data['flag_image'], 
                'flag',
                custom_style={'maxWidth': '150px', 'maxHeight': '100px'}
            ))
            image_added = True
        
        # Add wonder image if this was a wonders question
        if 'wonder_image' in question_data and question_data['wonder_image']:
            review_content.append(create_question_image(
                question_data['wonder_image'], 
                'wonder',
                custom_style={'maxWidth': '200px', 'maxHeight': '150px'}
            ))
            image_added = True
        
        # Add generic image if present and no specific image was added
        if 'image' in question_data and question_data['image'] and not image_added:
            review_content.append(create_question_image(
                question_data['image'], 
                'default',
                custom_style={'maxWidth': '175px', 'maxHeight': '125px'}
            ))
        
        # Show all options with highlighting
        options_div = html.Div([
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
        ], style={'marginBottom': '10px'})
        review_content.append(options_div)
        
        # Summary
        summary_div = html.Div([
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
            ], style={'marginBottom': '10px'})
        ])
        review_content.append(summary_div)
        
        # Add fun fact if available
        fun_fact = question_data.get('fun_fact', '')
        if fun_fact and fun_fact.strip():
            fun_fact_div = html.Div([
                html.Hr(style={'margin': '10px 0', 'border': '1px solid #dee2e6'}),
                html.P("💡 Fun Fact:", style={'fontWeight': 'bold', 'color': '#6f42c1', 'fontSize': '16px', 'marginBottom': '5px'}),
                html.P(fun_fact, style={'color': '#333', 'fontSize': '14px', 'lineHeight': '1.4', 'fontStyle': 'italic'})
            ], style={
                'backgroundColor': '#f8f9fa', 
                'padding': '10px', 
                'borderRadius': '6px', 
                'border': '1px solid #dee2e6',
                'marginTop': '10px'
            })
            review_content.append(fun_fact_div)
        
        question_review = html.Div(review_content, style={
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
        html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745', 'fontSize': '3rem'}),
        create_score_display(score, total, percentage, performance_msg, color),
        html.Div([
            html.Button(
                f"Restart {QUIZ_TYPE_LABEL[quiz_type]} Quiz",
                id="restart-current-quiz",
                style={
                    'padding': '20px 40px',
                    'fontSize': '20px',
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
                    'padding': '20px 40px',
                    'fontSize': '20px',
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
