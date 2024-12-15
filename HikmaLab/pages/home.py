"""The home page."""

from ..templates import template
from ..backend.table_state import TableState
from ..views.table import main_table

import reflex as rx


@template(route="/", title="Home")
def home() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page. 
    """
    return rx.container(
        rx.vstack(
            rx.heading("Welcome to Hikma Lab!", size="9"),
            rx.text(
                "At the Intersection of Tradition and Technology...",
                size="5",
            ),
            rx.link(
                rx.button("Learn more!"),
                href="/about",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )

