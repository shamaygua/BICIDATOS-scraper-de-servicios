from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configura el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())

# Opciones del navegador
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Mantiene la ventana abierta
options.add_argument("--start-maximized")  # Inicia maximizado

# Inicia el navegador
driver = webdriver.Chrome(service=service, options=options)

# Abre Google Maps
driver.get("https://www.google.com/maps")

# Espera a que cargue Google Maps
time.sleep(3)

# Encuentra la barra de búsqueda y escribe "Servicios de bicicletas en Cochabamba"
search_box = driver.find_element(By.XPATH, "//input[@id='searchboxinput']")
search_box.send_keys("Servicios de bicicletas en Cochabamba")
search_box.send_keys(Keys.RETURN)  # Presiona Enter

# Esperar a que carguen los resultados
time.sleep(20)

# Cierra el navegador después de revisar los resultados
driver.quit()
