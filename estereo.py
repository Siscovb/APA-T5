"""
PAU PERÁLVAREZ CASASAMPERE

Sonido estéreo y ficheros WAVE
"""

#Primer de tot fem una funció que ens llegeixi els fitxers 'WAVE':
import struct as st

def abreWave(fichero):
    with open(fichero, 'rb') as fpwave:  
        
        cabecera = '<4sI4s'  
        #Ara llegim:
        buffer = fpwave.read(st.calcsize(cabecera))
        #Assignem a les variables el que treiem de buffer (passat de binari a str)
        chunkID, chunksize, formatt = st.unpack(cabecera, buffer)
        if chunkID != b'RIFF' or formatt != b'WAVE':
            raise Exception('El fichero NO es formato WAVE') from None  
        
        subChunk1 = '<4sI2H2I2H'         
        buffer = fpwave.read(st.calcsize(subChunk1)) 
        #Posem un parentesis pq càpiga tot 
        (subChunkID, subChunkSize, audioFormat,
         numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample) = st.unpack(subChunk1, buffer)

        subChunk2 = '<4sI'         
        buffer = fpwave.read(st.calcsize(subChunk2))
        subChunk2ID, subChunk2Size = st.unpack(subChunk2, buffer)

        numMuestras = subChunk2Size // blockAlign
        datos = f'<{numMuestras}h'    
        buffer = fpwave.read(st.calcsize(datos))
        Datos = st.unpack(datos, buffer)

        return (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, Datos)
    
    
def creaCabecera(sampleRate, numCanales, bitsPerSample, duracionSeg):
    # Cabecera de un fichero wave sin datos
    cabeceraRIFF = b'RIFF'
    tamanyoRIFF = 36 + int(sampleRate * numCanales * bitsPerSample/8 * duracionSeg)
    cabeceraWAVE = b'WAVE'
    cabeceraFMT = b'fmt '
    tamanyoFMT = 16
    tipoCompresion = 1
    tamanyoBloque = numCanales * bitsPerSample // 8
    tasaMuestreo = sampleRate
    bytesPorSegundo = tasaMuestreo * tamanyoBloque
    cabeceraDATA = b'data'
    tamanyoDATA = int(sampleRate * numCanales * bitsPerSample/8 * duracionSeg)
    
    # Estructura de la cabecera del fichero wave
    estructura = f'< 4s I 4s 4s I h h I I h h 4s I'.encode('ascii')
    
    # Empaquetamos los datos de la cabecera utilizando la estructura especificada
    cabecera = st.pack(estructura, cabeceraRIFF, tamanyoRIFF, cabeceraWAVE, cabeceraFMT, 
                           tamanyoFMT, tipoCompresion, numCanales, tasaMuestreo, bytesPorSegundo, 
                           tamanyoBloque, bitsPerSample, cabeceraDATA, tamanyoDATA)
    
    return cabecera

    

def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, 
    y escribe el fichero ficMono, con una señal monofónica. 
    El tipo concreto de señal que se almacenará en ficMono 
    depende del argumento canal


    """
    #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostres) = abreWave(ficEste)

    #dividim les mostres per Canal L i R i passem les mostres a binari
    CanalL = mostres[0::2] 
    CanalLBin = st.pack(f'{len(CanalL)}i', *CanalL)

    CanalR = mostres[1::2]
    CanalRBin = st.pack(f'{len(CanalR)}i', *CanalR)

    semiSuma = ((CanalL[i] + CanalR[i]) // 2 for i in range(len(CanalR))) 
    semiSumaBin = st.pack(f'{len(CanalR)}i', *semiSuma)

    semiResta = ((CanalL[i] - CanalR[i]) // 2 for i in range(len(CanalR))) 
    semiRestaBin = st.pack(f'{len(CanalR)}i', *semiResta)

    cabecera = creaCabecera(sampleRate*2, 1, BitsxSample, (len(mostres) // sampleRate*2))

    #Avaluem els diferents casos i ho posem al fitxer ficMono
    with open(ficMono, 'wb') as fout:
        fout.write(cabecera)
        if canal == 0: fout.write(CanalLBin)
        if canal == 1: fout.write(CanalRBin)
        if canal == 2: fout.write(semiSumaBin) 
        if canal == 3: fout.write(semiRestaBin)

        

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas 
    correspondientes a los canales izquierdo y derecho, respectivamente, 
    y construye con ellas una señal estéreo que almacena en el fichero ficEste.


    """


