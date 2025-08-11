"""
Universal quiz callbacks that work across all quiz pages.
"""

import time
from dash import Input, Output, State, callback_context
import dash.exceptions
from utils.quiz_generators import get_quiz_questions, QUIZ_TYPE_LABEL
from utils.math_quiz_generators import get_math_quiz_questions, MATH_QUIZ_TYPE_LABEL
from utils.quiz_stats import quiz_stats
from .quiz_components import create_progress_bar, create_question_layout

NUM_OF_QUESTIONS = 20

def register_universal_username_modal_callbacks(app):
    """Register universal username modal callbacks that work across all quiz pages."""
    
    # Universal callback to show username modal when ANY quiz button is clicked
    @app.callback(
        Output('username-modal', 'style'),
        Output('username-input', 'value'),
        Output('pending-quiz-store', 'data'),
        [Input('start-currency-quiz', 'n_clicks'),
         Input('start-wonders-quiz', 'n_clicks'),
         Input('start-capital-quiz', 'n_clicks'),
         Input('start-continent-quiz','n_clicks'),
         Input('start-flag-quiz','n_clicks'),
         Input('start-physical-geography-quiz','n_clicks'),
         Input('start-india-capital-quiz','n_clicks'),
         Input('start-us-capital-quiz', 'n_clicks'),
         Input('start-k5-math-quiz', 'n_clicks'),
         Input('start-biology-quiz', 'n_clicks'),
         Input('start-chemistry-quiz', 'n_clicks'),
         Input('start-physics-quiz', 'n_clicks'),
         Input('start-astronomy-quiz', 'n_clicks'),
         Input('start-earth-science-quiz', 'n_clicks'),
         Input('start-technology-quiz', 'n_clicks')],
        [State('username-store', 'data'),
         State('pending-quiz-store', 'data')],
        prevent_initial_call=True,
        suppress_callback_exceptions=True
    )
    def show_universal_username_modal(*args):
        # Last two are states, rest are inputs
        *temp, username_store_data, pending_quiz_store_data = args if len(args) >= 2 else (None, None)
        
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_value = ctx.triggered[0]['value']

        # Handle quiz button clicks
        if triggered_value and triggered_value > 0:
            # Universal quiz type mapping
            quiz_type_mapping = {
                'start-currency-quiz': 'currency',
                'start-wonders-quiz': 'wonders',
                'start-capital-quiz': 'capital',
                'start-continent-quiz': 'continent',
                'start-flag-quiz': 'flag',
                'start-physical-geography-quiz': 'world_physical_geography',
                'start-india-capital-quiz': 'india_capital',
                'start-us-capital-quiz': 'us_capital',
                'start-k5-math-quiz': 'k5_math',
                'start-biology-quiz': 'biology',
                'start-chemistry-quiz': 'chemistry',
                'start-physics-quiz': 'physics',
                'start-astronomy-quiz': 'astronomy',
                'start-earth-science-quiz': 'earth_science',
                'start-technology-quiz': 'technology'
            }
            
            quiz_type = quiz_type_mapping.get(triggered_id)
            if quiz_type:
                # Show modal
                current_username = username_store_data.get('username', '')
                if current_username == 'anonymous_user':
                    current_username = ''
                
                pending_quiz = {'quiz_type': quiz_type}
                return {
                    'display': 'flex',
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'backgroundColor': 'rgba(0, 0, 0, 0.5)',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'zIndex': '1000'
                }, current_username, pending_quiz

        raise dash.exceptions.PreventUpdate

    # Universal callback for cancel button
    @app.callback(
        Output('username-modal', 'style', allow_duplicate=True),
        Input('username-cancel-btn', 'n_clicks'),
        State('username-store', 'data'),
        prevent_initial_call=True,
        suppress_callback_exceptions=True
    )
    def handle_universal_cancel_button(cancel_clicks, username_data):
        if cancel_clicks:
            return {'display': 'none'}
        raise dash.exceptions.PreventUpdate

    # Universal callback for username confirmation and quiz start
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Output('quiz-selection-area', 'style'),
        Output('quiz-content-area', 'style'),
        Output('progress-container', 'children'),
        Output('progress-container', 'style'),
        Output('main-layout-container-wrapper', 'style'),
        Output('quiz-active-store', 'data'),
        Output('page-content', 'data-navbar-auto-hide'),
        Output('username-store', 'data'),
        Output('username-modal', 'style', allow_duplicate=True),
        Input('username-confirm-btn', 'n_clicks'),
        [State('username-input', 'value'),
         State('pending-quiz-store', 'data'),
         State('username-store', 'data')],
        prevent_initial_call=True,
        suppress_callback_exceptions=True
    )
    def start_universal_quiz_with_username(confirm_clicks, username_input, pending_quiz, current_username_data):
        if not confirm_clicks or not pending_quiz.get('quiz_type'):
            raise dash.exceptions.PreventUpdate

        quiz_type = pending_quiz['quiz_type']
        
        # Use entered username or default to anonymous_user
        username = username_input.strip() if username_input and username_input.strip() else 'anonymous_user'
        
        # Get quiz questions - handle math vs regular quizzes vs science quizzes
        if quiz_type == 'k5_math':
            questions = get_math_quiz_questions(quiz_type, None, 10)  # Math quizzes use 10 questions
            quiz_type_display = MATH_QUIZ_TYPE_LABEL[quiz_type]
        else:
            # For all other quiz types including biology and chemistry
            questions = get_quiz_questions(quiz_type, None, NUM_OF_QUESTIONS)
            quiz_type_display = QUIZ_TYPE_LABEL.get(quiz_type, f"{quiz_type.capitalize()} Quiz")

        # Start a new quiz session for analytics with the username
        session_id = quiz_stats.start_quiz_session(
            session_name=f"{quiz_type_display}", 
            user_id=username
        )
        
        question_data = questions[0]
        new_data = {
            'index': 0,
            'score': 0,
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type,
            'quiz_type_display': quiz_type_display,
            'user_answers': {},
            'session_id': session_id,
            'question_start_time': time.time()
        }

        # Update username store
        updated_username_data = {'username': username}

        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))

        return (create_question_layout(question_data, 0, len(questions)),
                new_data,
                {'display': 'none'},
                {'display': 'block', 'width': '100%', 'minHeight': '100vh', 'padding': '10px 20px', 'margin': '0', 'boxSizing': 'border-box'},
                progress_bar,
                {'display': 'block'},
                {'display': 'flex', 'justifyContent': 'center', 'alignItems': 'flex-start', 'width': '100%', 'maxWidth': '98vw', 'margin': '0 auto', 'padding': '0'},
                {'active': True},
                "hide",
                updated_username_data,
                {'display': 'none'})
