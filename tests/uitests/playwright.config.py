"""
Playwright configuration for UI tests.
"""
from playwright.sync_api import Playwright

def pytest_configure_playwright(playwright: Playwright):
    """Configure Playwright for tests."""
    return {
        'browser_name': 'chromium',
        'headless': True,
        'viewport': {'width': 1280, 'height': 720},
        'video': 'retain-on-failure',
        'screenshot': 'only-on-failure',
        'trace': 'retain-on-failure',
    }
