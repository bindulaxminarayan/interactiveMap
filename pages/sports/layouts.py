"""
Sports quiz page layouts.
"""

from pages.trivia.ui_components import create_quiz_layout_structure

# Sports quiz cards
SPORTS_QUIZ_CARDS = [
    {
        "title": "Soccer/Football",
        "emoji": "⚽",
        "description": "World's most popular sport",
        "button_id": "start-soccer-quiz",
        "is_disabled": True
    },
    {
        "title": "Basketball",
        "emoji": "🏀",
        "description": "NBA, college basketball, and more",
        "button_id": "start-basketball-quiz",
        "is_disabled": True
    },
    {
        "title": "Baseball",
        "emoji": "⚾",
        "description": "America's pastime",
        "button_id": "start-baseball-quiz",
        "is_disabled": True
    },
    {
        "title": "American Football",
        "emoji": "🏈",
        "description": "NFL and college football",
        "button_id": "start-american-football-quiz",
        "is_disabled": True
    },
    {
        "title": "Tennis",
        "emoji": "🎾",
        "description": "Grand slams and tournaments",
        "button_id": "start-tennis-quiz",
        "is_disabled": True
    },
    {
        "title": "Olympics",
        "emoji": "🏅",
        "description": "Summer and winter Olympics",
        "button_id": "start-olympics-quiz",
        "is_disabled": True
    }
]

def get_sports_layout():
    """Get the layout for the sports quiz page."""
    return create_quiz_layout_structure(SPORTS_QUIZ_CARDS)