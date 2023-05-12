import struct as st
def estereo2mono (ficEste, ficMono, canal=2):

    with open(ficEste, 'rb') as ficEn:
        cabecera = '<4sI4s'  
        buffer = ficEn.read(st.calcsize(cabecera))
        chunkID, chunksize, formatt = st.unpack(cabecera, buffer)

        formato = '<4sI2H2I2H'         
        buffer = ficEn.read(st.calcsize(formato)) 
        (subChunkID, subChunkSize, audioFormat,numChannels, sampleRate, byteRate,blockAlign, BitsxSample) = st.unpack(formato, buffer)

        cabecera = '<4sI'         
        buffer = ficEn.read(st.calcsize(cabecera))
        subChunk2ID, subChunk2Size = st.unpack(cabecera, buffer)

        numMuestras = subChunk2Size // blockAlign
        datos = f'<{numMuestras}h' 
        buffer = ficEn.read(st.calcsize(datos))
        Datos = st.unpack(datos, buffer)
        DatosL=Datos[0::2]
        DatosR=Datos[1::2]
        semisuma= [(dl+dr)//2 for dl,dr in zip(DatosL,DatosR)]
        semiresta= [(dl-dr)//2 for dl,dr in zip(DatosL,DatosR)]
        cabeceraOut = st.pack('4sI4s4sIhhIIhh4sI', chunkID, (36+subChunk2Size), formatt, subChunkID, subChunkSize,
                            audioFormat,numChannels, sampleRate, byteRate, blockAlign, BitsxSample, subChunk2ID, subChunk2Size)
        with open(ficMono, 'wb') as Fsal:
            Fsal.write(cabeceraOut)
            if canal == 0:
                binario = st.pack(f'{len(DatosL)}i', *DatosL)
                Fsal.write(binario)
            if canal == 1:
                binario = st.pack(f'{len(DatosR)}i', *DatosR)
                Fsal.write(binario)
            if canal == 2:
                binario = st.pack(f'{len(semisuma)}i', *semisuma)
                Fsal.write(binario)
            if canal == 3:
                binario = st.pack(f'{len(semiresta)}i', *semiresta)
                Fsal.write(binario)
            
        
        




        

    
