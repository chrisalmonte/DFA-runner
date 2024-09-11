import re
import sys
from pathlib import Path

archivoAutomata = ""
cadena = ""

for arg in sys.argv:
    if arg.endswith(".afd"):
        archivoAutomata = arg
    else:
        cadena = arg

archivo = Path(archivoAutomata)
if not archivo.exists():
    sys.exit("No se encontró el archivo de autómata especificado.")


with open(archivoAutomata, "r", encoding="utf-8") as automata:

    def Escanear(claveIncio, claveFin):
        for linea in automata:
            resultado = re.search(claveIncio + "(.*)" + claveFin, linea)
            if resultado != None:
                return resultado.group(1)
        return None

    alfabeto = []
    estados = []
    aceptados = []
    estActual = ''
    tabla = []

    resultado = Escanear("A={","}")
    if resultado == None:
        sys.exit("No se encontró definición del alfabeto.")
    alfabeto = resultado.split(',')
        
    resultado = Escanear("F={","}")
    if resultado == None:
        sys.exit("No se encontró definición de los estados aceptados.")
    aceptados = resultado.split(',')
        
    resultado = Escanear("s={","}")
    if resultado == None:
        sys.exit("No se encontró definición de los estados posibles.")
    estados = resultado.split(',')
        
    resultado = Escanear("i=",'\\s')
    if resultado == None:
        sys.exit("No se encontró definición del estado inicial.")
    estActual = resultado

    for estado in estados:        
        for linea in automata:
            resultado = re.search(estado + ":(.*)" + '\\n', linea)
            if resultado != None:
                resultado = resultado.group(1).replace(" ","")
                tabla.append([estado] + resultado.split(','))
                break
    
    for caracter in cadena:
        print(estActual + ", " + caracter, end=": ")
        if caracter not in alfabeto:
            print("Caracter inexistente en el alfabeto")
            sys.exit("Se encontró un caracter inválido.")

        for linea in tabla:
            if (linea[0] == estActual):
                estActual = linea[alfabeto.index(caracter) + 1]
                print(estActual)
                break 

    if estActual in aceptados:
        print("La cadena es ACEPTADA. Estado " + estActual + " es de aceptación.")
    else:
        print("La cadena NO ES ACEPTADA. Estado " + estActual + " no es de aceptación.")
        


    
    
    

            
    