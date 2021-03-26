import requests

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# Este lazo for me ayudara a iterar el parametro "page" del API
for i in range (1, 4):
    # Esta URL, y los parametros la deciframos gracias al panel de Networks y a una tarea de investigacion
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=python&p=' + str(i)


    response = requests.get(url_api, headers=headers)

    # Parseo la respuesta en formato JSON. Requests automaticamente lo convierte en un diccionario de Python
    data = response.json()

    # Extraigo los datos del diccionario
    cursos = data["courses"]
    for curso in cursos:
        print (curso["title"])
        print (curso["num_reviews"])
        print (curso["rating"])

    # Hago que el usuario tenga que aplastar enter antes de seguir a la siguiente pagina
    input()


