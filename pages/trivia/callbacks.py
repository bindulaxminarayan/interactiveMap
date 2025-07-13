"""
Dash callbacks for the trivia module.
"""

from dash import Input, Output, State, callback_context, html
import dash.exceptions
from utils.data_processing import load_countries_data
from utils.quiz_generators import get_quiz_questions
from .quiz_components import create_progress_bar, create_question_layout, create_completion_screen
from .components import create_feedback_message

# Load the data for trivia questions
df = load_countries_data()

def register_trivia_callbacks(app):
    """Register all callbacks for the trivia page."""
    
    # Callback for starting quizzes from quiz cards
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Output('quiz-selection-area', 'style'),
        Output('quiz-content-area', 'style'),
        Output('progress-container', 'children'),
        Output('progress-container', 'style'),
        [Input('start-country-quiz', 'n_clicks'),
         Input('start-currency-quiz', 'n_clicks'),
         Input('start-capital-quiz', 'n_clicks'),
         Input('start-continent-quiz','n_clicks'),
         Input('start-flag-quiz','n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def start_quiz(country_clicks, currency_clicks, capital_clicks, continent_clicks, flag_clicks, current_data):
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
        elif triggered_id == 'start-continent-quiz':
            questions = get_quiz_questions('continent', df, 10)
            quiz_type = 'continent'
        elif triggered_id == 'start-country-quiz':
            questions = get_quiz_questions('country', df, 10)
            quiz_type = 'country'
        elif triggered_id == 'start-flag-quiz':
            questions = get_quiz_questions('flag', df, 10)
            quiz_type = 'flag'
        else:
            raise dash.exceptions.PreventUpdate
        
        question_data = questions[0]
        new_data = {
            'index': 0, 
            'score': 0, 
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type,
            'user_answers': {}
        }
        
        # Hide quiz selection and show quiz content
        quiz_selection_style = {'display': 'none'}
        quiz_content_style = {
            'display': 'block',
            'backgroundColor': '#ffffff',
            'borderRadius': '15px',
            'border': '1px solid #dee2e6',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'padding': '30px',
            'margin': '20px auto',
            'maxWidth': '800px',
            'minHeight': '500px'
        }
        
        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}
        
        return (create_question_layout(question_data, 0, len(questions)), 
                new_data, 
                quiz_selection_style,
                quiz_content_style,
                progress_bar, 
                progress_style)
    
    # Separate callback for restart buttons from results screen
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        [Input('restart-country-quiz-result', 'n_clicks'),
         Input('restart-currency-quiz-result', 'n_clicks'),
         Input('restart-capital-quiz-result', 'n_clicks'),
         Input('restart-continent-quiz-result', 'n_clicks'),
         Input('restart-flag-quiz-result', 'n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def restart_quiz_from_results(restart_country_clicks,restart_currency_clicks,restart_capital_clicks,restart_continent_clicks,restart_flag_clicks,current_data):
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
        elif triggered_id == 'restart-continent-quiz-result':
            questions = get_quiz_questions('continent', df, 10)
            quiz_type = 'continent'
        elif triggered_id == 'restart-country-quiz-result':
            questions = get_quiz_questions('country', df, 10)
            quiz_type = 'country'
        elif triggered_id == 'restart-flag-quiz-result':
            questions = get_quiz_questions('flag', df, 10)
            quiz_type = 'flag'
        else:
            raise dash.exceptions.PreventUpdate
        
        question_data = questions[0]
        new_data = {
            'index': 0, 
            'score': 0, 
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type,
            'user_answers': {}
        }
        
        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}
        
        return (create_question_layout(question_data, 0, len(questions)), 
                new_data, 
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
         Input('next-btn', 'n_clicks'),
         Input('view-results-btn', 'n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def handle_quiz_interactions(btn0, btn1, btn2, btn3, next_btn, view_results_btn, current_data):
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
            feedback = create_feedback_message(
                is_correct, 
                question_data['options'][question_data['correct']], 
                question_data['explanation'],
                question_data['moreinfo']
            )
            
            # Create layout with visual feedback
            layout = create_question_layout(question_data, current_index, len(questions), 
                                          selected_answer=clicked_index, is_answered=True)
            
            # Find and update the feedback div
            for i, child in enumerate(layout.children):
                if hasattr(child, 'id') and child.id == 'question-feedback':
                    layout.children[i] = feedback
                    break
            
            # Update data
            updated_data = current_data.copy()
            updated_data['score'] = new_score
            updated_data['answered'] = True
            updated_data['selected_answer'] = clicked_index
            
            # Store user answer
            if 'user_answers' not in updated_data:
                updated_data['user_answers'] = {}
            updated_data['user_answers'][current_index] = clicked_index
            
            # Check if this is the last question
            is_last_question = current_index >= len(questions) - 1
            
            if is_last_question:
                # Last question - show "View Results" button instead of immediately showing results
                progress_bar = create_progress_bar(current_index, len(questions), show_view_results_button=True, show_quit_quiz_button=False)
                return layout, updated_data, progress_bar
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
                quiz_type = current_data.get('quiz_type', 'quiz')
                user_answers = current_data.get('user_answers', {})
                completion_screen = create_completion_screen(
                    current_data['score'], 
                    len(questions), 
                    quiz_type, 
                    questions, 
                    user_answers
                )
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}}
                return completion_screen, completion_data, []
            else:
                # Next question
                question_data = questions[next_index]
                updated_data = current_data.copy()
                updated_data['index'] = next_index
                updated_data['answered'] = False
                updated_data['selected_answer'] = None
                
                # Update progress bar
                progress_bar = create_progress_bar(next_index, len(questions))
                
                return (create_question_layout(question_data, next_index, len(questions)), 
                        updated_data, 
                        progress_bar)
        
        # Handle view results button click
        elif triggered_id == 'view-results-btn':
            if not current_data.get('answered', False):
                raise dash.exceptions.PreventUpdate
            
            # Only process if button was actually clicked (n_clicks > 0)
            if not triggered_value or triggered_value == 0:
                raise dash.exceptions.PreventUpdate
            
            # Show results screen with review section
            quiz_type = current_data.get('quiz_type', 'quiz')
            questions = current_data.get('questions', [])
            user_answers = current_data.get('user_answers', {})
            completion_screen = create_completion_screen(
                current_data['score'], 
                len(questions), 
                quiz_type, 
                questions, 
                user_answers
            )
            completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}}
            return completion_screen, completion_data, []
        
        raise dash.exceptions.PreventUpdate
    
    # Callback specifically for quit quiz button
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('quiz-selection-area', 'style', allow_duplicate=True),
        Output('quiz-content-area', 'style', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Input('quit-quiz-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def quit_quiz(quit_clicks):
        if quit_clicks:
            return _return_to_quiz_selection()
        raise dash.exceptions.PreventUpdate

    # Callback for "Back to Quiz Selection" button on completion screen
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('quiz-selection-area', 'style', allow_duplicate=True),
        Output('quiz-content-area', 'style', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Input('back-to-selection', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_selection(back_clicks):
        if back_clicks:
            return _return_to_quiz_selection()
        raise dash.exceptions.PreventUpdate

def _return_to_quiz_selection():
    """Helper function to return to the quiz selection screen."""
    # Show quiz selection and hide quiz content
    quiz_selection_style = {'display': 'block'}
    quiz_content_style = {'display': 'none'}
    progress_style = {'display': 'none'}
    
    reset_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}}
    
    return [], reset_data, quiz_selection_style, quiz_content_style, progress_style, []
