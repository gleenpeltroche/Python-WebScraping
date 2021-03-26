from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

#URL SEMILLA
driver.get('https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias')


# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10 
PAGINACION_MAX = 10
PAGINACION_ACTUAL = 1

# Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
while PAGINACION_MAX > PAGINACION_ACTUAL:

  links_productos = driver.find_elements(By.XPATH, '//a[@class="item__info-title"]')
  links_de_la_pagina = []
  for a_link in links_productos:
    links_de_la_pagina.append(a_link.get_attribute("href"))

  for link in links_de_la_pagina:

    try:
      # Voy a cada uno de los links de los detalles de los productos
      driver.get(link)

      # Rara vez da error si no utilizamos una espera por eventos:
      # precio_element = WebDriverWait(driver, 10).until(
      #   EC.presence_of_element_located((By.XPATH, '//span[includes(@class,"price-tag")]'))
      # )
      titulo = driver.find_element(By.XPATH, '//h1').text
      precio = driver.find_element(By.XPATH, '//span[includes(@class,"price-tag")]').text
      print (titulo)
      print (precio.replace('\n', '').replace('\t', ''))

      # Aplasto el boton de retroceso
      driver.back()
    except Exception as e:
      print (e)
      # Si sucede algun error dentro del detalle, no me complico. Regreso a la lista y sigo con otro producto.
      driver.back()

  # Logica de deteccion de fin de paginacion
  try:
    # Intento obtener el boton de SIGUIENTE y le intento dar click
    puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
    puedo_seguir_horizontal.click()
  except: 
    # Si obtengo un error al intentar darle click al boton, quiere decir que no existe
    # Lo cual me indica que ya no puedo seguir paginando, por ende rompo el While
    break

  PAGINACION_ACTUAL += 1
