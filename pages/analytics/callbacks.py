"""
Analytics page callbacks for interactive functionality.
"""

import json
import logging
from datetime import date, timedelta

from dash import Input, Output
from utils.quiz_stats import QuizStatsManager
from utils.datetime_utils import get_local_today, is_same_local_date
from .layouts import (
    create_daily_performance_chart,
    create_category_performance_chart,
    create_sessions_table,
    create_trending_questions_table,
    create_leaderboard_table
)

def register_analytics_callbacks(app):
    """Register all analytics-related callbacks."""
    
    @app.callback(
        [
            Output('analytics-data-store', 'children'),
            Output('total-questions-today', 'children'),
            Output('overall-accuracy-today', 'children'),
            Output('active-sessions-today', 'children'),
            Output('avg-response-time-today', 'children')
        ],
        [
            Input('refresh-analytics-btn', 'n_clicks'),
            Input('analytics-refresh-interval', 'n_intervals'),
            Input('analytics-date-range', 'start_date'),
            Input('analytics-date-range', 'end_date')
        ]
    )
    def refresh_analytics_data(refresh_clicks, interval_triggers, start_date, end_date):
        """Refresh analytics data and update summary cards."""
        try:
            stats_manager = QuizStatsManager()
            
            # Get today's stats for summary cards
            today_stats = stats_manager.get_daily_stats()
            
            # Get recent sessions
            recent_sessions = stats_manager.get_recent_sessions(limit=20)
            
            # Get trending questions
            trending_questions = stats_manager.get_trending_questions(limit=15, period_days=7)
            
            # Get session leaderboard
            leaderboard = stats_manager.get_session_leaderboard(period_days=30, limit=15)
            
            # Get daily stats for the selected date range
            daily_stats_range = []
            if start_date and end_date:
                current_date = date.fromisoformat(start_date)
                end_date_obj = date.fromisoformat(end_date)
                
                while current_date <= end_date_obj:
                    day_stats = stats_manager.get_daily_stats(current_date.isoformat())
                    if day_stats['summary']['total_questions_asked'] > 0:
                        daily_stats_range.append(day_stats)
                    current_date += timedelta(days=1)
            
            # Prepare data store
            analytics_data = {
                'today_stats': today_stats,
                'daily_stats_range': daily_stats_range,
                'recent_sessions': recent_sessions,
                'trending_questions': trending_questions,
                'leaderboard': leaderboard,
                'last_updated': date.today().isoformat()
            }
            
            # Extract summary values
            summary = today_stats['summary']
            total_questions = summary['total_questions_asked']
            accuracy = f"{summary['overall_accuracy']:.1f}%"
            avg_time = f"{summary['avg_response_time']:.1f}s"
            
            # Count today's sessions (properly handle timezone conversion)
            today_local_date = get_local_today()  # Get today in local timezone
            
            active_sessions = len([s for s in recent_sessions 
                                 if s['started_at'] and is_same_local_date(s['started_at'], today_local_date)])
            
            return (
                json.dumps(analytics_data),
                str(total_questions),
                accuracy,
                str(active_sessions),
                avg_time
            )
            
        except Exception as e:
            logging.error("Error refreshing analytics data: %s",e)
            return (
                json.dumps({}),
                "Error",
                "Error",
                "Error",
                "Error"
            )
    
    @app.callback(
        Output('daily-performance-chart', 'figure'),
        Input('analytics-data-store', 'children')
    )
    def update_daily_performance_chart(analytics_data_json):
        """Update the daily performance chart."""
        try:
            if not analytics_data_json:
                return create_daily_performance_chart([])
            
            analytics_data = json.loads(analytics_data_json)
            daily_stats = analytics_data.get('daily_stats_range', [])
            
            return create_daily_performance_chart(daily_stats)
            
        except Exception as e:
            logging.error("Error updating daily performance chart: %s",e)
            return create_daily_performance_chart([])
    
    @app.callback(
        Output('category-performance-chart', 'figure'),
        Input('analytics-data-store', 'children')
    )
    def update_category_performance_chart(analytics_data_json):
        """Update the category performance chart."""
        try:
            if not analytics_data_json:
                return create_category_performance_chart([])
            
            analytics_data = json.loads(analytics_data_json)
            today_stats = analytics_data.get('today_stats', {})
            category_stats = today_stats.get('category_stats', [])
            
            return create_category_performance_chart(category_stats)
            
        except Exception as e:
            logging.error("Error updating category performance chart: %s",e)
            return create_category_performance_chart([])
    
    @app.callback(
        Output('recent-sessions-table', 'children'),
        Input('analytics-data-store', 'children')
    )
    def update_recent_sessions_table(analytics_data_json):
        """Update the recent sessions table."""
        try:
            if not analytics_data_json:
                return create_sessions_table([])
            
            analytics_data = json.loads(analytics_data_json)
            recent_sessions = analytics_data.get('recent_sessions', [])
            
            return create_sessions_table(recent_sessions)
            
        except Exception as e:
            logging.error("Error updating recent sessions table: %s",e)
            return create_sessions_table([])
    
    @app.callback(
        Output('trending-questions-table', 'children'),
        Input('analytics-data-store', 'children')
    )
    def update_trending_questions_table(analytics_data_json):
        """Update the trending questions table."""
        try:
            if not analytics_data_json:
                return create_trending_questions_table([])
            
            analytics_data = json.loads(analytics_data_json)
            trending_questions = analytics_data.get('trending_questions', [])
            
            return create_trending_questions_table(trending_questions)
            
        except Exception as e:
            logging.error("Error updating trending questions table: %s",e)
            return create_trending_questions_table([])
    
    @app.callback(
        Output('session-leaderboard-table', 'children'),
        Input('analytics-data-store', 'children')
    )
    def update_session_leaderboard_table(analytics_data_json):
        """Update the session leaderboard table."""
        try:
            if not analytics_data_json:
                return create_leaderboard_table([])
            
            analytics_data = json.loads(analytics_data_json)
            leaderboard = analytics_data.get('leaderboard', [])
            
            return create_leaderboard_table(leaderboard)
            
        except Exception as e:
            logging.error("Error updating session leaderboard table: %s",e)
            return create_leaderboard_table([])
