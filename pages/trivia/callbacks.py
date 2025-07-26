"""
Dash callbacks for the trivia module.
"""

from dash import Input, Output, State, callback_context
import dash.exceptions
import time
from utils.quiz_generators import get_quiz_questions,QUIZ_TYPE_LABEL
from utils.math_quiz_generators import get_math_quiz_questions, MATH_QUIZ_TYPE_LABEL
from utils.quiz_stats import quiz_stats
from .quiz_components import create_progress_bar, create_question_layout, create_completion_screen
from .ui_components import create_feedback_message

# Define reusable CSS class names for category buttons
ACTIVE_CATEGORY_CLASS = "category-button category-button-active"
INACTIVE_CATEGORY_CLASS = "category-button"
NUM_OF_QUESTIONS = 20

def register_trivia_callbacks(app):
    """Register all callbacks for the trivia page."""

    # Callback to show username modal when quiz buttons are clicked
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
         Input('username-cancel-btn', 'n_clicks')],
        [State('username-store', 'data'),
         State('pending-quiz-store', 'data')],
        prevent_initial_call=True
    )
    def show_username_modal(currency_clicks, wonders_clicks, capital_clicks, continent_clicks, 
                           flag_clicks, world_physical_geography_clicks, india_clicks, us_clicks,
                           k5_math_clicks, cancel_clicks, username_data, pending_quiz_data):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_value = ctx.triggered[0]['value']

        # Handle cancel button
        if triggered_id == 'username-cancel-btn':
            # Hide modal
            modal_style = {
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'backgroundColor': 'rgba(0, 0, 0, 0.5)',
                'display': 'none',
                'justifyContent': 'center',
                'alignItems': 'center',
                'zIndex': '1000'
            }
            return modal_style, username_data.get('username', ''), {}

        # Handle quiz button clicks
        if triggered_value and triggered_value > 0:
            # Determine quiz type
            quiz_type_mapping = {
                'start-currency-quiz': 'currency',
                'start-wonders-quiz': 'wonders',
                'start-capital-quiz': 'capital',
                'start-continent-quiz': 'continent',
                'start-flag-quiz': 'flag',
                'start-physical-geography-quiz': 'world_physical_geography',
                'start-india-capital-quiz': 'india_capital',
                'start-us-capital-quiz': 'us_capital',
                'start-k5-math-quiz': 'k5_math'
            }
            
            quiz_type = quiz_type_mapping.get(triggered_id)
            if quiz_type:
                # Show modal
                modal_style = {
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'backgroundColor': 'rgba(0, 0, 0, 0.5)',
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'zIndex': '1000'
                }
                current_username = username_data.get('username', '')
                if current_username == 'anonymous_user':
                    current_username = ''
                
                pending_quiz = {'quiz_type': quiz_type}
                return modal_style, current_username, pending_quiz

        raise dash.exceptions.PreventUpdate

    # Callback for username confirmation and quiz start
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
        prevent_initial_call=True
    )
    def start_quiz_with_username(confirm_clicks, username_input, pending_quiz, current_username_data):
        if not confirm_clicks or not pending_quiz.get('quiz_type'):
            raise dash.exceptions.PreventUpdate

        quiz_type = pending_quiz['quiz_type']
        
        # Use entered username or default to anonymous_user
        username = username_input.strip() if username_input and username_input.strip() else 'anonymous_user'
        
        # Get quiz questions - handle math vs regular quizzes
        if quiz_type == 'k5_math':
            questions = get_math_quiz_questions(quiz_type, None, 10)  # Math quizzes use 10 questions
            quiz_type_display = MATH_QUIZ_TYPE_LABEL[quiz_type]
        else:
            questions = get_quiz_questions(quiz_type, None, NUM_OF_QUESTIONS)
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]

        # Start a new quiz session for analytics with the username
        session_id = quiz_stats.start_quiz_session(
            session_name=f"{quiz_type_display} Quiz", 
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

        # Styles for when quiz is active
        quiz_selection_quiz_active_style = {'display': 'none'}
        quiz_content_quiz_active_style = {
            'display': 'block',
            'width': '100%',
            'minHeight': '100vh',
            'padding': '10px 20px',
            'margin': '0',
            'boxSizing': 'border-box'
        }
        main_layout_quiz_active_style = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'flex-start',
            'width': '100%',
            'maxWidth': '98vw',
            'margin': '0 auto',
            'padding': '0'
        }
        quiz_active_store_data = {'active': True}

        # Hide modal
        modal_style = {
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0, 0, 0, 0.5)',
            'display': 'none',
            'justifyContent': 'center',
            'alignItems': 'center',
            'zIndex': '1000'
        }

        # Update username store
        updated_username_data = {'username': username}

        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}

        return (create_question_layout(question_data, 0, len(questions)),
                new_data,
                quiz_selection_quiz_active_style,
                quiz_content_quiz_active_style,
                progress_bar,
                progress_style,
                main_layout_quiz_active_style,
                quiz_active_store_data,
                "hide",
                updated_username_data,
                modal_style)

    # Callback for restart button from completion screen (uses stored username)
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True),
        Output('quiz-active-store', 'data', allow_duplicate=True),
        Input('restart-current-quiz', 'n_clicks'),
        [State('current-question-store', 'data'),
         State('username-store', 'data')],
        prevent_initial_call=True
    )
    def restart_current_quiz(restart_clicks, current_data, username_data):
        if not restart_clicks or restart_clicks == 0:
            raise dash.exceptions.PreventUpdate

        # Get the quiz type from the previous quiz session (stored in completion data or fallback)
        quiz_type = 'currency'  # Default fallback
        if current_data and 'quiz_type' in current_data:
            quiz_type = current_data['quiz_type']
        
        # Set quiz_type_display and get questions based on quiz_type
        if quiz_type == 'k5_math':
            questions = get_math_quiz_questions(quiz_type, None, 10)  # Math quizzes use 10 questions
            quiz_type_display = MATH_QUIZ_TYPE_LABEL[quiz_type]
        elif quiz_type in QUIZ_TYPE_LABEL:
            questions = get_quiz_questions(quiz_type, None, NUM_OF_QUESTIONS)
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        else:
            questions = get_quiz_questions(quiz_type, None, NUM_OF_QUESTIONS)
            quiz_type_display = f"{quiz_type.capitalize()} Quiz" # Fallback just in case
        
        # Use stored username
        username = username_data.get('username', 'anonymous_user')
        
        # Start a new quiz session for analytics
        session_id = quiz_stats.start_quiz_session(
            session_name=f"{quiz_type_display} Quiz", 
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

        # Styles for when quiz is active (same as start_quiz)
        main_layout_quiz_active_style = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'flex-start',
            'width': '100%', # Take full width of its own parent (app-background)
            'maxWidth': '98vw', # Limit the overall visible width to 98% of viewport
            'margin': '0 auto', # Center this main wrapper horizontally
            'padding': '0' # Remove padding here, let inner elements handle it
        }
        quiz_active_store_data = {'active': True}

        # Show progress bar
        progress_bar = create_progress_bar(0, len(questions))
        progress_style = {'display': 'block'}

        return (create_question_layout(question_data, 0, len(questions)),
                new_data,
                progress_bar,
                progress_style,
                main_layout_quiz_active_style,
                quiz_active_store_data)

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

            # Record the answer for analytics
            if 'session_id' in current_data and 'question_start_time' in current_data:
                response_time = time.time() - current_data['question_start_time']
                try:
                    # Get question ID from the question data if available
                    question_id = question_data.get('id', current_index + 1)  # Fallback to index+1
                    user_answer = question_data['options'][clicked_index]
                    
                    quiz_stats.record_quiz_answer_with_session(
                        session_id=current_data['session_id'],
                        question_id=question_id,
                        is_correct=is_correct,
                        response_time=response_time,
                        user_answer=user_answer
                    )
                except Exception as e:
                    print(f"Error recording quiz answer: {e}")

            # Create feedback
            fun_fact = question_data.get('fun_fact', '')
            feedback = create_feedback_message(
                is_correct,
                question_data['options'][question_data['correct']],
                fun_fact
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
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}, 'quiz_type': quiz_type}
                return completion_screen, completion_data, []
            else:
                # Next question
                question_data = questions[next_index]
                updated_data = current_data.copy()
                updated_data['index'] = next_index
                updated_data['answered'] = False
                updated_data['selected_answer'] = None
                updated_data['question_start_time'] = time.time()  # Reset timer for next question

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

            # Complete the quiz session for analytics
            if 'session_id' in current_data:
                try:
                    quiz_stats.end_quiz_session(current_data['session_id'])
                except Exception as e:
                    print(f"Error ending quiz session: {e}")

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

            # Keep the quiz data for potential restart, but mark as completed
            completion_data = {
                'index': current_data['index'],
                'score': current_data['score'],
                'questions': questions,
                'answered': False,
                'user_answers': user_answers,
                'quiz_type': quiz_type,
                'completed': True
            }
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
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True),
        Output('quiz-active-store', 'data', allow_duplicate=True),
        Output('page-content', 'data-navbar-auto-hide', allow_duplicate=True),  # New output for navbar control
        Input('quit-quiz-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def quit_quiz(quit_clicks):
        if quit_clicks:
            return _return_to_quiz_selection(None)
        raise dash.exceptions.PreventUpdate

    # Callback for "Back to Quiz Selection" button on completion screen
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('quiz-selection-area', 'style', allow_duplicate=True),
        Output('quiz-content-area', 'style', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True),
        Output('quiz-active-store', 'data', allow_duplicate=True),
        Output('page-content', 'data-navbar-auto-hide', allow_duplicate=True),  # New output for navbar control
        Input('back-to-selection', 'n_clicks'),
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def back_to_selection(back_clicks, current_data):
        if back_clicks:
            return _return_to_quiz_selection(current_data)
        raise dash.exceptions.PreventUpdate


def _return_to_quiz_selection(current_data=None):
    """Helper function to return to the quiz selection screen."""
    # Styles for when quiz is NOT active (selection view)
    quiz_selection_default_style = {'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'padding': '20px', 'flexGrow': 1}
    quiz_content_default_style = {'display': 'none'}
    progress_style = {'display': 'none'} # Progress bar hidden
    main_layout_default_style = {
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'flex-start',
        'maxWidth': '1400px', # Revert to the default max-width for the selection screen
        'margin': '0 auto',
        'padding': '20px 0'
    }
    quiz_active_store_default_data = {'active': False}

    reset_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}}

    return ([], # question-container children (empty)
            reset_data, # current-question-store data (reset)
            quiz_selection_default_style, # quiz-selection-area style (visible)
            quiz_content_default_style, # quiz-content-area style (hidden)
            progress_style, # progress-container style (hidden)
            [], # progress-container children (empty)
            main_layout_default_style, # main-layout-container-wrapper style (default)
            quiz_active_store_default_data, # quiz-active-store data (inactive)
            "show" # Show navbar when returning to quiz selection
    )
