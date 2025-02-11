
import reflex as rx
from ..backend.isnad_state import QueryIsnads, isnads
from .. import styles
from ..templates import template
from ..views.isnad_table import isnads_table
from ..views.network_view import make_network_component
from ..backend.network_state import NetworkState

@template(route="/fetch_isnads", title="Fetch isnads tester")
def test_isnads() -> rx.Component:
    return rx.fragment(
        rx.input(
            placeholder="Enter hadith", 
            on_blur=NetworkState.set_hadith
        ),
        rx.input(
            placeholder="Enter taraf", 
            type_="number",
            on_blur=NetworkState.set_taraf
        ),
        rx.button(
            "Search by Hadith",
            on_click=NetworkState.get_hadith_network,   
        ),
        rx.button(
            "Search by Taraf",
            on_click=NetworkState.get_taraf_network,
        ),
        isnads_table(),
        make_network_component(),
    )