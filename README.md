# QuizVerse

A comprehensive learning platform built with Dash and Plotly, featuring interactive world map exploration, diverse quiz categories, and advanced analytics for tracking learning progress.

## Features

### Core Features
- **Interactive World Map**: Visualize country data with hover information and GDP highlighting
- **Comprehensive Quiz System**: Multiple quiz categories with session tracking and analytics
- **Analytics Dashboard**: Advanced performance tracking with charts, leaderboards, and statistics
- **Database-Driven**: Normalized SQLite database with efficient data management

### Quiz Categories

#### Geography Quizzes
Complete geography challenges with 8 quiz types:
- **Physical Geography**: Landscapes, mountain ranges, natural features
- **Wonders**: Famous landmarks and natural wonders
- **Flags**: Match flags with countries
- **Currencies**: Match countries with their currencies  
- **World Capitals**: Match countries with capital cities
- **Continents**: Match countries with their continents
- **India State Capitals**: Match Indian states with capitals
- **US State Capitals**: Match US states with capitals
#### History Quizzes
- **Leaders**: Famous leaders, influencers
#### Science Quizzes
- **Biology**: Life sciences and living organisms
- **Chemistry**: Elements and Chemical Reactions

#### Coming Soon
- **Sports Quizzes**: Sports facts, records, and trivia

### Analytics & Performance Tracking

#### Dashboard Features
- **📊 Real-time Analytics**: Live performance tracking and statistics
- **📈 Daily Performance Trends**: Track progress over time with interactive charts
- **📚 Category Performance**: Compare accuracy across different quiz categories
- **🕐 Recent Sessions**: Monitor latest quiz attempts with detailed information
- **🔥 Trending Questions**: Identify most challenging and popular questions
- **🏆 Leaderboards**: Session rankings based on accuracy and speed

#### Statistics Tracked
- **Question-Level Stats**: Times asked, accuracy rates, response times
- **Daily Aggregations**: Questions answered, overall accuracy, average response time
- **Session Analytics**: Complete session tracking with user identification
- **Category Performance**: Performance breakdown by quiz category
- **Historical Data**: Weekly rollover with long-term trend analysis

### Technical Features

#### Database & Storage
- **Normalized SQLite Database**: Efficient relational structure with proper foreign keys
- **UTC Timestamp Storage**: Consistent timezone handling with local display conversion
- **Automated Rollover**: Weekly aggregation of statistics with cleanup of old data
- **Session Management**: Complete quiz session lifecycle tracking

#### User Experience
- **Responsive Design**: Clean, modern interface with CSS-based styling
- **Username Support**: Personalized quiz sessions with user identification
- **Progress Tracking**: Real-time progress bars and session feedback
- **Timezone Awareness**: UTC storage with local timezone display
- **Auto-refresh**: Live updating analytics dashboard

## Prerequisites

- **For Docker**: Docker installed on your system
- **For Local Development**: Python 3.13+ and [uv](https://docs.astral.sh/uv/) package manager

## Installation & Setup

### Option 1: Using Docker (Recommended)

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd interactiveMap
```

#### Step 2: Build the Docker Image
```bash
docker build -t interactive-map .
```

#### Step 3: Run the Docker Container
```bash
docker run -p 8050:8050 interactive-map
```

#### Step 4: Access the Application
Open your browser and navigate to: http://localhost:8050

### Option 2: Using UV (Local Development)

#### Step 1: Install UV
If you don't have uv installed, install it first:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

#### Step 2: Clone the Repository
```bash
git clone <repository-url>
cd interactiveMap
```

#### Step 3: Sync Dependencies
```bash
uv sync
```

#### Step 4: Run the Application
```bash
uv run app.py
```

#### Step 5: Access the Application
Open your browser and navigate to: http://127.0.0.1:8050

## Usage Guide

### Taking Quizzes
1. **Navigate** to any quiz category from the navigation bar
2. **Enter Username** when prompted (or use anonymous mode)
3. **Select Quiz Type** from the available options
4. **Answer Questions** with immediate feedback and explanations
5. **View Results** with detailed performance breakdown
6. **Restart or Return** to try different quizzes

### Analytics Dashboard
1. **Access Analytics** from the navigation menu
2. **View Today's Stats** in the summary cards
3. **Explore Charts** for performance trends and category comparisons
4. **Check Tables** for recent sessions, trending questions, and leaderboards
5. **Filter Date Range** to analyze specific time periods
6. **Auto-Refresh** for real-time updates

### Database Management
The application includes utilities for database management:
- **Database Creation**: Automated normalized database setup
- **Data Import**: CSV to SQLite conversion utilities
- **Cleanup Tools**: Remove old data and optimize performance
- **Statistics Rollover**: Weekly aggregation for long-term analysis

## Testing

QuizVerse includes comprehensive testing to ensure reliability and functionality.

### Unit Tests
Located in `tests/unit/`, these tests cover core functionality:
```bash
# Run unit tests
pytest tests/unit/

# Run with coverage
pytest tests/unit/ --cov=utils --cov=components
```

### UI Tests (End-to-End)
Located in `tests/uitests/`, these Playwright-based tests validate the user interface:

#### Setup UI Tests
```bash
# Install test dependencies (try these options in order)
pip install -e ".[test]"

# If you get package discovery errors, install directly:
pip install pytest>=7.0.0 pytest-playwright>=0.4.0 playwright>=1.40.0 pytest-asyncio>=0.21.0

# Install Playwright browsers
playwright install chromium
```

#### Run UI Tests
```bash
# Run all UI tests
pytest tests/uitests/

# Run with our helper script
python tests/uitests/run_tests.py

# Run with visible browser (for debugging)
python tests/uitests/run_tests.py --headful --verbose

# Run only category validation tests
python tests/uitests/run_tests.py --category

# Generate HTML report
python tests/uitests/run_tests.py --report
```

#### UI Test Coverage
- **Category Validation**: Quiz category presence and functionality
- **Quiz Type Testing**: Validation of quiz types within each category  
- **User Interaction Flow**: Complete quiz selection and start process
- **Responsive Design**: Testing across different screen sizes
- **Keyboard Navigation**: Accessibility and keyboard interaction
- **Error Handling**: Graceful handling of edge cases

For detailed UI testing information, see [`tests/uitests/README.md`](tests/uitests/README.md).
