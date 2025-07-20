"""
Quiz data configurations for different categories.
"""

# Geography quiz cards
GEOGRAPHY_QUIZ_CARDS_DATA = [
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

# History quiz cards
HISTORY_QUIZ_CARDS_DATA = [
    {
        "title": "Coming Soon",
        "emoji": "⏳",
        "description": "History quizzes will be available soon!",
        "button_id": "history-coming-soon",
        "is_disabled": True
    }
]

# Science quiz cards
SCIENCE_QUIZ_CARDS_DATA = [
    {
        "title": "Coming Soon",
        "emoji": "⏳",
        "description": "Science quizzes will be available soon!",
        "button_id": "science-coming-soon",
        "is_disabled": True
    }
]

# Math quiz cards
MATH_QUIZ_CARDS_DATA = [
    {
        "title": "K-5",
        "emoji": "⏳",
        "description": "Math quizzes for K-5",
        "button_id": "math-k-5-soon",
        "is_disabled": True
    }
]

# Sports quiz cards
SPORTS_QUIZ_CARDS_DATA = [
    {
        "title": "Coming Soon",
        "emoji": "⏳",
        "description": "Sports quizzes will be available soon!",
        "button_id": "sports-coming-soon",
        "is_disabled": True
    }
]

# Legacy aliases for backward compatibility
WORLD_QUIZ_CARDS_DATA = GEOGRAPHY_QUIZ_CARDS_DATA

US_QUIZ_CARDS_DATA = [{
    "title": "Capital Cities",
    "emoji": "🏛️",
    "description": "Match states and capitals!",
    "button_id": "start-us-capital-quiz"
}]

# Category mapping
CATEGORY_QUIZ_CARDS_MAP = {
    'geography': GEOGRAPHY_QUIZ_CARDS_DATA,
    'math': MATH_QUIZ_CARDS_DATA,
    'history': HISTORY_QUIZ_CARDS_DATA,
    'science': SCIENCE_QUIZ_CARDS_DATA,
    'sports': SPORTS_QUIZ_CARDS_DATA
}

def get_cards_for_category(category):
    """Get quiz cards data for a specific category."""
    return CATEGORY_QUIZ_CARDS_MAP.get(category, GEOGRAPHY_QUIZ_CARDS_DATA)  # Default to geography
