"""
History quiz page layouts.
"""

from pages.trivia.ui_components import create_quiz_layout_structure

# History quiz cards
HISTORY_QUIZ_CARDS = [
    {
        "title": "Leaders",
        "emoji": "👑",
        "description": "Historical leaders and rulers, influencers",
        "button_id": "start-leaders-quiz"
    },
    {
        "title": "World History",
        "emoji": "🌍",
        "description": "Major world historical events",
        "button_id": "start-world-history-quiz",
        "is_disabled": True
    },
    {
        "title": "Ancient Civilizations",
        "emoji": "🏛️",
        "description": "Learn about ancient civilizations",
        "button_id": "start-ancient-civilizations-quiz",
        "is_disabled": True
    },
    {
        "title": "Wars & Conflicts",
        "emoji": "⚔️",
        "description": "Historical wars and conflicts",
        "button_id": "start-wars-quiz",
        "is_disabled": True
    },
    {
        "title": "Dates & Timeline",
        "emoji": "📅",
        "description": "Important historical dates",
        "button_id": "start-dates-quiz",
        "is_disabled": True
    }
]

def get_history_layout():
    """Get the layout for the history quiz page."""
    return create_quiz_layout_structure(HISTORY_QUIZ_CARDS)
