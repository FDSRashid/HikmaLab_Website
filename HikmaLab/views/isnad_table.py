import reflex as rx
from ..backend.isnad_state import QueryIsnads, isnads
from ..components.status_badge import status_badge




def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: isnads, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.source),
        rx.table.cell(item.destination),
        rx.table.cell(item.hadith_count),
        rx.table.cell(item.taraf_count),
        rx.table.cell(item.book_count),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(QueryIsnads.page_number),
                f" of {QueryIsnads.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=QueryIsnads.first_page,
                    opacity=rx.cond(QueryIsnads.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(QueryIsnads.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=QueryIsnads.prev_page,
                    opacity=rx.cond(QueryIsnads.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(QueryIsnads.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=QueryIsnads.next_page,
                    opacity=rx.cond(
                        QueryIsnads.page_number == QueryIsnads.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        QueryIsnads.page_number == QueryIsnads.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=QueryIsnads.last_page,
                    opacity=rx.cond(
                        QueryIsnads.page_number == QueryIsnads.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        QueryIsnads.page_number == QueryIsnads.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )


def isnads_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                rx.cond(
                    QueryIsnads.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=QueryIsnads.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=QueryIsnads.toggle_sort,
                    ),
                ),
                rx.select(
                    [
                        "source",
                        "destination",
                        "hadith_count",
                        "taraf_count",
                        "book_count",
                    ],
                    placeholder="Sort By: source",
                    size="3",
                    on_change=QueryIsnads.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=QueryIsnads.setvar("search_value", ""),
                        display=rx.cond(QueryIsnads.search_value, "flex", "none"),
                    ),
                    value=QueryIsnads.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=QueryIsnads.set_search_value,
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Source", "route"),
                    _header_cell("Destination", "list-checks"),
                    _header_cell("Hadith Count", "notebook-pen"),
                    _header_cell("Taraf Count", "calendar"),
                    _header_cell("Book Count", "clock"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    QueryIsnads.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )
