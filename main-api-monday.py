import requests
import json
from datetime import date

hoy = date.today()
#fecha_string = hoy.strftime("%m/%d/%Y")
fecha_string = hoy.strftime("%Y-%m-%d")

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYyNjg0Mjk4OCwiYWFpIjoxMSwidWlkIjo5OTYxODY0NiwiaWFkIjoiMjAyNi0wMi0yN1QxNDozNDowNi4xNzJaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjY5Mzg4MDgsInJnbiI6InVzZTEifQ.0cl3VB30rRout81PdN9F1jJQyQftdLWTvC5nfDWWr-4"

apiUrl = "https://api.monday.com/v2"

headers = {"Authorization": apiKey}

query2 = '{boards(limit:5) {name id description items_page{items{name column_values{id type text}}}}}'

query3 = 'mutation {create_item (board_id:18396349357, item_name:"cambios desde python!") {id}}'

query4 = 'mutation ($myItemName: String!) {create_item (board_id:18396349357, item_name: $myItemName) {id}}'
vars4 = {'myItemName': 'Hola desde python'}

#editar y subir datos por las columnas de la tabla
query5 = 'mutation ($myItemName: String!, $columnVals: JSON!) {create_item (board_id:18396349357, item_name: $myItemName, column_values: $columnVals) {id}}'

#aca declaramos las variables y los campos de cada columna
var5 = {
    'myItemName': 'Prueba python-monday',
    'columnVals': json.dumps({
        #resumen
        "long_text_mkzsc82j": {"text": "Resumen prueba"}, #etiqueta "resumen"
        "long_text_mkzsdhdf": {"text": "respuesta sugerida prueba"}, #etiqueta "respuesta sugerida"
        "date_mkzs9ak3": {"date": fecha_string}, #etiqueta "vencimiento"
        "color_mkzsgtnd": {"label": "SI"} #etiqueta si/no "procesado IA"
    })
}

data = {'query': query5, 'variables': var5}

r = requests.post(url=apiUrl, json=data, headers=headers)
print(r.json())