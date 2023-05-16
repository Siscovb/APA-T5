#! /usr/bin/python3

"""
    Cuarta tarea : Generación de números aleatorios

    Nombre y apellidos: Joan Marc Fuentes Soler

    
    >>> rand = Aleat(m=32, a=9, c=13, x0=11)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    16
    29
    18
    15
    >>> rand(29)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    18
    15
    20
    1
    >>> rand = aleat(m=64, a=5, c=46, x0=36)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    34
    24
    38
    44
    >>> rand.send(24)
    38
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    44
    10
    32
    14

"""

class Aleat:

    def __init__(self, m=2**48, a=25214903917, c=11, x0=1212121):
        """
        Definimos los valores iniciales (m,a,c,x0).
        """
        self.m = m
        self.a = a
        self.c = c
        self.x = x0
    
    def  __next__(self):
        """
        Generamos el valor y devuelve el siguiente valor.
        """
        self.x = (self.a * self.x + self.c) % self.m
        return self.x


    def __call__(self,num): 
        """
        Reiniciar la secuencia con la semilla indicada en su único argumento.
        """
        self.x = num

    def send(self, num):
        self.x = num 
        return next(self)
    
def aleat(m=2**48, a=25214903917, c=11,x0=1212121):
    """
    Esta función aleat() tiene el mismo algoritmo pero sin crear un objecto iterable
    """
    x = x0
    while True:
        x = (a * x + c) % m
        num = yield x
        if num is not None:
            x = num

import doctest
doctest.testmod()