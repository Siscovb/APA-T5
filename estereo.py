"""
    Quinta tarea : Sonido estéreo y ficheros WAVE

    Nombre y apellidos: Joan Marc Fuentes Soler
"""

import struct as st

def Bits2fmt(BitsPerSample):
    """ 
    Convierte los bits en formato WAVE 
    """
    if BitsPerSample == 8:
        return 'b'
    elif BitsPerSample == 16:
        return 'h'
    elif BitsPerSample == 32:
        return 'i'
    else:
        raise ValueError('El número de bits debe ser 8, 16 o 32')

def leeWave(ficWave):
    """
    Lee el fichero 'ficWave', que ha de ser del tipo WAVE y devuelve
    una tupla con la información más relevante contenida en el mismo:
    """
    with open(ficWave, 'rb') as freadWave:

        fmtFormat = '4sI4s4sIH'
        buffer = freadWave.read(st.calcsize(fmtFormat))
        (ChunkID, ChunkSize, format, SubchunkID,
         SubChunkSize, AudioFormat) = st.unpack(fmtFormat, buffer)
        if format == b'WAVE' and AudioFormat == 1:
            formato = '<HIIHH4sI'
            buffer = freadWave.read(st.calcsize(formato))
            (numChannels, SampleRate, ByteRate, BlockAlign,
             BitPerSample, SubChunk2Id, SubChunk2Size) = st.unpack(formato, buffer)
            longSen = SubChunk2Size // BlockAlign
            if numChannels == 1:
                fmtData = '<' + str(longSen) + Bits2fmt(BitPerSample)
            elif numChannels == 2:
                fmtData = '<' + str(longSen*2) + Bits2fmt(BitPerSample)
            buffer = freadWave.read(st.calcsize(fmtData))
            data = st.unpack(fmtData, buffer)
        else:
            raise ValueError(
                'El formato del fichero no corresponde con el de un fichero WAVE')

    return (numChannels, SampleRate, BitPerSample, data)


def escrWave(ficWave, /, *, numChannels=2, SampleRate=44100, BitsPerSample=16, data=[]):
    """
    Escribe la señal almacenada en el objeto tipo bytes 'data' en el fichero 'ficWave' con
    formato WAVE. Supondremos que la señal estará codificada como PCM lineal.
    """
    with open(ficWave, 'wb') as fwriteWave:
        NumSamples = len(data)
        SubChunk1Size = 16
        SubChunk2Size = (NumSamples * numChannels * (BitsPerSample//8))
        ChunkSize = 4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
        ByteRate = (SampleRate * numChannels * (BitsPerSample//8))
        BlockAlign = numChannels * BitsPerSample//8
        longSen = SubChunk2Size // BlockAlign
        formato = '<4sI4s4sIHHIIHH4sI' + str(NumSamples) + Bits2fmt(BitsPerSample)
        estructura = st.pack(formato, b'RIFF', ChunkSize, b'WAVE', b'fmt ', SubChunk1Size, 1, numChannels, SampleRate, 
                             ByteRate,BlockAlign, BitsPerSample, b'data', SubChunk2Size, *data)
        fwriteWave.write(estructura)


def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, 
    con una señal monofónica. El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:
    · canal=0: Se almacena el canal izquierdo. [L]
    · canal=1: Se almacena el canal derecho. [R]
    · canal=2: Se almacena la semisuma. [(L + R)/2] Es la opción por defecto.
    · canal=3: Se almacena la semidiferencia. [(L - R)/2]
    
    """
    numChannels, SampleRate, BitPerSample, data = leeWave(ficEste)
    data += (0, )
    if canal == 0:
        escrWave(ficMono, numChannels=1, SampleRate=SampleRate, BitsPerSample=BitPerSample, data=data[0::2])

    elif canal == 1:
        escrWave(ficMono, numChannels=1, SampleRate=SampleRate, BitsPerSample=BitPerSample, data=data[1::2])

    elif canal == 2:
        dataLR = ((dataL + dataR) // 2 for dataL, dataR in zip(data[::2], data[1::2]))
        escrWave(ficMono, numChannels=1, SampleRate=SampleRate, BitsPerSample=BitPerSample, data=list(dataLR))

    elif canal == 3:
        dataLR = ((dataL - dataR) // 2 for dataL, dataR in zip(data[::2], data[1::2]))
        escrWave(ficMono, numChannels=1, SampleRate=SampleRate, BitsPerSample=BitPerSample, data=list(dataLR))


def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales 
    izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero ficEste.
    """
    numCanalesLeft, SampleRateL, BitPerSampleL, dataL = leeWave(ficIzq)
    numCanalesRight, SampleRateR, BitPerSampleR, dataR = leeWave(ficDer)
    data = [data for pair in zip(dataL, dataR) for data in pair]

    escrWave(ficEste, numChannels=2, SampleRate=SampleRateL, BitsPerSample=BitPerSampleL, data=data)


def codEstereo(ficEste, ficCod):
    """
    Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
    y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas 
    monofónicos como por sistemas estéreo preparados para ello.
    """
    numChannels, sampleRate, bitsPerSample, data = leeWave(ficEste)
    dataCod = []
    for i in range(0, len(data), 2):
        dataL = data[i]
        dataR = data[i + 1]
        dataSUMA = (dataL + dataR) // 2
        dataDIF = (dataL - dataR) // 2
        dataCod.append(dataSUMA)
        dataCod.append(dataDIF)
    escrWave(ficCod, numChannels=1, SampleRate=sampleRate, BitsPerSample=32, data=dataCod)


def decEstereo(ficCod, ficDec):
    """
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia,
    y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los ficheros WAVE estéreo.
    """
    numChannels, sampleRate, bitsPerSample, data = leeWave(ficCod)
    dataL = []
    dataR = []
    for i in range(0, len(data), 2):
        dataSUMA = data[i]
        dataDIF = data[i + 1]
        L = (dataSUMA + dataDIF) // 2
        R = (dataSUMA - dataDIF) // 2
        dataL.append(L)
        dataR.append(R)
    DataALL = []
    for l, r in zip(dataL, dataR):
        DataALL.append(l)
        DataALL.append(r)
    escrWave(ficDec, numChannels=2, SampleRate=sampleRate, BitsPerSample=16, data=DataALL)


