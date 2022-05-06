#!/usr/bin/env python3
import RPi.GPIO as GPIO  # importa GPIO
from hx711 import HX711  # importa la clase HX711
import csv
from datetime import datetime
import time
import itertools
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from threading import Thread

GPIO.setwarnings(False)  # elimina los warnings

def balanza_comida():
    try:
        GPIO.setmode(GPIO.BCM)  # Pines GPIO en numeración BCM
        # Crea un objeto hx que represente el chip HX711 real
        # Los parámetros de entrada obligatorios son solo 'Pin_Dato' y 'PD_sck'
        global hx
        hx = HX711(dout_pin=5, pd_sck_pin=6)
        # Medir la tara y guardar el valor como compensación para el canal actual
        # y ganancia seleccionada. Eso significa canal A y ganancia 128
        err = hx.zero()
        # Verifica si todo está correcto
        if err:
            raise ValueError('La tara no se puede definir.')

        reading = hx.get_raw_data_mean()
        if reading:  # Verificar si el valor correcto
            # ahora el valor está cerca de 0
            print('Datos restados por compensación pero todavía no convertidos a unidades:', reading)
        else:
            print('Dato invalido', reading)

        # Para calcular la tasa de conversión a algunas unidades, en este caso gramos,
        # Se debe partir de un peso conocido para ajustar.
        input('Coloque un peso conocido en la balanza y luego presione Enter')
        reading = hx.get_data_mean()
        if reading:
            print('Valor medio de HX711 restado para compensar:', reading)
            known_weight_grams = input('Escriba cuántos gramos eran y presiona Enter: ')
            try:
                value = float(known_weight_grams)
                print(value, 'gramos')
            except ValueError:
                print('Entero o flotante esperado y tengo:', known_weight_grams)

            # establecer la relación de escala para un canal en particular y una ganancia
            # utilizada para calcular la conversión a unidades. El argumento requerido es solo
            # una relación de escala. Sin argumentos 'canal' y 'ganancia_A' establece
            # la relación entre el canal actual y la ganancia.
            ratio = reading / value  # calcular la relación para el canal A y la ganancia 128
            hx.set_scale_ratio(ratio)  # Determina la proporción para el canal actual
            print('Relación de peso establecida.')
        else:
            raise ValueError('No se puede calcular el valor medio . ERROR', reading)

        # Leer datos varias veces y devolver el valor medio
        # restado por compensación y escalado a las
        # unidades deseadas. En este caso en gramos.
        print("Ahora, leeré datos en un bucle infinito. Para salir presione 'CTRL + C'")
        #input('Presione Enter para comenzar a leer')
        #print('El peso actual en la balanza en gramos es: ')
        print('Ahora comenzara lectura de datos.')
        balanza_agua()

      
    except (KeyboardInterrupt, SystemExit):
        print('Chau :)')

    finally:
        GPIO.cleanup()
def balanza_agua():
    try:
        global hy
        #GPIO.setmode(GPIO.BCM)  # Pines GPIO en numeración BCM
        # Crea un objeto hx que represente el chip HX711 real
        # Los parámetros de entrada obligatorios son solo 'Pin_Dato' y 'PD_sck'
        hy = HX711(dout_pin=20, pd_sck_pin=21)
        # Medir la tara y guardar el valor como compensación para el canal actual
        # y ganancia seleccionada. Eso significa canal A y ganancia 128
        erry = hy.zero()
        # Verifica si todo está correcto
        if erry:
            raise ValueError('La tara no se puede definir.')

        readingy = hy.get_raw_data_mean()
        if readingy:  # Verificar si el valor correcto
            # ahora el valor está cerca de 0
            print('Datos restados por compensación pero todavía no convertidos a unidades:', readingy)
        else:
            print('Dato invalido', readingy)

        # Para calcular la tasa de conversión a algunas unidades, en este caso gramos,
        # Se debe partir de un peso conocido para ajustar.
        input('Coloque un peso conocido en la balanza y luego presione Enter')
        readingy = hy.get_data_mean()
        if readingy:
            print('Valor medio de HX711 restado para compensar:', readingy)
            known_weight_gramsy = input('Escriba cuántos gramos eran y presiona Enter: ')
            try:
                valuey = float(known_weight_gramsy)
                print(valuey, 'gramos')
            except ValueError:
                print('Entero o flotante esperado y tengo:', known_weight_gramsy)

            # establecer la relación de escala para un canal en particular y una ganancia
            # utilizada para calcular la conversión a unidades. El argumento requerido es solo
            # una relación de escala. Sin argumentos 'canal' y 'ganancia_A' establece
            # la relación entre el canal actual y la ganancia.
            ratioy = readingy / valuey  # calcular la relación para el canal A y la ganancia 128
            hy.set_scale_ratio(ratioy)  # Determina la proporción para el canal actual
            print('Relación de peso establecida.')
        else:
            raise ValueError('No se puede calcular el valor medio . ERROR', readingy)

        # Leer datos varias veces y devolver el valor medio
        # restado por compensación y escalado a las
        # unidades deseadas. En este caso en gramos.
        print("Ahora, leeré datos en un bucle infinito. Para salir presione 'CTRL + C'")
        print('Lectura de agua')
        # print('El peso actual en la balanza en gramos es: ')
        data_cvs()
    except (KeyboardInterrupt, SystemExit):
        print('Chau :)')

    finally:
        GPIO.cleanup()
        
def data_cvs():
    with open('datos.csv', mode='w') as csv_file:
        fieldnames = ['id_deposito', 'correlativo_lectura', 'peso_leido', 'fecha', 'hora']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        i=0
        
        while True:
            i += 1            
            peso = round(hx.get_weight_mean(30),2)
            agua = round(hy.get_weight_mean(30),2)
            Comida.step(round((peso*100)/pesomax))
            Agua.step(round(agua*100/pesomax))
            value_label = ttk.Label(root, text=f"     Alimento disponible  {Comida['value']}%  {peso} gr     ")
            value_label.grid(column=1, row=0, columnspan=3, padx=20, pady=10)
            value_label2 = ttk.Label(root, text=f"     Agua disponible: {Agua['value']}%  {agua} ml    ")
            value_label2.grid(column=1, row=2, columnspan=2, padx=20, pady=10)
            print("El peso actual en gramos es de %.2f" % peso)
            print("Volumen de agua en ML es de %.2f" % agua)
            writer.writerow({'id_deposito': 'Agua', 'correlativo_lectura': str(i), 'peso_leido': str(agua),
                             'fecha': str(datetime.now().strftime('%Y-%m-%d')),
                             'hora': str(datetime.now().strftime('%H:%M:%S'))})
            writer.writerow({'id_deposito': 'Comida', 'correlativo_lectura': str(i), 'peso_leido': str(peso),
                             'fecha': str(datetime.now().strftime('%Y-%m-%d')),
                             'hora': str(datetime.now().strftime('%H:%M:%S'))})
            
            root.update()
            Comida.step(round(-(peso*100)/pesomax))
            Agua.step(round(-agua*100/pesomax))
        
        root.mainloop()
        
        time.sleep(5)    
            
                            
def dashboard():
    global root
    root = tk.Tk()
    root.geometry('330x180')
    root.title('Visualizacion de datos')
    global pesomax
    pesomax=500

    global Comida
    Comida = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=180
    )
    global Agua
    Agua = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=180)

    # place the progressbar
    Comida.grid(column=1, row=1, columnspan=2, padx=45, pady=5, sticky='e')
    Agua.grid(column=1, row=3, columnspan=2, padx=45, pady=5, sticky='e')
    
    
    

if __name__ == '__main__':
    dashboard()
    balanza_comida()
    
    
    
    
    
    
    
