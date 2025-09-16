# UI Tests with Playwright

This directory contains end-to-end UI tests for the Interactive Map application using Playwright and pytest.

## Setup and Installation

### 1. Install Test Dependencies

First, install the test dependencies:

```bash
# Option 1: Install test dependencies (recommended)
pip install -e ".[test]"

# Option 2: If using uv and the above works:
uv pip install -e ".[test]"

# Option 3: If you get package discovery errors, install dependencies directly:
pip install pytest>=7.0.0 pytest-playwright>=0.4.0 playwright>=1.40.0 pytest-asyncio>=0.21.0

# Option 4: Using uv directly:
uv pip install pytest>=7.0.0 pytest-playwright>=0.4.0 playwright>=1.40.0 pytest-asyncio>=0.21.0
```

### 2. Install Playwright Browsers

After installing the packages, install the Playwright browsers:

```bash
playwright install chromium
```

Or install all browsers (optional):

```bash
playwright install
```

## Running Tests

### Run All UI Tests

```bash
# Run all UI tests
pytest tests/uitests/

# Run with verbose output
pytest tests/uitests/ -v

# Run with playwright output
pytest tests/uitests/ -s
```

### Run Specific Test Files

```bash
# Run only category validation tests
pytest tests/uitests/test_category_validation.py

# Run specific test method
pytest tests/uitests/test_category_validation.py::TestCategoryValidation::test_all_categories_present
```

### Run Tests with Visual Browser (for debugging)

To see the tests running in a browser window, modify the `conftest.py` file and change:

```python
browser = p.chromium.launch(headless=False)  # Set headless=False
```

Then run:

```bash
pytest tests/uitests/ -s --headed
```

### Generate Test Reports

```bash
# Generate HTML report
pytest tests/uitests/ --html=test-reports/ui-tests.html --self-contained-html

# Generate JUnit XML report
pytest tests/uitests/ --junitxml=test-reports/ui-tests.xml
```

## Test Structure

### Files Overview

- **`conftest.py`**: Contains pytest fixtures and configuration
- **`test_category_validation.py`**: Tests for quiz category functionality
- **`playwright.config.py`**: Playwright-specific configuration
- **`__init__.py`**: Python package initialization

### Test Categories

1. **Category Validation Tests**
   - Presence of all expected categories
   - Category button functionality
   - Category switching behavior
   - Responsive layout testing

2. **Quiz Type Validation Tests**
   - Quiz type buttons within each category
   - Quiz selection flow
   - Button attributes and accessibility

### Test Fixtures

- **`dash_app`**: Starts the Dash application on port 8051 for testing
- **`playwright_browser`**: Provides a Playwright browser instance
- **`page`**: Provides a clean browser page for each test
- **`trivia_page`**: Navigates directly to the trivia page

## Writing New Tests

### Basic Test Structure

```python
def test_example(trivia_page: Page):
    """Test description."""
    # Wait for elements to load
    trivia_page.wait_for_selector(".selector", timeout=10000)
    
    # Interact with elements
    button = trivia_page.locator(".button")
    button.click()
    
    # Assert expectations
    expect(button).to_have_class("active")
```

### Common Patterns

#### Waiting for Elements

```python
# Wait for element to be visible
page.wait_for_selector(".element", timeout=10000)

# Wait for element to be hidden
page.wait_for_selector(".element", state="hidden")

# Wait for network response
page.wait_for_response("**/api/**")
```

#### Element Interaction

```python
# Click element
page.locator(".button").click()

# Type text
page.locator("input").fill("text")

# Select dropdown
page.locator("select").select_option("value")

# Hover
page.locator(".element").hover()
```

#### Assertions

```python
# Element visibility
expect(page.locator(".element")).to_be_visible()

# Text content
expect(page.locator(".element")).to_have_text("Expected text")

# CSS class
expect(page.locator(".element")).to_have_class("class-name")

# Count
expect(page.locator(".elements")).to_have_count(5)
```

## Debugging Tests

### Screenshots on Failure

Tests are configured to take screenshots on failure. Screenshots will be saved in `test-results/` directory.

### Video Recording

Test runs are recorded (on failure) and saved in `test-results/` directory.

### Debug Mode

To debug tests interactively:

```python
# Add this to your test
page.pause()  # Opens Playwright Inspector
```

### Verbose Logging

```bash
# Enable debug logging
pytest tests/uitests/ --log-cli-level=DEBUG
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: UI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
          playwright install chromium
      
      - name: Run UI tests
        run: pytest tests/uitests/ --html=ui-test-report.html
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: ui-test-results
          path: |
            ui-test-report.html
            test-results/
```

## Best Practices

1. **Wait Strategies**: Always wait for elements to be ready before interacting
2. **Stable Selectors**: Use stable CSS classes or data attributes for element selection
3. **Test Independence**: Each test should be independent and not rely on others
4. **Clean State**: Use fixtures to ensure clean state for each test
5. **Meaningful Names**: Use descriptive test and method names
6. **Error Handling**: Handle expected errors gracefully with proper assertions

## Troubleshooting

### Common Issues

1. **Port Conflicts**: If port 8051 is in use, modify `TEST_APP_PORT` in `conftest.py`
2. **Timeout Errors**: Increase timeout values if your app takes longer to load
3. **Element Not Found**: Check CSS selectors match your actual application
4. **Browser Installation**: Ensure Playwright browsers are installed correctly

### Performance Tips

1. Use `headless=True` for faster test execution
2. Implement smart waiting strategies instead of fixed sleeps
3. Run tests in parallel with `pytest-xdist` for better performance

## Extending Tests

To add new test categories:

1. Create new test file: `test_new_category.py`
2. Import required fixtures from `conftest.py`
3. Follow existing test patterns
4. Add specific selectors and assertions for new functionality

Example:

```python
def test_new_functionality(trivia_page: Page):
    """Test new functionality."""
    # Your test implementation
    pass
