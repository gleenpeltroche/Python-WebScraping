from twisted.internet import reactor # viene instalado con scrapy
from twisted.internet.task import LoopingCall # viene instalado con scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider

class ExtractorClima(Spider):
    name = "MiCrawlerDeClima"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': True # Elimina los miles de logs que salen al ejecutar Scrapy en terminal
    }

    # Start URLs puede ser un arreglo de muchas URLs. Al no haber reglas, cada una de
    # estas URLs va a ejecutar la funcion parse una vez que se haga el requerimiento y
    # se obtenga una respuesta
    start_urls = [
        "https://www.accuweather.com/es/pe/lima/264120/weather-forecast/264120",
        "https://www.accuweather.com/es/pe/piura/259570/weather-forecast/259570",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]

    def parse(self, response):
        print(response)
        ciudad = response.xpath('//h1/text()').get()
        current = response.xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]/text()').get()
        real_feel = response.xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]/text()').get()

        # Limpieza de datos
        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_scrapy.csv", "a")
        f.write(ciudad + "," + current + "," + real_feel + "\n")
        f.close()
        print(ciudad)
        print(current)
        print(real_feel)
        print()

        # No necesito hacer yield. El yield me sirve cuando voy a guardar los datos
        # en un archivo, corriendo Scrapy desde Terminal

# Logica para correr una extraccion de Scrapy periodicamente. Es decir, automatizarla.
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(ExtractorClima))
task.start(20) # Tiempo en segundos desde la primera corrida del programa para repetir la extraccion
reactor.run()

# Segundos en 1 dia: 86400
# Segundos en 1 hora: 3600
# Segundos en 1 semana: 604800
# Segundos en 1 mes: 2.628e+6
# Segundos en 1 minuto: 60