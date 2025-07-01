"""
Trivia page for country-related quiz questions.
This file now serves as the main entry point for the refactored trivia module.
"""

# Import from the new modular structure
from .trivia import get_trivia_layout, register_trivia_callbacks

# Re-export the main functions for backward compatibility
__all__ = ['get_trivia_layout', 'register_trivia_callbacks']
