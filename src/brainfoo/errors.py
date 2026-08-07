"""
Brainfk Errors
"""

class BrainfkError(Exception):
    """Custom error class for exceptions in Brainfk execution"""
    NAME = "ERROR"

    def __init__(self, reason: str, row: int | None = None, col: int | None = None):
        """Initialize self and representation"""
        self.reason = reason
        self.row = row
        self.col = col


    def __str__(self) -> str:
        """Return str representation for when `raise` is called"""

        message = f"{type(self).NAME}: {self.reason}"

        if self.row is not None:
            message += f" | line {self.row}"
            if self.col is not None:
                message += f", column {self.col}"

        return message


class ImbalancedBracketError(BrainfkError):
    """Error for imbalanced brackets in Brainfk source"""
    NAME = "IMBALANCED BRACKET ERROR"

class CellUnderflowError(BrainfkError):
    """Error for an underflow of cells, where cell_index = 0 and the user tries to execute `<`"""
    NAME = "CELL UNDERFLOW ERROR"

class CellOverflowError(BrainfkError):
    """
    Error for an overflow of cells, where cell_index = CELL_ARRAY_LENGTH - 1 
    and the user tries to execute `>`
    """
    NAME = "CELL UNDERFLOW ERROR"
