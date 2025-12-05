import streamlit as st
from streamlit_folium import st_folium
import folium
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import matplotlib.pyplot as plt

# --------------------------------------------------
# Create the Folium map
# --------------------------------------------------
def create_map() -> folium.Map:
    """Create Folium map centered on default coordinates."""
    map_obj = folium.Map(location=[-22.817159, -47.069743], zoom_start=10)
    map_obj.add_child(folium.ClickForMarker())
    map_obj.add_child(folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=False))
    return map_obj


# --------------------------------------------------
# Pretty Map generator
# --------------------------------------------------
def plot_pretty_map(lat: float, lon: float, style: None) -> Plot:
    """Generate prettymapp Plot object from latitude and longitude."""
    try:
        aoi = get_aoi(address=f"{lat},{lon}", radius=1000, rectangular=False)
        df = get_osm_geometries(aoi=aoi)

        fig = Plot(
            df=df,
            aoi_bounds=aoi.bounds,
            draw_settings=STYLES["Citrus"],
        ).plot_all()

        return fig

    except Exception as e:
        st.error(f"Erro ao gerar mapa: {e}")
        return None


# --------------------------------------------------
# UI
# --------------------------------------------------
def main():
    st.subheader("Awesome Pretty Map App")
    st.write("Clique no mapa para selecionar coordenadas.")

    col1, col2 = st.columns(2)

    with col1:
        map_obj = create_map()
        st_data = st_folium(map_obj, width=350, height=350)
        lat_lon = None

        # Captura coordenadas do clique
        if st_data and st_data.get("last_clicked"):
            lat = st_data["last_clicked"]["lat"]
            lon = st_data["last_clicked"]["lng"]
            lat_lon = f"{lat:.5f} {lon:.5f}"
            st.session_state.lat_lon_box = lat_lon
        else:
            st.session_state.setdefault("lat_lon", "")

        lat_lon_input = st.text_input(
            "Latitude e Longitude", 
            value=lat_lon, 
            key="lat_lon_box"
        )

        st.write("Selecione o estilo a ser utilizado no mapa!")
        style_name = st.selectbox("Estilo", list(STYLES.keys()))

        if st.button("Gerar Pretty Map"):
            parts = lat_lon_input.split()
            if len(parts) != 2:
                st.error("Digite latitude e longitude no formato: -22.81 -47.06")
                return

            try:
                lat, lon = map(float, parts)
                with col2:
                    with st.spinner("Aguarde o mapa ser criado...", show_time=True):
                        fig = plot_pretty_map(lat, lon, style_name)
                        if fig:
                            st.pyplot(fig)

            except ValueError:
                st.error("Coordenadas inválidas. Digite números válidos.")



if __name__ == "__main__":
    main()
