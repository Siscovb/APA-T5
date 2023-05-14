"""

Ada Salvador Avalos

"""

import struct as st


def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
    con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
    `canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Es la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

    """
    with open(ficEste, 'rb') as fpwave:
        #cabecera
        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)

        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es wave') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        if numchannels != 2 :
             raise Exception('Fichero no estereo') from None


        if canal not in [0,1,2,3]:
             raise Exception('Canal no válido') from None

        #datos
        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign
       
        formato = f'<{nummuestras*2}h'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datos = st.unpack(formato,buffer4)

    #fichero de salida mono
    with open(ficMono,'wb') as fout :
        #creación cabecera
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * blockalign, b'WAVE', b'fmt ', 16, 1, 1, samplerate, byterate // numchannels , blockalign // numchannels, bitspersample, b'data', nummuestras * 2)
        pack1 =  st.pack(cabecera_fmt, *cabecera)
        fout.write(pack1)

        #datos
        if bitspersample==16 : formato = 'h'
        else : formato = 'b'
        if canal  in [0,1] :
           
            for iter in range(nummuestras) :
                muestra = datos[iter * 2 + canal]
                fout.write(st.pack(formato,muestra))
        else :
            if canal == 2:
                for iter in range(nummuestras ) :
                    muestra = (datos[2* iter] + datos[iter * 2 + 1]) // 2
                    fout.write(st.pack(formato,muestra))
            else :
                for iter in range(nummuestras ) :
                    muestra = (datos[2* iter] - datos[iter * 2 + 1]) // 2
                    fout.write(st.pack(formato,muestra))



def mono2stereo(ficIzq, ficDer, ficEste) :
    """
    Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
    izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
    `ficEste`.
    """
    #canal izquierda
    with open(ficIzq, 'rb') as fin :
        #lectura cabeceras
        cabecera1 = '<4sI4s'
        buffer1 = fin.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1, buffer1)

        if ChunkID != b'RIFF' or format != b'WAVE' :
            raise Exception('El fichero no es WAVE') from None
        
        cabecera2 = '<4sI2H2I2H'
        buffer2 = fin.read(st.calcsize(cabecera2))
        ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample = st.unpack(cabecera2, buffer2)

        if numchannels != 1:
            raise Exception('El fichero no es mono')
        
        # DATOS
        cabecera3 = '<4sI'
        buffer3 = fin.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3, buffer3)
        nummuestras = ChunkSize3 // blockalign

        formato = f'<{nummuestras}h'
        size = st.calcsize(formato)
        buffer4 = fin.read(size)


        datosL= st.unpack(formato, buffer4)

    #canal derecha
    with open(ficDer, 'rb') as fin :
        #lectura cabeceras
        cabecera1 = '<4sI4s'
        buffer1 = fin.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1, buffer1)

        if ChunkID != b'RIFF' or format != b'WAVE' :
            raise Exception('El fichero no es WAVE') from None
        
        cabecera2 = '<4sI2H2I2H'
        buffer2 = fin.read(st.calcsize(cabecera2))
        ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample = st.unpack(cabecera2, buffer2)

        if numchannels != 1:
            raise Exception('El fichero no es mono')
        
        # DATOS
        cabecera3 = '<4sI'
        buffer3 = fin.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3, buffer3)
        nummuestras = ChunkSize3 // blockalign

        formato = f'<{nummuestras}h'
        buffer4 = fin.read(st.calcsize(formato))
        datosR= st.unpack(formato, buffer4)
    
    #ESCRITURA EN EL FICHERO
    with open(ficEste, 'wb') as fout:
        #cabecera
    
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
    
        cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras * 4)
 
        fout.write(st.pack(cabecera_fmt, *cabecera))
        
        #datos
        for muestrasL, muestrasR in zip(datosL, datosR):
            muestrasEstereo = st.pack('<hh' , muestrasL, muestrasR) #'<hh'cada muestra es un entero de 16 bits
            fout.write(muestrasEstereo)


def codEstereo(ficEste, ficCod) :
    """
    Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
    construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
    monofónicos como por sistemas estéreo preparados para ello.
    """
    # lectura fichero
    with open(ficEste, 'rb') as fpwave:

        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)

        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es wave') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        if numchannels != 2 :
             raise Exception('Fichero no estereo') from None


        #datos
        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign
       
        formato = f'<{nummuestras*2}h'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datos = st.unpack(formato,buffer4)


    datosL = []
    datosR = []

    for iter in range(nummuestras) :
        datosL.append(datos[2* iter])
        datosR.append(datos[iter * 2 + 1]) 

    datos_cod = bytearray()
    for muestraL, muestraR in zip(datosL, datosR) :
        semisuma = (muestraL + muestraR) // 2
        semidif = (muestraL - muestraR) // 2
        muestracod = (semisuma << 16) | (semidif >> 16) #semisuma deplaza a izq 16 bits(más significativos) y or con semidif que deplaza a derecha  usando así 16 bits menos significativos.
        datos_cod.extend(st.pack('<i',muestracod))

    
    #escritura en archivo codificado
    with open(ficCod, 'wb') as fout:
        #cabecera
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras *4)
        fout.write(st.pack(cabecera_fmt, *cabecera))

        #datos
        fout.write(datos_cod)


def decEstereo(ficCod, ficEste) :
   """
   Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
    semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los
    ficheros WAVE estéreo.
   """

   with open(ficCod, 'rb') as fpwave:
       
        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)

        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es wave') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        if numchannels != 2 :
             raise Exception('Fichero no estereo') from None


        #datos
        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign
       
        formato = f'<{nummuestras}i'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datoscod = st.unpack(formato,buffer4)
   


        datosL =[]
        datosR = []


        for i in range(nummuestras) :
            semisuma = (datoscod[i] >> 16) 
            semidif =  datoscod[i] & 0x0000ffff   
    
            muestraR = (semisuma - semidif)  
            muestraL = (semidif + semisuma)  
       

            datosL.append(muestraL)
            datosR.append(muestraR)



        #escritura en el fichero estereo
        with open(ficEste,'wb') as fout :
            #cabecera

            cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
    
            cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras * 4)
 

            fout.write(st.pack(cabecera_fmt, *cabecera))

            #datos
            for muestra_L, muestra_R in zip(datosL,datosR) :         
                muestracod =   muestra_L << 16 | muestra_R 
                fout.write(st.pack('<i',muestracod))



estereo2mono('wav\komm.wav','wav\kommMono1.wav',canal=1)
estereo2mono('wav\komm.wav','wav\kommMono0.wav',canal=0)
estereo2mono('wav\komm.wav','wav\kommMono2.wav',canal=2)

mono2stereo("wav\kommMono0.wav","wav\kommMono1.wav","wav\kommStOut.wav")


codEstereo('wav\komm.wav','wav\kommCodec.wav')
decEstereo('wav\kommCodec.wav','wav\kommDeCodec.wav')