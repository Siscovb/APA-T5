"""
Oriol Garcia Moreiras
Sonido estéreo y ficheros WAVE


A continuación se escribiran  las funciones que permitirán el manejo de los canales de
una señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos

Funciones:
"""
from struct import *

def cod_2en1(uno, dos, /, *, numBits=16):
    """
    Codifica dos números de "numBits" bits en un entero del doble de bits, de manera que el
    primero ocupa los numBits bits más significativos y el otro los numBits menos
    significativos.
    La función utiliza el operador de desplazamiento a la izquierda (<<) 
    para mover los bits del primer valor (uno) hacia la izquierda por una
    cantidad de posiciones igual al número de bits especificado (numBits).
    Luego, combina este valor desplazado con el segundo valor (dos) utilizando
    el operador de OR bit a bit (|).

Finalmente, se agrega 2 elevado a la (numBits - 1) para ajustar el valor resultante y asegurarse de que esté dentro del rango válido de valores enteros con signo.
    """
    return (uno << numBits) | dos + 2 ** (numBits - 1)


def dec_2en1(cod, /, *, numBits=16):
    """
    Decodifica los dos números de "numBits" bits codificados en un entero del doble de bits
    en el que el primero los numBits bits más significativos y el seguno los numBits menos
    significativos.
    """
    mascara = (1 << numBits) - 1
    uno = (cod >> numBits)
    dos = (cod & mascara) - 2 ** (numBits - 1)
    return uno, dos


def bits2fmt(bitsPerSample):
    """
    Devuelve la cadena que representa enteros de "bitsPerSample" bits en los formatos
    definidos para la biblioteca "struct".
    Si el número de bits por muestra es 8, devuelve la cadena 'b',
    que indica un número entero con signo de 1 byte.
    Si es 16, devuelve la cadena 'h', que indica un número entero con signo de 2 bytes,
    y si es 32, devuelve la cadena 'i', que indica un número entero con signo de 4 bytes.
    Si el número de bits por muestra no es uno de los tres valores esperados,
    la función genera una excepción ValueError con un mensaje de error explicativo.
    """
    if bitsPerSample == 8:
        return 'b'
    elif bitsPerSample == 16:
        return 'h'
    elif bitsPerSample == 32:
        return 'i'
    else:
        raise ValueError('El número de bits solo puede ser 8, 16 o 32')


def readWave(ficWave):
    """
    Lee el fichero 'ficWave', que ha de ser del tipo WAVE y devuelve una tupla con la información de los siguientes parámetros:
    - numChannels: numero de canales del fichero (1: mono, 2: estéreo, ...)
    - sampleRate: frecuencia de muestreo
    - bitsPerSample: número de bits de cada muestra
    - data objeto del tipo bytes con la señal almacenada en el fichero
    Eleva la excepción ValueError si el formato del fichero no corresponde con el de un
    fichero WAVE codificado con PCM lineal.
    """
    with open(ficWave, 'rb') as fpWav:
        fmtFormat = '4sI4s4sIH'
        buffer = fpWav.read(calcsize(fmtFormat))
        (ChunkID, ChunkSize, format, subchunkID,
        subchunkSize, audioFormat) = unpack(fmtFormat, buffer)
        if format == b'WAVE' and audioFormat == 1:
            formato = '<HIIHH4sI'
            buffer = fpWav.read(calcsize(formato))
            (numChannels, sampleRate, byteRate, blockAlign, 
            bitPerSample, subChunk2Id, subChunk2Size) = unpack(formato, buffer)
            longSen = subChunk2Size // blockAlign 
            if numChannels == 1: fmtData = '<' + str(longSen) + bits2fmt(bitPerSample)
            elif numChannels == 2: fmtData = '<' + str(longSen*2) + bits2fmt(bitPerSample)
            buffer = fpWav.read(calcsize(fmtData))
            data = unpack(fmtData, buffer)
        else:
            raise ValueError('El formato del fichero no corresponde con el de un fichero WAVE')

    return (numChannels, sampleRate, bitPerSample, data)


def writeWave(ficWave, /, *, numChannels=2, sampleRate=44100, bitsPerSample=16, data=[]):
    """
    Toma los datos de audio y los escribe en un archivo en formato Wave,
    junto con la cabecera necesaria para describir los datos de audio almacenados en el archivo.
    """
    with open(ficWave, 'wb') as fpWave:
        NumSamples = len(data)
        Subchunk1Size = 16
        Subchunk2Size = (NumSamples * numChannels * (bitsPerSample//8))
        ChunkSize = 4 + (8 + Subchunk1Size) + (8 + Subchunk2Size)
        ByteRate = (sampleRate * numChannels * (bitsPerSample//8))
        BlockAlign = numChannels * bitsPerSample//8
        longSen = Subchunk2Size // BlockAlign
        formato = '<4sI4s4sIHHIIHH4sI' + str(NumSamples) + bits2fmt(bitsPerSample)
        estructura = pack(formato, b'RIFF', ChunkSize, b'WAVE', b'fmt ', Subchunk1Size, 1, numChannels, sampleRate, ByteRate, BlockAlign, bitsPerSample, b'data', Subchunk2Size, *data)
        fpWave.write(estructura)
    

def estereo2mono(ficEste, ficMono, canal=2):
    """
    Convierte un archivo de audio estéreo en un archivo de audio mono.
    La función toma tres argumentos: "ficEste" es el nombre del archivo de entrada estéreo,
    "ficMono" es el nombre del archivo de salida mono y "canal"
    especifica qué canal de audio se debe utilizar para crear el archivo mono.
    """
    numChannels, sampleRate, bitPerSample, data = readWave(ficEste)
    data += (0, )
    if canal == 0:
        writeWave(ficMono, numChannels=1, sampleRate=sampleRate,
                 bitsPerSample=bitPerSample, data=data[::2])
    elif canal == 1:
        writeWave(ficMono, numChannels=1, sampleRate=sampleRate,
                 bitsPerSample=bitPerSample, data=data[1::2])
    elif canal == 2:
        dataLR = ((dataL + dataR) // 2
                  for dataL, dataR in zip(data[::2], data[1::2]))
        writeWave(ficMono, numChannels=1, sampleRate=sampleRate,
                 bitsPerSample=bitPerSample, data=list(dataLR))
    elif canal == 3:
        dataLR = ((dataL - dataR) // 2
                  for dataL, dataR in zip(data[::2], data[1::2]))
        writeWave(ficMono, numChannels=1, sampleRate=sampleRate,
                 bitsPerSample=bitPerSample, data=list(dataLR))

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Recibe como entrada los nombres de dos archivos de audio en formato WAVE
    para canales izquierdo y derecho, y el nombre del archivo de salida
    en el que se desea guardar el archivo estéreo resultante.

    Primero, se lee la información de ambos archivos de audio usando la función readWave.
    Luego, los datos de ambos canales se combinan en una lista data alternando una
    muestra de cada canal, de modo que se convierten dos canales mono en un canal estéreo.
    Por último, se escribe la información combinada en un archivo WAVE estéreo
    usando la función writeWave.
    """
    numCanalesLeft, sampleRateL, bitPerSampleL, dataL = readWave(ficIzq)
    numCanalesRight, sampleRateR, bitPerSampleR, dataR = readWave(ficDer)
    data = [data for pair in zip(dataL, dataR) for data in pair]

    writeWave(ficEste, numChannels=2, sampleRate=sampleRateL,
             bitsPerSample=bitPerSampleL, data=data)


def codEstereo(ficEste, ficCod):
    """
    Recibe dos nombres de archivo, el primero corresponde a un archivo de audio en
    formato estéreo que será codificado y el segundo corresponde al
    nombre del archivo en el que se guardará el resultado del proceso de codificación.
    En primer lugar, se lee el archivo de audio estéreo utilizando la función readWave(),
    que devuelve cuatro valores: el número de canales, la tasa de muestreo, la profundidad
    de bits y los datos de audio.
    Luego, se calcula la suma y la diferencia de los datos de audio
    correspondientes a los canales izquierdo y derecho,
    utilizando comprensión de listas y la operación aritmética correspondiente.
    A continuación, se combinan los datos de suma y diferencia en un solo arreglo,
    intercalando los valores correspondientes. Estos datos se pasan a la función cod_2en1(),
    que codifica cada par de valores como un solo número entero de 32 bits mediante
    la función cod_2en1().
    Finalmente, los datos codificados se escriben en un archivo de audio utilizando la
    función writeWave(), con el número de canales igual a 1, la profundidad de bits igual a 32
    y los datos de audio codificados.
    """
    numChannels, sampleRate, bitPerSample, data = readWave(ficEste)
    dataSuma = [(dataL + dataR) // 2
                for dataL, dataR in zip(data[::2], data[1::2])]
    dataDif = [(dataL - dataR) // 2
               for dataL, dataR in zip(data[::2], data[1::2])]
    dataCod = [data for pair in zip(dataSuma, dataDif) for data in pair]
    estructura = [cod_2en1(datasum, datadif, numBits=16)
                  for datasum, datadif in zip(dataCod[::2], dataCod[1::2])]
    writeWave(ficCod, numChannels=1, sampleRate=sampleRate,
             bitsPerSample=32, data=estructura)


def decEstereo(ficCod, ficEste):
    """
    Decodifica un archivo de audio estéreo codificado mediante el método de codificación
    estéreo para obtener una señal estéreo con los dos canales separados.
    """
    numChannels, sampleRate, bitPerSample, data = readWave(ficCod)
    dataL, dataR = [], []
    for var in data:
        dataSum, dataDif = dec_2en1(var, numBits=16)
        L = dataSum + dataDif
        R = (dataSum * 2) - L
        dataL.append(L), dataR.append(R)
    dataTot = [data for pair in zip(dataL, dataR) for data in pair]
    writeWave(ficEste, numChannels=2, sampleRate=sampleRate,
             bitsPerSample=16, data=dataTot)

estereo2mono('wav_komm.wav', 'monoI.wav', canal=0)
estereo2mono('wav_komm.wav', 'monoD.wav', canal=1)
mono2estereo('monoI.wav', 'monoD.wav', 'estereo.wav')
codEstereo('wav_komm.wav', 'codificado.wav')
decEstereo('codificado.wav', 'decodificado.wav')