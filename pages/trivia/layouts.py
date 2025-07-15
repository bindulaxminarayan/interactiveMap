"""
Layout components for the trivia module.
"""

from dash import html, dcc

def create_side_panel():
    """Create a side panel with category labels."""
    return html.Div([
        html.H2("Categories", className="side-panel-title"),
        html.Button("World", id="category-world", className="category-button category-button-active"), # Default active
        html.Button("United States", id="category-us", className="category-button"),
        html.Button("India", id="category-india", className="category-button"),
        html.Button("China", id="category-china", className="category-button"),
    ], id="side-panel", className="side-panel-container") # Added id="side-panel"

def create_quiz_card(title, emoji, description, button_text_unused, button_id, is_disabled=False):
    """Create a quiz card with title, description and button."""
    # Determine dynamic styles based on is_disabled
    wrapper_style = {
        'opacity': '1' if not is_disabled else '0.7',
    }
    title_style = {
        'color': '#007bff' if not is_disabled else '#6c757d',
    }
    description_style = {
        'color': '#666' if not is_disabled else '#999',
    }
    button_style = {
        'backgroundColor': '#28a745' if not is_disabled else '#6c757d',
        'cursor': 'pointer' if not is_disabled else 'not-allowed',
        'opacity': '1' if not is_disabled else '0.6',
    }

    return html.Div([
        html.Div([
            html.H3(f"{emoji} {title}", className="quiz-card-title", style=title_style),
            html.P(description, className="quiz-card-description", style=description_style),
            html.Button("Start Quiz", # Updated button text
                       id=button_id,
                       disabled=is_disabled,
                       className="quiz-card-button",
                       style=button_style)
        ], className='quiz-card-container')  # Removed inline style from main container
    ], style=wrapper_style)  # Apply opacity to wrapper instead

def create_quiz_cards_grid():
    """Create a grid of quiz cards."""
    return html.Div([
        # First row
        html.Div([
              create_quiz_card(
                title="General",
                emoji="🌎",
                description="Match countries, capital, currencies!",
                button_text_unused="Start Country Quiz", # Parameter not used directly now
                button_id="start-country-quiz"
            ),
            create_quiz_card(
                title="Currencies",
                emoji="💰",
                description="Match countries with their currencies!",
                button_text_unused="Start Currency Quiz", # Parameter not used directly now
                button_id="start-currency-quiz"
            ),
            create_quiz_card(
                title="Capital Cities",
                emoji="🏛️",
                description="Match countries with their capitals!",
                button_text_unused="Start Capital Quiz", # Parameter not used directly now
                button_id="start-capital-quiz"
            ),
        ], className="quiz-cards-row"),

        # Second row
        html.Div([
            create_quiz_card(
                title="Continents",
                emoji="🌐",
                description="Match countries with their continents!",
                button_text_unused="Start Continent Quiz", # Parameter not used directly now
                button_id="start-continent-quiz"
            ),
            create_quiz_card(
                title="Flags",
                emoji="🇺🇳",
                description="Match flag with their countries!",
                button_text_unused="Start Flag Quiz", # Parameter not used directly now
                button_id="start-flag-quiz"
            ),
            # Removed the "Locate Countries" quiz card as requested
        ], className="quiz-cards-row")
    ], className="quiz-cards-grid-container")

def create_hidden_elements():
    """Create hidden elements that callbacks need to reference."""
    return html.Div([
        html.Button("Restart Currency", id="restart-currency-quiz-result", style={'display': 'none'}),
        html.Button("Restart Capital", id="restart-capital-quiz-result", style={'display': 'none'}),
        html.Button("Restart Continent", id="restart-continent-quiz-result", style={'display': 'none'}),
        html.Button("Restart Country", id="restart-country-quiz-result", style={'display': 'none'}),
        html.Button("Restart Flag", id="restart-flag-quiz-result", style={'display': 'none'}),
        html.Button("Restart Current", id="restart-current-quiz", style={'display': 'none'}),
        html.Button("Next Question", id='next-btn', style={'display': 'none'}),
        html.Button("View Results", id='view-results-btn', style={'display': 'none'}),
        html.Button("Quit Quiz", id='quit-quiz-btn', style={'display': 'none'}),
        html.Button("Back to Selection", id="back-to-selection", style={'display': 'none'}),
        html.Button("", id='answer-btn-0', style={'display': 'none'}),
        html.Button("", id='answer-btn-1', style={'display': 'none'}),
        html.Button("", id='answer-btn-2', style={'display': 'none'}),
        html.Button("", id='answer-btn-3', style={'display': 'none'}),
    ], id='hidden-elements-container', style={'display': 'none'})

def get_trivia_layout():
    """Get the layout for the trivia page with card-based quiz selection."""
    return html.Div([
        html.H1("World Trivia", className="main-title"),
        html.Div(id="quiz_type_display", className="quiz-type-display"),

        # Global hidden elements that callbacks need to reference
        create_hidden_elements(),

        # Main content area with side panel and quiz content
        html.Div([
            # Side Panel
            create_side_panel(),

            # Quiz selection area or active quiz area
            html.Div([
                # Quiz Cards Grid (initially displayed)
                html.Div([
                    create_quiz_cards_grid()
                ], id="quiz-selection-area"), # This will be hidden when quiz starts

                # Quiz Content Area (initially hidden)
                html.Div([
                    # Progress bar container (initially hidden)
                    html.Div(id="progress-container", children=[], style={'display': 'none'}),

                    # Question container
                    html.Div(id="question-container", children=[]),

                    # Hidden storage for current question
                    dcc.Store(id='current-question-store', data={'index': 0, 'score': 0}),

                    # Hidden trigger for button clicks
                    html.Div(id='hidden-trigger', style={'display': 'none'}),

                    # Results area
                    html.Div(id="results-area", style={'marginTop': '30px'}),

                ], id="quiz-content-area", className="quiz-content-area", style={'display': 'none'}) # Initially hidden
            ], id="main-content-area", className="main-content-area"), # This will expand

        ], id="main-layout-container-wrapper", className="main-layout-container"), # Added id="main-layout-container-wrapper"

        # Hidden dcc.Store to track if a quiz is active
        dcc.Store(id='quiz-active-store', data={'active': False})

    ], className="app-background")
