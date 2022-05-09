#!/usr/bin/env python3
import RPi.GPIO as GPIO       # importa GPIO
from hx711 import HX711       # importa HX711
import csv                    # importa CVS
from datetime import datetime # importa  datetime
import time                   # importa time
import tkinter as tk          # importa tkinter
from tkinter import ttk
GPIO.setwarnings(False)       # Omite warnings para impedir la interrupción de la rutina

def balanza_comida():
    try:
        GPIO.setmode(GPIO.BCM)  # Pines GPIO en numeración BCM
        # Crea un objeto hx que  Los parámetros de entrada obligatorios son solo 'Pin_Dato' y 'PD_sck'
        global hx
        hx = HX711(dout_pin=5, pd_sck_pin=6)
        # Medir la tara y guardar el valor como compensación para el canal actual
        # y ganancia seleccionada. Eso significa canal A y ganancia 128
        err = hx.zero()
        # Verifica si todo está correcto
        if err:
            raise ValueError('La tara no se puede definir')

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
        
        #mostrar el comienzo de la funcion balanza_agua
        print('Ahora comenzara la compensacion y tara del deposito de agua')
        balanza_agua()

      
    except (KeyboardInterrupt, SystemExit):
        print('Finalizacion de la lectura')

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

        
        # mostrar comienzo del bucle de lectura y medicion del volumen de agua en el deposito
        print("Ahora, leeré datos en un bucle infinito. Para salir presione 'CTRL + C'")
        print('Lectura del volumen de agua en el deposito')
        #llamado de la funcion data_cvs
        data_cvs()
    except (KeyboardInterrupt, SystemExit):
        print('Finalizacion de la lectura')

    finally:
        GPIO.cleanup()
        
def data_cvs():
    #crea un archivo llamado datos.cvs si no existe y lo abre. 
    with open('datos.csv', mode='w') as csv_file:
        # crea columans con los nombres id_dispositivo, correlativo de lectura, peso leido, fecha, hora
        fieldnames = ['id_deposito', 'correlativo_lectura', 'peso_leido', 'fecha', 'hora']
        # varible para escibir en la basde de datos
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #valor inicial del contador para el correlativo de lectura
        i=0
        # Leer datos durante la ejecucion del ciclo, devolver el valor medio de peso y agua. ademas de escribir los datos en el cvs y mostrarlos en la ventana root
        while True:
            # contador incemental en 1
            i += 1            
            # variables de lectura de peso y agua por parte de HX711
            peso = round(hx.get_weight_mean(30),2)
            agua = round(hy.get_weight_mean(30),2)
            #variables de porcentaje para la barra de progreso y label
            Comida.step(round((peso*100)/pesomax))
            Agua.step(round(agua*100/pesomax))
            # varibles visuales para la interfas grafica de la lecturas del sensor de carga
            value_label = ttk.Label(root, text=f"     Alimento disponible  {Comida['value']}%  {peso} gr     ")
            value_label.grid(column=1, row=0, columnspan=3, padx=20, pady=10)
            value_label2 = ttk.Label(root, text=f"     Agua disponible: {Agua['value']}%  {agua} ml    ")
            value_label2.grid(column=1, row=2, columnspan=2, padx=20, pady=10)
            #muestra en el pront el valor de las variables de los sensores de carga
            print("El peso actual en gramos es de %.2f" % peso)
            print("Volumen de agua en ML es de %.2f" % agua)
            #escribe en el arcivo dato.cvs los datos recopiladores de las varibles del deposito de agua, correlativo de lectura, peso leido, fecha y hora
            writer.writerow({'id_deposito': 'Agua', 'correlativo_lectura': str(i), 'peso_leido': str(agua),
                             'fecha': str(datetime.now().strftime('%Y-%m-%d')),
                             'hora': str(datetime.now().strftime('%H:%M:%S'))})
            #escribe en el arcivo dato.cvs los datos recopiladores de las varibles del deposito de comida, correlativo de lectura, peso leido, fecha y hora
            writer.writerow({'id_deposito': 'Comida', 'correlativo_lectura': str(i), 'peso_leido': str(peso),
                             'fecha': str(datetime.now().strftime('%Y-%m-%d')),
                             'hora': str(datetime.now().strftime('%H:%M:%S'))})
            #actualiza los parametros en la ventana root
            root.update()
            #resta el valores de la barra de progreso para evitar que se sumen los valores por la funcion while True
            Comida.step(round(-(peso*100)/pesomax))
            Agua.step(round(-agua*100/pesomax))
        # termino de eventos de tkinter
        root.mainloop()
        #tiempo de reposo o espera de 5 segundos
        time.sleep(5)    
            
                            
def dashboard():
    #variable global de root
    global root
    #asignar varible de tkinter
    root = tk.Tk()
    #Tamaño de la venta
    root.geometry('330x180')
    #titulo de la ventana
    root.title('Visualizacion de datos')
    #variable global del peso amximo de los deposito decomida y agua
    global pesomax
    #asignar valor a la variable de pesomaximo en unidades de gramos
    pesomax=500
    #varible global de Comida
    global Comida
    #barra de progreso del deposito de comida y caracteristicas de posicion, modo y largo
    Comida = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=180
    )
    #varible global de Agua
    global Agua
    #barra de progreso del deposito de agua y caracteristicas de posicion, modo y largo
    Agua = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=180)

    # posicion de las barras de progreso de comida y agua
    Comida.grid(column=1, row=1, columnspan=2, padx=45, pady=5, sticky='e')
    Agua.grid(column=1, row=3, columnspan=2, padx=45, pady=5, sticky='e')
    
    
    

if __name__ == '__main__':
    #ejecucion de las funciones de dashboar y balanza_comida
    dashboard()
    balanza_comida()
    
    
    
    
    
    
    
    
    
