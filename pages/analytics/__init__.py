"""
Analytics page for quiz performance statistics.
"""

from .layouts import get_analytics_layout
from .callbacks import register_analytics_callbacks

__all__ = ['get_analytics_layout', 'register_analytics_callbacks']
