# BICIDATOS - Scraper de Servicios

Scraper de servicios de bicicletas en los departamentos de Bolivia.

## Instalación

Es necesario instalar las siguientes dependencias:

```bash
pip install selenium webdriver-manager
```

## Observaciones

Para hacer scraping de los distintos departamentos, se deben modificar las siguientes líneas en el código:

```python
search_box.send_keys("servicio de bicicletas en Oruro")
```

y el nombre del archivo que se creará:

```python
with open('servicios_bicicletas_Oruro.csv', mode='w', newline='', encoding='utf-8') as file:
```




