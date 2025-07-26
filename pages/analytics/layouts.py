"""
Analytics page layouts for quiz performance statistics.
"""

from dash import html, dcc, dash_table
import plotly.graph_objs as go
import plotly.express as px
from datetime import date, timedelta
from utils.datetime_utils import utc_to_local_string, utc_to_local_date_string

def get_analytics_layout():
    """Create the analytics page layout."""
    return html.Div([
        # Page header
        html.Div([
            html.H1("📊 Quiz Analytics Dashboard", className="page-title"),
            html.P("Track quiz performance, sessions, and statistics", className="page-subtitle")
        ], className="page-header"),
        
        # Refresh button and date picker
        html.Div([
            html.Div([
                html.Button("🔄 Refresh Data", id="refresh-analytics-btn", className="btn btn-primary"),
                html.Span(" ", style={"margin": "0 10px"}),
                html.Label("Date Range:", style={"font-weight": "bold"}),
                dcc.DatePickerRange(
                    id='analytics-date-range',
                    start_date=date.today() - timedelta(days=7),
                    end_date=date.today(),
                    display_format='YYYY-MM-DD',
                    style={"margin-left": "10px"}
                )
            ], className="analytics-controls")
        ], style={"margin-bottom": "20px"}),
        
        # Summary cards
        html.Div([
            html.Div([
                html.Div([
                    html.H3(id="total-questions-today", children="0"),
                    html.P("Questions Today", className="card-subtitle")
                ], className="analytics-card")
            ], className="col-md-3"),
            
            html.Div([
                html.Div([
                    html.H3(id="overall-accuracy-today", children="0%"),
                    html.P("Today's Accuracy", className="card-subtitle")
                ], className="analytics-card")
            ], className="col-md-3"),
            
            html.Div([
                html.Div([
                    html.H3(id="active-sessions-today", children="0"),
                    html.P("Sessions Today", className="card-subtitle")
                ], className="analytics-card")
            ], className="col-md-3"),
            
            html.Div([
                html.Div([
                    html.H3(id="avg-response-time-today", children="0s"),
                    html.P("Avg Response Time", className="card-subtitle")
                ], className="analytics-card")
            ], className="col-md-3")
        ], className="row", style={"margin-bottom": "30px"}),
        
        # Charts section
        html.Div([
            # Daily performance chart
            html.Div([
                html.H3("📈 Daily Performance Trends"),
                dcc.Graph(id="daily-performance-chart")
            ], className="chart-container", style={"margin-bottom": "30px"}),
            
            # Category performance
            html.Div([
                html.H3("📚 Category Performance"),
                dcc.Graph(id="category-performance-chart")
            ], className="chart-container", style={"margin-bottom": "30px"})
        ]),
        
        # Tables section
        html.Div([
            # Recent sessions table
            html.Div([
                html.H3("🕐 Recent Quiz Sessions"),
                html.Div(id="recent-sessions-table")
            ], className="table-container", style={"margin-bottom": "30px"}),
            
            # Trending questions
            html.Div([
                html.H3("🔥 Trending Questions"),
                html.Div(id="trending-questions-table")
            ], className="table-container", style={"margin-bottom": "30px"}),
            
            # Session leaderboard
            html.Div([
                html.H3("🏆 Session Leaderboard"),
                html.Div(id="session-leaderboard-table")
            ], className="table-container", style={"margin-bottom": "30px"})
        ]),
        
        # Hidden div to store analytics data
        html.Div(id="analytics-data-store", style={"display": "none"}),
        
        # Auto-refresh interval (every 30 seconds)
        dcc.Interval(
            id='analytics-refresh-interval',
            interval=30*1000,  # 30 seconds
            n_intervals=0
        )
    ], className="analytics-page")

def create_daily_performance_chart(daily_stats):
    """Create daily performance trend chart."""
    if not daily_stats:
        return go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Extract data for chart
    dates = [stat['date'] for stat in daily_stats]
    questions = [stat['summary']['total_questions_asked'] for stat in daily_stats]
    accuracy = [stat['summary']['overall_accuracy'] for stat in daily_stats]
    
    fig = go.Figure()
    
    # Add questions asked line
    fig.add_trace(go.Scatter(
        x=dates,
        y=questions,
        mode='lines+markers',
        name='Questions Asked',
        line=dict(color='#1f77b4'),
        yaxis='y'
    ))
    
    # Add accuracy line on secondary y-axis
    fig.add_trace(go.Scatter(
        x=dates,
        y=accuracy,
        mode='lines+markers',
        name='Accuracy %',
        line=dict(color='#ff7f0e'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Daily Quiz Performance",
        xaxis_title="Date",
        yaxis=dict(title="Questions Asked", side="left"),
        yaxis2=dict(title="Accuracy %", side="right", overlaying="y", range=[0, 100]),
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig

def create_category_performance_chart(category_stats):
    """Create category performance chart."""
    if not category_stats:
        return go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    categories = [stat['category'] for stat in category_stats]
    accuracy = [stat['accuracy_rate'] for stat in category_stats]
    questions = [stat['questions_asked'] for stat in category_stats]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=accuracy,
            text=[f"{acc:.1f}%" for acc in accuracy],
            textposition='auto',
            marker_color='lightblue',
            customdata=questions,
            hovertemplate='<b>%{x}</b><br>Accuracy: %{y:.1f}%<br>Questions: %{customdata}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Category Performance Comparison",
        xaxis_title="Category",
        yaxis_title="Accuracy %",
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_sessions_table(sessions_data):
    """Create recent sessions table."""
    if not sessions_data:
        return html.P("No recent sessions found.")
    
    # Prepare data for table
    table_data = []
    for session in sessions_data:
        table_data.append({
            'Session ID': session['session_id'][:8] + '...',
            'Name': session['session_name'] or 'Unnamed Session',
            'User': session['user_id'] or 'Anonymous',
            'Questions': session['total_questions'],
            'Accuracy': f"{session['accuracy_rate']:.1f}%",
            'Avg Time': f"{session['avg_response_time']:.1f}s" if session['avg_response_time'] else 'N/A',
            'Status': session['status'].title(),
            'Started': utc_to_local_string(session['started_at'])
        })
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {"name": "Session ID", "id": "Session ID"},
            {"name": "Name", "id": "Name"},
            {"name": "User", "id": "User"},
            {"name": "Questions", "id": "Questions", "type": "numeric"},
            {"name": "Accuracy", "id": "Accuracy"},
            {"name": "Avg Time", "id": "Avg Time"},
            {"name": "Status", "id": "Status"},
            {"name": "Started", "id": "Started"}
        ],
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{Status} = Completed'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Status} = Active'},
                'backgroundColor': '#fff3cd',
                'color': 'black',
            }
        ],
        page_size=10,
        sort_action="native"
    )

def create_trending_questions_table(trending_data):
    """Create trending questions table."""
    if not trending_data:
        return html.P("No trending questions found.")
    
    table_data = []
    for i, question in enumerate(trending_data, 1):
        table_data.append({
            'Rank': i,
            'Category': question['category'],
            'Subcategory': question['subcategory'] or '-',
            'Question': question['question'][:100] + '...' if len(question['question']) > 100 else question['question'],
            'Asked': question['total_asked'],
            'Accuracy': f"{question['avg_accuracy']:.1f}%",
            'Avg Time': f"{question['avg_response_time']:.1f}s"
        })
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {"name": "#", "id": "Rank", "type": "numeric"},
            {"name": "Category", "id": "Category"},
            {"name": "Subcategory", "id": "Subcategory"},
            {"name": "Question", "id": "Question"},
            {"name": "Times Asked", "id": "Asked", "type": "numeric"},
            {"name": "Accuracy", "id": "Accuracy"},
            {"name": "Avg Time", "id": "Avg Time"}
        ],
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#fff3cd',
                'color': 'black',
                'fontWeight': 'bold'
            }
        ],
        page_size=10
    )

def create_leaderboard_table(leaderboard_data):
    """Create session leaderboard table."""
    if not leaderboard_data:
        return html.P("No completed sessions found for leaderboard.")
    
    table_data = []
    for i, session in enumerate(leaderboard_data, 1):
        table_data.append({
            'Rank': i,
            'Session Name': session['session_name'] or 'Unnamed Session',
            'User': session['user_id'] or 'Anonymous',
            'Questions': session['total_questions'],
            'Correct': session['correct_answers'],
            'Accuracy': f"{session['accuracy_rate']:.1f}%",
            'Avg Time': f"{session['avg_response_time']:.1f}s",
            'Date': utc_to_local_date_string(session['started_at'])
        })
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {"name": "#", "id": "Rank", "type": "numeric"},
            {"name": "Session Name", "id": "Session Name"},
            {"name": "User", "id": "User"},
            {"name": "Questions", "id": "Questions", "type": "numeric"},
            {"name": "Correct", "id": "Correct", "type": "numeric"},
            {"name": "Accuracy", "id": "Accuracy"},
            {"name": "Avg Time", "id": "Avg Time"},
            {"name": "Date", "id": "Date"}
        ],
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#d4edda',
                'color': 'black',
                'fontWeight': 'bold'
            },
            {
                'if': {'row_index': 1},
                'backgroundColor': '#f8d7da',
                'color': 'black',
                'fontWeight': 'bold'
            },
            {
                'if': {'row_index': 2},
                'backgroundColor': '#ffeaa7',
                'color': 'black',
                'fontWeight': 'bold'
            }
        ],
        page_size=10
    )
