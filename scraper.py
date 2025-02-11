from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar Selenium
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Mantiene la ventana abierta
options.add_argument("--start-maximized")  # Inicia maximizado

# Iniciar navegador
driver = webdriver.Chrome(service=service, options=options)

# Abrir Google Maps
driver.get("https://www.google.com/maps")

# Esperar la barra de búsqueda
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchboxinput"))
)

# Escribir la búsqueda
search_box.send_keys("servicio de bicicletas en Cochabamba")
search_box.send_keys(Keys.RETURN)

# Esperar a que los resultados aparezcan
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
)

time.sleep(3)  # Espera para que carguen los elementos

# Hacer scroll para cargar más resultados
scrollable_div = driver.find_element(By.XPATH, "//div[@role='feed']")
for _ in range(5):  # Ajusta la cantidad de scrolls si es necesario
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(2)

# Extraer nombres, direcciones y calificaciones
services = driver.find_elements(By.XPATH, "//div[@role='feed']//div[contains(@class, 'Nv2PK')]")

print("\nServicios de bicicletas encontrados:\n")

for index, service in enumerate(services, start=1):
    try:
        name = service.find_element(By.XPATH, ".//div[contains(@class, 'qBF1Pd')]").text  # Nombre
    except:
        name = "No disponible"

    try:
        address = service.find_element(By.XPATH, ".//div[contains(@class, 'W4Efsd')]").text  # Dirección
    except:
        address = "No disponible"

    try:
        rating = service.find_element(By.XPATH, ".//span[contains(@class, 'MW4etd')]").text  # Calificación
    except:
        rating = "No disponible"

    print(f"{index}. {name}")
    print(f"   Dirección: {address}")
    print(f"   Calificación: {rating}\n")

# Mantener el navegador abierto unos segundos para revisión
time.sleep(10)
driver.quit()
