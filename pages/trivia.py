"""
Trivia page for country-related quiz questions.
"""

from dash import html, dcc, Input, Output, State, callback_context
import dash.exceptions
import random
import json
from utils.data_processing import load_countries_data

# Load the data for trivia questions
df = load_countries_data()

def generate_quiz_questions(num_questions=10):
    """Generate random country-currency questions."""
    # Filter out countries with missing or invalid currency data
    valid_countries = df[
        (df['currency'].notna()) & 
        (df['currency'] != '') & 
        (df['currency'] != 'No reliable data available')
    ].copy()
    
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        correct_currency = country_row['currency']
        
        # Generate 3 wrong currency options
        other_currencies = valid_countries[
            (valid_countries['country'] != correct_country) & 
            (valid_countries['currency'] != correct_currency)
        ]['currency'].unique()
        
        if len(other_currencies) >= 3:
            wrong_currencies = random.sample(list(other_currencies), 3)
        else:
            # If not enough unique currencies, use what we have and pad with generic ones
            wrong_currencies = list(other_currencies)
            generic_currencies = ['Dollar', 'Euro', 'Pound', 'Franc', 'Peso', 'Real', 'Rupiah']
            for currency in generic_currencies:
                if len(wrong_currencies) < 3 and currency != correct_currency:
                    wrong_currencies.append(currency)
                if len(wrong_currencies) >= 3:
                    break
        
        # Create options list with correct answer at random position
        options = wrong_currencies[:3] + [correct_currency]
        random.shuffle(options)
        correct_index = options.index(correct_currency)
        
        question = {
            "question": f"What is the currency of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "explanation": f"The currency of {correct_country} is {correct_currency}."
        }
        questions.append(question)
    
    return questions

def get_trivia_layout():
    """Get the layout for the trivia page."""
    return html.Div([
        html.H1("Country Trivia", style={'textAlign': 'center', 'marginBottom': '30px'}),
        html.P("Test your knowledge about countries around the world!", 
               style={'textAlign': 'center', 'marginBottom': '30px', 'fontSize': '18px'}),
        
        # Question container
        html.Div(id="question-container", children=[
            html.Div([
                html.Button("Start Quiz", id="start-quiz-btn", 
                           style={'padding': '15px 30px', 'fontSize': '18px', 
                                  'backgroundColor': '#007bff', 'color': 'white', 
                                  'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
            ], style={'textAlign': 'center'})
        ]),
        
        # Hidden storage for current question
        dcc.Store(id='current-question-store', data={'index': 0, 'score': 0}),
        
        # Hidden trigger for button clicks
        html.Div(id='hidden-trigger', style={'display': 'none'}),
        
        # Results area
        html.Div(id="results-area", style={'marginTop': '30px'}),
        
    ], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'})

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
        html.H3(f"Question {question_index + 1} of {total_questions}", 
                style={'textAlign': 'center', 'color': '#007bff'}),
        html.H4(question_data['question'], 
                style={'marginBottom': '20px', 'textAlign': 'center'}),
        
        html.Div(answer_buttons),
        
        html.Div(id="question-feedback", style={'marginTop': '20px'}),
        
        html.Div([
            html.Button("Next Question", id='next-btn', 
                       style={'padding': '10px 20px', 'fontSize': '16px',
                              'backgroundColor': '#28a745', 'color': 'white',
                              'border': 'none', 'borderRadius': '5px', 
                              'cursor': 'pointer', 'display': 'block' if is_answered else 'none'})
        ], style={'textAlign': 'center', 'marginTop': '20px'})
    ])

def register_trivia_callbacks(app):
    """Register callbacks for the trivia page."""
    
    # Callback for starting the quiz
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Input('start-quiz-btn', 'n_clicks'),
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def start_quiz(n_clicks, current_data):
        if n_clicks:
            questions = generate_quiz_questions(10)
            question_data = questions[0]
            new_data = {
                'index': 0, 
                'score': 0, 
                'questions': questions,
                'answered': False
            }
            return create_question_layout(question_data, 0, len(questions)), new_data
        raise dash.exceptions.PreventUpdate
    
    # Single callback to handle all quiz interactions with fixed IDs
    @app.callback(
        Output('question-container', 'children', allow_duplicate=True),
        Output('current-question-store', 'data', allow_duplicate=True),
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
            layout.children[3] = feedback
            
            # Update data
            updated_data = current_data.copy()
            updated_data['score'] = new_score
            updated_data['answered'] = True
            
            return layout, updated_data
        
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
                
                return html.Div([
                    html.H2("Quiz Completed! 🎉", style={'textAlign': 'center', 'color': '#28a745'}),
                    html.Div([
                        html.H3(f"Your Score: {score} out of {total}", 
                               style={'textAlign': 'center', 'fontSize': '24px', 'margin': '20px 0'}),
                        html.H4(f"{percentage}%", 
                               style={'textAlign': 'center', 'fontSize': '36px', 'color': color, 'margin': '10px 0'}),
                        html.P(performance_msg, 
                              style={'textAlign': 'center', 'fontSize': '20px', 'color': color, 'margin': '20px 0'})
                    ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'borderRadius': '10px', 'margin': '20px 0'}),
                    html.Button("Start New Quiz", id="start-quiz-btn", 
                               style={'padding': '15px 30px', 'fontSize': '18px', 
                                      'backgroundColor': '#007bff', 'color': 'white', 
                                      'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                ], style={'textAlign': 'center'}), {'index': 0, 'score': 0, 'questions': [], 'answered': False}
            else:
                # Next question
                question_data = questions[next_index]
                updated_data = current_data.copy()
                updated_data['index'] = next_index
                updated_data['answered'] = False
                return create_question_layout(question_data, next_index, len(questions)), updated_data
        
        raise dash.exceptions.PreventUpdate
