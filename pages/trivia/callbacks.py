"""
Dash callbacks for the trivia module.
"""

from dash import Input, Output, State, callback_context, html
import dash.exceptions
from utils.data_processing import load_countries_data
from utils.quiz_generators import get_quiz_questions,QUIZ_TYPE_LABEL
from .quiz_components import create_progress_bar, create_question_layout, create_completion_screen
from .components import create_feedback_message
from .layouts import create_quiz_cards_grid, WORLD_QUIZ_CARDS_DATA # Re-added import

# Load the data for trivia questions
df = load_countries_data()

# Define reusable CSS class names for category buttons
ACTIVE_CATEGORY_CLASS = "category-button category-button-active"
INACTIVE_CATEGORY_CLASS = "category-button"

def register_trivia_callbacks(app):
    """Register all callbacks for the trivia page."""

    # Callback for starting quizzes from quiz cards
    @app.callback(
        Output('quiz_type_display','children'),
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Output('quiz-selection-area', 'style'),
        Output('quiz-content-area', 'style'),
        Output('progress-container', 'children'),
        Output('progress-container', 'style'),
        Output('side-panel', 'style'),
        Output('main-layout-container-wrapper', 'style'),
        Output('quiz-active-store', 'data'),
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
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        elif triggered_id == 'start-capital-quiz':
            questions = get_quiz_questions('capital', df, 10)
            quiz_type = 'capital'
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        elif triggered_id == 'start-continent-quiz':
            questions = get_quiz_questions('continent', df, 10)
            quiz_type = 'continent'
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        elif triggered_id == 'start-country-quiz':
            questions = get_quiz_questions('country', df, 10)
            quiz_type = 'country'
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        elif triggered_id == 'start-flag-quiz':
            questions = get_quiz_questions('flag', df, 10)
            quiz_type = 'flag'
            quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
        else:
            raise dash.exceptions.PreventUpdate

        question_data = questions[0]
        new_data = {
            'index': 0,
            'score': 0,
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type,
            'quiz_type_display': quiz_type_display,
            'user_answers': {}
        }

        # Styles for when quiz is active
        side_panel_quiz_active_style = {'display': 'none'} # Hide side panel
        quiz_selection_quiz_active_style = {'display': 'none'} # Hide quiz selection area
        quiz_content_quiz_active_style = {
            'display': 'block', # Or 'flex' depending on inner content
            'backgroundColor': '#ffffff',
            'borderRadius': '15px',
            'border': '1px solid #dee2e6',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'padding': '30px', # Internal padding for content
            'margin': '0', # No external margin, let parent handle spacing
            'minHeight': '500px',
            'flexGrow': 1,
            'width': '100%', # Take up 100% of its parent's available width
            'boxSizing': 'border-box' # Include padding in element's total width/height
        }
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

        return (quiz_type_display,
                create_question_layout(question_data, 0, len(questions)),
                new_data,
                quiz_selection_quiz_active_style, # Hide quiz selection
                quiz_content_quiz_active_style,   # Show quiz content
                progress_bar,
                progress_style,
                side_panel_quiz_active_style,     # Hide side panel
                main_layout_quiz_active_style,    # Adjust main wrapper
                quiz_active_store_data            # Update quiz-active-store
        )

    # Callback for restart button from completion screen
    @app.callback(
        Output('quiz_type_display','children',allow_duplicate=True),
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
        Output('progress-container', 'children', allow_duplicate=True),
        Output('progress-container', 'style', allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True), # Added output
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True), # Added output
        Output('quiz-active-store', 'data', allow_duplicate=True), # Added output
        Input('restart-current-quiz', 'n_clicks'),
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def restart_current_quiz(restart_clicks, current_data):
        if not restart_clicks or restart_clicks == 0:
            raise dash.exceptions.PreventUpdate

        # Get the quiz type from the previous quiz session (stored in completion data or fallback)
        quiz_type = 'country'  # Default fallback
        if current_data and 'quiz_type' in current_data:
            quiz_type = current_data['quiz_type']
            if quiz_type in QUIZ_TYPE_LABEL:
                quiz_type_display = QUIZ_TYPE_LABEL[quiz_type]
            else:
                quiz_type_display = f"{quiz_type.capitalize()} Quiz" # Fallback just in case

        questions = get_quiz_questions(quiz_type, df, 10)
        question_data = questions[0]
        new_data = {
            'index': 0,
            'score': 0,
            'questions': questions,
            'answered': False,
            'quiz_type': quiz_type,
            'quiz_type_display': quiz_type_display,
            'user_answers': {}
        }

        # Styles for when quiz is active (same as start_quiz)
        side_panel_quiz_active_style = {'display': 'none'}
        quiz_content_quiz_active_style = { # Corrected variable name
            'display': 'block',
            'backgroundColor': '#ffffff',
            'borderRadius': '15px',
            'border': '1px solid #dee2e6',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'padding': '30px',
            'margin': '0', # No external margin, let parent handle spacing
            'minHeight': '500px',
            'flexGrow': 1,
            'width': '100%',
            'boxSizing': 'border-box'
        }
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

        return (quiz_type_display,
                create_question_layout(question_data, 0, len(questions)),
                new_data,
                progress_bar,
                progress_style,
                side_panel_quiz_active_style,
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
                completion_data = {'index': 0, 'score': 0, 'questions': [], 'answered': False, 'user_answers': {}, 'quiz_type': quiz_type}
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
        Output('quiz_type_display','children',allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True),
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True),
        Output('quiz-active-store', 'data', allow_duplicate=True),
        Output('category-world', 'className', allow_duplicate=True), # New output for category button styling
        Output('category-us', 'className', allow_duplicate=True),    # New output
        Output('category-india', 'className', allow_duplicate=True), # New output
        Output('category-china', 'className', allow_duplicate=True), # New output
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
        Output('quiz_type_display','children',allow_duplicate=True),
        Output('side-panel', 'style', allow_duplicate=True),
        Output('main-layout-container-wrapper', 'style', allow_duplicate=True),
        Output('quiz-active-store', 'data', allow_duplicate=True),
        Output('category-world', 'className', allow_duplicate=True), # New output
        Output('category-us', 'className', allow_duplicate=True),    # New output
        Output('category-india', 'className', allow_duplicate=True), # New output
        Output('category-china', 'className', allow_duplicate=True), # New output
        Input('back-to-selection', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_selection(back_clicks):
        if back_clicks:
            return _return_to_quiz_selection()
        raise dash.exceptions.PreventUpdate

    # New Callback for Category Selection
    @app.callback(
        Output('quiz-selection-area', 'children'),
        Output('category-world', 'className'),
        Output('category-us', 'className'),
        Output('category-india', 'className'),
        Output('category-china', 'className'),
        [Input('category-world', 'n_clicks'),
         Input('category-us', 'n_clicks'),
         Input('category-india', 'n_clicks'),
         Input('category-china', 'n_clicks')],
        State('quiz-active-store', 'data'), # Use State to prevent category changes during an active quiz
        prevent_initial_call=True
    )
    def display_category_cards(world_clicks, us_clicks, india_clicks, china_clicks, quiz_active_state):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        # Prevent category changes if a quiz is currently active
        if quiz_active_state and quiz_active_state.get('active', False):
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Default class names
        world_class = INACTIVE_CATEGORY_CLASS
        us_class = INACTIVE_CATEGORY_CLASS
        india_class = INACTIVE_CATEGORY_CLASS
        china_class = INACTIVE_CATEGORY_CLASS

        quiz_cards_to_display = []

        if triggered_id == 'category-world':
            quiz_cards_to_display = create_quiz_cards_grid(WORLD_QUIZ_CARDS_DATA)
            world_class = ACTIVE_CATEGORY_CLASS
        elif triggered_id == 'category-us':
            # For US, India, China, return an empty list for now
            quiz_cards_to_display = html.Div([
                html.P("Coming Soon!", style={'textAlign': 'center', 'fontSize': '24px', 'marginTop': '50px', 'color': '#6c757d'})
            ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
            us_class = ACTIVE_CATEGORY_CLASS
        elif triggered_id == 'category-india':
            quiz_cards_to_display = html.Div([
                html.P("Coming Soon!", style={'textAlign': 'center', 'fontSize': '24px', 'marginTop': '50px', 'color': '#6c757d'})
            ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
            india_class = ACTIVE_CATEGORY_CLASS
        elif triggered_id == 'category-china':
            quiz_cards_to_display = html.Div([
                html.P("Coming Soon!", style={'textAlign': 'center', 'fontSize': '24px', 'marginTop': '50px', 'color': '#6c757d'})
            ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
            china_class = ACTIVE_CATEGORY_CLASS

        return (quiz_cards_to_display,
                world_class,
                us_class,
                india_class,
                china_class)


def _return_to_quiz_selection():
    """Helper function to return to the quiz selection screen."""
    # Styles for when quiz is NOT active (selection view)
    side_panel_default_style = {'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'flexShrink': 0,
                                'backgroundColor': '#ffffff', 'borderRadius': '15px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                                'padding': '30px 20px', 'margin': '20px', 'width': '250px', 'minHeight': 'calc(100vh - 40px)'}
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
            "", # quiz_type_display children (empty)
            side_panel_default_style, # side-panel style (visible)
            main_layout_default_style, # main-layout-container-wrapper style (default)
            quiz_active_store_default_data, # quiz-active-store data (inactive)
            ACTIVE_CATEGORY_CLASS, # Set World button to active
            INACTIVE_CATEGORY_CLASS, # Set US button to inactive
            INACTIVE_CATEGORY_CLASS, # Set India button to inactive
            INACTIVE_CATEGORY_CLASS  # Set China button to inactive
    )
