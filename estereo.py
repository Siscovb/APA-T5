"""
    Quinta tarea : Sonido estéreo y ficheros WAVE

    Nombre y apellidos: Joan Marc Fuentes Soler
"""


def leeWave(ficWave):
    """
    Lee el fichero 'ficWave', que ha de ser del tipo WAVE y devuelve
    una tupla con la información más relevante contenida en el mismo:
    """
    ...


def escrWave(ficWave, /, *, numChannels=2, SampleRate=44100, BitsPerSample=16, data=[]):
    """
    Escribe la señal almacenada en el objeto tipo bytes 'data' en el fichero 'ficWave' con
    formato WAVE. Supondremos que la señal estará codificada como PCM lineal.
    """
    ...


def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, 
    con una señal monofónica. El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:
    · canal=0: Se almacena el canal izquierdo. [L]
    · canal=1: Se almacena el canal derecho. [R]
    · canal=2: Se almacena la semisuma. [(L + R)/2] Es la opción por defecto.
    · canal=3: Se almacena la semidiferencia. [(L - R)/2]
    
    """
    ...


def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales 
    izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero ficEste.
    """
    ...


def codEstereo(ficEste, ficCod):
    """
    Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
    y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas 
    monofónicos como por sistemas estéreo preparados para ello.
    """
    ...


def decEstereo(ficCod, ficDec):
    """
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia,
    y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los ficheros WAVE estéreo.
    """
    ...


