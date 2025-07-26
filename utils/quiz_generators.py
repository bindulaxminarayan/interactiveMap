"""
Quiz generators for different types of country trivia questions.
"""

import random
import pandas as pd
from typing import List, Dict, Any
from .database_utils import quiz_db

def generate_currency_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random country-currency questions."""
    # Filter out countries with missing or invalid currency data
    valid_countries = df[(df['currency'].notna()) & (df['currency'] != '')].copy()
    
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        correct_currency = country_row['currency']
        capital = country_row['capital']
        gdp = country_row['gdp']
        continent = country_row['continent']
        
        # Generate 3 wrong currency options
        other_currencies = valid_countries[
            (valid_countries['country'] != correct_country) & 
            (valid_countries['currency'] != correct_currency)
        ]['currency'].unique()
        
        if len(other_currencies) >= 3:
            wrong_currencies = random.sample(list(other_currencies), 3)
        else:
            # If not enough unique currencies, use what we have and pad with generic ones
            wrong_currencies = list(other_currencies)
            generic_currencies = ['Dollar', 'Euro', 'Pound', 'Franc', 'Peso', 'Real', 'Rupiah', 'Yen', 'Won', 'Ruble']
            for currency in generic_currencies:
                if len(wrong_currencies) < 3 and currency != correct_currency and currency not in wrong_currencies:
                    wrong_currencies.append(currency)
                if len(wrong_currencies) >= 3:
                    break
        
        # Create options list with correct answer at random position
        options = wrong_currencies[:3] + [correct_currency]
        random.shuffle(options)
        correct_index = options.index(correct_currency)
        
        question = {
            "question": f"What is the currency of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "currency"
        }
        questions.append(question)
    
    return questions

def generate_country_capital_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random country-capital questions."""
    # Filter out countries with missing or invalid capital data
    valid_countries = df[(df['capital'].notna()) & (df['capital'] != '')].copy()
    
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        correct_capital = country_row['capital']
        # currency = country_row['currency']
        # gdp = country_row['gdp']
        # continent = country_row['continent']
        
        # Handle complex capital entries (like "La Paz (admin), Sucre (judicial)")
        display_capital = correct_capital.split('(')[0].strip() if '(' in correct_capital else correct_capital
        
        # Generate 3 wrong capital options
        other_countries = valid_countries[
            (valid_countries['country'] != correct_country) & 
            (valid_countries['capital'] != correct_capital)
        ]
        
        # Get other capitals, cleaning them of parenthetical information for display
        other_capitals = []
        for _, other_row in other_countries.iterrows():
            other_capital = other_row['capital']
            clean_capital = other_capital.split('(')[0].strip() if '(' in other_capital else other_capital
            if clean_capital != display_capital and clean_capital not in other_capitals:
                other_capitals.append(clean_capital)
        
        if len(other_capitals) >= 3:
            wrong_capitals = random.sample(other_capitals, 3)
        else:
            # If not enough unique capitals, use what we have and pad with generic ones
            wrong_capitals = other_capitals[:3]
            generic_capitals = ['London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Vienna', 'Prague', 'Warsaw', 'Budapest', 'Stockholm']
            for capital in generic_capitals:
                if len(wrong_capitals) < 3 and capital != display_capital and capital not in wrong_capitals:
                    wrong_capitals.append(capital)
                if len(wrong_capitals) >= 3:
                    break
        
        # Create options list with correct answer at random position
        options = wrong_capitals[:3] + [display_capital]
        random.shuffle(options)
        correct_index = options.index(display_capital)
        
        question = {
            "question": f"What is the capital of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "capital"
        }
        questions.append(question)
    
    return questions

def generate_continent_questions(df: pd.DataFrame, num_questions: int =10) -> List[Dict[str, Any]]:
    """Generate random country-continent questions."""
    # Filter out countries with missing or invalid continent data
    valid_countries = df[(df['continent'].notna()) & (df['continent'] != '')].copy()
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    all_possible_continents = list(df['continent'].unique())
    # Add any standard continents that might not be in your DataFrame but you want as options
    standard_continents_to_add = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Australia', 'Transcontinental(Asia and Europe)']
    for sc in standard_continents_to_add:
        if sc not in all_possible_continents:
            all_possible_continents.append(sc)
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        correct_continent = country_row['continent']
        currency = country_row['currency']
        gdp = country_row['gdp']
        capital = country_row['capital']
        
        # Collect all potential wrong continents
        # Start with continents from other countries in the DataFrame
        potential_wrong_options = set(valid_countries[
            (valid_countries['country'] != correct_country) & 
            (valid_countries['continent'] != correct_continent)
        ]['continent'].unique())
        
        # Add from the comprehensive list of all possible continents, ensuring uniqueness
        # and excluding the correct continent
        for continent in all_possible_continents:
            if continent != correct_continent:
                potential_wrong_options.add(continent)
        
        # Convert to a list to sample from
        potential_wrong_options_list = list(potential_wrong_options)

        # Ensure we have enough options to sample 3
        if len(potential_wrong_options_list) >= 3:
            wrong_continents = random.sample(potential_wrong_options_list, 3)
        else:
            # If not enough, use all available unique wrong options
            wrong_continents = potential_wrong_options_list 
            # You might want to handle this edge case if you absolutely need 3 wrong options,
            # perhaps by allowing fewer options for such questions, or returning fewer questions overall.
            # For now, it will use whatever unique wrong options are available.
            print(f"Warning: Not enough unique wrong continents for {correct_country}. Found {len(wrong_continents)} unique wrong options.")


        # Create options list with correct answer at random position
        options = wrong_continents + [correct_continent]
        random.shuffle(options)
        correct_index = options.index(correct_continent)
        
        question = {
            "question": f"What is the continent of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "continent"
        }
        questions.append(question)
    
    return questions

def generate_flag_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate flag questions - show flag image and ask for country name."""
    # Filter out countries with missing or invalid flag data
    valid_countries = df[(df['flag'].notna()) & (df['flag'] != '')].copy()
    
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        flag_filename = country_row['flag']
        capital = country_row['capital']
        currency = country_row['currency']
        gdp = country_row['gdp']
        continent = country_row['continent']
        
        # Generate 3 wrong country options
        other_countries = valid_countries[
            valid_countries['country'] != correct_country
        ]['country'].unique()
        
        if len(other_countries) >= 3:
            wrong_countries = random.sample(list(other_countries), 3)
        else:
            # If not enough unique countries with flags, use what we have and pad with generic ones
            wrong_countries = list(other_countries)
            # Add some common country names as fallbacks
            generic_countries = ['United States', 'Canada', 'Brazil', 'Germany', 'France', 'Japan', 'China', 'India', 'Russia', 'South Africa']
            for country in generic_countries:
                if len(wrong_countries) < 3 and country != correct_country and country not in wrong_countries:
                    wrong_countries.append(country)
                if len(wrong_countries) >= 3:
                    break
        
        # Create options list with correct answer at random position
        options = wrong_countries[:3] + [correct_country]
        random.shuffle(options)
        correct_index = options.index(correct_country)
        
        question = {
            "question": f"Which country does this flag belong to?",
            "flag_image": f"assets/flags/{flag_filename}",
            "options": options,
            "correct": correct_index,
            "type": "flag"
        }
        questions.append(question)
    
    return questions

def generate_capital_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random US state-capital questions."""
    # Filter out states with missing or invalid capital data
    valid_states = df[(df['capital'].notna()) & (df['capital'] != '')].copy()
    
    if len(valid_states) < num_questions:
        num_questions = len(valid_states)
    
    # Select random states for questions
    selected_states = valid_states.sample(n=num_questions)
    questions = []
    
    for _, state_row in selected_states.iterrows():
        correct_state = state_row['state']
        correct_capital = state_row['capital']
        
        # Generate 3 wrong capital options from other states
        other_states = valid_states[
            (valid_states['state'] != correct_state) & 
            (valid_states['capital'] != correct_capital)
        ]
        
        other_capitals = other_states['capital'].unique()
        
        if len(other_capitals) >= 3:
            wrong_capitals = random.sample(list(other_capitals), 3)
        else:
            # If not enough unique capitals, use what we have and pad with generic ones
            wrong_capitals = list(other_capitals)
            generic_capitals = ['Chicago', 'New York City', 'Los Angeles', 'Miami', 'Seattle', 'Portland', 'Las Vegas', 'San Antonio', 'Philadelphia', 'Detroit']
            for capital in generic_capitals:
                if len(wrong_capitals) < 3 and capital != correct_capital and capital not in wrong_capitals:
                    wrong_capitals.append(capital)
                if len(wrong_capitals) >= 3:
                    break
        
        # Create options list with correct answer at random position
        options = wrong_capitals[:3] + [correct_capital]
        random.shuffle(options)
        correct_index = options.index(correct_capital)
        
        question = {
            "question": f"What is the capital of {correct_state}?",
            "options": options,
            "correct": correct_index,
            "type": "us_capital"
        }
        questions.append(question)
    
    return questions

def _format_questions(question_rows: List[Dict], category: str) -> List[Dict[str, Any]]:
    """Helper function to format question data consistently"""
    questions = []
    
    for question_row in question_rows:
        correct_question = question_row['question']
        
        # Handle different column names for correct answer
        correct_answer = question_row.get('correct_answer') or question_row.get('correctanswer')
        
        # Include fun_fact if it exists in the data
        fun_fact = question_row.get('fun_fact', '')
        
        # Include image if it exists in the data
        image = question_row.get('image', '')
        
        other_options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3']
        ]   
        options = other_options + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        question = {
            "question": correct_question,
            "options": options,
            "correct": correct_index,
            "type": f"{category}_quiz",
            "fun_fact": fun_fact
        }
        
        # Add image path if image exists
        if image and str(image).strip():
            if category == 'wonders':
                question["wonder_image"] = f"assets/wonders/{image}"
            elif category == 'math':
                question["math_image"] = f"assets/math_images/{image}"
            else:
                question["image"] = f"assets/images/{image}"
        
        questions.append(question)
    
    return questions

def _format_questions_normalized(question_rows: List[Dict], category: str) -> List[Dict[str, Any]]:
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
        if image and str(image).strip():
            image_filename = str(image).lower()
            question_text = question_row.get('question', '').lower()
            
            # Determine the correct asset subfolder based on content
            if 'flag' in question_text or 'country' in question_text:
                question["flag_image"] = f"assets/flags/{image}"
            elif any(keyword in question_text for keyword in ['monument', 'wonder', 'landmark', 'temple', 'palace', 'tower']):
                question["wonder_image"] = f"assets/wonders/{image}"
            elif 'math' in question_text or category_name == 'math':
                question["math_image"] = f"assets/math_images/{image}"
            else:
                # Default to wonders for now since that's what most images seem to be
                question["wonder_image"] = f"assets/wonders/{image}"
        
        questions.append(question)
    
    return questions

def generate_questions_by_category(df: pd.DataFrame = None, num_questions: int = 10, category: str = "geography", subcategory: str = None) -> List[Dict[str, Any]]:
    """
    Generate questions from SQLite database by category (unified approach)
    Note: df parameter is kept for backward compatibility but ignored when using database
    """
    
    # Map specific quiz types to normalized category/subcategory structure
    quiz_type_mapping = {
        'world_physical_geography': ('geography', 'physical'),
        'wonders': ('geography', 'modern'),
        'us_capital': ('geography', 'us_states'),
        'india_capital': ('geography', 'india_states'),
        'math': ('math', None),
        'history': ('history', None),
        'science': ('science', None),
        'sports': ('sports', None)
    }
    
    # If category matches a specific quiz type, map it to normalized structure
    if category in quiz_type_mapping:
        actual_category, actual_subcategory = quiz_type_mapping[category]
    else:
        # For other cases, use as-is
        actual_category = category
        actual_subcategory = subcategory
    
    # First try the new normalized approach
    try:
        if actual_subcategory:
            # Query with both category and subcategory
            query = """
                SELECT q.*, c.name as category_name, s.name as subcategory_name
                FROM questions_normalized q
                JOIN categories c ON q.category_id = c.id
                LEFT JOIN subcategories s ON q.subcategory_id = s.id
                WHERE c.name = ? AND s.name = ? AND q.is_active = 1 AND c.is_active = 1
                ORDER BY RANDOM() LIMIT ?
            """
            question_rows = quiz_db.execute_query(query, (actual_category, actual_subcategory, num_questions))
            print(f"Querying for category='{actual_category}', subcategory='{actual_subcategory}' - found {len(question_rows) if question_rows else 0} questions")
        else:
            # Query by category only
            query = """
                SELECT q.*, c.name as category_name, s.name as subcategory_name
                FROM questions_normalized q
                JOIN categories c ON q.category_id = c.id
                LEFT JOIN subcategories s ON q.subcategory_id = s.id
                WHERE c.name = ? AND q.is_active = 1 AND c.is_active = 1
                ORDER BY RANDOM() LIMIT ?
            """
            question_rows = quiz_db.execute_query(query, (actual_category, num_questions))
            print(f"Querying for category='{actual_category}' - found {len(question_rows) if question_rows else 0} questions")
        
        if question_rows:
            return _format_questions_normalized(question_rows, actual_category)
    except Exception as e:
        print(f"Normalized query failed: {e}")
        # Fallback to old approach
        pass
    
    # Fallback: Try simple questions table approach
    try:
        query = "SELECT * FROM questions WHERE category = ? AND question IS NOT NULL AND question != '' ORDER BY RANDOM() LIMIT ?"
        question_rows = quiz_db.execute_query(query, (category, num_questions))
        
        if question_rows:
            return _format_questions(question_rows, category)
    except Exception:
        # Fallback to old table structure for backward compatibility
        pass
    
    # Fallback to legacy table names - include specific quiz type mappings
    legacy_table_mapping = {
        'geography': 'world_physical_geography',
        'wonders': 'wonders',
        'math': 'math',
        'india_capital': 'india_states',  # Map india_capital back to india_states table
        'us_capital': 'us_states',       # Map us_capital back to us_states table
        'world_physical_geography': 'world_physical_geography'
    }
    
    table_name = legacy_table_mapping.get(category, category)
    
    try:
        query = f"SELECT * FROM {table_name} WHERE question IS NOT NULL AND question != '' ORDER BY RANDOM() LIMIT ?"
        question_rows = quiz_db.execute_query(query, (num_questions,))
        return _format_questions(question_rows, category)
    except Exception as e:
        print(f"Error querying {table_name}: {e}")
        return []

# Keep the old function for backward compatibility
def generate_random_questions(df: pd.DataFrame = None, num_questions: int = 10, table_name: str = "world_physical_geography") -> List[Dict[str, Any]]:
    """
    Legacy function - use generate_questions_by_category instead
    """
    # Map old table names to categories with proper subcategories
    table_to_category_subcategory = {
        'world_physical_geography': ('geography', 'physical'),
        'wonders': ('geography', 'modern'),
        'math': ('math', None)
    }
    
    if table_name in table_to_category_subcategory:
        category, subcategory = table_to_category_subcategory[table_name]
        return generate_questions_by_category(df, num_questions, category, subcategory)
    else:
        # Fallback for unknown table names
        return generate_questions_by_category(df, num_questions, table_name)

def generate_currency_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random country-currency questions from database."""
    # Query random countries from database
    query = "SELECT * FROM countries WHERE currency IS NOT NULL AND currency != '' ORDER BY RANDOM() LIMIT ?"
    country_rows = quiz_db.execute_query(query, (num_questions * 2,))  # Get more than needed for options
    
    if len(country_rows) < num_questions:
        num_questions = len(country_rows)
    
    questions = []
    used_countries = set()
    
    for country_row in country_rows[:num_questions]:
        correct_country = country_row['country']
        correct_currency = country_row['currency']
        
        # Get wrong currency options from other countries
        wrong_currencies = []
        for other_row in country_rows:
            if (other_row['country'] != correct_country and 
                other_row['currency'] != correct_currency and 
                other_row['currency'] not in wrong_currencies):
                wrong_currencies.append(other_row['currency'])
                if len(wrong_currencies) >= 3:
                    break
        
        # If not enough wrong currencies, add generic ones
        if len(wrong_currencies) < 3:
            generic_currencies = ['Dollar', 'Euro', 'Pound', 'Franc', 'Peso', 'Real', 'Rupiah', 'Yen', 'Won', 'Ruble']
            for currency in generic_currencies:
                if (len(wrong_currencies) < 3 and 
                    currency != correct_currency and 
                    currency not in wrong_currencies):
                    wrong_currencies.append(currency)
        
        # Create options list with correct answer at random position
        options = wrong_currencies[:3] + [correct_currency]
        random.shuffle(options)
        correct_index = options.index(correct_currency)
        
        question = {
            "question": f"What is the currency of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "currency"
        }
        questions.append(question)
    
    return questions

def generate_country_capital_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random country-capital questions from database."""
    # Query random countries from database
    query = "SELECT * FROM countries WHERE capital IS NOT NULL AND capital != '' ORDER BY RANDOM() LIMIT ?"
    country_rows = quiz_db.execute_query(query, (num_questions * 2,))
    
    if len(country_rows) < num_questions:
        num_questions = len(country_rows)
    
    questions = []
    
    for country_row in country_rows[:num_questions]:
        correct_country = country_row['country']
        correct_capital = country_row['capital']
        
        # Handle complex capital entries
        display_capital = correct_capital.split('(')[0].strip() if '(' in correct_capital else correct_capital
        
        # Get wrong capital options
        wrong_capitals = []
        for other_row in country_rows:
            if other_row['country'] != correct_country:
                other_capital = other_row['capital']
                clean_capital = other_capital.split('(')[0].strip() if '(' in other_capital else other_capital
                if clean_capital != display_capital and clean_capital not in wrong_capitals:
                    wrong_capitals.append(clean_capital)
                    if len(wrong_capitals) >= 3:
                        break
        
        # Add generic capitals if needed
        if len(wrong_capitals) < 3:
            generic_capitals = ['London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Vienna', 'Prague', 'Warsaw', 'Budapest', 'Stockholm']
            for capital in generic_capitals:
                if (len(wrong_capitals) < 3 and 
                    capital != display_capital and 
                    capital not in wrong_capitals):
                    wrong_capitals.append(capital)
        
        # Create options list
        options = wrong_capitals[:3] + [display_capital]
        random.shuffle(options)
        correct_index = options.index(display_capital)
        
        question = {
            "question": f"What is the capital of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "capital"
        }
        questions.append(question)
    
    return questions

def generate_continent_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate random country-continent questions from database."""
    # Query random countries from database
    query = "SELECT * FROM countries WHERE continent IS NOT NULL AND continent != '' ORDER BY RANDOM() LIMIT ?"
    country_rows = quiz_db.execute_query(query, (num_questions,))
    
    questions = []
    all_continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Australia', 'Transcontinental(Asia and Europe)']
    
    for country_row in country_rows:
        correct_country = country_row['country']
        correct_continent = country_row['continent']
        
        # Get wrong continent options
        wrong_continents = [cont for cont in all_continents if cont != correct_continent]
        if len(wrong_continents) >= 3:
            wrong_continents = random.sample(wrong_continents, 3)
        
        # Create options list
        options = wrong_continents[:3] + [correct_continent]
        random.shuffle(options)
        correct_index = options.index(correct_continent)
        
        question = {
            "question": f"What is the continent of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "type": "continent"
        }
        questions.append(question)
    
    return questions

def generate_flag_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate flag questions from database."""
    # Query random countries with flags from database
    query = "SELECT * FROM countries WHERE flag IS NOT NULL AND flag != '' ORDER BY RANDOM() LIMIT ?"
    country_rows = quiz_db.execute_query(query, (num_questions * 2,))
    
    if len(country_rows) < num_questions:
        num_questions = len(country_rows)
    
    questions = []
    
    for country_row in country_rows[:num_questions]:
        correct_country = country_row['country']
        flag_filename = country_row['flag']
        
        # Get wrong country options
        wrong_countries = []
        for other_row in country_rows:
            if (other_row['country'] != correct_country and 
                other_row['country'] not in wrong_countries):
                wrong_countries.append(other_row['country'])
                if len(wrong_countries) >= 3:
                    break
        
        # Add generic countries if needed
        if len(wrong_countries) < 3:
            generic_countries = ['United States', 'Canada', 'Brazil', 'Germany', 'France', 'Japan', 'China', 'India', 'Russia', 'South Africa']
            for country in generic_countries:
                if (len(wrong_countries) < 3 and 
                    country != correct_country and 
                    country not in wrong_countries):
                    wrong_countries.append(country)
        
        # Create options list
        options = wrong_countries[:3] + [correct_country]
        random.shuffle(options)
        correct_index = options.index(correct_country)
        
        question = {
            "question": f"Which country does this flag belong to?",
            "flag_image": f"assets/flags/{flag_filename}",
            "options": options,
            "correct": correct_index,
            "type": "flag"
        }
        questions.append(question)
    
    return questions

def generate_us_capital_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate US state capital questions from database."""
    # Query random US states from database
    query = "SELECT * FROM us_states ORDER BY RANDOM() LIMIT ?"
    state_rows = quiz_db.execute_query(query, (num_questions * 2,))
    
    if len(state_rows) < num_questions:
        num_questions = len(state_rows)
    
    questions = []
    
    for state_row in state_rows[:num_questions]:
        correct_state = state_row['state']
        correct_capital = state_row['capital']
        
        # Get wrong capital options
        wrong_capitals = []
        for other_row in state_rows:
            if (other_row['state'] != correct_state and 
                other_row['capital'] != correct_capital and 
                other_row['capital'] not in wrong_capitals):
                wrong_capitals.append(other_row['capital'])
                if len(wrong_capitals) >= 3:
                    break
        
        # Add generic capitals if needed
        if len(wrong_capitals) < 3:
            generic_capitals = ['Chicago', 'New York City', 'Los Angeles', 'Miami', 'Seattle', 'Portland', 'Las Vegas', 'San Antonio', 'Philadelphia', 'Detroit']
            for capital in generic_capitals:
                if (len(wrong_capitals) < 3 and 
                    capital != correct_capital and 
                    capital not in wrong_capitals):
                    wrong_capitals.append(capital)
        
        # Create options list
        options = wrong_capitals[:3] + [correct_capital]
        random.shuffle(options)
        correct_index = options.index(correct_capital)
        
        question = {
            "question": f"What is the capital of {correct_state}?",
            "options": options,
            "correct": correct_index,
            "type": "us_capital"
        }
        questions.append(question)
    
    return questions

def generate_india_capital_questions_db(df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """Generate India state capital questions from normalized database."""
    # Use the normalized database approach for India states
    return generate_questions_by_category(df, num_questions, 'india_capital')

def generate_math_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Generate K-5 math questions from the math.csv dataset.
    """
    # Filter out questions with missing or invalid data
    valid_questions = df[(df['question'].notna()) & (df['question'] != '')].copy()
    
    if len(valid_questions) < num_questions:
        num_questions = len(valid_questions)
    
    # Select random questions
    selected_questions = valid_questions.sample(n=num_questions)
    questions = []
    
    for _, question_row in selected_questions.iterrows():
        question_text = question_row['question']
        correct_answer = question_row['correctanswer']
        topic = question_row.get('topic', '')
        
        # Include image if it exists in the data (handle NaN values)
        image = question_row.get('image', '')
        
        # Get the three options plus correct answer
        other_options = [
            question_row['option1'],
            question_row['option2'],
            question_row['option3']
        ]
        
        # Create options list and find correct index
        # The correct answer might be one of the three options or a separate value
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
            "question": question_text,
            "options": options,
            "correct": correct_index,
            "type": "k5_math",
            "topic": topic
        }
        
        # Add image path if image exists (handle both string and NaN values)
        if pd.notna(image) and str(image).strip():
            question_data["math_image"] = f"assets/math_images/{image}"
        
        questions.append(question_data)
    
    return questions

# Quiz type registry for easy expansion
QUIZ_GENERATORS = {
    'currency': generate_currency_questions_db,
    'capital': generate_country_capital_questions_db,
    'continent': generate_continent_questions_db,
    'flag': generate_flag_questions_db,
    'us_capital': generate_questions_by_category,
    'world_physical_geography': generate_random_questions,
    'india_capital': generate_india_capital_questions_db,
    'wonders': generate_questions_by_category,
    'k5_math': generate_math_questions
}

def get_quiz_questions(quiz_type: str, df: pd.DataFrame = None, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Get questions for a specific quiz type.
    
    Args:
        quiz_type: Type of quiz ('currency', 'capital','continent', 'flag', 'us_capital', 'world_physical_geography', 'india_capital', 'wonders', 'k5_math')
        df: DataFrame containing data (optional for database-backed quizzes)
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    if quiz_type not in QUIZ_GENERATORS:
        raise ValueError(f"Unknown quiz type: {quiz_type}. Available types: {list(QUIZ_GENERATORS.keys())}")
    
    generator_func = QUIZ_GENERATORS[quiz_type]
    
    # Database-backed quiz types that don't need a DataFrame
    database_backed_types = [
        'world_physical_geography', 
        'wonders', 
        'currency', 
        'capital', 
        'continent', 
        'flag', 
        'us_capital', 
        'india_capital'
    ]
    
    if quiz_type in database_backed_types:
        # For quiz types that use generate_random_questions, pass the correct table name
        if quiz_type in ['world_physical_geography', 'wonders']:
            return generator_func(df, num_questions, quiz_type)
        else:
            return generator_func(df, num_questions)
    else:
        # For other quiz types like k5_math, df is required
        if df is None:
            raise ValueError(f"DataFrame is required for quiz type: {quiz_type}")
        return generator_func(df, num_questions)

QUIZ_TYPE_LABEL = {
    "currency": "Currencies",
    "capital": "Capitals",
    "continent": "Continents",
    "flag": "Flags",
    "us_capital": "US State Capitals",
    "world_physical_geography": "Physical Geography",
    "india_capital": "India State Capitals",
    "wonders" :  "Wonders",
    "k5_math": "K-5 Math"
}
