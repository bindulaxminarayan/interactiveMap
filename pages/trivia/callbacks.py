"""
Dash callbacks for the trivia module.
"""

from dash import Input, Output, State, callback_context
import dash.exceptions
from utils.data_processing import load_countries_data
from utils.quiz_generators import get_quiz_questions
from .quiz_components import create_progress_bar, create_question_layout, create_completion_screen
from .components import create_welcome_content, create_feedback_message

# Load the data for trivia questions
df = load_countries_data()

def register_trivia_callbacks(app):
    """Register all callbacks for the trivia page."""
    
    # Callback for starting quizzes from side panel
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Output('side-panel', 'style'),
        Output('progress-container', 'children'),
        Output('progress-container', 'style'),
        [Input('start-currency-quiz', 'n_clicks'),
         Input('start-capital-quiz', 'n_clicks'),
         Input('start-continent-quiz','n_clicks')],
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def start_quiz(currency_clicks, capital_clicks, continent_clicks, current_data):
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
            feedback = create_feedback_message(
                is_correct, 
                question_data['options'][question_data['correct']], 
                question_data['explanation']
            )
            
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
                quiz_type = current_data.get('quiz_type', 'quiz')
                completion_screen = create_completion_screen(new_score, len(questions), quiz_type)
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
                quiz_type = current_data.get('quiz_type', 'quiz')
                completion_screen = create_completion_screen(current_data['score'], len(questions), quiz_type)
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
                return completion_screen, completion_data, []
            else:
                # Next question
                question_data = questions[next_index]
                updated_data = current_data.copy()
                updated_data['index'] = next_index
                updated_data['answered'] = False
                
                # Update progress bar
                progress_bar = create_progress_bar(next_index, len(questions))
                
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
            return _return_to_welcome()
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
            return _return_to_welcome()
        raise dash.exceptions.PreventUpdate

def _return_to_welcome():
    """Helper function to return to the welcome screen."""
    # Show side panel and hide progress bar
    side_panel_style = {
        'width': '300px',
        'marginRight': '30px',
        'flexShrink': '0'
    }
    progress_style = {'display': 'none'}
    
    welcome_content = create_welcome_content()
    reset_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False}
    
    return welcome_content, reset_data, side_panel_style, progress_style, []
