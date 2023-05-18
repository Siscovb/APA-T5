"""
aleat.py

Usage:
  aleat.py [--semilla=<semilla> --numero=<numero> --norm] [--help | -h] [--version]

Options:
  --semilla=<semilla>, -s <semilla>   Semilla del generador de números aleatorios.
  --numero=<numero>, -n <numero>      Número de números aleatorios a generar. [default: 1]
  --norm, -N                          Generar números aleatorios normalizados en el rango 0 ≤ x < 1.
  --help, -h                          Mostrar la ayuda.
  --version                           Mostrar el nombre del alumno y el año de realización.
"""

import time
import random
from datetime import datetime as dt
from docopt import docopt


class Aleat:
    def __init__(self, semilla=None):
        self.semilla = semilla if semilla is not None else hash(dt.now())

    def generar_numero_aleatorio(self, norm=False):
        random.seed(self.semilla)
        if norm:
            return random.random()
        else:
            return random.randint(0, 2**48)


def generar_numeros_aleatorios(semilla, numero, norm=False):
    generador = Aleat(semilla)
    for _ in range(numero):
        numero_aleatorio = generador.generar_numero_aleatorio(norm)
        print(numero_aleatorio)


def main():
    arguments = docopt(__doc__, version="aleat.py - Victor Ceballos Fouces, 2023")
    semilla = int(arguments["--semilla"]) if arguments["--semilla"] else None
    numero = int(arguments["--numero"])
    norm = arguments["--norm"]
    if arguments["--version"]:
        print("aleat.py - Victor Ceballos Fouces, 2023")
    elif arguments["--help"]:
        print(__doc__)
    else:
        generar_numeros_aleatorios(semilla, numero, norm)


if __name__ == "__main__":
    main()