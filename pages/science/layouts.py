"""
Science quiz page layouts.
"""

from pages.trivia.ui_components import create_quiz_layout_structure

# Science quiz cards
SCIENCE_QUIZ_CARDS = [
    {
        "title": "Biology",
        "emoji": "🧬",
        "description": "Life sciences and living organisms",
        "button_id": "start-biology-quiz",
    },
    {
        "title": "Chemistry",
        "emoji": "🧪",
        "description": "Elements and chemical reactions",
        "button_id": "start-chemistry-quiz",
    },
    {
        "title": "Physics",
        "emoji": "⚛️",
        "description": "Laws of physics and motion",
        "button_id": "start-physics-quiz",
        "is_disabled": True
    },
    {
        "title": "Astronomy",
        "emoji": "🌌",
        "description": "Space, stars, and planets",
        "button_id": "start-astronomy-quiz",
        "is_disabled": True
    },
    {
        "title": "Earth Science",
        "emoji": "🌍",
        "description": "Geology, weather, and climate",
        "button_id": "start-earth-science-quiz",
        "is_disabled": True
    },
    {
        "title": "Technology",
        "emoji": "💻",
        "description": "Modern technology and computing",
        "button_id": "start-technology-quiz",
        "is_disabled": True
    }
]

def get_science_layout():
    """Get the layout for the science quiz page."""
    return create_quiz_layout_structure(SCIENCE_QUIZ_CARDS)
