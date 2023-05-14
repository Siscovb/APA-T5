'''
Pràctcia 5:
    Oriol Garcia Vila 
'''
import struct as st

def nBits(bitsXsample):
    """
    Función para devolver el número de bits en formato de cabeceras WAVE
    """
    if bitsXsample == 8:
        return 'b'
    elif bitsXsample == 16:
        return 'h'
    elif bitsXsample == 32:
        return 'i'
    else: 
        raise ValueError('ERROR: expected (8, 16, 32)')

def abreWave(fichero):
    with open(fichero, 'rb') as fwave:  
        
        cabecera = '<4sI4s'  
        buffer = fwave.read(st.calcsize(cabecera))
        chunkID, chunkSize, fformat = st.unpack(cabecera, buffer)
        if chunkID != b'RIFF' or fformat != b'WAVE':
            raise Exception('El fichero NO es  WAVE') from None  
        
        fmtChunck = '<4sI2H2I2H'         
        buffer = fwave.read(st.calcsize(fmtChunck)) 
        (subChunkID, subChunkSize, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsXsample) = st.unpack(fmtChunck, buffer)

        dataChunck = '<4sI'         
        buffer = fwave.read(st.calcsize(dataChunck))
        subChunk2ID, subChunk2Size = st.unpack(dataChunck, buffer)

        nMuestras = subChunk2Size / blockAlign
        fformat = f'<{nMuestras}h'    
        
        # Diferenciamos de Estereo o Mono:
        if numChannels == 1:
            header = '<' + str(nMuestras) + nBits(bitsXsample)
        elif numChannels == 2:
            header = '<' + str(nMuestras*2) + nBits(bitsXsample)
            
        buffer = fwave.read(st.calcsize(header))
        data = st.unpack(fformat, buffer)

        return (numChannels, sampleRate,  bitsXsample, data)

def creaWave(fichero, data, numChannels=2, sampleRate=44100, bitsXsample=16):
    """
    Escribe el contenido de la variable data en un fichero WAVE despues de crear las cabeceras de los chunks
    """
    numSamples = len(data)
    fmtChunkSize = 16
    dataChunkSize = numSamples * numChannels * (bitsXsample // 8)
    chunkSize = 4 + (8 + fmtChunkSize) + (8 + dataChunkSize)
    blockAlign = numChannels * (bitsXsample // 8)
    byteRate = sampleRate * blockAlign

    with open(fichero, 'wb') as fwave:
        # Cabecera RIFF
        fwave.write(st.pack('<4sI4s', b'RIFF', chunkSize, b'WAVE'))

        # Subchunk fmt
        fwave.write(st.pack('<4sIHHII', b'fmt ', fmtChunkSize, 1, numChannels, sampleRate, byteRate, blockAlign, bitsXsample))

        # Subchunk data
        fwave.write(st.pack('<4sI', b'data', dataChunkSize))
        for sample in data:
            fwave.write(st.pack(f'<{numChannels}h', *sample))

def estereo2mono(ficEste, ficMono, canal=2):
    '''
    La función lee el fichero ficEste, que debe contener una señal estéreo,
    y escribe el fichero ficMono, con una señal monofónica.
    El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:
    
    canal=0: Se almacena el canal izquierdo LL.
    canal=1: Se almacena el canal derecho RR.
    canal=2: Se almacena la semisuma (L+R)/2(L+R)/2. Es la opción por defecto.
    canal=3: Se almacena la semidiferencia (L-R)/2(L−R)/2.
    '''
    (numChannels, sampleRate,  bitsXsample, data) = abreWave(ficEste)

    if numChannels != 2:
        raise ValueError('ERROR: El archivo de entrada no es estéreo')

    if canal == 0:
        # Canal izquierdo
        monoData = [(sample[0],) for sample in data]
    elif canal == 1:
        # Canal derecho
        monoData = [(sample[1],) for sample in data]
    elif canal == 2:
        # Semisuma (L+R)/2
        monoData = [((sample[0] + sample[1])//2,) for sample in data]
    elif canal == 3:
        # Semidiferencia (L-R)/2
        monoData = [((sample[0] - sample[1])//2,) for sample in data]
    else:
        raise ValueError('ERROR: valor de canal no válido')

    creaWave(ficMono, monoData, numChannels=1, sampleRate=sampleRate, bitsXsample=bitsXsample)


def mono2estereo(ficIzq, ficDer, ficEste):
    '''
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas 
    correspondientes a los canales izquierdo y derecho, respectivamente,
    y construye con ellas una señal estéreo que almacena en el fichero ficEste.
    '''

    with open(ficIzq, 'rb') as f1, open(ficDer, 'rb') as f2:
        dataIzq = f1.read() 
        dataDer = f2.read() 

    # Calcular la longitud de los datos de audio
    lenData = min(len(dataIzq), len(dataDer))
    
    with open(ficEste, 'wb') as fwave:
        # Cabecera:
        fwave.write(st.pack('<4sI4s', b'RIFF', 36 + lenData, b'WAVE'))
        # 36 --> Chunk Size

        # Chunk fmt
        fwave.write(st.pack('<4sIHHIIHH', b'fmt ', 16, 1, 2, 44100, 176400, 4, 16))
        # 16 --> Subchunk size
        # 1 --> Audio Format  (PCM)
        # 2 --> num Channels
        # 44100 --> Sample Rate
        # 176400 --> Byte Rate
        # 4 --> Block Align
        # 16 --> Bits x Sample
        
        # Chunk Data
        fwave.write(st.pack('<4sI', b'data', lenData))

        # Combinar los datos de audio de los dos canales en uno solo
        for i in range(0, lenData, 2):
            sample1 = st.unpack('<h', dataIzq[i:i+2])[0]
            sample2 = st.unpack('<h', dataDer[i:i+2])[0]
            sample = st.pack('<hh', sample1, sample2)
            fwave.write(sample)


def codEstereo(ficEste, ficCod):
    """
    Lee el fichero ficEste, que contiene una señal estéreo codificada con
    PCM lineal de 16 bits, y construye con ellas una señal codificada con 32 bits
    que permita su reproducción tanto por sistemas 
    monofónicos como por sistemas estéreo preparados para ello.

    """
    (numChannels, sampleRate,  bitsXsample, data) = abreWave(ficEste)
    
    data32 = []
    
    for i in range(0, len(data), 2):         
        dataLeft = data[i]                         
        dataRight = data[i + 1]                    
        dataSsuma = (dataLeft + dataRight) // 2    
        dataSresta = (dataLeft - dataRight) // 2  
        data32.append(dataSsuma)
        data32.append(dataSresta)
    
    creaWave(ficCod, numChannels=1, sampleRate=sampleRate, bitXsample=32, data=data32)


def decEstereo(ficCod, ficDec):
    """
    Lee el fichero ficCod con una señal monofónica de 32 bits en la que 
    los 16 bits más significativos contienen la semisuma de los dos canales 
    de una señal estéreo y los 16 bits menos significativos la semidiferencia, 
    y escribe el fichero ficEste con los dos canales por separado en el formato de los ficheros WAVE estéreo.
    """
    (numChannels, sampleRate,  bitsXsample, data) = abreWave(ficCod)
    
    # Control de errores (tiene que ser una señal monofonica de 32 bits)
    if numChannels != 1 or bitsXsample != 32:
        raise ValueError("ERROR: expected (32 bits monophonic signal)")
    
    datosLeft= []
    datosRight= []
    for i in range(0, len(data), 2):
        dataSsuma = data[i]    
        dataSresta = data[i + 1]       
        sampleLeft = (dataSsuma + dataSresta) // 2
        sampleRight = (dataSsuma - dataSresta) // 2
        datosLeft.append(sampleLeft)
        datosRight.append(sampleRight)
    dataLR= []
    for left, right in zip(datosLeft, datosRight):    
        dataLR.append(left)
        dataLR.append(right)
    
    creaWave(ficDec, numChannels=2, sampleRate=sampleRate, bitsXsample=bitsXsample, data=dataLR)
    
