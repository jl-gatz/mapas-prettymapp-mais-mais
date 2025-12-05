import streamlit as st
from streamlit_folium import st_folium
import folium
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import matplotlib.pyplot as plt
import io
from PIL import Image
import clipboard as clip


# Primeira versão, corrigida no app2
def create_map():
     # Center on a default location (latitude, longitude) with a base zoom level
     mapinha = folium.Map(location=[-22.81716, -47.06975], zoom_start=10)
     # marca latitude e longitude
     mapinha.add_child(
         folium.ClickForMarker(),
    )
     mapinha.add_child(
         folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=False)
     )
     return mapinha

def plot_pretty_map(lat, lon):
    try:
        # Define the area of interest (AOI) around the given latitude and longitude
        aoi = get_aoi(address=f"{lat},{lon}", radius=1000, rectangular=False)
        # Fetch OpenStreetMap geometries (roads, parks, buildings, etc.) within that area
        df = get_osm_geometries(aoi=aoi)
        # Use prettymapp's Plot to draw the map with a chosen style
        fig = Plot(df=df, aoi_bounds=aoi.bounds, draw_settings=STYLES["Peach"]).plot_all()
        return fig  # fig is a Matplotlib figure
    except Exception as e:
        st.error(f"Error: {e}")  # Display an error message in the Streamlit app
        return None

st.subheader("Awesome Pretty Map App")
st.write("Click on the map to select latitude and longitude")

col1, col2 = st.columns(2)

def main():
    with col1:
        map_obj = create_map()
        st_data = st_folium(map_obj, width=350, height=350)

        # função para separar [ '[', ']', '.', ',']
        # Se for '.' continua até encontrar a ',', exclui, continua
        if st_data['last_clicked']:
            lat, lon = st_data['last_clicked']['lat'], st_data['last_clicked']['lng']
            lat_lon_str = f"{lat:.5f} {lon:.5f}"
            st.session_state.lat_lon_input = lat_lon_str
            st.text_input("Latitude and Longitude", value=lat_lon_str, key="lat_lon_input")
        else:
            st.text_input("Latitude and Longitude", value="", key="lat_lon_input")

        if st.button("Draw My Pretty Map"):
            lat_lon_input = st.session_state.lat_lon_input.split()
            if len(lat_lon_input) == 2:
                try:
                    lat, lon = float(lat_lon_input[0]), float(lat_lon_input[1])
                    fig = plot_pretty_map(lat, lon)
                    if fig:
                        buf = io.BytesIO()
                        fig.set_size_inches(10, 10)
                        fig.savefig(buf, format="png", dpi=100)
                        buf.seek(0)
                        img = Image.open(buf)
                        with col2:
                            st.image(img, caption="Awesome Pretty Map!", width="stretch")
                except ValueError:
                    st.error("Invalid latitude and longitude input. Please enter valid numbers.")
                except Exception as e:
                    st.error(f"Error generating map: {e}")

if __name__ == "__main__":
    main()
