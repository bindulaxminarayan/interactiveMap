"""
Quiz generators for different types of country trivia questions.
"""
import logging
import random
from typing import List, Dict, Any
import pandas as pd
from .database_utils import quiz_db


def _format_questions_normalized(question_rows: List[Dict], category: str, subcategory: str) -> List[Dict[str, Any]]:
    """Helper function to format normalized question data consistently"""
    questions = []
    
    for question_row in question_rows:
        correct_question = question_row['question']
        correct_answer = question_row['correct_answer']
        
        # Include fun_fact if it exists in the data
        fun_fact = question_row.get('fun_fact', '')
        
        # Include image if it exists in the data
        image = question_row.get('image', '')
        
        # Get category and subcategory info from the joined data
        category_name = question_row.get('category_name', category)
        subcategory_name = question_row.get('subcategory_name', '')
        
        other_options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3']
        ]   
        options = other_options + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        question = {
            "id": question_row.get('id'),  # Include database ID for analytics
            "question": correct_question,
            "options": options,
            "correct": correct_index,
            "type": f"{category_name}_quiz",
            "fun_fact": fun_fact,
            "category": category_name,
            "subcategory": subcategory_name,
            "difficulty": question_row.get('difficulty', 'medium'),
            "points": question_row.get('points', 1)
        }
        
        # Add image path if image exists - determine subfolder from image filename or question content
        if category == 'geography' and subcategory == 'flag':
            question["image"] = f"assets/flags/{image}"
        elif category == 'geography' and subcategory == 'wonders':
            question["image"] = f"assets/wonders/{image}"
        questions.append(question)
    return questions

def generate_questions_by_category(df: pd.DataFrame = None, num_questions: int = 10, category: str = "geography", subcategory: str = None) -> List[Dict[str, Any]]:
    """
    Generate questions from SQLite database by category (unified approach)
    Note: df parameter is kept for backward compatibility but ignored when using database
    """
    logging.debug("In generate questions: %s,%s",category,subcategory)
    try:
        # Query with both category and subcategory
        query = """
                SELECT q.*, c.name as category_name, s.name as subcategory_name
                FROM questions_normalized q
                JOIN categories c ON q.category_id = c.id
                JOIN subcategories s ON q.subcategory_id = s.id
                WHERE c.name = ? AND s.name = ? AND q.is_active = 1 AND c.is_active = 1 AND s.is_active = 1
                ORDER BY RANDOM() LIMIT ?
            """
        question_rows = quiz_db.execute_query(query, (category, subcategory, num_questions))
        logging.debug("Querying for category=%s, subcategory=%s. Found number of questions %s",category,subcategory,len(question_rows))
        return _format_questions_normalized(question_rows, category,subcategory)
    except Exception as e:
        logging.error("Generation of questions for category %s, subcategory %s failed.Exception: %s",category,subcategory,e)

# Quiz type registry for easy expansion
QUIZ_GENERATORS = {
    # Geography Question Generations
    'flag':lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'flag'),
    'continent':lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'continent'),
    'capital':lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'capital'),
    'india_capital': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'india_states'),
    'us_capital': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'us_states'),
    'wonders': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'wonders'),
    'currency': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'currency'),
    'physical':lambda df, num_questions: generate_questions_by_category(df, num_questions, 'geography', 'physical'),
    # History Categories
    'famous_people': lambda df, num_questions: generate_questions_by_category(df, num_questions,'science','biology'),
    # Science Categories
    'biology': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'science', 'biology'),
    'chemistry': lambda df, num_questions: generate_questions_by_category(df, num_questions, 'science', 'chemistry')
}

def get_quiz_questions(quiz_type: str, df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Get questions for a specific quiz type.
    
    Args:
        quiz_type: Type of quiz ('currency', 'capital','continent', 'flag', 'us_capital', 'physical', 'india_capital', 'wonders', 'k5_math')
        df: DataFrame containing data (optional for database-backed quizzes)
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    logging.debug("Getting questions for Quiztype: %s",quiz_type)
    if quiz_type not in QUIZ_GENERATORS:
        logging.error("Quiz type: %s is not in Quiz generators",quiz_type)
        raise ValueError(f"Unknown quiz type: {quiz_type}. Available types: {list(QUIZ_GENERATORS.keys())}")
    
    generator_func = QUIZ_GENERATORS[quiz_type]
    return generator_func(df, num_questions)

QUIZ_TYPE_LABEL = {
    "currency": "Currencies",
    "capital": "Capitals",
    "continent": "Continents",
    "flag": "Flags",
    "us_capital": "US State Capitals",
    "physical": "Physical Geography",
    "india_capital": "India State Capitals",
    "wonders" :  "Wonders",
    "k5_math": "K-5 Math",
    "biology": "Biology",
    "chemistry": "Chemistry",
    "famous_people": "Famous"
}
