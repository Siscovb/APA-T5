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

        if numChannels == 2:
            numMuestras = (subChunk2Size // blockAlign) * 2 #Com que es estereo --> 2 elements cada mostra
            datos = f'<{numMuestras}h'    
            buffer = fpwave.read(st.calcsize(datos))
            Datos = st.unpack(datos, buffer)

        if numChannels == 1:
            numMuestras = (subChunk2Size // blockAlign) 
            datos = f'<{numMuestras}h'    
            buffer = fpwave.read(st.calcsize(datos))
            Datos = st.unpack(datos, buffer)

        return (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate, blockAlign, 
        BitsxSample, subChunk2ID, subChunk2Size, Datos)
    
    
def creaCabeceraWAVE(sampleRate, numCanales, bitsPerSample, DataSize):
    # Cabecera de un fichero wave sin datos
    chunkID = b'RIFF'
    chunksize = 36 + DataSize
    formatt = b'WAVE'
    subChunkID = b'fmt '
    subChunkSize = 16
    audioFormat = 1
    numChannels = numCanales
    bytesPorSegundo = sampleRate * numCanales * (bitsPerSample // 8)
    blockAlign = numCanales * (bitsPerSample // 8)
    subChunk2ID = b'data'
    
    # Estructura de la cabecera del fichero wave
    estructura = f'< 4s I 4s 4s I h h I I h h 4s I'
    
    # Empaquetamos los datos de la cabecera utilizando la estructura especificada
    cabecera = st.pack(estructura, chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
                                   numChannels, sampleRate, bytesPorSegundo,
                                   blockAlign, bitsPerSample, subChunk2ID, DataSize)

    
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
    CanalLBin = st.pack(f'{len(CanalL)}h', *CanalL) 

    CanalR = mostres[1::2]
    CanalRBin = st.pack(f'{len(CanalR)}h', *CanalR)

    semiSuma = ((CanalL[i] + CanalR[i]) // 2 for i in range(len(CanalR))) 
    semiSumaBin = st.pack(f'{len(CanalR)}h', *semiSuma)

    semiResta = ((CanalL[i] - CanalR[i]) // 2 for i in range(len(CanalR))) 
    semiRestaBin = st.pack(f'{len(CanalR)}h', *semiResta)

    cabecera = creaCabeceraWAVE(sampleRate, 1, 16, len(CanalLBin))     

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
    #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostresL) = abreWave(ficIzq)
    
    #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostresR) = abreWave(ficDer)
    
    #Ajuntem les mostres com a L1, L2, R1, R2
    
    # mostres_stereo = []
    # for i in range(len(mostresR)):
    #     mostres_stereo.append(mostresL[i]) 
    #     mostres_stereo.append(mostresR[i])
    # Fent COMPREHENSION:
    mostres_stereo = [valor for parell in zip(mostresL, mostresR) for valor in parell]

    #Fem nova cabecera
    cabecera = creaCabeceraWAVE(sampleRate, 2, BitsxSample, len(mostres_stereo))

    #Creem i passem a bytes les mostres
    with open(ficEste, 'wb') as fout: 
        fout.write(cabecera)
        fout.write(st.pack(f'{len(mostres_stereo)}h', *mostres_stereo))


def codEstereo(ficEste, ficCod):
    """Lee el fichero ficEste que contiene una señal estéreo codificada con PCM lineal de 16 bits, 
    y construye con ellas una señal codificada con 32 bits que permita su reproducción 
    tanto por sistemas monofónicos como por sistemas estéreo preparados para ello.
    """
    #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostres) = abreWave(ficEste)
    
    estereo2mono(ficEste, 'wav\mono2.wav', canal = 2)
    estereo2mono(ficEste, 'wav\mono3.wav', canal = 3)


    # #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostresSS) = abreWave('wav\mono2.wav')
    
    # #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostresSR) = abreWave('wav\mono3.wav')
    
    mostres_codStereo = [valor for parell in zip(mostresSS, mostresSR) for valor in parell]

    cabecera = creaCabeceraWAVE(sampleRate, 2, 32, len(mostres_codStereo))

    with open(ficCod, 'wb') as fout:
        fout.write(cabecera)
        fout.write(st.pack(f'{len(mostres_codStereo)}h', *mostres_codStereo))


def decEstereo(ficCod, ficEste):
    """Lee el fichero ficCod con una señal monofónica de 32 bits 
    en la que los 16 bits más significativos contienen la semisuma 
    de los dos canales de una señal estéreo y los 16 bits menos 
    significativos la semidiferencia, y escribe el fichero ficEste 
    con los dos canales por separado en el formato de los ficheros WAVE estéreo.
    """

    #utlilitzem la funció creada per extreue les dades del fitxer:
    (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2ID, mostres) = abreWave(ficCod)
    
    Semisuma = mostres[0::2]
    Semiresta = mostres[1::2]

    CanalL = [(Semisuma[i] + Semiresta[i]) for i in range(len(Semisuma))]
    CanalR = [(Semisuma[i] - Semiresta[i]) for i in range(len(Semisuma))]

    mostres_stereo = [valor for parell in zip(CanalL, CanalR) for valor in parell]

    cabecera = creaCabeceraWAVE(sampleRate, 2, 16, len(CanalL))

    with open(ficEste, 'wb') as fout:
        fout.write(cabecera)
        fout.write(st.pack(f'{len(mostres_stereo)}h', *mostres_stereo))


