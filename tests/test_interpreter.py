import pytest
from brainfoo.interpreter import BrainfkInterpreter, BrainfkError

@pytest.fixture
def interpreter():
    """Initializes a fresh interpreter instance before each test."""
    return BrainfkInterpreter()

def test_interpret_hello_world(interpreter):
    """Verifies that the engine correctly produces output."""
    # Example Brainfk hello world snippet
    code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
    result = interpreter.run(code)
    assert result == "Hello World!\n"

def test_data_pointer_bounds(interpreter):
    """Ensures tape boundaries throw expected errors or wrap correctly."""
    with pytest.raises(BrainfkError):
        interpreter.run("<")  # Assuming moving left of zero faults

