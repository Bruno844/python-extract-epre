import streamlit as st


st.set_page_config(page_title="Extract data pdf epre", layout="centered")

st.title("extractor de pdf de epre")
st.markdown("sube un archivo para limpiar su nombre y extraer contenido relevante")


upload_file = st.file_uploader("Elegi un archivo pdf", type="pdf")
