"""
Trivia page for country-related quiz questions.
"""

from dash import html, dcc, Input, Output, State
import random
from utils.data_processing import load_countries_data

# Load the data for trivia questions
df = load_countries_data()

# Sample trivia questions
TRIVIA_QUESTIONS = [
    {
        "question": "Which country has the highest GDP?",
        "options": ["United States", "China", "Japan", "Germany"],
        "correct": 0,
        "explanation": "The United States has the world's largest economy by nominal GDP."
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "correct": 2,
        "explanation": "Canberra is the capital city of Australia, not Sydney or Melbourne as commonly thought."
    },
    {
        "question": "Which currency is used in Japan?",
        "options": ["Yuan", "Won", "Yen", "Rupee"],
        "correct": 2,
        "explanation": "The Japanese Yen is the official currency of Japan."
    }
]

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
        
        # Results area
        html.Div(id="results-area", style={'marginTop': '30px'}),
        
    ], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'})

def create_question_layout(question_data, question_index, total_questions):
    """Create layout for a single question."""
    return html.Div([
        html.H3(f"Question {question_index + 1} of {total_questions}", 
                style={'textAlign': 'center', 'color': '#007bff'}),
        html.H4(question_data['question'], 
                style={'marginBottom': '20px', 'textAlign': 'center'}),
        
        html.Div([
            html.Button(option, id={'type': 'answer-btn', 'index': i}, 
                       style={'display': 'block', 'width': '100%', 'margin': '10px 0',
                              'padding': '15px', 'fontSize': '16px', 'backgroundColor': '#f8f9fa',
                              'border': '2px solid #dee2e6', 'borderRadius': '5px', 
                              'cursor': 'pointer', 'textAlign': 'left'})
            for i, option in enumerate(question_data['options'])
        ]),
        
        html.Div(id="question-feedback", style={'marginTop': '20px'}),
        
        html.Div([
            html.Button("Next Question", id="next-question-btn", 
                       style={'padding': '10px 20px', 'fontSize': '16px',
                              'backgroundColor': '#28a745', 'color': 'white',
                              'border': 'none', 'borderRadius': '5px', 
                              'cursor': 'pointer', 'display': 'none'})
        ], style={'textAlign': 'center', 'marginTop': '20px'})
    ])

def register_trivia_callbacks(app):
    """Register callbacks for the trivia page."""
    @app.callback(
        Output('question-container', 'children'),
        Output('current-question-store', 'data'),
        Input('start-quiz-btn', 'n_clicks'),
        Input('next-question-btn', 'n_clicks'),
        Input({'type': 'answer-btn', 'index': 'ALL'}, 'n_clicks'),
        State('current-question-store', 'data'),
        prevent_initial_call=True
    )
    def handle_quiz_flow(start_clicks, next_clicks, answer_clicks, current_data):
        from dash import callback_context
        
        if not callback_context.triggered:
            return html.Div(), current_data
        
        trigger_id = callback_context.triggered[0]['prop_id']
        
        # Start quiz
        if 'start-quiz-btn' in trigger_id:
            question_data = TRIVIA_QUESTIONS[0]
            return create_question_layout(question_data, 0, len(TRIVIA_QUESTIONS)), {'index': 0, 'score': 0}
        
        # Answer selected
        elif 'answer-btn' in trigger_id:
            # Process answer and show feedback
            current_index = current_data['index']
            question_data = TRIVIA_QUESTIONS[current_index]
            
            feedback = html.Div([
                html.P(f"Correct answer: {question_data['options'][question_data['correct']]}", 
                       style={'fontWeight': 'bold', 'color': '#28a745'}),
                html.P(question_data['explanation'], style={'fontStyle': 'italic'}),
            ])
            
            layout = create_question_layout(question_data, current_index, len(TRIVIA_QUESTIONS))
            layout.children[3] = feedback  # Replace feedback div
            layout.children[4].children[0].style['display'] = 'block'  # Show next button
            
            return layout, current_data
        
        # Next question
        elif 'next-question-btn' in trigger_id:
            next_index = current_data['index'] + 1
            
            if next_index >= len(TRIVIA_QUESTIONS):
                # Quiz completed
                return html.Div([
                    html.H2("Quiz Completed!", style={'textAlign': 'center', 'color': '#28a745'}),
                    html.P(f"Thanks for playing! You answered {current_data['score']} out of {len(TRIVIA_QUESTIONS)} questions correctly.", 
                           style={'textAlign': 'center', 'fontSize': '18px'}),
                    html.Button("Start Over", id="start-quiz-btn", 
                               style={'padding': '15px 30px', 'fontSize': '18px', 
                                      'backgroundColor': '#007bff', 'color': 'white', 
                                      'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                ], style={'textAlign': 'center'}), {'index': 0, 'score': 0}
            else:
                # Next question
                question_data = TRIVIA_QUESTIONS[next_index]
                return create_question_layout(question_data, next_index, len(TRIVIA_QUESTIONS)), {'index': next_index, 'score': current_data['score']}
        
        return html.Div(), current_data
