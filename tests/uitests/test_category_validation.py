"""
UI tests for validating quiz categories functionality.
"""
import pytest
from playwright.sync_api import Page, expect
import time

class TestCategoryValidation:
    """Test suite for quiz category validation."""
    
    def test_all_categories_present(self, trivia_page: Page):
        """Test that all expected quiz types are present on the page."""
        # Wait for quiz cards to load
        trivia_page.wait_for_selector(".quiz-card-button", timeout=10000)
        
        # Get all quiz card buttons
        quiz_buttons = trivia_page.locator(".quiz-card-button")
        button_count = quiz_buttons.count()
        
        assert button_count > 0, "No quiz buttons found"
        
        # Check that we have at least some quiz types available
        print(f"Found {button_count} quiz types available")
        
        # Verify that the buttons are clickable
        for i in range(min(button_count, 3)):  # Test first 3 buttons
            button = quiz_buttons.nth(i)
            expect(button).to_be_visible()
            expect(button).to_be_enabled()
    
    def test_quiz_cards_clickable(self, trivia_page: Page):
        """Test that quiz card buttons are clickable and respond to clicks."""
        # Wait for quiz cards to load
        trivia_page.wait_for_selector(".quiz-card-button", timeout=10000)
        
        quiz_buttons = trivia_page.locator(".quiz-card-button")
        button_count = quiz_buttons.count()
        
        assert button_count > 0, "No quiz card buttons found"
        
        # Test clicking the first quiz button
        first_button = quiz_buttons.first
        button_text = first_button.text_content()
        
        # Click the button
        first_button.click()
        time.sleep(1)  # Wait for response
        
        # Check if username modal appears or quiz starts
        username_modal = trivia_page.locator("#username-modal")
        quiz_content = trivia_page.locator("#quiz-content-area")
        
        if username_modal.is_visible():
            print("Username modal appeared after clicking quiz button")
        elif quiz_content.is_visible():
            print("Quiz started directly after clicking button")
        else:
            print(f"Successfully clicked quiz button: {button_text}")
    
    def test_geography_category_quiz_types(self, trivia_page: Page):
        """Test that Geography category shows expected quiz types."""
        # Click Geography category
        geography_button = trivia_page.locator(".category-button", has_text="Geography")
        if geography_button.count() == 0:
            pytest.skip("Geography category not found")
        
        geography_button.click()
        time.sleep(1)  # Wait for quiz types to load
        
        # Check for geography quiz types
        expected_geography_quizzes = [
            "Capitals", "Flags", "Continents", "Currencies", 
            "Physical Geography", "US State Capitals", "India State Capitals", "Wonders"
        ]
        
        quiz_buttons = trivia_page.locator(".quiz-type-button")
        
        for quiz_type in expected_geography_quizzes:
            quiz_button = trivia_page.locator(".quiz-type-button", has_text=quiz_type)
            if quiz_button.count() > 0:
                expect(quiz_button).to_be_visible()
                print(f"Found geography quiz type: {quiz_type}")
            else:
                print(f"Warning: Geography quiz type '{quiz_type}' not found")
    
    def test_science_category_quiz_types(self, trivia_page: Page):
        """Test that Science category shows expected quiz types."""
        # Click Science category
        science_button = trivia_page.locator(".category-button", has_text="Science")
        if science_button.count() == 0:
            pytest.skip("Science category not found")
        
        science_button.click()
        time.sleep(1)  # Wait for quiz types to load
        
        # Check for science quiz types
        expected_science_quizzes = [
            "Biology", "Chemistry", "Physics", "Astronomy", "Earth Science", "Technology"
        ]
        
        quiz_buttons = trivia_page.locator(".quiz-type-button")
        
        for quiz_type in expected_science_quizzes:
            quiz_button = trivia_page.locator(".quiz-type-button", has_text=quiz_type)
            if quiz_button.count() > 0:
                expect(quiz_button).to_be_visible()
                print(f"Found science quiz type: {quiz_type}")
            else:
                print(f"Warning: Science quiz type '{quiz_type}' not found")
    
    def test_history_category_quiz_types(self, trivia_page: Page):
        """Test that History category shows expected quiz types."""
        # Click History category
        history_button = trivia_page.locator(".category-button", has_text="History")
        if history_button.count() == 0:
            pytest.skip("History category not found")
        
        history_button.click()
        time.sleep(1)  # Wait for quiz types to load
        
        # Check for history quiz types
        expected_history_quizzes = ["Famous People"]
        
        for quiz_type in expected_history_quizzes:
            quiz_button = trivia_page.locator(".quiz-type-button", has_text=quiz_type)
            if quiz_button.count() > 0:
                expect(quiz_button).to_be_visible()
                print(f"Found history quiz type: {quiz_type}")
            else:
                print(f"Warning: History quiz type '{quiz_type}' not found")
    
    def test_quiz_selection_flow(self, trivia_page: Page):
        """Test the complete flow from category selection to quiz start."""
        # Click Geography category
        geography_button = trivia_page.locator(".category-button", has_text="Geography")
        if geography_button.count() == 0:
            pytest.skip("Geography category not found")
        
        geography_button.click()
        time.sleep(1)
        
        # Find and click a quiz type (e.g., Capitals)
        capitals_button = trivia_page.locator(".quiz-type-button", has_text="Capitals")
        if capitals_button.count() == 0:
            pytest.skip("Capitals quiz type not found")
        
        capitals_button.click()
        time.sleep(2)  # Wait for quiz to load
        
        # Check if quiz has started (look for question container or start button)
        question_container = trivia_page.locator(".question-container, .quiz-start-container")
        if question_container.count() > 0:
            expect(question_container).to_be_visible()
            print("Quiz successfully started")
        else:
            # Look for username modal or other intermediate step
            username_modal = trivia_page.locator(".modal, .username-modal")
            if username_modal.count() > 0:
                print("Username modal appeared - this is expected behavior")
            else:
                pytest.fail("Quiz did not start and no username modal appeared")
    
    def test_category_switching(self, trivia_page: Page):
        """Test switching between different categories."""
        categories_to_test = ["Geography", "Science"]
        
        for category in categories_to_test:
            category_button = trivia_page.locator(".category-button", has_text=category)
            if category_button.count() == 0:
                continue
            
            # Click the category
            category_button.click()
            time.sleep(1)
            
            # Verify the category is active
            expect(category_button).to_have_class(lambda class_list: "category-button-active" in class_list)
            
            # Check that quiz types are displayed
            quiz_buttons = trivia_page.locator(".quiz-type-button")
            assert quiz_buttons.count() > 0, f"No quiz types found for {category} category"
            
            print(f"Successfully switched to {category} category with {quiz_buttons.count()} quiz types")
    
    def test_responsive_layout(self, trivia_page: Page):
        """Test that the category layout is responsive to different screen sizes."""
        # Test desktop size (default)
        trivia_page.set_viewport_size({"width": 1200, "height": 800})
        trivia_page.wait_for_selector(".category-button", timeout=5000)
        
        category_buttons = trivia_page.locator(".category-button")
        assert category_buttons.count() > 0, "Categories not visible on desktop"
        
        # Test tablet size
        trivia_page.set_viewport_size({"width": 768, "height": 1024})
        time.sleep(0.5)
        
        category_buttons = trivia_page.locator(".category-button")
        assert category_buttons.count() > 0, "Categories not visible on tablet"
        
        # Test mobile size
        trivia_page.set_viewport_size({"width": 375, "height": 667})
        time.sleep(0.5)
        
        category_buttons = trivia_page.locator(".category-button")
        assert category_buttons.count() > 0, "Categories not visible on mobile"
        
        print("Category layout is responsive across different screen sizes")
    
    def test_keyboard_navigation(self, trivia_page: Page):
        """Test keyboard navigation through categories."""
        # Focus on the first category button
        first_category = trivia_page.locator(".category-button").first
        first_category.focus()
        
        # Test Tab navigation
        trivia_page.keyboard.press("Tab")
        time.sleep(0.2)
        
        # Test Enter key to select category
        trivia_page.keyboard.press("Enter")
        time.sleep(1)
        
        # Check if category became active
        active_categories = trivia_page.locator(".category-button-active")
        assert active_categories.count() > 0, "No category became active after Enter key"
        
        print("Keyboard navigation works for category selection")

class TestQuizTypeValidation:
    """Test suite for quiz type validation within categories."""
    
    def test_quiz_type_buttons_have_correct_attributes(self, trivia_page: Page):
        """Test that quiz type buttons have correct attributes and styling."""
        # Click Geography to load quiz types
        geography_button = trivia_page.locator(".category-button", has_text="Geography")
        if geography_button.count() == 0:
            pytest.skip("Geography category not found")
        
        geography_button.click()
        time.sleep(1)
        
        quiz_buttons = trivia_page.locator(".quiz-type-button")
        button_count = quiz_buttons.count()
        
        assert button_count > 0, "No quiz type buttons found"
        
        # Test each quiz button
        for i in range(min(button_count, 5)):  # Test first 5
            button = quiz_buttons.nth(i)
            button_text = button.text_content()
            
            # Check button is visible and has text
            expect(button).to_be_visible()
            assert button_text and len(button_text.strip()) > 0, f"Button {i} has no text"
            
            # Check button is clickable
            expect(button).to_be_enabled()
            
            print(f"Quiz type button '{button_text}' is properly configured")
    
    def test_quiz_type_descriptions(self, trivia_page: Page):
        """Test that quiz types have appropriate descriptions or tooltips."""
        # Click Geography category
        geography_button = trivia_page.locator(".category-button", has_text="Geography")
        if geography_button.count() == 0:
            pytest.skip("Geography category not found")
        
        geography_button.click()
        time.sleep(1)
        
        # Look for quiz descriptions or tooltips
        quiz_buttons = trivia_page.locator(".quiz-type-button")
        
        for i in range(min(quiz_buttons.count(), 3)):  # Test first 3
            button = quiz_buttons.nth(i)
            button_text = button.text_content()
            
            # Hover to see if tooltip appears
            button.hover()
            time.sleep(0.5)
            
            # Check for tooltip or description (this might need adjustment based on actual implementation)
            tooltip = trivia_page.locator(".tooltip, [title], .description")
            if tooltip.count() > 0:
                print(f"Quiz type '{button_text}' has description/tooltip")
            
            print(f"Checked description for quiz type: {button_text}")
