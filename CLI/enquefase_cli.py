# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
import sqlite3
import sys


def consulta_fase(nombre_city):
    """Scraping en pagina web, buscando la comuna consultada"""
    opciones_settings = Options()
    opciones_settings.headless = True

    url = "https://www.enquefase.cl/"

    ruta_exec = ""
    plataforma = sys.platform
    if plataforma == "linux":
        ruta_exec = "geckodriver/geckodriver"
    elif plataforma == "win32":
        ruta_exec = "geckodriver/geckodriver.exe"

    driver = webdriver.Firefox(options=opciones_settings, executable_path=ruta_exec)
    driver.get(url)

    buscador = driver.find_element_by_xpath(
        "/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div/div/span/span[1]/span/span[2]/b")
    buscador.click()

    barra_buscar = buscador.find_element_by_xpath("/html/body/span/span/span[1]/input")
    barra_buscar.send_keys(nombre_city)
    sleep(1)
    barra_buscar.send_keys(Keys.ENTER)
    sleep(1)

    WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div/div"))
    )

    items_obtenidos = driver.find_elements_by_xpath("/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div/div")

    for item in items_obtenidos:
        print(item.text)

    driver.close()


def busca_comuna(comuna):
    """Busca comuna correcta, en DB local."""
    conexion = sqlite3.connect("db_comunas/comunas_db")
    ejecutor = conexion.cursor()

    resultados = ejecutor.execute('SELECT nombre from comuna_chile WHERE {} LIKE "%{}%"'.format("nombre", comuna))
    datos = resultados.fetchall()

    ejecutor.close()

    return datos


while True:
    buscar = input("Nombre comuna\n>>>: ")
    if buscar != "":
        data = busca_comuna(buscar)
        if data:
            print()
            i = 1
            for x in data:
                print(i, x[0])
                i += 1
            print()
            seleccion = int(input("Seleccione una comuna\n>>>: "))
            print("\n")
            consulta_fase(data[seleccion - 1][0])
            print("\n")
        else:
            print("Ingrese ciudad correcta")
    else:
        break
