from pypdf import PdfReader
import streamlit as st
import hashlib
import sqlite3
import os
from dotenv import load_dotenv
import datetime
import shutil
import requests
from datetime import date
import json

#cargamos al inicio de todo la configuracion y habilitacion de los environments
load_dotenv()

def init_db():
    conn = sqlite3.connect("gestion_pdfs.db")
    c = conn.cursor()
    c.execute( """
            CREATE TABLE IF NOT EXISTS archivos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                hash VARCHAR(100) NOT NULL,
                timestamp VARCHAR(100) NOT NULL,
                contenido VARCHAR(300) 
            )


        """
    )
    conn.commit()
    conn.close()
#hola

def guardar_db(hash,fecha,content):
    conn = sqlite3.connect("gestion_pdfs.db")
    c = conn.cursor()
    c.execute(
        '''
            INSERT INTO archivos (hash, timestamp, contenido) VALUES(?,?,?)
        ''', (hash, fecha,content)
    )
    conn.commit()
    conn.close()


def extract():

    #seteamos fecha para su posterior guardado en monday
    hoy = date.today()
    fecha_string = hoy.strftime("%Y-%m-%d")

    #configuramos apiKey para la conexion con monday
    api_key_monday = os.getenv("MONDAY_API_KEY")


    #config de la query para guardar en monday(usa graphql)
    query5 = 'mutation ($myItemName: String!, $columnVals: JSON!) {create_item (board_id:18396349357, item_name: $myItemName, column_values: $columnVals) {id}}'

    #aca declaramos las variables y los campos de cada columna
    query_original = {
    'myItemName': 'Prueba python-monday',
    'columnVals': json.dumps({
        #resumen
        "long_text_mkzsc82j": {"text": texto_completo}, #etiqueta "resumen"
        "long_text_mkzsdhdf": {"text": "aca resumimos lo que traiga gemini"}, #etiqueta "respuesta sugerida"
        "date_mkzs9ak3": {"date": fecha_string}, #etiqueta "vencimiento"
        "color_mkzsgtnd": {"label": "SI"} #etiqueta si/no "procesado IA"
    })
}

    #config de streamlit
    st.set_page_config(page_title="extraccion epre", layout="centered")

    st.title("extraccion epre pdf")
    st.markdown("sube un archivo para limpiar su nombre y extraer los datos")

    #subida de archivo
    uploaded_file = st.file_uploader("elegi un archivo pdf", type="pdf")

    #decimos si el archivo subido no es nulo, osea que hay uno seleccionado
    if uploaded_file is not None:
        #limpiamos nombre de espacios
        nombre_original = uploaded_file.name
        nombre_limpio = nombre_original.replace(" ", "")

        try:
            texto_completo = ""
            #seleccionamos el pdf subido
            reader = PdfReader(uploaded_file)
            #tomamos la primera hoja
            page = reader.pages[0]
            text = page.extract_text()
            texto_completo = text + "\n"
            
            col1 , col2 = st.columns(2)

            #con with abrimos una tarea asincrona y para realizar una accion, y luego cierra
            with col1:
                st.subheader("contenido extraido")
                st.text_area("vista previa del texto", texto_completo, height=400)
            with col2:
                st.subheader("Acciones")
                if st.button("guardar en base de datos"):
                    #lo convertimos a utf-8
                    datos_bytes = text.encode('utf-8')

                    #creamos el hash objeto
                    sha1_hash = hashlib.sha1()

                    #actualizamos con los datos
                    sha1_hash.update(datos_bytes)

                    #obtenemos el resultado en hexadecimal, que este dato es el vamos a guardar
                    resultado_hash = sha1_hash.hexdigest()

                    #configuramos el timestamp now
                    fecha_creacion = datetime.datetime.now()
                    guardar_db(resultado_hash,fecha_creacion,texto_completo)
                    
                    st.info("datos almacenados en sql correctamente")
                    carpeta_analizados =  "archivos_analizados"
                    archivo_original = uploaded_file.getvalue
                    #creamos una carpeta si no existe para guardar los docs analizados
                    if not os.path.exists(carpeta_analizados):
                        os.makedirs(carpeta_analizados)
                    ruta_destino = os.path.join(carpeta_analizados, os.path.basename(archivo_original))
                    shutil.move(archivo_original, ruta_destino)
                    st.info("archivo original almacenado en carpeta de analizados")
        except Exception as e:
            print(f"error: {e}")




