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
        chunkID, chunkSize, _format = st.unpack(cabecera, buffer)
        if chunkID != b'RIFF' or _format != b'WAVE':
            raise Exception('El fichero NO es  WAVE') from None  
        
        fmtChunck = '<4sI2H2I2H'         
        buffer = fwave.read(st.calcsize(fmtChunck)) 
        (subChunkID, subChunkSize, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsXsample) = st.unpack(fmtChunck, buffer)

        dataChunck = '<4sI'         
        buffer = fwave.read(st.calcsize(dataChunck))
        subChunk2ID, subChunk2Size = st.unpack(dataChunck, buffer)

        nMuestras = subChunk2Size / blockAlign
        _format = f'<{nMuestras}h'    
        
        # Diferenciamos de Estereo o Mono:
        if numChannels == 1:
            header = '<' + str(nMuestras) + nBits(bitsXsample)
        elif numChannels == 2:
            header = '<' + str(nMuestras*2) + nBits(bitsXsample)
            
        buffer = fwave.read(st.calcsize(header))
        data = st.unpack(_format, buffer)

        return (chunkID, chunkSize, _format, subChunkID, subChunkSize, audioFormat, numChannels, sampleRate, byteRate, blockAlign, BitsxSample, subChunk2ID, subChunk2Size, data)

def write_wave(fichero, data, numChannels=2, sampleRate=44100, bitsXsample=16):
    """
    Escribe el contenido de la variable data en un fichero WAVE
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
    pass

def mono2estereo(ficIzq, ficDer, ficEste):
    pass

def codEstereo(ficEste, ficCod):
    pass

def decEstereo(ficCod, ficEste):
    pass