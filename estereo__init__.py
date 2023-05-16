#! /usr/bin/python3
"""
Gestión de números aleatorios y manejo de archivos WAVE mono y estéreo.

Usage:
    estereo.py [opciones] <ficL> [ficR] <ficEste> 
    estereo.py mono [options] <ficEste> <ficMono> 

Options:
  -l, --left                     La señal mono es el canal izquierdo de la señal estéreo.
  -r, --right                    La señal mono es el canal derecho de la señal estéreo.
  -s, --suma                     La señal mono es la semisuma de los dos canales de la señal estéreo.
  -d, --diferencia               La señal mono es la semidiferencia de los dos canales de la señal estéreo.
  -h, --help                     Mostrar la ayuda
  --version                      Mostrar la versión del programa
"""
from docopt import docopt
from estereo import *

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Manejo de archivos WAVE mono y estéreo")
    if arguments['mono']:
        ficEste = arguments["<ficEste>"]
        ficMono = arguments["<ficMono>"]
        modo = 2
        if arguments['--left']:
            modo = 0
        elif arguments['--right']:
            modo = 1
        elif arguments['--suma']:
            modo = 2
        elif arguments['--diferencia']:
            modo = 3
        estereo2mono(ficEste, ficMono, canal=modo)
        print("La conversión se ha realizado correctamente.")
    else:
        ficL = arguments["<ficL>"]
        ficR = arguments["<ficR>"]
        ficEste = arguments["<ficEste>"]

        if ficR is None:
            raise ValueError("Error: Falta el fichero mono de la derecha")
        else:
            mono2estereo(ficL, ficR, ficEste)

