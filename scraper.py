from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

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

# Hacer scroll dinámico hasta cargar todos los resultados
scrollable_div = driver.find_element(By.XPATH, "//div[@role='feed']")
previous_height = -1

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(2)

    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

    if new_height == previous_height:
        break

    previous_height = new_height

# Extraer los elementos de los resultados
services = driver.find_elements(By.XPATH, "//div[@role='feed']//div[contains(@class, 'Nv2PK')]")

print("\nServicios de bicicletas encontrados:\n")

# Recorre los resultados y hace clic en cada uno
for index, service in enumerate(services, start=1):
    try:
        name = service.find_element(By.XPATH, ".//div[contains(@class, 'qBF1Pd')]").text
    except:
        name = "No disponible"

    # Hacer clic en el servicio para abrir el panel lateral
    driver.execute_script("arguments[0].scrollIntoView();", service)
    time.sleep(1)  # Pequeña pausa para asegurar que el desplazamiento ocurra

    actions = ActionChains(driver)
    actions.move_to_element(service).click().perform()

    # Esperar que el panel lateral cargue
    time.sleep(2)

    # Extraer dirección correctamente
    try:
        address = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Io6YTe fontBodyMedium kR99db fdkmkc')]"))
        ).text
    except:
        address = "No disponible"

    # Extraer número de teléfono
    try:
        phone_number = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Teléfono')]/div").text
    except:
        phone_number = "No disponible"

    # Extraer tipo de servicio
    try:
        service_type = driver.find_element(By.XPATH, "//button[contains(@class, 'DkEaL')]").text
    except:
        service_type = "No disponible"

    # Extraer calificación
    try:
        rating = service.find_element(By.XPATH, ".//span[contains(@class, 'MW4etd')]").text
    except:
        rating = "No disponible"

    # Extraer descripción
    try:
        description = driver.find_element(By.XPATH, "//span[@class='snippet-text']").text
    except:
        description = "No disponible"

    # Extraer coordenadas desde la URL de Maps
    try:
        current_url = driver.current_url
        coords_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', current_url)
        if coords_match:
            latitude, longitude = coords_match.groups()
            coordinates = f"{latitude}, {longitude}"
        else:
            coordinates = "No disponible"
    except:
        coordinates = "No disponible"

    # Extraer horarios
    try:
        hours_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Horarios')]")
        hours_button.click()
        time.sleep(1)
        hours = driver.find_element(By.XPATH, "//div[contains(@class, 'section-hours')]").text
    except:
        hours = "No disponible"

    # Extraer enlace del sitio web
    try:
        website = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'Sitio web')]").get_attribute("href")
    except:
        website = "No disponible"

    # Mostrar resultados
    print(f"{index}. {name}")
    print(f"  Dirección: {address}")  # Ahora sí extrae el texto correctamente
    print(f"  Coordenadas: {coordinates}")
    print(f"  Tipo de servicio: {service_type}")
    print(f"  Calificación: {rating}")
    print(f"  Descripción: {description}")
    print(f"  Teléfono: {phone_number}")
    print(f"  Horarios: {hours}")
    print(f"  Sitio web: {website}\n")

# Mantener el navegador abierto unos segundos para revisión
time.sleep(10)
driver.quit()
