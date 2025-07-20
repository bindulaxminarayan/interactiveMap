"""
Science quiz callbacks.
"""

from pages.trivia.callbacks import register_trivia_callbacks

def register_science_callbacks(app):
    """Register callbacks for the science quiz page."""
    # Reuse the existing trivia callbacks since they handle all the quiz logic
    register_trivia_callbacks(app)
