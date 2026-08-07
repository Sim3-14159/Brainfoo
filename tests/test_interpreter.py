import pytest
from brainfoo.errors import BrainfkError, CellUnderflowError
from brainfoo.interpreter import BrainfkInterpreter

def test_interpret_hello_world():
    """Verifies that the engine correctly produces output."""
    # Example Brainfk hello world snippet
    interpreter = BrainfkInterpreter("++++++++++[>+++++++>++++++++++>+++>+<<<<-" +
        "]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
    result = ''.join([item for item in interpreter.run()])
    assert result == "Hello World!\n"

def test_data_pointer_bounds():
    """Ensures tape boundaries throw expected errors or wrap correctly."""
    with pytest.raises(CellUnderflowError):
        BrainfkInterpreter("<").run()  # Assuming moving left of zero faults

