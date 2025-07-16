"""
Quiz generators for different types of country trivia questions.
"""

import random
import pandas as pd
from typing import List, Dict, Any

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
            "explanation": f"The currency of {correct_country} is {correct_currency}.",
            "moreinfo": f"Capital:{capital}, GDP:{gdp}, Continent:{continent}",
            "type": "currency"
        }
        questions.append(question)
    
    return questions

def generate_capital_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
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
        currency = country_row['currency']
        gdp = country_row['gdp']
        continent = country_row['continent']
        
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
            "explanation": f"The capital of {correct_country} is {display_capital}.",
            "moreinfo":f"Currency:{currency}, GDP:{gdp}, Continent: {continent}",
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
            "explanation": f"The continent of {correct_country} is {correct_continent}.",
            "moreinfo": f"Currency: {currency}, GDP: {gdp}, Capital:{capital}",
            "type": "continent"
        }
        questions.append(question)
    
    return questions

def generate_country_questions(df: pd.DataFrame, num_questions: int =10) -> List[Dict[str, Any]]:
    """Generate random country-continent questions."""
    total_categories = 3
    base = num_questions // total_categories
    remainder = num_questions % total_categories
    counts = [base] * total_categories
    # Randomly assign the remainder
    if remainder > 0:
        for i in random.sample(range(total_categories), remainder):
            counts[i] += 1
    q_funcs = [generate_continent_questions, generate_capital_questions, generate_currency_questions]
    questions = []
    for func, count in zip(q_funcs, counts):
        if count > 0:
            questions.extend(func(df, count))
    random.shuffle(questions)
    
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
            "flag_image": f"assets/{flag_filename}",
            "options": options,
            "correct": correct_index,
            "explanation": f"This is the flag of {correct_country}.",
            "moreinfo": f"Capital: {capital}, Currency: {currency}, GDP: {gdp}, Continent: {continent}",
            "type": "flag"
        }
        questions.append(question)
    
    return questions

def generate_us_capital_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
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
            "explanation": f"The capital of {correct_state} is {correct_capital}.",
            "moreinfo": f"State: {correct_state}",
            "type": "us_capital"
        }
        questions.append(question)
    
    return questions

def generate_world_physical_geography_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Generate physical geography questions from data set
    """
      # Filter out states with missing or invalid capital data
    valid_questions = df[(df['question'].notna()) & (df['question'] != '')].copy()
    
    if len(valid_questions) < num_questions:
        num_questions = len(valid_questions)
    
    # Select random states for questions
    selected_questions = valid_questions.sample(n=num_questions)
    questions = []
    for _, question_row in selected_questions.iterrows():
            correct_question = question_row['question']
            correct_answer = question_row['correct_answer']
        
            other_options=[
            question_row['option1'],
            question_row['option2'],
            question_row['option3']]   
            options = other_options + [correct_answer]
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            question = {
            "question": correct_question,
            "options": options,
            "correct": correct_index,
            "explanation": f"No explanation",
            "moreinfo": f"No extra information available",
            "type": "world_physical-geography-quiz"
        }
            questions.append(question)
    
    
    return questions

# Quiz type registry for easy expansion
QUIZ_GENERATORS = {
    'currency': generate_currency_questions,
    'capital': generate_capital_questions,
    'continent': generate_continent_questions,
    'country': generate_country_questions,
    'flag': generate_flag_questions,
    'us_capital': generate_us_capital_questions,
    'world_physical_geography': generate_world_physical_geography_questions
}

def get_quiz_questions(quiz_type: str, df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Get questions for a specific quiz type.
    
    Args:
        quiz_type: Type of quiz ('currency', 'capital','continent', 'location', 'us_capital')
        df: DataFrame containing country data or US states data
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    if quiz_type not in QUIZ_GENERATORS:
        raise ValueError(f"Unknown quiz type: {quiz_type}. Available types: {list(QUIZ_GENERATORS.keys())}")
    
    generator_func = QUIZ_GENERATORS[quiz_type]
    return generator_func(df, num_questions)

QUIZ_TYPE_LABEL = {
    "currency": "Currencies",
    "capital": "Capitals",
    "continent": "Continents",
    "country": "Countries",
    "flag": "Flags",
    "us_capital": "US State Capitals",
    "world_physical_geography": "World Physical Geography"
}
