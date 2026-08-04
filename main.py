from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header, Label, TextArea
import sys


class Cell(Label):
    """A widget to display the value of a cell in memory."""


class CellLine(HorizontalGroup):
    """A cell widget."""

    def compose(self) -> ComposeResult:
        """Create a single line of cells"""

        for x in range(10):
            yield Cell("000", variant="cell_label")


class BrainfkView(TextArea):
    """The area where Brainfk will be displayed"""


class BrainfooApp(App):
    """The main Brainfoo app"""

    CSS_PATH = "style.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit", "Quit"),
                ("r", "run", "Run")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        
        cellGrid: list[CellLine] = []
        for _ in range(50):
            cellGrid.append(CellLine())
        
        yield Button("Run", classes="run_button")
        yield HorizontalGroup(
            VerticalScroll(*cellGrid),
            BrainfkView("+++..>>[]>..<"),
            id="main_area"
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit(self) -> None:
        """Quit the app"""
        self.exit()

    def action_run(self) -> None:
        """Start execution of brainfk"""
        ...


if __name__ == "__main__":
    app = BrainfooApp()
    app.run()
