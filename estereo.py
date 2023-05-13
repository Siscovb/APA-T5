"""
TasK 5 

NOMBRE I APELLIDOS: POL SEDÓ i MOTA

"""

import struct as st

def BitsCabecera(bitspersample):
    """
    bits en formato de cabeceras WAVE
    """
    if bitspersample == 8:
        return 'b'
    elif bitspersample == 16:
        return 'h'
    elif bitspersample ==32:
        return 'i'
    else: 
        raise ValueError('Numero de bits x sampe incorrecto (8, 16, 32)')

def abrewave(fichero):
    """
    lee y devuelve el numero de bits, cantidad de canales, freq de muestreo i los datos en una tupla
    """
    with open(fichero, "rb") as ficwave:
        cabecera = "<4sI4s "
        buffer = ficwave.read(st.calcsize(cabecera))
        chunkID , chunkSize , Format = st.unpack(cabecera,buffer)
        if chunkID != b"RIFF" or Format != b"WAVE":
            raise Exception("Fichero no es Wave") from None
        cabecera = "<4sI2H2I2H"
        buffer = ficwave.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat, numchannels, samplerate, byterate, blockalign, bitspersample )= st.unpack(cabecera,buffer)

        cabecera = "<4sI"
        buffer = ficwave.read(st.calcsize(cabecera))
        (subchunk2ID, subchunk2size ) = st.unpack(cabecera,buffer)
        nummuestras = subchunk2size/blockalign
        formato = f"<{nummuestras}h"
        if numchannels==1:
            cabecera = '<' + str(nummuestras) + BitsCabecera(bitspersample)
        elif numchannels==2:
            cabecera = '<' + str(nummuestras*2) + BitsCabecera(bitspersample)
        buffer = ficwave.read(st.calcsize(cabecera))
        datos = st.unpack(formato , buffer)


    return (numchannels, samplerate, bitspersample, datos)
    # chunkID , chunkSize , Format, subchunk1ID, subchunk1size, audioformat, numchannels, samplerate, byterate, blockalign, bitspersamble

def WriteWave(fichero, /, *, numchannels=2, samplerate=44100, bitspersample=16, data=[]):
    """
    Escribe el contenido de la variable data en un fichero WAVE
    """

    with open(fichero, 'wb') as ficwave:
        nummuestras = len(data)
        subchunk1Size = 16
        subchunk2Size = ((nummuestras*(2 if numchannels == 2 else 1))*(bitspersample//8))
        BlockAlign = numchannels * bitspersample//8
        longSen = subchunk2Size//BlockAlign
        ChunkSize = 4 + (8 + subchunk1Size) + (8 + subchunk2Size)
        byterate = ((samplerate*(2 if numchannels == 2 else 1))*(bitspersample//8))
        formato = '<4sI4s4sIHHIIHH4sI' + str(nummuestras) + BitsCabecera(bitspersample)
        struct = st.pack(formato, b'RIFF', ChunkSize, b'WAVE', b'fmt', subchunk1Size, 1, numchannels, samplerate, byterate, BlockAlign, bitspersample, b'data', subchunk2Size, *data)
        ficwave.write(struct)

def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, con una señal monofónica.
    El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:
    canal=0: Se almacena el canal izquierdo (L)
    canal=1: Se almacena el canal derecho (R)
    canal=2: Se almacena la semisuma [(L+R)/2] esta es la opcion por defecto
    canal=3: Se almacena la semidiferencia [(L-R)/2]
    """
    # Leemos los datos del archivo estéreo
    frecuencia, bits, datos = abrewave(ficEste)

    # Procesamos los datos según el valor del argumento canal
    if canal == 0:
        datos_mono = datos[::2]
    elif canal == 1:
        datos_mono = datos[1::2]
    elif canal == 2:
        datos_mono = [(x + y) / 2 for x, y in zip(datos[::2], datos[1::2])]
    elif canal == 3:
        datos_mono = [(x - y) / 2 for x, y in zip(datos[::2], datos[1::2])]
    else:
        raise ValueError("Valor de canal no válido")

    # Escribimos los datos procesados en el archivo mono
    WriteWave(ficMono, numchannels=1, samplerate=frecuencia, bitspersample=bits, data=datos_mono)
    
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Combina dos ficheros de audio mono en uno estéreo.
    """
    _, samplerate, bitspersample, data_izq = abrewave(ficIzq)
    _, _, _, data_der = abrewave(ficDer)

    # Combinar las señales mono en una señal estéreo
    data_est = list(zip(data_izq, data_der))

    WriteWave(ficEste, numchannels=2, samplerate=samplerate, bitspersample=bitspersample, data=data_est)

def codEstereo(ficEste, ficCod):
    """
    Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
    y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas 
    monofónicos como por sistemas estéreo preparados para ello.

    """
    # Lectura
    _, samplerate, _, data = abrewave(ficEste)
    
    datosCod = []
    
    for i in range(0, len(data), 2):         # Itera a través de los datos de audio estéreo, de dos en dos
        dataL = data[i]                         # canal esquerra
        dataR = data[i + 1]                     # canal dret
        dataSUMA = (dataL + dataR) // 2            # semisuma
        dataDIF = (dataL - dataR) // 2           # semidif
        datosCod.append(dataSUMA)
        datosCod.append(dataDIF)
    
    WriteWave(ficCod, numChannels=1, SampleRate=samplerate, BitsPerSample=32, data=datosCod)

def decEstereo(ficCod, ficDec):
    """
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia,
    y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los ficheros WAVE estéreo.
    """
    # Lectura
    numchannels, samplerate, bitspersample, data = abrewave(ficCod)
    
    # Asegurarse de que la señal es monofónica de 32 bits
    if numchannels != 1 or bitspersample != 32:
        raise ValueError("El archivo debe contener una señal monofónica de 32 bits")
    
    # Decodifica la señal separando en dos canales 
    datosL= []
    datosR= []
    for i in range(0, len(data), 2):
        dataSUMA = data[i]    
        dataDIF = data[i + 1]       
        sampleL = (dataSUMA + dataDIF) // 2
        sampleR = (dataSUMA - dataDIF) // 2
        datosL.append(sampleL)
        datosR.append(sampleR)
    DatosDec= []
    for L,R in zip(datosL, datosR):         # combina los dos canales intercalando con el zip
        DatosDec.append(L)
        DatosDec.append(R)
    
    WriteWave(ficDec, numChannels=2, sampleRate=samplerate, bitsPerSample=bitspersample, data=DatosDec)
