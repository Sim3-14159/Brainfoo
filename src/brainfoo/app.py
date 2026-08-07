"""
Brainfoo is a TUI debugger for Brainfk written in Python, designed to be
keyboard and mouse friendly.
"""

from pathlib import Path
import ctypes
import asyncio

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Footer, Label, TextArea, Static
from textual.widget import Widget

from brainfoo.interpreter import BrainfkInterpreter


class CharInput(Widget):
    """Custom widget for getting a single character input"""
    can_focus = True

    def __init__(self):
        super().__init__()
        self.bytes = []

    def on_key(self, event) -> None:
        """React to when a single key is pressed"""
        # Ignore control keys
        if event.is_printable:
            # store the character's byte value (ctypes to allow wraparound)
            self.bytes.append(ctypes.c_ubyte(ord(event.character)).value)
        
        elif event.name == "backspace":
            if self.bytes:
                self.bytes.pop(-1)

        self.refresh()


    def render(self) -> str:
        if self.bytes == []:
            self.styles.color = "gray"
            return "Program stdin"
        else:
            self.styles.color = "white"
            return ''.join([chr(byte) for byte in self.bytes])


class Cell(Label):
    """A widget to display the value of a cell in memory."""


class CellLine(HorizontalGroup):
    """A cell widget."""

    def compose(self) -> ComposeResult:
        """Create a single line of cells"""

        for _ in range(10):
            yield Cell("000", variant="cell_label")


class BrainfkView(TextArea):
    """The area where Brainfk will be displayed"""


class BrainfooApp(App):
    """The main Brainfoo app"""

    CSS_PATH = Path(__file__).parent / "assets" / "style.css"
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode"),
                ("ctrl+q", "quit", "Quit"),
                ("ctrl+r", "run", "Run")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.char_input = CharInput()
        self.bf_view = BrainfkView("+++++++++++++++++++++++++++...>++++[<+>-]..")
        self.output_view = TextArea(placeholder="Program output")

        yield Footer()

        # build a 50x10 grid of Cell widgets and keep references for updates
        self.cell_widgets: list[list[Cell]] = []
        row_groups: list[HorizontalGroup] = []
        for _ in range(50):
            row_cells: list[Cell] = []
            for _ in range(10):
                cell = Cell("000", variant="cell_label")
                row_cells.append(cell)
            self.cell_widgets.append(row_cells)
            row_groups.append(HorizontalGroup(*row_cells))

        # keep a reference to the run button so its label can be updated while running
        self.run_button = Button("▶ RUN", classes="run_button")
        self.stop_button = Button("⬤ STOP", classes="stop_button")

        header: list[Button | CharInput] = [
            self.run_button,
            self.stop_button,
            self.char_input
        ]
        yield HorizontalGroup(
            VerticalGroup(
                HorizontalGroup(*header),
                VerticalScroll(*row_groups),
                classes="side_group"
            ),
            VerticalGroup(self.bf_view, self.output_view),
            id="main_area"
        )

    def _on_tick(self, cell_index: int, value: int) -> None:
        """Update the visible cell widgets with the current cell value."""
        row = cell_index // 10
        col = cell_index % 10
        if 0 <= row < len(self.cell_widgets):
            self.cell_widgets[row][col].update(f"{int(value):03d}")
            self.cell_widgets[row][col].refresh()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def action_quit(self) -> None:
        """Quit the app"""
        self.exit()

    async def action_run(self) -> None:
        """Start execution of brainfk"""
        # indicate running by changing the Run button to Pause
        self.run_button.label = "⏸ PAUSE"
        self.run_button.refresh()

        # yield once to let the UI update the button state before running
        await asyncio.sleep(0)

        interpreter = BrainfkInterpreter(code=self.bf_view.text, stdin=self.char_input, tick_callback=self._on_tick)
        waiting_for_input = False
        for out_char in interpreter.run():
            if out_char != True:
                self.output_view.text += out_char
            else:
                self.char_input.placeholder = "Waiting..."
                waiting_for_input = True

            while waiting_for_input:
                await asyncio.sleep(0.1)
                if self.char_input.bytes:
                    waiting_for_input = False
            self.output_view.refresh()
            # yield briefly so UI (output + cell grid) can refresh during long runs
            await asyncio.sleep(0)

        # restore the Run button label
        self.run_button.label = "▶ RUN"
        self.run_button.refresh()
