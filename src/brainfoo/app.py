"""
Brainfoo is a TUI debugger for Brainfk written in Python, designed to be
keyboard and mouse friendly.
"""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Footer, Label, TextArea


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
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit", "Quit"),
                ("r", "run", "Run")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Footer()

        cell_grid: list[CellLine] = []
        for _ in range(50):
            cell_grid.append(CellLine())

        buttons: list[Button] = [
            Button("▶ RUN", classes="run_button", compact=True),
            Button("⬤ STOP", classes="stop_button", compact=True)
        ]
        yield HorizontalGroup(
            VerticalGroup(
                HorizontalGroup(*buttons),
                VerticalScroll(*cell_grid)
            ),
            BrainfkView("+++..>>[]>..<"),
            id="main_area"
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def action_quit(self) -> None:
        """Quit the app"""
        self.exit()

    def action_run(self) -> None:
        """Start execution of brainfk"""
        # To be implemented
