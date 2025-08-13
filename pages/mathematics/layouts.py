"""
Mathematics quiz page layouts.
"""

from pages.trivia.ui_components import create_quiz_layout_structure

# Mathematics quiz cards
MATHEMATICS_QUIZ_CARDS = [
    {
        "title": "K-5 Math",
        "emoji": "🔢",
        "description": "Elementary math for grades K-5",
        "button_id": "start-k5-math-quiz",
        "is_disabled": True
    },
    {
        "title": "6-8 Math",
        "emoji": "📐",
        "description": "Middle school mathematics",
        "button_id": "start-middle-math-quiz",
        "is_disabled": True
    },
    {
        "title": "Algebra",
        "emoji": "🔡",
        "description": "Basic and advanced algebra",
        "button_id": "start-algebra-quiz",
        "is_disabled": True
    },
    {
        "title": "Geometry",
        "emoji": "📏",
        "description": "Shapes, angles, and measurements",
        "button_id": "start-geometry-quiz",
        "is_disabled": True
    },
    {
        "title": "Calculus",
        "emoji": "∫",
        "description": "Differential and integral calculus",
        "button_id": "start-calculus-quiz",
        "is_disabled": True
    },
    {
        "title": "Statistics",
        "emoji": "📊",
        "description": "Data analysis and probability",
        "button_id": "start-statistics-quiz",
        "is_disabled": True
    }
]

def get_mathematics_layout():
    """Get the layout for the mathematics quiz page."""
    return create_quiz_layout_structure(MATHEMATICS_QUIZ_CARDS)