"""
Tarea 5b: Programa para acceder a gestión de señales de audio y estéreo de estereo.py
Nombre y Apellidos: Johny Silva Mendes

"""

USAGE= """
estereoMod.py

Usage:
  estereoMod.py [mono] [options] <ficL> [<ficR>] <ficEste>
  estereoMod.py --help
  estereoMod.py --version

Options:
  --left, -l    Usa el canal izquierdo de la señal estereo [default: False]
  --right, -r   Usa el canal derecho de la señal estereo  [default: False]
  --suma, -s    Usa la semi-suma de los dos canales [default: False]
  --diferencia, -d   Usa la semi-diferencia de los dos canales [default: False]
"""
import struct 
import wave
import numpy as np
from docopt import docopt

def abrewave(fichero):
    """
    lee y devuelve el numero de bits, cantidad de canales, freq de muestreo i los datos en una tupla
    """
    with open(fichero, "rb") as fpWave:
        cabecera = '<4sI4s'
        # Leer y desempaquetar la cabecera del archivo
        chunkID, chunkSize, formato = struct.unpack(cabecera, fpWave.read(struct.calcsize(cabecera)))
        if chunkID != b'RIFF' or formato != b'WAVE':
            raise Exception('El fichero no tiene formato wave')

        fmtCap = '<4sI2H2I2H'
        # Leer y desempaquetar la subcabecera del formato
        (subChunk1ID, subChunk1Size, audioFormat, numChannels,
        sampleRate, byteRate, blockAlign, bitsPerSample) = struct.unpack(fmtCap, fpWave.read(struct.calcsize(fmtCap)))

        fmtData = '<4sI'
        # Leer y desempaquetar la subcabecera de los datos
        subChunk2ID, subChunk2Size = struct.unpack(fmtData, fpWave.read(struct.calcsize(fmtData)))
        data = fpWave.read(subChunk2Size)

        bytesPerSample = bitsPerSample // 8
        fmtSample = 'h' if bytesPerSample == 2 else 'h'  # Utilizar 'h' tanto para muestras de 16 bits como de 32 bits

        if numChannels == 1:
            numSamples = subChunk2Size // bytesPerSample
            fmtSen = '<' + str(numSamples) + fmtSample
            # Desempaquetar la señal monofónica
            senyal = [struct.unpack(fmtSen, data)]

        elif numChannels == 2:
            numSamples = subChunk2Size // (bytesPerSample * 2)
            fmtSen = '<' + str(numSamples * 2) + fmtSample
            # Desempaquetar la señal estéreo
            senyal = struct.unpack(fmtSen, data)
            senyal = [senyal[::2], senyal[1::2]]

    return senyal, sampleRate




def writeWave(fileWave, senyal, sampleRate):
    '''
    Escribe un archivo WAV a partir de una señal de audio dada 
    '''
    with open(fileWave, 'wb') as fpWave:
        # Tamaño total del chunk del archivo WAV
        chunkSize = 44 + 2 * len(senyal[0]) + 2 * (len(senyal[1]) if len(senyal) > 1 else 0)
        # Escribir los primeros 12 bytes de la cabecera del archivo WAV
        fpWave.write(struct.pack('<4sI4s', b'RIFF', chunkSize, b'WAVE'))

        # Escribir los siguientes 24 bytes de la cabecera del archivo WAV
        fpWave.write(struct.pack('<4sI2H2I2H', b'fmt ', 16, 1, len(senyal), sampleRate, 16 // 8 * sampleRate * len(senyal), len(senyal) * 16 // 8, 16))

        # Número total de muestras en la señal
        numMuestras = len(senyal[0]) + (len(senyal[1]) if len(senyal) > 1 else 0)
        # Escribir los siguientes 8 bytes de la cabecera del archivo WAV
        fpWave.write(struct.pack('<4sI', b'data', 2 * numMuestras))

        # Formato de empaquetado de las muestras de audio
        fmtSen = '<' + str(numMuestras) + 'h'

        if len(senyal) == 1:
            # Señal mono: escribir las muestras directamente en el archivo WAV
            fpWave.write(struct.pack(fmtSen, *senyal[0]))

        elif len(senyal) == 2:
            # Señal estéreo: combinar las muestras de ambos canales y escribir en el archivo WAV
            sen = [None] * (len(senyal[0]) + len(senyal[1]))
            sen[::2] = senyal[0]
            sen[1::2] = senyal[1]
            fpWave.write(struct.pack(fmtSen, *sen))


# ESTEREO A MONO 
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, con una señal monofónica.
    El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:
    canal=0: Se almacena el canal izquierdo (L)
    canal=1: Se almacena el canal derecho (R)
    canal=2: Se almacena la semisuma [(L+R)/2] esta es la opcion por defecto
    canal=3: Se almacena la semidiferencia [(L-R)/2]
    """
    # Leer la señal estéreo y la frecuencia de muestreo del archivo de entrada
    senyal, sampleRate = abrewave(ficEste)
    
    if canal == 0:
        # Almacenar el canal izquierdo L en el archivo de salida
        writeWave(ficMono, [senyal[0]], sampleRate)
    elif canal == 1:
        # Almacenar el canal derecho R en el archivo de salida
        writeWave(ficMono, [senyal[1]], sampleRate)
    elif canal == 2:
        # Calcular la semisuma (L+R)/2 y almacenarla en el archivo de salida
        semisuma = [(v1 + v2) // 2 for v1, v2 in zip(senyal[0], senyal[1])]
        writeWave(ficMono, [semisuma], sampleRate)
    elif canal == 3:
        # Calcular la semidiferencia (L-R)/2 y almacenarla en el archivo de salida
        semidiferencia = [(v1 - v2) // 2 for v1, v2 in zip(senyal[0], senyal[1])]
        writeWave(ficMono, [semidiferencia], sampleRate)


# MONO A ESTEREO
def mono2estereo(ficIzq, ficDer, ficEste):      
    '''
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales
    izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
    ficEste.
    '''
    # Leer la señal y la frecuencia de muestreo del canal izquierdo del archivo de entrada
    signalIzq, sampleRate = abrewave(ficIzq)
    # Leer la señal y la frecuencia de muestreo del canal derecho del archivo de entrada
    signalDer, sampleRate = abrewave(ficDer)
    # Concatenar las señales de ambos canales y almacenar la señal estéreo resultante en el archivo de salida
    writeWave(ficEste, [*signalIzq, *signalDer], sampleRate)


# CODIFICADOR ESTEREO 
def codEstereo(ficEste, ficCod):
    """
    Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
    y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas 
    monofónicos como por sistemas estéreo preparados para ello.

    """
    # Leer la señal estéreo y la frecuencia de muestreo del archivo de entrada
    senyal, sampleRate = abrewave(ficEste)
    
    with open(ficCod, 'wb') as fpWave:
        # Calcular el tamaño del chunk del archivo de salida
        chunkSize = 44 + 32 // 8 * len(senyal[0]) + 32 // 8 * (len(senyal[1]) if len(senyal) > 1 else 0)
        fmtRiff = '<4sI4s'
        fpWave.write(struct.pack(fmtRiff, b'RIFF', chunkSize, b'WAVE'))
        
        fmtCap = '<4sI2H2I2H'
        # Escribir la subcabecera del formato del archivo de salida
        fpWave.write(struct.pack(fmtCap, b'fmt ', 16, 1, 1, sampleRate, 32 // 8 * sampleRate * 1, 1 * 32 // 8, 32)) #1:audioformat fmlineal
        
        fmtData = '<4sI'
        numMuestras = len(senyal[0]) + (len(senyal[1]) if len(senyal) > 1 else 0)
        # Escribir la subcabecera de los datos de audio del archivo de salida
        fpWave.write(struct.pack(fmtData, b'data', 32 // 8 * numMuestras))
        
        fmtSen = '<' + str(numMuestras) + 'h'
        
        # Calcular la semisuma y la semidiferencia de los canales estéreo
        semisuma = [(v1 + v2) // 2 for v1, v2 in zip(senyal[0], senyal[1])]
        semidiferencia = [(v1 - v2) // 2 for v1, v2 in zip(senyal[0], senyal[1])]
        
        # Concatenar de las muestras de semisuma y semidiferencia en una única lista
        sen = [None] * (len(semisuma) + len(semidiferencia))
        sen[::2] = semisuma
        sen[1::2] = semidiferencia
        
        # Escribir los datos de audio en el archivo de salida
        fpWave.write(struct.pack(fmtSen, *sen))



# DECODIFICADOR ESTEREO 
def decEstereo(ficCod, ficEste):
    '''
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
    semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los
    ficheros WAVE estéreo.
    '''    
    # Leer la señal monofónica y la frecuencia de muestreo del archivo de entrada
    senyal, sampleRate = abrewave(ficCod)
    
    with open(ficEste, 'wb') as fpWave:
        # Calcular el tamaño del chunk del archivo de salida
        chunkSize = 44 + 2 * len(senyal[0]) + 2 * (len(senyal[1]) if len(senyal) > 1 else 0)
        fmtRiff = '<4sI4s'
        fpWave.write(struct.pack(fmtRiff, b'RIFF', chunkSize, b'WAVE'))
        
        fmtCap = '<4sI2H2I2H'
        # Escribir la subcabecera del formato del archivo de salida
        fpWave.write(struct.pack(fmtCap, b'fmt ', 16, 1, 2, sampleRate, 16 // 8 * sampleRate * 2, 2 * 16 // 8, 16)) #1:audioformat fmlineal
        
        fmtData = '<4sI'
        numMuestras = len(senyal[0]) + (len(senyal[1]) if len(senyal) > 1 else 0)
        # Escribir la subcabecera de los datos de audio del archivo de salida
        fpWave.write(struct.pack(fmtData, b'data', 2 * numMuestras))
                       
        fmtSen = '<' + str(numMuestras) + 'h'
        
        # Extraer la semisuma y la semidiferencia de la señal de entrada
        semisuma = senyal[0][::2]
        semidiferencia = senyal[0][1::2]
        
        # Calcular los canales izquierdo y derecho de la señal estéreo de salida
        sen = [None] * (len(semisuma) + len(semidiferencia))
        sen[::2] = [v1 + v2 for v1, v2 in zip(semisuma, semidiferencia)]
        sen[1::2] = [v1 - v2 for v1, v2 in zip(semisuma, semidiferencia)]
        
        # Escribir los datos de audio en el archivo de salida
        fpWave.write(struct.pack(fmtSen, *sen))



def main():
    args = docopt(USAGE, version="estereoMod.py - Johny Silva Mendes, 2023")
    
    # Procesamiento de los argumentos y opciones
    ficL = args['<ficL>']
    ficR = args['<ficR>']
    ficEste = args['<ficEste>']
    ficMono = args['<ficMono>']
    canal = 0

    if args['mono']:
        # Lógica para procesar el caso de conversión de estéreo a mono
        if args['--left']:
            canal = 0
        elif args['--right']:
            canal = 1
        elif args['--suma']:
            canal = 2
        elif args['--diferencia']:
            canal = 3

        # Llamada a la función estereo2mono
        estereo2mono(ficEste, ficMono, canal)
    else:
        # Lógica para procesar el caso de conversión de mono a estéreo
        # Llamada a la función mono2estereo
        mono2estereo(ficL, ficR, ficEste)

if __name__ == '__main__':
    main()