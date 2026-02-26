from pypdf import PdfReader
import streamlit as st
import hashlib
import sqlite3
import os
import datetime
import shutil


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



# #primero, eliminamos los espacios en los nombres de los pdf
# def remove_space_from_pdfs_names(path):
#     for filename in os.listdir(path):
#         #chequeamos si el archivo es un pdf y si contiene espacios
#         if filename.endswith(".pdf") and " " in filename:
#             #creamos un nuevo filename separando los espacios
#             new_filename = filename.replace(" ", "") #los espacios por sin espacio

#             #construimos la ruta vieja de los nombres por los nuevos cambios
#             old_path = os.path.join(path, filename)#original con espacios
#             new_path = os.path.join(path, new_filename) #sin espacios

#             try:
#                 #creamos un objeto reader de pdf
#                 reader = PdfReader(f"{path}/Nota Ext 976227- Inf s-EXPTE 31241-21 Registradores Barrio Rio Sol - Las Perlas.pdf")

#                 #imprimimos el numero de paginas
#                 print(len(reader.pages))

#                 #obtenemos una pagina en especifico, es la primera
#                 page = reader.pages[0]

#                 #extraemos
#                 text = page.extract_text()
#                 if text:
#                     #si el texto se extrajo de manera correcta, abrimos conexion con la db
#                     conn = sqlite3.connect("gestion_pdfs.db")
#                     cursor = conn.cursor()

#                     #ahora hasheamos el contenido extraido

#                     #lo convertimos a utf-8
#                     datos_bytes = text.encode('utf-8')

#                     #creamos el hash objeto
#                     sha1_hash = hashlib.sha1()

#                     #actualizamos con los datos
#                     sha1_hash.update(datos_bytes)

#                     #obtenemos el resultado en hexadecimal, que este dato es el vamos a guardar
#                     resultado_hash = sha1_hash.hexdigest()

#                     #configuramos el timestamp now
#                     fecha_creacion = datetime.datetime.now()

#                     #y ahora almacenamos nuestros datos
#                     cursor.execute(
#                         "INSERT INTO archivos (hash, timestamp, contenido) VALUES (?,?,?)", (resultado_hash, fecha_creacion, text)
#                     )
#                     #cerramos conexion y almacenamos
#                     conn.commit()

#                     print(text)

#                     os.rename(old_path, new_path)
#                     print("renamed success")
#             except OSError as e:
#                 print(f"error en la conversion: {e}")
#             finally:
#                 conn.close()
                

# remove_space_from_pdfs_names('files')
