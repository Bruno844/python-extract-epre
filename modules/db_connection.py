#en este archivos creamos nuestra db donde va a estar almacenando los datos
import sqlite3

def connect_db():
    


    #conectamos, si no existe ninguno archivo, lo crea
    conexion = sqlite3.connect("gestion_pdfs.db")

    #creamos un cursor, que es el puntero para ejecutar comandos SQL
    cursor = conexion.cursor()


    #creamos una tabla con los datos
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS archivos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                hash VARCHAR(100) NOT NULL,
                timestamp VARCHAR(100) NOT NULL,
                contenido VARCHAR(300) 
            )


        """
    )


    #guardamos cambios y cerramos
    conexion.commit()
    conexion.close()