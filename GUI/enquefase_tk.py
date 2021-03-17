# -*- coding: utf-8 -*-
import sqlite3
from time import sleep
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys


def get_event(*args):
    """Obtiene elemento desde el evento de seleccion desde listbox."""
    seleccion = lista_comunas.selection_get()
    return seleccion


def consulta_fase():
    """Scraping en pagina web, buscando la comuna consultada."""

    nombre_city = get_event()

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
        "/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div/div/span/span[1]/span/span[2]/b"
    )
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

    texto = ""
    for item in items_obtenidos:
        texto += item.text

    driver.close()

    resultado_txt['state'] = "normal"
    resultado_txt.delete("1.0", resultado_txt.index('end'))
    resultado_txt.insert(INSERT, texto)
    resultado_txt['state'] = "disabled"


def busca_comuna():
    """Busca comuna correcta, en DB local."""
    comuna = entrada_ciudad.get()
    conexion = sqlite3.connect("db_comunas/comunas_db")
    ejecutor = conexion.cursor()
    resultados = ejecutor.execute('SELECT nombre from comuna_chile WHERE {} LIKE "%{}%"'.format("nombre", comuna))
    datos = resultados.fetchall()
    if len(datos) == 0:
        messagebox.showerror(title="Comuna no encontrada", message="No existe la comuna\nRevise la escritura.")
    else:
        ejecutor.close()
        xi = 0
        lista_comunas.delete(0, END)
        for item in datos:
            lista_comunas.insert(xi, item[0])
            xi += 1


base = Tk()
base.title("En que Fase")

frame1 = Frame(base, width=200, height=100)
frame2 = Frame(base, width=200, height=100)
frame3 = Frame(base, width=200, height=100)
frame4 = Frame(base, width=200, height=10)

texto_var = StringVar()
entrada_ciudad = Entry(frame1, textvariable=texto_var, show=None, justify="center")
boton_buscar = Button(frame1, text="Buscar", command=busca_comuna)

lista_comunas = Listbox(frame2, selectmode="single", width=30, height=6)

consulta_boton = Button(frame3, text="Consultar", command=consulta_fase)

resultado_txt = Text(frame4, wrap="word", width=30, height=4)
resultado_txt['state'] = 'disabled'

boton_salir = Button(frame4, text="Salir", command=quit, width=5)

frame1.grid(pady=(5, 1))
frame2.grid()
frame3.grid()
frame4.grid()

entrada_ciudad.grid(column=1, row=1, ipady=4)
boton_buscar.grid(column=2, row=1)
lista_comunas.grid(sticky="WE")
lista_comunas.bind('<<ListboxSelect>>', get_event)
consulta_boton.grid()

resultado_txt.grid(pady=(0, 5))

boton_salir.grid()

base.mainloop()
