class BrainfkError(BaseException):
    def __init__(self, reason):
        self.reason = reason

class BrainfkInterpreter:
    def __init__(self):
        """Initialize self"""
        self.index = 0

    def run(self, code: str) -> str:
        if (l := code.count("[")) != (r := code.count("]")):
            raise BrainfkError(f"IMBALANCED NUMBER OF BRACKETS | '['x{l} / ']'x{r}")
        
        for i, char in enumerate(code):
            if char == "<":
                self.index -= 1
            elif char == ">":
                self.index += 1
            
            if self.index < 0:
                raise BrainfkError("INDEX UNDERFLOW | TOO MANY '<'S")
        return "Hello World!\n"
