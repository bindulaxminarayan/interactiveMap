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
            "type": "capital"
        }
        questions.append(question)
    
    return questions

def generate_continent_questions(df: pd.DataFrame, num_questions: int =10) -> List[Dict[str, Any]]:
    """Generate random country-continent questions."""
    # Filter out countries with missing or invalid currency data
    valid_countries = df[(df['currency'].notna()) & (df['currency'] != '')].copy()
    
    if len(valid_countries) < num_questions:
        num_questions = len(valid_countries)
    
    # Select random countries for questions
    selected_countries = valid_countries.sample(n=num_questions)
    questions = []
    
    for _, country_row in selected_countries.iterrows():
        correct_country = country_row['country']
        correct_continent = country_row['continent']
        currency = country_row['currency']
        gdp = country_row['gdp']
        
        # Generate 3 wrong continent options
        other_continents = valid_countries[
            (valid_countries['country'] != correct_country) & 
            (valid_countries['continent'] != correct_continent)
        ]['continent'].unique()
        
        if len(other_continents) >= 3:
            wrong_continents = random.sample(list(other_continents), 3)
        else:
            # If not enough unique currencies, use what we have and pad with generic ones
            wrong_continents = list(other_continents)
        
        # Create options list with correct answer at random position
        options = wrong_continents[:3] + [correct_continent]
        random.shuffle(options)
        correct_index = options.index(correct_continent)
        
        question = {
            "question": f"What is the continent of {correct_country}?",
            "options": options,
            "correct": correct_index,
            "explanation": f"The continent of {correct_country} is {correct_continent}. Currency: {currency}, GDP: {gdp}",
            "type": "currency"
        }
        questions.append(question)
    
    return questions

def generate_location_questions(df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Generate location-based questions (placeholder for future implementation).
    This could include questions about continents, neighboring countries, etc.
    """
    # Placeholder for future implementation
    questions = []
    
    # Example structure for when this is implemented:
    # for i in range(num_questions):
    #     question = {
    #         "question": "Which continent is [country] located in?",
    #         "options": ["Africa", "Asia", "Europe", "North America"],
    #         "correct": 0,
    #         "explanation": "[Country] is located in [continent].",
    #         "type": "location"
    #     }
    #     questions.append(question)
    
    return questions

# Quiz type registry for easy expansion
QUIZ_GENERATORS = {
    'currency': generate_currency_questions,
    'capital': generate_capital_questions,
    'continent': generate_continent_questions,
    'location': generate_location_questions,
}

def get_quiz_questions(quiz_type: str, df: pd.DataFrame, num_questions: int = 10) -> List[Dict[str, Any]]:
    """
    Get questions for a specific quiz type.
    
    Args:
        quiz_type: Type of quiz ('currency', 'capital','continent', 'location')
        df: DataFrame containing country data
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    if quiz_type not in QUIZ_GENERATORS:
        raise ValueError(f"Unknown quiz type: {quiz_type}. Available types: {list(QUIZ_GENERATORS.keys())}")
    
    generator_func = QUIZ_GENERATORS[quiz_type]
    return generator_func(df, num_questions)
