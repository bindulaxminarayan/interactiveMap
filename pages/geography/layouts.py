"""
Geography quiz page layouts.
"""

from pages.trivia.ui_components import create_quiz_layout_structure
from dash import html

# Geography quiz cards
GEOGRAPHY_QUIZ_CARDS = [
    {
        "title": "Physical Geography",
        "emoji": "🏔️",
        "description": "Landscapes etc",
        "button_id": "start-physical-geography-quiz"
    },
    {
        "title": "Wonders",
        "emoji": "🤩",
        "description": "Wonders of the world!",
        "button_id": "start-wonders-quiz"
    },
    {
        "title": "Flags",
        "emoji": "🏳️",
        "description": "Match a flag with a country!",
        "button_id": "start-flag-quiz"
    },
    {
        "title": "Currencies",
        "emoji": "💰",
        "description": "Match a country with currency!",
        "button_id": "start-currency-quiz"
    },
    {
        "title": "Capitals",
        "emoji": "🏛️",
        "description": "Match a country with capital!",
        "button_id": "start-capital-quiz"
    },
    {
        "title": "Continents",
        "emoji": "🌐",
        "description": "Match a country with continent!",
        "button_id": "start-continent-quiz"
    },
    {
        "title": "US States",
        "emoji": "🇺🇸",
        "description": "Match state with capital!",
        "button_id": "start-us-capital-quiz"
    },
    {
        "title": "India States",
        "emoji": "🇮🇳",
        "description": "Match state with capital!",
        "button_id": "start-india-capital-quiz"
    }
]

def get_geography_layout():
    """Get the layout for the geography quiz page."""
    return create_quiz_layout_structure(GEOGRAPHY_QUIZ_CARDS)
