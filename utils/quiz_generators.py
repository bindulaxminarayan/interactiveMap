"""
Quiz generators for different types of country trivia questions.
"""
import logging
import random
from typing import List, Dict, Any, Optional
from .database_utils import quiz_db


# Quiz type configuration - single source of truth
QUIZ_CONFIG = {
    # Geography quizzes
    'flag': {'category': 'geography', 'subcategory': 'flag', 'image_folder': 'flags'},
    'continent': {'category': 'geography', 'subcategory': 'continent'},
    'capital': {'category': 'geography', 'subcategory': 'capital'},
    'india_capital': {'category': 'geography', 'subcategory': 'india_states'},
    'us_capital': {'category': 'geography', 'subcategory': 'us_states'},
    'wonders': {'category': 'geography', 'subcategory': 'wonders', 'image_folder': 'wonders'},
    'currency': {'category': 'geography', 'subcategory': 'currency'},
    'physical': {'category': 'geography', 'subcategory': 'physical'},
    
    # Science quizzes
    'biology': {'category': 'science', 'subcategory': 'biology'},
    'chemistry': {'category': 'science', 'subcategory': 'chemistry'},
    'physics': {'category': 'science', 'subcategory': 'physics'},
    'astronomy': {'category': 'science', 'subcategory': 'astronomy'},
    'earth_science': {'category': 'science', 'subcategory': 'earth_science'},
    'technology': {'category': 'science', 'subcategory': 'technology'},
    
    # History quizzes
    'famous_people': {'category': 'history', 'subcategory': 'famous_people', 'image_folder': 'famous'},
    'world_history':{'category': 'history', 'subcategory': 'world_history'}
}

# Display labels for quiz types
QUIZ_TYPE_LABEL = {
    "currency": "Currencies",
    "capital": "Capitals",
    "continent": "Continents",
    "flag": "Flags",
    "us_capital": "US State Capitals",
    "physical": "Physical Geography",
    "india_capital": "India State Capitals",
    "wonders": "Wonders",
    "biology": "Biology",
    "chemistry": "Chemistry",
    "physics": "Physics",
    "astronomy": "Astronomy",
    "earth_science": "Earth Science",
    "technology": "Technology",
    "famous_people": "Famous People",
    "world_history": "World History"
}


def _build_image_path(image: str, image_folder: Optional[str]) -> str:
    """Build image path based on folder configuration."""
    if not image or not image_folder:
        return ""
    return f"assets/{image_folder}/{image}"


def _format_questions_normalized(question_rows: List[Dict], quiz_config: Dict) -> List[Dict[str, Any]]:
    """Helper function to format normalized question data consistently."""
    questions = []
    
    for question_row in question_rows:
        # Build options list and shuffle
        options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3'],
            question_row['correct_answer']
        ]
        random.shuffle(options)
        correct_index = options.index(question_row['correct_answer'])
        
        # Build question object
        question = {
            "id": question_row.get('id'),
            "question": question_row['question'],
            "options": options,
            "correct": correct_index,
            "type": f"{quiz_config['category']}_quiz",
            "fun_fact": question_row.get('fun_fact', ''),
            "category": question_row.get('category_name', quiz_config['category']),
            "subcategory": question_row.get('subcategory_name', quiz_config['subcategory']),
            "difficulty": question_row.get('difficulty', 'medium'),
            "points": question_row.get('points', 1)
        }
        
        # Add image path if configured
        if quiz_config.get('image_folder') and question_row.get('image'):
            question["image"] = _build_image_path(
                question_row['image'], 
                quiz_config['image_folder']
            )
        
        questions.append(question)
    
    return questions


def _fetch_questions_from_db(category: str, subcategory: str, num_questions: int, exclude_ids: List[int] = None) -> List[Dict]:
    """Fetch questions from database by category and subcategory, excluding specified IDs and prioritizing least asked questions."""
    # Build the base query with LEFT JOIN to question stats to get usage counts
    query = """
        SELECT q.*, c.name as category_name, s.name as subcategory_name,
               COALESCE(SUM(dqs.times_asked), 0) as total_times_asked
        FROM questions_normalized q
        JOIN categories c ON q.category_id = c.id
        JOIN subcategories s ON q.subcategory_id = s.id
        LEFT JOIN daily_question_stats dqs ON q.id = dqs.question_id
        WHERE c.name = ? AND s.name = ? AND q.is_active = 1 AND c.is_active = 1 AND s.is_active = 1
    """
    
    params = [category, subcategory]
    
    # Add exclusion clause if we have IDs to exclude
    if exclude_ids and len(exclude_ids) > 0:
        placeholders = ','.join(['?' for _ in exclude_ids])
        query += f" AND q.id NOT IN ({placeholders})"
        params.extend(exclude_ids)
    
    # Group by question and order by least asked first, then randomize within same usage count
    query += """ 
        GROUP BY q.id, q.question, q.correct_answer, q.option1, q.option2, q.option3, 
                 q.fun_fact, q.category_id, q.subcategory_id, q.difficulty, q.points, 
                 q.image, q.is_active, c.name, s.name
        ORDER BY total_times_asked ASC, RANDOM() 
        LIMIT ?
    """
    params.append(num_questions)
    
    try:
        question_rows = quiz_db.execute_query(query, tuple(params))
        logging.debug(
            "Querying for category=%s, subcategory=%s. Found %d questions (excluding %d previously asked), prioritizing least asked",
            category, subcategory, len(question_rows), len(exclude_ids) if exclude_ids else 0
        )
        
        # Log usage statistics for debugging
        if question_rows:
            usage_counts = [row.get('total_times_asked', 0) for row in question_rows]
            logging.debug("Question usage counts: min=%d, max=%d, avg=%.1f", 
                         min(usage_counts), max(usage_counts), sum(usage_counts)/len(usage_counts))
        
        return question_rows
    except Exception as e:
        logging.error(
            "Failed to fetch questions for category=%s, subcategory=%s: %s",
            category, subcategory, e
        )
        return []


def generate_questions_by_category(
    category: str, 
    subcategory: str, 
    num_questions: int = 10
) -> List[Dict[str, Any]]:
    """
    Generate questions from SQLite database by category.
    
    Args:
        category: Category name
        subcategory: Subcategory name
        num_questions: Number of questions to generate
    
    Returns:
        List of formatted question dictionaries
    """
    logging.debug("Generating questions for category=%s, subcategory=%s", category, subcategory)
    
    # Fetch from database
    question_rows = _fetch_questions_from_db(category, subcategory, num_questions)
    
    # Create config for formatting
    quiz_config = {'category': category, 'subcategory': subcategory}
    
    return _format_questions_normalized(question_rows, quiz_config)


def get_quiz_questions(quiz_type: str, num_questions: int = 10, exclude_ids: List[int] = None) -> List[Dict[str, Any]]:
    """
    Get questions for a specific quiz type.
    
    Args:
        quiz_type: Type of quiz (e.g., 'currency', 'capital', 'flag', etc.)
        num_questions: Number of questions to generate
        exclude_ids: List of question IDs to exclude (previously asked questions)
    
    Returns:
        List of question dictionaries
    
    Raises:
        ValueError: If quiz_type is not supported
    """
    logging.debug("Getting questions for quiz type: %s (excluding %d questions)", 
                  quiz_type, len(exclude_ids) if exclude_ids else 0)
    
    if quiz_type not in QUIZ_CONFIG:
        available_types = list(QUIZ_CONFIG.keys())
        logging.error("Unknown quiz type: %s. Available: %s", quiz_type, available_types)
        raise ValueError(f"Unknown quiz type: {quiz_type}. Available types: {available_types}")
    
    # Get configuration for this quiz type
    config = QUIZ_CONFIG[quiz_type]
    category = config['category']
    subcategory = config['subcategory']
    
    # Fetch questions from database, excluding specified IDs
    question_rows = _fetch_questions_from_db(category, subcategory, num_questions, exclude_ids)
    logging.info("Fetched questions from db: %s",len(question_rows))
    
    # Format and return questions
    return _format_questions_normalized(question_rows, config)


def get_available_quiz_types() -> List[str]:
    """Get list of all available quiz types."""
    return list(QUIZ_CONFIG.keys())


def get_quiz_types_by_category(category: str) -> List[str]:
    """Get quiz types for a specific category."""
    return [
        quiz_type for quiz_type, config in QUIZ_CONFIG.items()
        if config['category'] == category
    ]


def get_quiz_display_name(quiz_type: str) -> str:
    """Get the display name for a quiz type."""
    return QUIZ_TYPE_LABEL.get(quiz_type, quiz_type.replace('_', ' ').title())
