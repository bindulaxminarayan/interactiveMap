"""
Mathematics-specific quiz generators.
"""

import random
import pandas as pd
from typing import List, Dict, Any
from .database_utils import quiz_db

def generate_k5_math_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Generate K-5 math questions from the normalized database.
    """
    try:
        # Query math questions from normalized database
        query = """
            SELECT q.*, c.name as category_name, s.name as subcategory_name
            FROM questions_normalized q
            JOIN categories c ON q.category_id = c.id
            LEFT JOIN subcategories s ON q.subcategory_id = s.id
            WHERE c.name = 'math' AND q.is_active = 1 AND c.is_active = 1
            ORDER BY RANDOM() LIMIT ?
        """
        question_rows = quiz_db.execute_query(query, (num_questions,))
        
        if question_rows:
            return _format_math_questions_normalized(question_rows)
    except Exception as e:
        print(f"Database query failed: {e}")
        # Fallback to old table approach
        pass
    
    # Fallback: Try legacy math table
    try:
        query = "SELECT * FROM math WHERE question IS NOT NULL AND question != '' ORDER BY RANDOM() LIMIT ?"
        question_rows = quiz_db.execute_query(query, (num_questions,))
        return _format_math_questions_legacy(question_rows)
    except Exception as e:
        print(f"Legacy math table query failed: {e}")
        return []

def _format_math_questions_normalized(question_rows: List[Dict]) -> List[Dict[str, Any]]:
    """Format normalized math questions with proper database IDs"""
    questions = []
    
    for question_row in question_rows:
        correct_question = question_row['question']
        correct_answer = question_row['correct_answer']
        
        # Get other options
        other_options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3']
        ]
        options = other_options + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        question_data = {
            "id": question_row.get('id'),  # Include database ID for analytics
            "question": correct_question,
            "options": options,
            "correct": correct_index,
            "type": "k5_math",
            "category": question_row.get('category_name', 'math'),
            "subcategory": question_row.get('subcategory_name', ''),
            "difficulty": question_row.get('difficulty', 'medium'),
            "points": question_row.get('points', 1),
            "fun_fact": question_row.get('fun_fact', '')
        }
        
        # Add image if exists
        image = question_row.get('image', '')
        if image and str(image).strip():
            question_data["math_image"] = f"assets/math_images/{image}"
        
        questions.append(question_data)
    
    return questions

def _format_math_questions_legacy(question_rows: List[Dict]) -> List[Dict[str, Any]]:
    """Format legacy math questions"""
    questions = []
    
    for question_row in question_rows:
        question_text = question_row['question']
        correct_answer = question_row.get('correctanswer') or question_row.get('correct_answer')
        topic = question_row.get('topic', '')
        
        # Get other options
        other_options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3']
        ]
        
        # Create options list and handle duplicates
        options = other_options + [correct_answer]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_options = []
        for option in options:
            if option not in seen:
                unique_options.append(option)
                seen.add(option)
        
        # If we have duplicates, the correct answer was already in the options
        if len(unique_options) < len(options):
            options = unique_options
        else:
            # Need to shuffle and remove one option to keep it to 4 choices
            random.shuffle(options)
            options = options[:4]
        
        # Make sure correct answer is still in the options
        if correct_answer not in options:
            # Replace a random option with the correct answer
            random_index = random.randint(0, len(options) - 1)
            options[random_index] = correct_answer
        
        # Shuffle the final options
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        question_data = {
            "id": question_row.get('id'),  # Include ID if available
            "question": question_text,
            "options": options,
            "correct": correct_index,
            "type": "k5_math",
            "topic": topic
        }
        
        # Add image path if image exists
        image = question_row.get('image', '')
        if image and str(image).strip():
            question_data["math_image"] = f"assets/math_images/{image}"
        
        questions.append(question_data)
    
    return questions

def generate_k5_math_questions(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Generate K-5 math questions - now uses database by default.
    """
    return generate_k5_math_questions_db(df, num_questions)

# Mathematics quiz type registry
MATH_QUIZ_GENERATORS = {
    'k5_math': generate_k5_math_questions
}

def get_math_quiz_questions(quiz_type: str, df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Get math questions for a specific quiz type.
    
    Args:
        quiz_type: Type of math quiz ('k5_math', etc.)
        df: DataFrame containing math question data
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    if quiz_type not in MATH_QUIZ_GENERATORS:
        raise ValueError(f"Unknown math quiz type: {quiz_type}. Available types: {list(MATH_QUIZ_GENERATORS.keys())}")
    
    generator_func = MATH_QUIZ_GENERATORS[quiz_type]
    return generator_func(df, num_questions)

MATH_QUIZ_TYPE_LABEL = {
    "k5_math": "K-5 Math"
}
