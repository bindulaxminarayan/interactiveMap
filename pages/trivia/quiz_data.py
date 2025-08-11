"""
Quiz data configurations for different categories.
"""

from ..science.layouts import SCIENCE_QUIZ_CARDS
from ..geography.layouts import GEOGRAPHY_QUIZ_CARDS
from ..history.layouts import HISTORY_QUIZ_CARDS
from ..mathematics.layouts import MATHEMATICS_QUIZ_CARDS
from ..sports.layouts import SPORTS_QUIZ_CARDS

# Category mapping
CATEGORY_QUIZ_CARDS_MAP = {
    'geography': GEOGRAPHY_QUIZ_CARDS,
    'math': MATHEMATICS_QUIZ_CARDS,
    'history': HISTORY_QUIZ_CARDS,
    'science': SCIENCE_QUIZ_CARDS,
    'sports': SPORTS_QUIZ_CARDS
}

def get_cards_for_category(category):
    """Get quiz cards data for a specific category."""
    return CATEGORY_QUIZ_CARDS_MAP.get(category, GEOGRAPHY_QUIZ_CARDS)  # Default to geography
