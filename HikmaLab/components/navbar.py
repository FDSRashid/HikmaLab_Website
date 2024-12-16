"""Navbar component for the app."""

from .. import styles

import reflex as rx

def navbar_link(text: str, url: str) -> rx.Component:
    """Create a link for the navbar with the given text and url.

    Args:
        text: The text of the link.
        url: The URL of the link.

    Returns:
        The link component.
    """
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

def dropdown_link(text: str, url: str) -> rx.Component:
    return rx.link(
        text, href=url, style={"color": "white", "text-decoration": "none"},
    )


def navbar_dropdown() -> rx.Component:
    return rx.hstack(
                rx.hstack(
                    navbar_link("Home", "/"),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.text(
                                    "About",
                                    size="4",
                                    weight="medium",
                                ),
                                rx.icon("chevron-down"),
                                weight="medium",
                                variant="ghost",
                                size="3",
                            ),
                        ),
                        rx.menu.content(
                            dropdown_link("About the project", "/about"),
                            dropdown_link("Team", "/"),
                        ),
                    ),
                    navbar_link("Settings", "/settings"),
                    justify="end",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
            )

def navbar() -> rx.Component:
    """The navbar.

    Returns:
        The navbar component.
    """

    return rx.el.nav(
        rx.hstack(
            # The logo.
            rx.color_mode_cond(
                rx.image(src="/logo_white_bg-removebg-preview.png", height="2em"),
                rx.image(src="/logo_black_bg-removebg-preview.png", height="2em"),
            ),
            rx.spacer(),
            navbar_dropdown(),
            rx.color_mode.button(style={"opacity": "0.8", "scale": "0.95"}),
            align="center",
            width="100%",
            padding_y="1.25em",
            padding_x=["1em", "1em", "2em"],
        ),
        display=["block", "block", "block", "block", "block", "none"],
        position="sticky",
        background_color=rx.color("gray", 1),
        top="0px",
        z_index="5",
        border_bottom=styles.border,
    )
