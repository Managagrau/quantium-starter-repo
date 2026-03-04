from app import app
from dash import html, dcc


def _find_components(layout, component_type, component_id=None):
    found = []
    if isinstance(layout, component_type):
        if component_id is None or getattr(layout, "id", None) == component_id:
            found.append(layout)
    if hasattr(layout, "children"):
        children = layout.children
        if isinstance(children, list):
            for child in children:
                found.extend(_find_components(child, component_type, component_id))
        elif children is not None:
            found.extend(_find_components(children, component_type, component_id))
    return found


def test_header_present():
    headers = _find_components(app.layout, html.H1)
    assert len(headers) > 0
    assert "Pink Morsel" in headers[0].children


def test_visualisation_present():
    graphs = _find_components(app.layout, dcc.Graph, "sales-chart")
    assert len(graphs) > 0


def test_region_picker_present():
    radios = _find_components(app.layout, dcc.RadioItems, "region")
    assert len(radios) > 0
