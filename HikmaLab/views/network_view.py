import reflex as rx 
from ..custom_components.reflex_d3_graph.graph import d3_graph
import reflex as rx
from ..backend.isnad_state import QueryIsnads, isnads
from ..backend.network_state import NetworkState,narrators
from ..components.status_badge import status_badge
from ..styles import color_picker_style
from typing import Dict,Any

class NetGraphState(rx.State): 
    @rx.event(background=True)
    async def test_log(self, source, target) -> rx.Component:
        return rx.toast((source, "->", target))

    @rx.event(background=True) 
    async def test_on_click(self, node_id, node)  -> rx.Component:
        return rx.toast(str((node_id, node)))
    

def make_network_component() -> rx.Component:
    network_data = {
        'nodes': NetworkState.processed_nodes,
        'links': NetworkState.processed_edges
    }

    return d3_graph(
        id="osef_id",
        data=network_data,
        config=get_config(),
        on_click_node=NetGraphState.test_on_click,
        on_click_link=NetGraphState.test_log,
        width='100vw',
        height="70vh",
    )

def get_config() -> Dict[str, Any]:
    return {
    "directed": True,
    "automatic_rearrange_after_drop_node": False,
    "collapsible": False,
    "height": "500",
    "highlight_degree": 2,
    "highlight_opacity": 0.2,
    "link_highlight_behavior": False,
    "max_zoom": 12,
    "min_zoom": 0.05,
    "node_highlight_behavior": False,
    "pan_and_zoom": False,
    "static_graph": True,
    "width": "800",
    "node": {
        "color": "#d3d3d3",
        "font_color": "green",
        "font_size": 10,
        "font_weight": "normal",
        "highlight_color": "red",
        "highlight_font_size": 14,
        "highlight_font_weight": "bold",
        "highlight_stroke_color": "red",
        "highlight_stroke_width": 1.5,
        "label_property": "n => (n.name ? `${n.id} - ${n.name}` : n.id)",
        "mouse_cursor": "crosshair",
        "opacity": 0.9,
        "render_label": True,
        "size": 200,
        "stroke_color": "none",
        "stroke_width": 1.5,
        "symbol_type": "circle",
        "view_generator": None
    },
    "link": {
        "color": "lightgray",
        "highlight_color": "red",
        "mouse_cursor": "pointer",
        "opacity": 1,
        "semantic_stroke_width": True,
        "stroke_width": 3,
        "type": "STRAIGHT"
    }
}



