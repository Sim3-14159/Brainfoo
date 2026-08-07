import pytest
from brainfoo.errors import BrainfkError, CellUnderflowError
from brainfoo.interpreter import BrainfkInterpreter

def test_interpret_hello_world():
    """Verifies that the engine correctly produces output."""
    # Example Brainfk hello world snippet
    interpreter = BrainfkInterpreter(code="++++++++++[>+++++++>++++++++++>+++>+<<<<-" +
        "]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
    result = ''.join(list(interpreter.run()))
    assert result == "Hello World!\n"

def test_data_pointer_bounds():
    """Ensures tape boundaries throw expected errors or wrap correctly."""
    with pytest.raises(CellUnderflowError):
        next(BrainfkInterpreter(code="<").run())  # Assuming moving left of zero faults

