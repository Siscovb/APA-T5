import struct as st

def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste,"rb") as fpwave:
        cabecera = "<4sI4s"
        buffer = fpwave.read(st.calcsize(cabecera))
        chunkID, chunksize, format = st.unpack(cabecera,buffer)
        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception("Fichero no es wave") from None

        cabecera = "<4sI2H2I2H"
        buffer = fpwave.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat,
        numchannels, samplerate, byterate,
        blockalign, bitspersample) = st.unpack(cabecera,buffer)

        cabecera = "<4sI"
        buffer = fpwave.read(st.calcsize(cabecera))
        subchunk2ID, subchunk2size = st.unpack(cabecera,buffer)
        nummuestras = subchunk2size//blockalign 

        if canal not in [0, 1, 2, 3]:
            raise ValueError("Canal debe ser 0, 1, 2 o 3")

        formato = f"<{nummuestras}h"
        buffer = fpwave.read(st.calcsize(formato))
        datos = st.unpack(formato, buffer)

        if canal == 0:
            datos = datos[::2]  # canal izquierdo
        elif canal == 1:
            datos = datos[1::2]  # canal derecho
        elif canal == 2:
            datos = [(dataL + dataR) // 2 for dataL, dataR in zip(datos[::2], datos[1::2])]# semisuma
        else:
            datos = [(dataL - dataR) // 2 for dataL, dataR in zip(datos[::2], datos[1::2])]  # semidiferencia

    with open(ficMono, "wb") as fpout:
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * blockalign, b'WAVE', b'fmt ', 16, 1, 1, samplerate, byterate // numchannels , blockalign // numchannels, bitspersample, b'data', nummuestras * 2)
        pack1 =  st.pack(cabecera_fmt, *cabecera)
        fpout.write(pack1)
        fpout.write(st.pack(f"<{len(datos)}h", *datos))
    

def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq,"rb") as fpIzq, open(ficDer,"rb") as fpDer:
        # Lectura de la cabecera del archivo del canal izquierdo
        cabecera = "<4sI4s"
        buffer = fpIzq.read(st.calcsize(cabecera))
        chunkID, chunksize, format = st.unpack(cabecera,buffer)
        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception("Fichero no es wave") from None
        
        cabecera2 = '<4sI2H2I2H'
        buffer = fpIzq.read(st.calcsize(cabecera2))
        ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample = st.unpack(cabecera2, buffer)

        cabecera3 = '<4sI'
        buffer = fpIzq.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3, buffer)
        nummuestras = ChunkSize3 // blockalign 

        formato = f'<{nummuestras}h'
        size = st.calcsize(formato)
        buffer = fpIzq.read(size)
        datosIzq= st.unpack(formato, buffer)###error: unpack requires a buffer of 930110 bytes

        # Lectura de la cabecera del archivo del canal derecho
        cabecera = "<4sI4s"
        buffer = fpDer.read(st.calcsize(cabecera))
        chunkID, chunksize, format = st.unpack(cabecera,buffer)
        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception("Fichero no es wave") from None

        cabecera = "<4sI2H2I2H"
        buffer = fpDer.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat,
        numchannels, samplerate, byterate,
        blockalign, bitspersample) = st.unpack(cabecera,buffer)

        cabecera = "<4sI"
        buffer = fpDer.read(st.calcsize(cabecera))
        subchunk2ID, subchunk2size = st.unpack(cabecera,buffer)
        nummuestras = subchunk2size//blockalign 

        formato = f"<{nummuestras}h"
        buffer = fpDer.read(st.calcsize(formato))
        datosDer = st.unpack(formato, buffer)

        # Combinación de los datos de ambos canales
        if len(datosIzq) != len(datosDer):
            raise Exception("Los archivos no tienen la misma duración") from None
        
        datosStereo = [(datosIzq[i], datosDer[i]) for i in range(len(datosIzq))]

        # Escritura del archivo estéreo
        with open(ficEste, "wb") as fpout:
            cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
            cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras * 4)
            fpout.write(st.pack(cabecera_fmt, *cabecera))
            fpout.write(st.pack(f"<{len(datosStereo)}h", *datosStereo))

def codEstereo(ficEste, ficCod):
    with open(ficEste, 'rb') as fest, open(ficCod, 'wb') as fcod:
        # Leer la cabecera del fichero de entrada
        cabecera = "<4sI4s"
        buffer = fest.read(st.calcsize(cabecera))
        chunkID, chunksize, format = st.unpack(cabecera, buffer)
        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception("Fichero no es wave") from None

        cabecera = "<4sI2H2I2H"
        buffer = fest.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat,
         numchannels, samplerate, byterate,
         blockalign, bitspersample) = st.unpack(cabecera, buffer)

        cabecera = "<4sI"
        buffer = fest.read(st.calcsize(cabecera))
        subchunk2ID, subchunk2size = st.unpack(cabecera, buffer)
        nummuestras = subchunk2size // blockalign

        formato = f"<{nummuestras}h"
        buffer = fest.read(st.calcsize(formato))
        datos = list(st.unpack(formato, buffer))

        # Convertir los datos a la representación de 32 bits
        datos_codificados = []
        for dataL, dataR in zip(datos[::2], datos[1::2]):
            semisuma = (dataL + dataR) // 2
            semidiferencia = (dataL - dataR) // 2
            datos_codificados.extend([semisuma, semidiferencia])

        # Escribir la cabecera y los datos codificados en el fichero de salida
        with open(ficCod, "wb") as fpout:
            cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
            cabecera = (b'RIFF', 36 + nummuestras * blockalign, b'WAVE', b'fmt ', 16, 1, 2, samplerate, byterate // numchannels , blockalign // numchannels, bitspersample, b'data', nummuestras * 2)
            pack1 =  st.pack(cabecera_fmt, *cabecera)
            fpout.write(pack1)
            fpout.write(st.pack(f"<{len(datos_codificados)}h", *datos_codificados))

def decEstereo(ficCod, ficEste):
    with open(ficCod, 'rb') as fcod:
        # Leer la cabecera del fichero codificado
        cabecera = "<4sI4s"
        buffer = fcod.read(st.calcsize(cabecera))
        chunkID, chunksize, format = st.unpack(cabecera, buffer)
        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception("Fichero no es wave") from None

        cabecera = "<4sI2H2I2H"
        buffer = fcod.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat,
         numchannels, samplerate, byterate,
         blockalign, bitspersample) = st.unpack(cabecera, buffer)

        cabecera = "<4sI"
        buffer = fcod.read(st.calcsize(cabecera))
        subchunk2ID, subchunk2size = st.unpack(cabecera, buffer)
        nummuestras = subchunk2size // blockalign
        print(nummuestras)
        print("nummuestras")
        formato = f"<{nummuestras}h"
        buffer = fcod.read(st.calcsize(formato))
        print(st.calcsize(formato))
        datos_codificados = list(st.unpack(formato, buffer))###error: unpack requires a buffer of 930110 bytes

        # Decodificar los datos a dos canales separados
        datos_estereo = []
        for i in range(0, len(datos_codificados), 2):
            semisuma = datos_codificados[i]
            semidiferencia = datos_codificados[i + 1]
            dataL = semisuma + semidiferencia
            dataR = semisuma - semidiferencia
            datos_estereo.extend([dataL, dataR])

        # Escribir la cabecera y los datos decodificados en el fichero de salida
        with open(ficEste, "wb") as fpout:
            cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
            cabecera = (b'RIFF', 36 + nummuestras * blockalign, b'WAVE', b'fmt ', 16, 1, 2, samplerate, byterate // numchannels , blockalign // numchannels, bitspersample, b'data', nummuestras * 2)
            pack1 =  st.pack(cabecera_fmt, *cabecera)
            fpout.write(pack1)
            fpout.write(st.pack(f"<{len(datos_estereo)}h", *datos_estereo))