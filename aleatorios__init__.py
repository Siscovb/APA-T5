#! /usr/bin/python3

"""Gestión de números aleatorios.

Usage:
  aleatorios.py aleat [--semilla=<ENTERO>] [--numero=<ENTERO>] [--norm] [--help] [--version]

Options:
  –semilla=ENTERO, -s ENTERO         Semilla del generador de números aleatorios.
  --numero=ENTERO, -n ENTERO         Número de números aleatorios a generar. [default: 1]
  --norm, -N                         Generar números aleatorios normalizados en el rango 0 ≤ x < 1.
  --help, -h                         Mostrar la ayuda.
  --version                          Mostrar la versión.

"""

from docopt import docopt
from datetime import datetime as dt
from aleatorios import *


if __name__ == '__main__':
  
    arguments = docopt(__doc__, version="Generador de Numeros Aleatorios 1.1")
    if arguments['aleat']:
      semilla = None
      if semilla == None:
          semilla = hash(dt.now())
          numero = int(arguments['--numero'])
          norm = arguments['--norm']
          rand = Aleat(semilla, numero, norm)
          for _ in range(1):
            print(next(rand))
          print("Se ha realiazado correctamente")  



      
            



