def create_map() -> folium.Map:
    """Create Folium map centered on default coordinates."""
    # placeholder = st.empty()
    map_obj = folium.Map(location=[-22.817159, -47.069743], zoom_start=10)
    map_obj.add_child(folium.ClickForMarker())
    map_obj.add_child(folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=False))
    return map_obj