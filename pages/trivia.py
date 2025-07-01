"""
Trivia page for country-related quiz questions.
"""

from dash import html, dcc, Input, Output, State, callback_context
import dash.exceptions
import random
import json
from utils.data_processing import load_countries_data
from utils.quiz_generators import get_quiz_questions

# Load the data for trivia questions
df = load_countries_data()

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
        html.Div([
            html.H4("💰 Currencies", style={
                'backgroundColor': '#f8f9fa',
                'padding': '15px',
                'margin': '0 0 10px 0',
                'borderRadius': '8px',
                'cursor': 'pointer',
                'border': '2px solid #007bff',
                'color': '#007bff',
                'fontWeight': 'bold'
            }),
            html.Div([
                html.P("Test your knowledge of world currencies!", 
                       style={'margin': '10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.Button("Start Currency Quiz", 
                           id="start-currency-quiz", 
                           style={
                               'width': '100%',
                               'padding': '10px',
                               'backgroundColor': '#28a745',
                               'color': 'white',
                               'border': 'none',
                               'borderRadius': '5px',
                               'cursor': 'pointer',
                               'fontSize': '14px',
                               'fontWeight': 'bold'
                           })
            ], style={'padding': '0 15px 15px 15px'})
        ], style={'marginBottom': '15px'}),
        
        # Capitals Section
        html.Div([
            html.H4("🏛️ Capital Cities", style={
                'backgroundColor': '#f8f9fa',
                'padding': '15px',
                'margin': '0 0 10px 0',
                'borderRadius': '8px',
                'cursor': 'pointer',
                'border': '2px solid #007bff',
                'color': '#007bff',
                'fontWeight': 'bold'
            }),
            html.Div([
                html.P("Match countries with their capitals!", 
                       style={'margin': '10px 0', 'fontSize': '14px', 'color': '#666'}),
                html.Button("Start Capital Quiz", 
                           id="start-capital-quiz", 
                           style={
                               'width': '100%',
                               'padding': '10px',
                               'backgroundColor': '#28a745',
                               'color': 'white',
                               'border': 'none',
                               'borderRadius': '5px',
                               'cursor': 'pointer',
                               'fontSize': '14px',
                               'fontWeight': 'bold'
                           })
            ], style={'padding': '0 15px 15px 15px'})
        ], style={'marginBottom': '15px'}),
        
        # Future Quiz Categories (Coming Soon)
        html.Div([
            html.H4("🗺️ Locate Countries", style={
                'backgroundColor': '#f8f9fa',
                'padding': '15px',
                'margin': '0 0 10px 0',
                'borderRadius': '8px',
                'border': '2px solid #dee2e6',
                'color': '#6c757d',
                'fontWeight': 'bold',
                'opacity': '0.7'
            }),
            html.Div([
                html.P("Find countries on the map!", 
                       style={'margin': '10px 0', 'fontSize': '14px', 'color': '#999'}),
                html.Button("Coming Soon", 
                           disabled=True,
                           style={
                               'width': '100%',
                               'padding': '10px',
                               'backgroundColor': '#6c757d',
                               'color': 'white',
                               'border': 'none',
                               'borderRadius': '5px',
                               'cursor': 'not-allowed',
                               'fontSize': '14px',
                               'opacity': '0.6'
                           })
            ], style={'padding': '0 15px 15px 15px'})
        ])
        
    ], style={
        'width': '280px',
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'border': '1px solid #dee2e6',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'height': 'fit-content'
    })

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
                    html.Div([
                        html.H2("Welcome to Country Trivia! 🌍", 
                               style={'textAlign': 'center', 'color': '#007bff', 'marginBottom': '20px'}),
                        html.P("Select a quiz category from the panel on the left to get started!", 
                               style={'textAlign': 'center', 'fontSize': '18px', 'color': '#666'})
                    ], style={'textAlign': 'center', 'padding': '60px 20px'})
                ]),
                
                # Hidden storage for current question
                dcc.Store(id='current-question-store', data={'index': 0, 'score': 0}),
                
                # Hidden restart buttons that callbacks need to reference
                html.Div([
                    html.Button("Restart Currency", id="restart-currency-quiz-result", style={'display': 'none'}),
                    html.Button("Restart Capital", id="restart-capital-quiz-result", style={'display': 'none'}),
                    html.Button("Next Question", id='next-btn', style={'display': 'none'}),
                    html.Button("Quit Quiz", id='quit-quiz-btn', style={'display': 'none'}),
                    html.Button("Back to Selection", id="back-to-selection", style={'display': 'none'}),
                    html.Button("", id='answer-btn-0', style={'display': 'none'}),
                    html.Button("", id='answer-btn-1', style={'display': 'none'}),
                    html.Button("", id='answer-btn-2', style={'display': 'none'}),
                    html.Button("", id='answer-btn-3', style={'display': 'none'}),
                ], style={'display': 'none'}),
                
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

def create_progress_bar(current_question, total_questions, show_next_button=False):
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
                           })
            ], style={'textAlign': 'right'})
        ])
    ], style={
        'padding': '20px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '8px',
        'marginBottom': '20px',
        'border': '1px solid #dee2e6'
    })

def create_question_layout(question_data, question_index, total_questions, selected_answer=None, is_answered=False):
    """Create layout for a single question."""
    
    # Determine button styles based on whether question is answered
    def get_button_style(option_index):
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
    
    # Create buttons with fixed IDs
    answer_buttons = []
    for i in range(4):  # Always create 4 buttons
        if i < len(question_data['options']):
            button = html.Button(
                question_data['options'][i], 
                id=f'answer-btn-{i}',
                style=get_button_style(i)
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

def register_trivia_callbacks(app):
    """Register callbacks for the trivia page."""
    
    # Callback for starting quizzes from side panel
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Output('side-panel', 'style'),
        Output('progress-container', 'children'),
        Output('progress-container', 'style'),
        [Input('start-currency-quiz', 'n_clicks'),
         Input('start-capital-quiz', 'n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def start_quiz(currency_clicks, capital_clicks, current_data):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_value = ctx.triggered[0]['value']
        
        # Only process if button was actually clicked (n_clicks > 0)
        if not triggered_value or triggered_value == 0:
            raise dash.exceptions.PreventUpdate
        
        if triggered_id == 'start-currency-quiz':
            questions = get_quiz_questions('currency', df, 10)
            quiz_type = 'currency'
        elif triggered_id == 'start-capital-quiz':
            questions = get_quiz_questions('capital', df, 10)
            quiz_type = 'capital'
        else:
            raise dash.exceptions.PreventUpdate
        
        question_data = questions[0]
        new_data = {
            'index': 0, 
            'score': 0, 
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type
        }
        
        # Hide side panel during quiz
        side_panel_style = {'display': 'none'}
        
        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}
        
        return (create_question_layout(question_data, 0, len(questions)), 
                new_data, 
                side_panel_style, 
                progress_bar, 
                progress_style)
    
    # Separate callback for restart buttons from results screen
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        [Input('restart-currency-quiz-result', 'n_clicks'),
         Input('restart-capital-quiz-result', 'n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def restart_quiz_from_results(restart_currency_clicks, restart_capital_clicks, current_data):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_value = ctx.triggered[0]['value']
        
        # Only process if button was actually clicked (n_clicks > 0)
        if not triggered_value or triggered_value == 0:
            raise dash.exceptions.PreventUpdate
        
        if triggered_id == 'restart-currency-quiz-result':
            questions = get_quiz_questions('currency', df, 10)
            quiz_type = 'currency'
        elif triggered_id == 'restart-capital-quiz-result':
            questions = get_quiz_questions('capital', df, 10)
            quiz_type = 'capital'
        else:
            raise dash.exceptions.PreventUpdate
        
        question_data = questions[0]
        new_data = {
            'index': 0, 
            'score': 0, 
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type
        }
        
        # Hide side panel during quiz
        side_panel_style = {'display': 'none'}
        
        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}
        
        return (create_question_layout(question_data, 0, len(questions)), 
                new_data, 
                side_panel_style, 
                progress_bar, 
                progress_style)
    
    # Single callback to handle all quiz interactions with fixed IDs
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        [Input('answer-btn-0', 'n_clicks'),
         Input('answer-btn-1', 'n_clicks'),
         Input('answer-btn-2', 'n_clicks'),
         Input('answer-btn-3', 'n_clicks'),
         Input('next-btn', 'n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def handle_quiz_interactions(btn0, btn1, btn2, btn3, next_btn, current_data):
        ctx = callback_context
        if not ctx.triggered or not current_data or 'questions' not in current_data:
            raise dash.exceptions.PreventUpdate
        
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_value = ctx.triggered[0]['value']
        
        # Handle answer button clicks
        if 'answer-btn-' in triggered_id:
            if current_data.get('answered', False):
                raise dash.exceptions.PreventUpdate
            
            # Only process if button was actually clicked (n_clicks > 0)
            if not triggered_value or triggered_value == 0:
                raise dash.exceptions.PreventUpdate
            
            # Get clicked button index
            clicked_index = int(triggered_id.split('-')[-1])
            
            # Get current question data
            current_index = current_data['index']
            questions = current_data['questions']
            question_data = questions[current_index]
            
            # Check if answer is correct and update score
            is_correct = clicked_index == question_data['correct']
            new_score = current_data['score'] + (1 if is_correct else 0)
            
            # Create feedback
            if is_correct:
                feedback = html.Div([
                    html.P("✅ Correct!", style={'fontWeight': 'bold', 'color': '#28a745', 'fontSize': '18px'}),
                    html.P(question_data['explanation'], style={'fontStyle': 'italic'}),
                ])
            else:
                feedback = html.Div([
                    html.P("❌ Incorrect!", style={'fontWeight': 'bold', 'color': '#dc3545', 'fontSize': '18px'}),
                    html.P(f"Correct answer: {question_data['options'][question_data['correct']]}", 
                           style={'fontWeight': 'bold', 'color': '#28a745'}),
                    html.P(question_data['explanation'], style={'fontStyle': 'italic'}),
                ])
            
            # Create layout with visual feedback
            layout = create_question_layout(question_data, current_index, len(questions), 
                                          selected_answer=clicked_index, is_answered=True)
            layout.children[2] = feedback  # Put feedback in the correct div
            
            # Update data
            updated_data = current_data.copy()
            updated_data['score'] = new_score
            updated_data['answered'] = True
            
            # Check if this is the last question
            is_last_question = current_index >= len(questions) - 1
            
            if is_last_question:
                # Quiz completed - show results immediately
                score = new_score
                total = len(questions)
                percentage = round((score / total) * 100, 1)
                quiz_type = current_data.get('quiz_type', 'quiz')
                
                if percentage >= 80:
                    performance_msg = "Excellent work! 🏆"
                    color = '#28a745'
                elif percentage >= 60:
                    performance_msg = "Good job! 👍"
                    color = '#17a2b8'
                elif percentage >= 40:
                    performance_msg = "Not bad! Keep learning! 📚"
                    color = '#ffc107'
                else:
                    performance_msg = "Keep practicing! 💪"
                    color = '#fd7e14'
                
                completion_screen = html.Div([
                    html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745'}),
                    html.Div([
                        html.H3(f"Your Score: {score} out of {total}", 
                               style={'textAlign': 'center', 'fontSize': '24px', 'margin': '20px 0'}),
                        html.H4(f"{percentage}%", 
                               style={'textAlign': 'center', 'fontSize': '36px', 'color': color, 'margin': '10px 0'}),
                        html.P(performance_msg, 
                              style={'textAlign': 'center', 'fontSize': '20px', 'color': color, 'margin': '20px 0'})
                    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '10px', 'margin': '20px 0'}),
                    html.Div([
                        html.Button(f"Start New {quiz_type.title()} Quiz", 
                                   id=f"restart-{quiz_type}-quiz-result", 
                                   style={'padding': '15px 30px', 'fontSize': '16px', 
                                          'backgroundColor': '#28a745', 'color': 'white', 
                                          'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                                          'marginRight': '10px'}),
                        html.Button("Back to Quiz Selection", id="back-to-selection", 
                                   style={'padding': '15px 30px', 'fontSize': '16px', 
                                          'backgroundColor': '#007bff', 'color': 'white', 
                                          'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                    ], style={'textAlign': 'center'})
                ], style={'textAlign': 'center', 'padding': '40px'})
                
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
                
                return completion_screen, completion_data, []
            else:
                # Not the last question - show next button
                progress_bar = create_progress_bar(current_index, len(questions), show_next_button=True)
                return layout, updated_data, progress_bar
        
        # Handle next button click
        elif triggered_id == 'next-btn':
            if not current_data.get('answered', False):
                raise dash.exceptions.PreventUpdate
            
            # Only process if button was actually clicked (n_clicks > 0)
            if not triggered_value or triggered_value == 0:
                raise dash.exceptions.PreventUpdate
            
            next_index = current_data['index'] + 1
            questions = current_data['questions']
            
            if next_index >= len(questions):
                # Quiz completed
                score = current_data['score']
                total = len(questions)
                percentage = round((score / total) * 100, 1)
                quiz_type = current_data.get('quiz_type', 'quiz')
                
                if percentage >= 80:
                    performance_msg = "Excellent work! 🏆"
                    color = '#28a745'
                elif percentage >= 60:
                    performance_msg = "Good job! 👍"
                    color = '#17a2b8'
                elif percentage >= 40:
                    performance_msg = "Not bad! Keep learning! 📚"
                    color = '#ffc107'
                else:
                    performance_msg = "Keep practicing! 💪"
                    color = '#fd7e14'
                
                completion_screen = html.Div([
                    html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745'}),
                    html.Div([
                        html.H3(f"Your Score: {score} out of {total}", 
                               style={'textAlign': 'center', 'fontSize': '24px', 'margin': '20px 0'}),
                        html.H4(f"{percentage}%", 
                               style={'textAlign': 'center', 'fontSize': '36px', 'color': color, 'margin': '10px 0'}),
                        html.P(performance_msg, 
                              style={'textAlign': 'center', 'fontSize': '20px', 'color': color, 'margin': '20px 0'})
                    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '10px', 'margin': '20px 0'}),
                    html.Div([
                        html.Button(f"Start New {quiz_type.title()} Quiz", 
                                   id=f"restart-{quiz_type}-quiz-result", 
                                   style={'padding': '15px 30px', 'fontSize': '16px', 
                                          'backgroundColor': '#28a745', 'color': 'white', 
                                          'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                                          'marginRight': '10px'}),
                        html.Button("Back to Quiz Selection", id="back-to-selection", 
                                   style={'padding': '15px 30px', 'fontSize': '16px', 
                                          'backgroundColor': '#007bff', 'color': 'white', 
                                          'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                    ], style={'textAlign': 'center'})
                ], style={'textAlign': 'center', 'padding': '40px'})
                
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
                side_panel_style = {'display': 'none'}  # Keep hidden during completion screen
                progress_style = {'display': 'none'}    # Hide progress bar on completion
                
                return completion_screen, completion_data, []
            else:
                # Next question
                question_data = questions[next_index]
                updated_data = current_data.copy()
                updated_data['index'] = next_index
                updated_data['answered'] = False
                
                # Update progress bar
                progress_bar = create_progress_bar(next_index, len(questions))
                side_panel_style = {'display': 'none'}  # Keep hidden during quiz
                progress_style = {'display': 'block'}   # Keep visible during quiz
                
                return (create_question_layout(question_data, next_index, len(questions)), 
                        updated_data, 
                        progress_bar)
        
        raise dash.exceptions.PreventUpdate
    
    # Callback specifically for quit quiz button
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Input('quit-quiz-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def quit_quiz(quit_clicks):
        if quit_clicks:
            # Show side panel and hide progress bar
            side_panel_style = {
                'width': '300px',
                'marginRight': '30px',
                'flexShrink': '0'
            }
            progress_style = {'display': 'none'}
            
            welcome_content = html.Div([
                html.H2("Welcome to Country Trivia! 🌍", 
                       style={'textAlign': 'center', 'color': '#007bff', 'marginBottom': '20px'}),
                html.P("Select a quiz category from the panel on the left to get started!", 
                       style={'textAlign': 'center', 'fontSize': '18px', 'color': '#666'})
            ], style={'textAlign': 'center', 'padding': '60px 20px'})
            
            reset_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
            
            return welcome_content, reset_data, side_panel_style, progress_style, []
        raise dash.exceptions.PreventUpdate

    # Callback for "Back to Quiz Selection" button on completion screen
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Input('back-to-selection', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_selection(back_clicks):
        if back_clicks:
            # Show side panel and hide progress bar
            side_panel_style = {
                'width': '300px',
                'marginRight': '30px',
                'flexShrink': '0'
            }
            progress_style = {'display': 'none'}
            
            welcome_content = html.Div([
                html.H2("Welcome to Country Trivia! 🌍", 
                       style={'textAlign': 'center', 'color': '#007bff', 'marginBottom': '20px'}),
                html.P("Select a quiz category from the panel on the left to get started!", 
                       style={'textAlign': 'center', 'fontSize': '18px', 'color': '#666'})
            ], style={'textAlign': 'center', 'padding': '60px 20px'})
            
            reset_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
            
            return welcome_content, reset_data, side_panel_style, progress_style, []
        raise dash.exceptions.PreventUpdate
