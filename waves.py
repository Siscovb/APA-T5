import struct as st

def abreWave(fichero):
    with open(fichero, 'rb') as fpwave:  #AIXÒ ES UN GESTOR DE FICHERO, EL TANCA SOL.
        cabecera = '<4sI4s'  #< = portable LittleEndian (Estem seguint dibuixet del format de WAVE), 4s crec q vol dir 4 bytes s(sense signe) (cabecera = lila)
        
        #Ara llegim:
        buffer = fpwave.read(st.calcsize(cabecera))

        #Assignem a variables el que treiem de buffer (passat de binari a str)
        chunkID, chunksize, formatt = st.unpack(cabecera, buffer)
        if chunkID != b'RIFF' or formatt != b'WAVE':
            raise Exception('El fichero NO es formato WAVE') from None  #el from None, es pq no surti en principi tot el rollo

        formato = '<4sI2H2I2H'         #ho fem amb majuscula per si de cas es molt gran o negatiiu'
        buffer = fpwave.read(st.calcsize(formato)) #Ho lleggiiim

        #Posem un parentesis pq càpiga tot 
        (subChunkID, subChunkSize, audioFormat,
         numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample) = st.unpack(formato, buffer)

        cabecera = '<4sI'         
        buffer = fpwave.read(st.calcsize(cabecera))
        subChunk2ID, subChunk2Size = st.unpack(cabecera, buffer)

        numMuestras = subChunk2Size // blockAlign
        datos = f'<{numMuestras}h'    #entre {} perque serà un numero, es perque substitueixi xx el valor de la variable, la f es pq es fstring
        buffer = fpwave.read(st.calcsize(datos))
        Datos = st.unpack(datos, buffer)


        return (chunkID, chunksize, formatt, subChunkID, subChunkSize, audioFormat,
        numChannels, sampleRate, byteRate,
        blockAlign, BitsxSample, subChunk2ID, subChunk2Size)

    

