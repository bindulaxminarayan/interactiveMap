# Trivia Module Documentation

This directory contains the refactored trivia quiz functionality, organized into separate modules for better maintainability and readability.

## Module Structure

### `__init__.py`
Main module entry point that exports the primary functions:
- `get_trivia_layout()`: Returns the main trivia page layout
- `register_trivia_callbacks()`: Registers all Dash callbacks

### `components.py`
Reusable UI components used throughout the trivia module:
- `create_quiz_category_section()`: Creates quiz category sections in the side panel
- `create_quiz_button()`: Standardized button creation with different styles
- `create_score_display()`: Score display component for quiz results
- `create_feedback_message()`: Simple feedback messages for correct/incorrect answers (shows only basic status and correct answer when wrong)
- `create_welcome_content()`: Welcome screen content

### `quiz_components.py`
Quiz-specific UI components:
- `create_progress_bar()`: Progress indicator during quizzes
- `create_question_layout()`: Layout for individual quiz questions
- `get_answer_button_style()`: Styling logic for answer buttons based on state
- `get_performance_data()`: Performance evaluation logic
- `create_completion_screen()`: Quiz completion screen with results

### `layouts.py`
Main layout components:
- `create_side_panel()`: Quiz category selection panel
- `create_hidden_elements()`: Hidden DOM elements required for callbacks
- `get_trivia_layout()`: Main page layout combining all components

### `callbacks.py`
All Dash callback functions:
- `start_quiz()`: Handles quiz initialization from side panel
- `restart_quiz_from_results()`: Handles quiz restart from results screen
- `handle_quiz_interactions()`: Main quiz interaction logic (answers, next question)
- `quit_quiz()`: Quiz termination logic
- `back_to_selection()`: Return to main menu logic
- `_return_to_welcome()`: Helper function for returning to welcome screen

## Benefits of This Structure

1. **Modularity**: Each file has a clear, single responsibility
2. **Reusability**: Components can be easily reused across different parts of the app
3. **Maintainability**: Easier to locate and modify specific functionality
4. **Testability**: Individual components can be tested in isolation
5. **Readability**: Smaller, focused files are easier to understand
6. **Scalability**: Easy to add new quiz types or features without cluttering existing code

## Usage

The module maintains backward compatibility. The original `pages/trivia.py` file now imports from the new structure, so existing code using:

```python
from pages.trivia import get_trivia_layout, register_trivia_callbacks
```

...will continue to work without changes.

## Adding New Features

To add new quiz types or features:

1. **New Quiz Type**: Add to `layouts.py` side panel and update `callbacks.py`
2. **New Components**: Add to `components.py` or `quiz_components.py` as appropriate
3. **New Styling**: Extend the component functions with additional style parameters
4. **New Callbacks**: Add to `callbacks.py` following the existing pattern

## File Dependencies

```
trivia/
├── __init__.py           # Main exports
├── components.py         # Basic UI components
├── quiz_components.py    # Quiz-specific components (depends on components.py)
├── layouts.py           # Page layouts (depends on components.py)
├── callbacks.py         # Dash callbacks (depends on quiz_components.py, components.py)
└── README.md           # This documentation
```

External dependencies:
- `utils.data_processing`: Data loading functions
- `utils.quiz_generators`: Quiz question generation
- `dash`: UI framework and callback system
