"""
Navigation bar component for the interactive map application.
"""

from dash import html

def create_simple_navbar():
    """Create a simple navigation bar without Bootstrap dependencies."""
    return html.Div([
        html.Nav([
            html.Div([
                html.A("QuizVerse", href="/", className="navbar-brand"),
                html.Div([
                    html.A("Geography", href="/geography", className="nav-link"),
                    html.A("History", href="/history", className="nav-link"),
                    html.A("Science", href="/science", className="nav-link"),
                    html.A("Mathematics", href="/mathematics", className="nav-link"),
                    html.A("Sports", href="/sports", className="nav-link"),
                    html.A("Explore", href="/", className="nav-link"),
                ], className="navbar-nav")
            ], className="navbar-container")
        ], className="navbar"),
    ])
