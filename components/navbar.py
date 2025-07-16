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
                    html.A("Geography", href="/trivia?category=geography", className="nav-link"),
                    html.A("History", href="/trivia?category=history", className="nav-link"),
                    html.A("Science", href="/trivia?category=science", className="nav-link"),
                    html.A("Sports", href="/trivia?category=sports", className="nav-link"),
                    html.A("Explore", href="/", className="nav-link"),
                ], className="navbar-nav")
            ], className="navbar-container")
        ], className="navbar"),
    ])
