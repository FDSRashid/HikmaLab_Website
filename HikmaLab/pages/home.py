"""The home page."""

from ..templates import template
from ..templates.template import ThemeState
import reflex as rx
from reflex_type_animation import type_animation
from .. import styles
from ..components.navbar import navbar       

@rx.page(route="/", title="Home")
def home() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page. 
    """

    return  rx.theme(rx.flex(
                navbar(),
                rx.flex(
                    rx.vstack(
                        rx.vstack(
            rx.heading("Welcome to Hikma Lab!", size="9"),
            type_animation(sequence=[
                "At the Intersection of Technology and Tradition...",
                1000 # waits 1 second before next word
            ]),
            rx.link(
                rx.button("Learn more!"),
                href="/about",
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        ),
                        width="100%",
                        **styles.template_content_style,
                        align="center",
                    ),
                    width="100%",
                    **styles.template_page_style,
                    max_width=[
                        "100%",
                        "100%",
                        "100%",
                        "100%",
                        "100%",
                        styles.max_width,
                    ],
                ),
                flex_direction=[
                    "column",
                    "column",
                    "column",
                    "column",
                    "column",
                    "row",
                ],
                width="100%",
                margin="auto",
                position="relative",
                background=rx.color_mode_cond(
                    light="url('/white_bg.jpg')",
                    dark="url('/bg_black.png')"
                    ),
                background_size="cover"
            ),
                            has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
    )


