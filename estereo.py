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

        numMuestrasmono = 2*subChunk2Size // blockAlign #dividimos por dos ya que en cada bloque nos interesa dividir los datos de cada canal
        print(numMuestrasmono)
        datos = f'<{numMuestrasmono}h' 
        print(datos)
        buffer = ficEn.read(st.calcsize(datos))
        Datos = st.unpack(datos, buffer)
        print (len(Datos))
    
        DatosL=Datos[0::4]
        print(len(DatosL))
        DatosR=Datos[1::4]
        print(len(DatosR))
        semisuma= [(dl+dr)//2 for  dl,dr in zip(DatosL,DatosR)]
        semiresta= [(dl-dr)//2 for dl,dr in zip(DatosL,DatosR)]
        
        #damos valores para crear cabecera nuevo archivo:
        bitsPerSampleM = 16
        sampleRateM = 16000
        numChannelsM = 1
        subChunk2sizeM = numMuestrasmono * numChannelsM * (bitsPerSampleM//8) //2
        chunkSizeM = 36 + subChunk2sizeM
        byteRateM = sampleRateM * numChannelsM * bitsPerSampleM//8
        blockAlignM = numChannelsM * bitsPerSampleM//8



        cabeceraOut = st.pack('4sI4s4sIhhIIhh4sI', chunkID, chunkSizeM, formatt, subChunkID, subChunkSize,
                            audioFormat, numChannelsM, sampleRateM, byteRateM, blockAlignM , bitsPerSampleM, subChunk2ID, subChunk2sizeM)
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

def mono2estereo(ficIzq, ficDer, ficEste):
    #extraemos datos dicIzq
    with open(ficIzq, 'rb') as izq:
        cabecera = '<4sI4s'  
        buffer = izq.read(st.calcsize(cabecera))
        chunkID, chunksize, formatt = st.unpack(cabecera, buffer)

        formato = '<4sI2H2I2H'         
        buffer = izq.read(st.calcsize(formato)) 
        (subChunkID, subChunkSize, audioFormat,numChannels, sampleRate, byteRate,blockAlign, BitsxSample) = st.unpack(formato, buffer)

        cabecera = '<4sI'         
        buffer = izq.read(st.calcsize(cabecera))
        subChunk2ID, subChunk2Size = st.unpack(cabecera, buffer)

        numMuestras = 8*subChunk2Size//16
        print(numMuestras)
        datosl = f'<{numMuestras}h' 
        buffer = izq.read(st.calcsize(datosl))
        print(len(buffer))
        DatosL = st.unpack(datosl, buffer)
        print(len(DatosL))
        
    #extraemos datos dicDer
    with open(ficDer, 'rb') as der:
        cabecera = '<4sI4s'  
        buffer = der.read(st.calcsize(cabecera))
        chunkID, chunksize, formatt = st.unpack(cabecera, buffer)

        formato = '<4sI2H2I2H'         
        buffer = der.read(st.calcsize(formato)) 
        (subChunkID, subChunkSize, audioFormat,numChannels, sampleRate, byteRate,blockAlign, BitsxSample) = st.unpack(formato, buffer)

        cabecera = '<4sI'         
        buffer = der.read(st.calcsize(cabecera))
        subChunk2ID, subChunk2Size = st.unpack(cabecera, buffer)

        numMuestras =  8*subChunk2Size//16 
        print(numMuestras)
        datosr = f'<{numMuestras}h' 
        buffer = der.read(st.calcsize(datos))
        print(len(buffer))
        DatosR = st.unpack(datosr, buffer)
        print(len(DatosR))
    
    #damos valores para crear cabecera nuevo archivo:
        bitsPerSampleE = 16
        sampleRateE = 16000
        numChannelsE = 2
        subChunk2sizeE = numMuestras * numChannelsE * (bitsPerSampleE//8)
        chunkSizeE = 36 + subChunk2sizeE
        byteRateE = sampleRateE * numChannelsE * bitsPerSampleE//8
        blockAlignE = numChannelsE * bitsPerSampleE//8



    cabeceraOut = st.pack('4sI4s4sIhhIIhh4sI', chunkID, chunkSizeE, formatt, subChunkID, subChunkSize,
                            audioFormat, numChannelsE, sampleRateE, byteRateE, blockAlignE , bitsPerSampleE, subChunk2ID, subChunk2sizeE)
    
    
   
    est = bytearray()
    for i in range(len(DatosR)):
        est.extend(st.pack('h', DatosL[i]))
        est.extend(st.pack('h', DatosR[i]))
    print (len(est))
    
    #i=0
    #datosout=()
    #while i < len(DatosR)+2:
    #    datosout += DatosR[i:i+2] + DatosL[i:i+2]
    #    i+=2
    #print ("longitud datosOut" + len(datosout))
    #binario = st.pack(f'{len(datosout)}i', *datosout)

    with open(ficEste, 'wb') as Fsal:
            Fsal.write(cabeceraOut)
            Fsal.write(est)



    

            
        
        




        

    
