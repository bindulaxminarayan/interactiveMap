"""
Pytest configuration and fixtures for UI tests.
"""
import pytest
import time
import requests
from playwright.sync_api import sync_playwright
import threading
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Test configuration
TEST_APP_PORT = 8051
TEST_APP_URL = f"http://localhost:{TEST_APP_PORT}"

class DashAppServer:
    """Helper class to manage the Dash app server during tests."""
    
    def __init__(self, port=TEST_APP_PORT):
        self.port = port
        self.process = None
        self.thread = None
    
    def start(self):
        """Start the Dash app in a separate process."""
        import app  # Import your main app module
        
        def run_app():
            # Use the app instance directly and run on the test port
            app.app.run(debug=False, port=self.port, host='127.0.0.1', threaded=True)
        
        self.thread = threading.Thread(target=run_app, daemon=True)
        self.thread.start()
        
        # Wait for the server to start
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(TEST_APP_URL, timeout=2)
                if response.status_code == 200:
                    print(f"Test server started successfully on {TEST_APP_URL}")
                    return
            except requests.exceptions.RequestException as e:
                if i < 5:  # Only print first few attempts to avoid spam
                    print(f"Attempt {i+1}: Server not ready yet - {e}")
                pass
            time.sleep(1)
        
        raise RuntimeError(f"Failed to start Dash app on port {self.port} after {max_retries} attempts")
    
    def stop(self):
        """Stop the Dash app server."""
        # Since we're using threading, the server will stop when the main process ends
        pass

@pytest.fixture(scope="session")
def dash_app():
    """Fixture to start and stop the Dash app for testing."""
    server = DashAppServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope="session")
def playwright_browser():
    """Fixture to provide a Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False for debugging
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_browser, dash_app):
    """Fixture to provide a new page for each test."""
    context = playwright_browser.new_context()
    page = context.new_page()
    
    # Navigate to the app
    page.goto(TEST_APP_URL)
    
    # Wait for the app to load
    page.wait_for_selector("body", timeout=10000)
    
    yield page
    
    context.close()

@pytest.fixture(scope="function")
def trivia_page(page):
    """Fixture to navigate to the trivia page."""
    # Navigate to trivia page
    page.goto(f"{TEST_APP_URL}/trivia")
    
    # Wait for the trivia page to load (wait for the quiz cards grid)
    page.wait_for_selector(".quiz-cards-grid-container-inner", timeout=10000)
    
    yield page
