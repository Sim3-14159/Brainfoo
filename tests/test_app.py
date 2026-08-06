'''
import pytest
from brainfoo.app import BrainfooApp

@pytest.mark.asyncio
async def test_app_startup():
    """Tests that the primary application interface boots up without crashing."""
    app = BrainfooApp()
    async with app.run_test() as pilot:
        # Asserts the initial UI state or terminal view is active
        assert app.title == "Brainfoo"
        await pilot.press("q")  # Tests exit hotkey behavior
'''
