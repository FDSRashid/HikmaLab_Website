
import reflex as rx
from ..backend.isnad_state import QueryIsnads, isnads
from .. import styles
from ..templates import template

@template(route="/fetch_isnads", title="About the team")
def test_isnads() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Enter hadith", 
            on_blur=QueryIsnads.set_hadith
        ),
        rx.input(
            placeholder="Enter taraf", 
            type_="number",
            on_blur=QueryIsnads.set_taraf
        ),
        rx.button(
            "Search by Hadith",
            on_click=QueryIsnads.get_isnads_hadith,
        ),
        rx.button(
            "Search by Taraf",
            on_click=QueryIsnads.get_isnads_taraf,
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Source"),
                    rx.table.column_header_cell("Destination"),
                    rx.table.column_header_cell("Hadith Count"),
                    rx.table.column_header_cell("Taraf Count"),
                    rx.table.column_header_cell("Book Count"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    QueryIsnads.edges,
                    lambda edge: rx.table.row(
                        rx.table.cell(edge.source),
                        rx.table.cell(edge.destination),
                        rx.table.cell(edge.hadith_count),
                        rx.table.cell(edge.taraf_count),
                        rx.table.cell(edge.book_count),
                    )
                )
            ),
        )
    )