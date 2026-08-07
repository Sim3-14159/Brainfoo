"""
Brainfk interpreter
"""

import ctypes
from pathlib import Path
from brainfoo.errors import BrainfkError, ImbalancedBracketError, CellUnderflowError


class BrainfkInterpreter:
    """Brainfk interpreter/debugger"""
    def __init__(self, file: str | Path | None = None, code: str | None = None, 
                 stdin=None, tick_callback=None):
        """Initialize self

        MUST HAVE `file` or `code`
        file: file object to read from
        code: str object to execute"""

        self.cell_index = 0
        self.instruction_index = 0
        self.cells = (ctypes.c_ubyte * 30000)()
        self.stdin = stdin
        self.tick_callback = tick_callback

        # must have file or code
        assert file is not None or code is not None

        if code is None:
            try:
                code = open(file).read()
            except FileNotFoundError:
                self.code = f"ERROR: FILE \"{file}\" NOT FOUND"
            except PermissionError:
                self.code = f"ERROR: PERMISSION DENIED TO \"{file}\""
            except:
                self.code = "ERROR: CANNOT OPEN \"{file}\""
        else:
            self.code = code


    def run(self) -> None:
        """Run Brainfk code"""
        if (l := self.code.count("[")) != (r := self.code.count("]")):
            raise ImbalancedBracketError(f"IMBALANCED NUMBER OF BRACKETS ('['x{l} / ']'x{r})")

        # Keep going as long as there are potential instructions left
        while self.instruction_index < len(self.code):
            instruction = self.code[self.instruction_index]
            match instruction:
                case ">":
                    self.cell_index += 1
                case "<":
                    self.cell_index -= 1
                    if self.cell_index < 0:
                        raise CellUnderflowError("TRIED TO MOVE LEFT ('<') WHEN IN CELL #0")
                case "+":
                    self.cells[self.cell_index] += 1
                case "-":
                    self.cells[self.cell_index] -= 1
                case ".":
                    yield chr(self.cells[self.cell_index])
                case ",":
                    # read from provided stdin widget if available
                    if self.stdin and getattr(self.stdin, 'bytes', None):
                        self.cells[self.cell_index] = self.stdin.bytes.pop(0)
                        if hasattr(self.stdin, 'refresh'):
                            self.stdin.refresh()
                    else:
                        yield True
                        self.cells[self.cell_index] = self.stdin.bytes.pop(0)
                case "[":
                    if self.cells[self.cell_index] == 0:
                        self.instruction_index = self.find_bracket_match(self.instruction_index,
                                                                         True)
                case "]":
                    if self.cells[self.cell_index] != 0:
                        self.instruction_index = self.find_bracket_match(self.instruction_index,
                                                                         False)

            # notify UI about the current cell after handling the instruction
            if getattr(self, 'tick_callback', None):
                try:
                    self.tick_callback(self.cell_index, int(self.cells[self.cell_index]))
                except Exception:
                    pass

            self.instruction_index += 1


    def find_bracket_match(self, start: int, forward: bool) -> int:
        """Find bracket match in Brainfk source code. `forwards` is whether to go forwards or backwards 
        searching for a ']' or '[', respectively
        """

        direction = 1 if forward else -1
        in_between_brackets = 0
        location = start + direction
        start_bracket = "[" if forward else "]"
        end_bracket = "]" if forward else "["

        while 0 <= location < len(self.code):
            if self.code[location] == end_bracket:
                if in_between_brackets == 0:
                    return location
                in_between_brackets -= 1
            elif self.code[location] == start_bracket:
                in_between_brackets += 1
            location += direction

        # Didn't find a match
        return start


    @staticmethod
    def _clean(code):
        new = ''
        for char in code:
            if char in "<>[]-+.,":
                new += char
        return new
