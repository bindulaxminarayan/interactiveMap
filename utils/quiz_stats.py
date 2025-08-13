#!/usr/bin/env python3
"""
Quiz Statistics Management System

This module provides functionality to track and manage quiz performance statistics
including daily stats, rollover functionality, and performance analytics.
"""

import sqlite3
from datetime import date, timedelta,timezone, datetime
from typing import Dict, List
from dataclasses import dataclass
import logging
import uuid

@dataclass
class QuizStats:
    """Data class to represent quiz statistics"""
    question_id: int
    date: str
    times_asked: int = 0
    times_correct: int = 0
    total_response_time: float = 0.0
    avg_response_time: float = 0.0
    accuracy_rate: float = 0.0

class QuizStatsManager:
    """
    Manages quiz statistics including daily tracking, rollover, and analytics
    """
    
    def __init__(self, db_path: str = "data/quiz_database.db"):
        logging.debug("Setting DB path as: %s",db_path)
        self.db_path = db_path
        self.init_stats_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_stats_tables(self):
        """Initialize statistics tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Daily question statistics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_question_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    times_asked INTEGER DEFAULT 0,
                    times_correct INTEGER DEFAULT 0,
                    total_response_time REAL DEFAULT 0.0,
                    avg_response_time REAL DEFAULT 0.0,
                    accuracy_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions_normalized(id),
                    UNIQUE(question_id, date)
                )
            """)
            
            # Daily category statistics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_category_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    subcategory_id INTEGER,
                    date DATE NOT NULL,
                    questions_asked INTEGER DEFAULT 0,
                    questions_correct INTEGER DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    avg_response_time REAL DEFAULT 0.0,
                    accuracy_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id),
                    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id),
                    UNIQUE(category_id, subcategory_id, date)
                )
            """)
            
            # Historical aggregated stats (for rollover)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_question_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    week_ending DATE NOT NULL,
                    total_asked INTEGER DEFAULT 0,
                    total_correct INTEGER DEFAULT 0,
                    avg_response_time REAL DEFAULT 0.0,
                    accuracy_rate REAL DEFAULT 0.0,
                    days_active INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions_normalized(id),
                    UNIQUE(question_id, week_ending)
                )
            """)
            
            # Individual quiz answers per session
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    question_id INTEGER NOT NULL,
                    user_answer TEXT,
                    is_correct BOOLEAN NOT NULL,
                    response_time REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions_normalized(id)
                )
            """)
            
            # Session-level statistics and metadata
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    session_name TEXT,
                    user_id TEXT,
                    category_filter TEXT,
                    total_questions INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    accuracy_rate REAL DEFAULT 0.0,
                    total_time REAL DEFAULT 0.0,
                    avg_response_time REAL DEFAULT 0.0,
                    fastest_answer REAL DEFAULT 0.0,
                    slowest_answer REAL DEFAULT 0.0,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def record_quiz_answer(self, question_id: int, is_correct: bool, response_time: float, 
                          session_id: str = None, user_answer: str = None):
        """
        Record a quiz answer and update daily statistics
        
        Args:
            question_id: ID of the question answered
            is_correct: Whether the answer was correct
            response_time: Time taken to answer in seconds
            session_id: Optional session identifier
            user_answer: The answer provided by the user
        """
     
        today = datetime.now(timezone.utc).date().isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Record individual answer in sessions table
            if session_id:
                cursor.execute("""
                    INSERT INTO quiz_sessions 
                    (session_id, question_id, user_answer, is_correct, response_time)
                    VALUES (?, ?, ?, ?, ?)
                """, (session_id, question_id, user_answer, is_correct, response_time))
            
            # Update daily question stats
            cursor.execute("""
                INSERT INTO daily_question_stats 
                (question_id, date, times_asked, times_correct, total_response_time)
                VALUES (?, ?, 1, ?, ?)
                ON CONFLICT(question_id, date) DO UPDATE SET
                    times_asked = times_asked + 1,
                    times_correct = times_correct + ?,
                    total_response_time = total_response_time + ?,
                    avg_response_time = (total_response_time + ?) / (times_asked + 1),
                    accuracy_rate = CAST(times_correct + ? AS REAL) / (times_asked + 1) * 100,
                    updated_at = CURRENT_TIMESTAMP
            """, (question_id, today, 1 if is_correct else 0, response_time,
                  1 if is_correct else 0, response_time, response_time, 1 if is_correct else 0))
            
            # Update daily category stats
            cursor.execute("""
                SELECT category_id, subcategory_id FROM questions_normalized 
                WHERE id = ?
            """, (question_id,))
            
            question_info = cursor.fetchone()
            if question_info:
                category_id = question_info['category_id']
                subcategory_id = question_info['subcategory_id']
                
                cursor.execute("""
                    INSERT INTO daily_category_stats 
                    (category_id, subcategory_id, date, questions_asked, questions_correct)
                    VALUES (?, ?, ?, 1, ?)
                    ON CONFLICT(category_id, subcategory_id, date) DO UPDATE SET
                        questions_asked = questions_asked + 1,
                        questions_correct = questions_correct + ?,
                        accuracy_rate = CAST(questions_correct AS REAL) / questions_asked * 100,
                        updated_at = CURRENT_TIMESTAMP
                """, (category_id, subcategory_id, today, 1 if is_correct else 0,
                      1 if is_correct else 0))
            
            conn.commit()
    
    def get_daily_stats(self, date_str: str = None) -> Dict:
        """
        Get daily statistics for a specific date
        
        Args:
            date_str: Date in YYYY-MM-DD format, defaults to today
            
        Returns:
            Dictionary containing daily stats
        """
        if date_str is None:
            date_str = datetime.now(timezone.utc).date().isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Question-level stats
            cursor.execute("""
                SELECT dqs.*, qn.question, c.display_name as category, sc.display_name as subcategory
                FROM daily_question_stats dqs
                JOIN questions_normalized qn ON dqs.question_id = qn.id
                JOIN categories c ON qn.category_id = c.id
                LEFT JOIN subcategories sc ON qn.subcategory_id = sc.id
                WHERE dqs.date = ?
                ORDER BY dqs.times_asked DESC
            """, (date_str,))
            
            question_stats = [dict(row) for row in cursor.fetchall()]
            
            # Category-level stats
            cursor.execute("""
                SELECT dcs.*, c.display_name as category, sc.display_name as subcategory
                FROM daily_category_stats dcs
                JOIN categories c ON dcs.category_id = c.id
                LEFT JOIN subcategories sc ON dcs.subcategory_id = sc.id
                WHERE dcs.date = ?
                ORDER BY dcs.questions_asked DESC
            """, (date_str,))
            
            category_stats = [dict(row) for row in cursor.fetchall()]
            
            return {
                'date': date_str,
                'question_stats': question_stats,
                'category_stats': category_stats,
                'summary': self._calculate_daily_summary(question_stats)
            }
    
    def _calculate_daily_summary(self, question_stats: List[Dict]) -> Dict:
        """Calculate summary statistics for the day"""
        if not question_stats:
            return {
                'total_questions_asked': 0,
                'total_correct_answers': 0,
                'overall_accuracy': 0.0,
                'avg_response_time': 0.0
            }
        
        total_asked = sum(stat['times_asked'] for stat in question_stats)
        total_correct = sum(stat['times_correct'] for stat in question_stats)
        total_response_time = sum(stat['total_response_time'] for stat in question_stats)
        
        return {
            'total_questions_asked': total_asked,
            'total_correct_answers': total_correct,
            'overall_accuracy': (total_correct / total_asked * 100) if total_asked > 0 else 0.0,
            'avg_response_time': (total_response_time / total_asked) if total_asked > 0 else 0.0
        }
    
    def get_question_performance(self, question_id: int, days: int = 7) -> Dict:
        """
        Get performance statistics for a specific question over the last N days
        
        Args:
            question_id: ID of the question
            days: Number of days to look back
            
        Returns:
            Dictionary containing performance data
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM daily_question_stats
                WHERE question_id = ? AND date BETWEEN ? AND ?
                ORDER BY date
            """, (question_id, start_date.isoformat(), end_date.isoformat()))
            
            daily_stats = [dict(row) for row in cursor.fetchall()]
            
            # Calculate aggregated metrics
            total_asked = sum(stat['times_asked'] for stat in daily_stats)
            total_correct = sum(stat['times_correct'] for stat in daily_stats)
            
            return {
                'question_id': question_id,
                'period': f"{start_date} to {end_date}",
                'daily_stats': daily_stats,
                'summary': {
                    'total_asked': total_asked,
                    'total_correct': total_correct,
                    'accuracy_rate': (total_correct / total_asked * 100) if total_asked > 0 else 0.0,
                    'days_active': len([s for s in daily_stats if s['times_asked'] > 0])
                }
            }
    
    def rollover_weekly_stats(self):
        """
        Rollover daily stats to weekly historical stats and clean up old daily data
        This should be run weekly to maintain database performance
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Find the week ending date (last Sunday)
            today = date.today()
            days_since_sunday = (today.weekday() + 1) % 7
            week_ending = today - timedelta(days=days_since_sunday)
            week_start = week_ending - timedelta(days=6)
            
            # Aggregate weekly stats
            cursor.execute("""
                INSERT OR REPLACE INTO historical_question_stats
                (question_id, week_ending, total_asked, total_correct, avg_response_time, accuracy_rate, days_active)
                SELECT 
                    question_id,
                    ? as week_ending,
                    SUM(times_asked) as total_asked,
                    SUM(times_correct) as total_correct,
                    AVG(avg_response_time) as avg_response_time,
                    (SUM(times_correct) * 100.0 / SUM(times_asked)) as accuracy_rate,
                    COUNT(DISTINCT date) as days_active
                FROM daily_question_stats
                WHERE date BETWEEN ? AND ?
                GROUP BY question_id
                HAVING SUM(times_asked) > 0
            """, (week_ending.isoformat(), week_start.isoformat(), week_ending.isoformat()))
            
            # Remove old daily stats (keep last 30 days)
            cutoff_date = today - timedelta(days=30)
            cursor.execute("""
                DELETE FROM daily_question_stats 
                WHERE date < ?
            """, (cutoff_date.isoformat(),))
            
            cursor.execute("""
                DELETE FROM daily_category_stats 
                WHERE date < ?
            """, (cutoff_date.isoformat(),))
            
            # Remove old session data (keep last 7 days)
            session_cutoff = today - timedelta(days=7)
            cursor.execute("""
                DELETE FROM quiz_sessions 
                WHERE DATE(timestamp) < ?
            """, (session_cutoff.isoformat(),))
            
            conn.commit()
            
            return {
                'week_ending': week_ending.isoformat(),
                'stats_aggregated': cursor.rowcount,
                'old_daily_stats_removed': cutoff_date.isoformat(),
                'old_sessions_removed': session_cutoff.isoformat()
            }
    
    def get_trending_questions(self, limit: int = 10, period_days: int = 7) -> List[Dict]:
        """
        Get trending questions based on recent activity and difficulty
        
        Args:
            limit: Number of questions to return
            period_days: Number of days to consider for trending
            
        Returns:
            List of trending questions with stats
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=period_days-1)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    dqs.question_id,
                    qn.question,
                    qn.difficulty,
                    c.display_name as category,
                    sc.display_name as subcategory,
                    SUM(dqs.times_asked) as total_asked,
                    SUM(dqs.times_correct) as total_correct,
                    AVG(dqs.accuracy_rate) as avg_accuracy,
                    AVG(dqs.avg_response_time) as avg_response_time
                FROM daily_question_stats dqs
                JOIN questions_normalized qn ON dqs.question_id = qn.id
                JOIN categories c ON qn.category_id = c.id
                LEFT JOIN subcategories sc ON qn.subcategory_id = sc.id
                WHERE dqs.date BETWEEN ? AND ?
                GROUP BY dqs.question_id
                HAVING total_asked >= 3
                ORDER BY total_asked DESC, avg_accuracy ASC
                LIMIT ?
            """, (start_date.isoformat(), end_date.isoformat(), limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def start_quiz_session(self, session_name: str = None, 
                          user_id: str = None, category_filter: str = None) -> str:
        """
        Start a new quiz session
        
        Args:
            session_name: Optional name for the session
            user_id: Optional user identifier
            category_filter: Optional category filter (JSON string)
            
        Returns:
            String session ID
        """
        session_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_stats 
                (session_id, session_name, user_id, category_filter, status)
                VALUES (?, ?, ?, ?, 'active')
            """, (session_id, session_name, user_id, category_filter))
            
            conn.commit()
            
            return session_id
    
    def update_session_stats(self, session_id: str):
        """
        Update session statistics based on recorded answers
        
        Args:
            session_id: Session identifier to update
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Calculate session statistics from individual answers
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_questions,
                    SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_answers,
                    SUM(response_time) as total_time,
                    AVG(response_time) as avg_response_time,
                    MIN(response_time) as fastest_answer,
                    MAX(response_time) as slowest_answer
                FROM quiz_sessions
                WHERE session_id = ?
            """, (session_id,))
            
            stats = cursor.fetchone()
            if stats and stats['total_questions'] > 0:
                accuracy_rate = (stats['correct_answers'] / stats['total_questions']) * 100
                
                cursor.execute("""
                    UPDATE session_stats SET
                        total_questions = ?,
                        correct_answers = ?,
                        accuracy_rate = ?,
                        total_time = ?,
                        avg_response_time = ?,
                        fastest_answer = ?,
                        slowest_answer = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """, (stats['total_questions'], stats['correct_answers'], 
                      accuracy_rate, stats['total_time'], stats['avg_response_time'],
                      stats['fastest_answer'], stats['slowest_answer'], session_id))
                
                conn.commit()
    
    def end_quiz_session(self, session_id: str) -> Dict:
        """
        End a quiz session and finalize statistics
        
        Args:
            session_id: Session identifier to end
            
        Returns:
            Final session statistics
        """
        # Update final stats
        self.update_session_stats(session_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Mark session as completed
            cursor.execute("""
                UPDATE session_stats SET
                    status = 'completed',
                    ended_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """, (session_id,))
            
            # Get final session stats
            cursor.execute("""
                SELECT * FROM session_stats WHERE session_id = ?
            """, (session_id,))
            
            session_stats = dict(cursor.fetchone()) if cursor.fetchone() else None
            
            conn.commit()
            
            return session_stats
    
    def get_session_stats(self, session_id: str) -> Dict:
        """
        Get current statistics for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary containing session stats and detailed answers
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get session metadata
            cursor.execute("""
                SELECT * FROM session_stats WHERE session_id = ?
            """, (session_id,))
            
            session_data = cursor.fetchone()
            if not session_data:
                return None
            
            session_info = dict(session_data)
            
            # Get detailed answers for this session
            cursor.execute("""
                SELECT 
                    qs.*,
                    qn.question,
                    qn.correct_answer,
                    c.display_name as category,
                    sc.display_name as subcategory
                FROM quiz_sessions qs
                JOIN questions_normalized qn ON qs.question_id = qn.id
                JOIN categories c ON qn.category_id = c.id
                LEFT JOIN subcategories sc ON qn.subcategory_id = sc.id
                WHERE qs.session_id = ?
                ORDER BY qs.timestamp
            """, (session_id,))
            
            answers = [dict(row) for row in cursor.fetchall()]
            
            return {
                'session_info': session_info,
                'answers': answers,
                'summary': {
                    'total_questions': len(answers),
                    'correct_answers': sum(1 for a in answers if a['is_correct']),
                    'accuracy_rate': (sum(1 for a in answers if a['is_correct']) / len(answers) * 100) if answers else 0,
                    'total_time': sum(a['response_time'] for a in answers),
                    'avg_response_time': sum(a['response_time'] for a in answers) / len(answers) if answers else 0
                }
            }
    
    def get_recent_sessions(self, limit: int = 10, user_id: str = None) -> List[Dict]:
        """
        Get recent quiz sessions
        
        Args:
            limit: Number of sessions to return
            user_id: Optional filter by user ID
            
        Returns:
            List of recent sessions with basic stats
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM session_stats
                WHERE 1=1
            """
            params = []
            
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            
            query += " ORDER BY started_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_session_leaderboard(self, period_days: int = 7, limit: int = 10) -> List[Dict]:
        """
        Get leaderboard of best session performances
        
        Args:
            period_days: Number of days to look back
            limit: Number of sessions to return
            
        Returns:
            List of top-performing sessions
        """
        start_date = (date.today() - timedelta(days=period_days)).isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    session_id,
                    session_name,
                    user_id,
                    total_questions,
                    correct_answers,
                    accuracy_rate,
                    avg_response_time,
                    started_at,
                    ended_at
                FROM session_stats
                WHERE DATE(started_at) >= ? 
                    AND status = 'completed'
                    AND total_questions >= 5
                ORDER BY accuracy_rate DESC, avg_response_time ASC
                LIMIT ?
            """, (start_date, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def record_quiz_answer_with_session(self, session_id: str, question_id: int, 
                                       is_correct: bool, response_time: float, 
                                       user_answer: str = None):
        """
        Record a quiz answer and automatically update session stats
        
        Args:
            session_id: Session identifier
            question_id: ID of the question answered
            is_correct: Whether the answer was correct
            response_time: Time taken to answer in seconds
            user_answer: The answer provided by the user
        """
        # Record the individual answer
        self.record_quiz_answer(
            question_id=question_id,
            is_correct=is_correct,
            response_time=response_time,
            session_id=session_id,
            user_answer=user_answer
        )
        
        # Update session statistics
        self.update_session_stats(session_id)

# Initialize default stats manager
quiz_stats = QuizStatsManager()
