from .. import styles
from ..templates import template

import reflex as rx

@template(route="/about_people", title="About the team")
def about_people() -> rx.Component:
    """The about page.

    Returns:
        The UI for the about page. (General).
    """
    with open(r'assets\mairaj_syed.md', encoding="utf-8",) as html:
        content = html.read()
    return rx.vstack(
        rx.heading("About the team", size="5"),
        rx.hstack(rx.image(src="/Mairaj_Syed.jpg", height='10em',style={"border-radius": "50%"}), rx.markdown(content, component_map=styles.markdown_style), align="center", spacing="4"),
        align="center",
    )