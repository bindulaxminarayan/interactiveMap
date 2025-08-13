"""
Unit tests for quiz_generators module.
"""
from unittest.mock import patch
import pytest
from utils.quiz_generators import (
    get_quiz_questions,
    get_available_quiz_types,
    get_quiz_types_by_category,
    get_quiz_display_name,
    generate_questions_by_category,
    _build_image_path,
    _format_questions_normalized,
    QUIZ_CONFIG,
    QUIZ_TYPE_LABEL
)

# Mock database data
MOCK_DB_DATA = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "correct_answer": "Paris",
        "option1": "Berlin",
        "option2": "Madrid",
        "option3": "Rome",
        "fun_fact": "Paris is known as the City of Light.",
        "image": "",
        "category_name": "geography",
        "subcategory_name": "capital",
        "difficulty": "easy",
        "points": 1,
    },
    {
        "id": 2,
        "question": "Which country has the flag with a red circle?",
        "correct_answer": "Japan",
        "option1": "China",
        "option2": "South Korea",
        "option3": "Thailand",
        "fun_fact": "Japan's flag is called Hinomaru.",
        "image": "japan.png",
        "category_name": "geography",
        "subcategory_name": "flag",
        "difficulty": "medium",
        "points": 1,
    }
]


class TestQuizConfiguration:
    """Test quiz configuration constants."""
    
    def test_quiz_config_contains_expected_types(self):
        """Test that QUIZ_CONFIG contains expected quiz types."""
        expected_types = ['flag', 'capital', 'currency', 'biology', 'famous_people']
        for quiz_type in expected_types:
            assert quiz_type in QUIZ_CONFIG
    
    def test_quiz_config_structure(self):
        """Test that each quiz config has required fields."""
        for quiz_type, config in QUIZ_CONFIG.items():
            assert 'category' in config
            assert 'subcategory' in config
            assert isinstance(config['category'], str)
            assert isinstance(config['subcategory'], str)
    
    def test_quiz_type_labels_complete(self):
        """Test that all quiz types have display labels."""
        for quiz_type in QUIZ_CONFIG.keys():
            assert quiz_type in QUIZ_TYPE_LABEL
            assert isinstance(QUIZ_TYPE_LABEL[quiz_type], str)
            assert len(QUIZ_TYPE_LABEL[quiz_type]) > 0


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_get_available_quiz_types(self):
        """Test getting all available quiz types."""
        quiz_types = get_available_quiz_types()
        assert isinstance(quiz_types, list)
        assert len(quiz_types) > 0
        
        # Check some expected types are present
        expected_types = ['flag', 'capital', 'biology', 'famous_people']
        for expected_type in expected_types:
            assert expected_type in quiz_types
    
    def test_get_quiz_types_by_category(self):
        """Test filtering quiz types by category."""
        # Test geography category
        geography_types = get_quiz_types_by_category('geography')
        assert isinstance(geography_types, list)
        assert 'flag' in geography_types
        assert 'capital' in geography_types
        
        # Test science category
        science_types = get_quiz_types_by_category('science')
        assert 'biology' in science_types
        assert 'chemistry' in science_types
        
        # Test history category
        history_types = get_quiz_types_by_category('history')
        assert 'famous_people' in history_types
        
        # Test non-existent category
        empty_types = get_quiz_types_by_category('nonexistent')
        assert empty_types == []
    
    def test_get_quiz_display_name(self):
        """Test getting display names for quiz types."""
        assert get_quiz_display_name('flag') == 'Flags'
        assert get_quiz_display_name('famous_people') == 'Famous People'
        assert get_quiz_display_name('us_capital') == 'US State Capitals'
        
        # Test fallback for unknown type
        assert get_quiz_display_name('unknown_type') == 'Unknown Type'
    
    def test_build_image_path(self):
        """Test image path building."""
        # Test with valid image and folder
        path = _build_image_path('japan.png', 'flags')
        assert path == 'assets/flags/japan.png'
        
        # Test with empty image
        path = _build_image_path('', 'flags')
        assert path == ''
        
        # Test with no folder
        path = _build_image_path('japan.png', None)
        assert path == ''


class TestQuestionFormatting:
    """Test question formatting functionality."""
    
    def test_format_questions_basic(self):
        """Test basic question formatting."""
        quiz_config = {'category': 'geography', 'subcategory': 'capital'}
        questions = _format_questions_normalized([MOCK_DB_DATA[0]], quiz_config)
        
        assert len(questions) == 1
        question = questions[0]
        
        # Check required fields
        assert question['id'] == 1
        assert question['question'] == "What is the capital of France?"
        assert len(question['options']) == 4
        assert 'Paris' in question['options']
        assert isinstance(question['correct'], int)
        assert 0 <= question['correct'] <= 3
        assert question['options'][question['correct']] == 'Paris'
        assert question['type'] == 'geography_quiz'
        assert question['fun_fact'] == "Paris is known as the City of Light."
        assert question['category'] == 'geography'
        assert question['subcategory'] == 'capital'
        assert question['difficulty'] == 'easy'
        assert question['points'] == 1
    
    def test_format_questions_with_image(self):
        """Test question formatting with image paths."""
        quiz_config = {
            'category': 'geography', 
            'subcategory': 'flag',
            'image_folder': 'flags'
        }
        questions = _format_questions_normalized([MOCK_DB_DATA[1]], quiz_config)
        
        assert len(questions) == 1
        question = questions[0]
        assert 'image' in question
        assert question['image'] == 'assets/flags/japan.png'
    
    def test_format_questions_without_image_folder(self):
        """Test question formatting without image folder configured."""
        quiz_config = {'category': 'geography', 'subcategory': 'capital'}
        questions = _format_questions_normalized([MOCK_DB_DATA[0]], quiz_config)
        
        question = questions[0]
        assert 'image' not in question
    
    def test_options_are_shuffled(self):
        """Test that options are shuffled but correct answer is maintained."""
        quiz_config = {'category': 'geography', 'subcategory': 'capital'}
        
        # Test multiple times to verify shuffling
        for _ in range(5):
            questions = _format_questions_normalized([MOCK_DB_DATA[0]], quiz_config)
            question = questions[0]
            
            # Verify correct answer is always tracked properly
            assert question['options'][question['correct']] == 'Paris'
            assert len(question['options']) == 4
            assert all(opt in ['Paris', 'Berlin', 'Madrid', 'Rome'] for opt in question['options'])


class TestDatabaseIntegration:
    """Test database integration functions."""
    
    @patch('utils.quiz_generators.quiz_db.execute_query')
    def test_get_quiz_questions_success(self, mock_execute_query):
        """Test successful quiz question retrieval."""
        mock_execute_query.return_value = [MOCK_DB_DATA[0]]
        
        questions = get_quiz_questions('capital', num_questions=1)
        
        assert len(questions) == 1
        assert questions[0]['question'] == "What is the capital of France?"
        assert questions[0]['category'] == 'geography'
        assert questions[0]['subcategory'] == 'capital'
        
        # Verify database was called
        mock_execute_query.assert_called_once()
    
    @patch('utils.quiz_generators.quiz_db.execute_query')
    def test_get_quiz_questions_with_images(self, mock_execute_query):
        """Test quiz questions with image configuration."""
        mock_execute_query.return_value = [MOCK_DB_DATA[1]]
        
        questions = get_quiz_questions('flag', num_questions=1)
        
        assert len(questions) == 1
        assert 'image' in questions[0]
        assert questions[0]['image'] == 'assets/flags/japan.png'
    
    def test_get_quiz_questions_invalid_type(self):
        """Test error handling for invalid quiz type."""
        with pytest.raises(ValueError) as exc_info:
            get_quiz_questions('invalid_type')
        
        assert "Unknown quiz type: invalid_type" in str(exc_info.value)
        assert "Available types:" in str(exc_info.value)
    
    @patch('utils.quiz_generators.quiz_db.execute_query')
    def test_generate_questions_by_category(self, mock_execute_query):
        """Test generating questions by category and subcategory."""
        mock_execute_query.return_value = [MOCK_DB_DATA[0]]
        
        questions = generate_questions_by_category(
            category='geography',
            subcategory='capital',
            num_questions=1
        )
        
        assert len(questions) == 1
        assert questions[0]['category'] == 'geography'
        assert questions[0]['subcategory'] == 'capital'
        
        # Verify correct database call
        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]
        assert 'geography' in call_args[1]
        assert 'capital' in call_args[1]
        assert call_args[1][2] == 1  # num_questions
    
    @patch('utils.quiz_generators.quiz_db.execute_query')
    def test_database_error_handling(self, mock_execute_query):
        """Test handling of database errors."""
        mock_execute_query.side_effect = Exception("Database connection failed")
        
        questions = get_quiz_questions('capital', num_questions=1)
        
        # Should return empty list on database error
        assert questions == []
    
    @patch('utils.quiz_generators.quiz_db.execute_query')
    def test_empty_database_result(self, mock_execute_query):
        """Test handling when database returns no results."""
        mock_execute_query.return_value = []
        
        questions = get_quiz_questions('capital', num_questions=1)
        
        assert questions == []


class TestQuizTypeConfiguration:
    """Test quiz type configuration mappings."""
    
    def test_all_categories_have_quiz_types(self):
        """Test that geography, science, and history categories have quiz types."""
        geography_types = get_quiz_types_by_category('geography')
        science_types = get_quiz_types_by_category('science')
        history_types = get_quiz_types_by_category('history')
        
        assert len(geography_types) > 0
        assert len(science_types) > 0
        assert len(history_types) > 0
    
    def test_image_folders_configured_correctly(self):
        """Test that quiz types with images have correct folder configuration."""
        # Check that flag, wonders, and famous_people have image folders
        assert 'image_folder' in QUIZ_CONFIG['flag']
        assert QUIZ_CONFIG['flag']['image_folder'] == 'flags'
        
        assert 'image_folder' in QUIZ_CONFIG['wonders']
        assert QUIZ_CONFIG['wonders']['image_folder'] == 'wonders'
        
        assert 'image_folder' in QUIZ_CONFIG['famous_people']
        assert QUIZ_CONFIG['famous_people']['image_folder'] == 'famous'
        
        # Check that text-only quizzes don't have image folders
        text_only_types = ['capital', 'currency', 'biology']
        for quiz_type in text_only_types:
            assert 'image_folder' not in QUIZ_CONFIG[quiz_type]


if __name__ == '__main__':
    pytest.main([__file__])
