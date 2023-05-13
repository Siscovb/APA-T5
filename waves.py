import struct as st

def abrewave(fichero):
    with open(fichero, "rb") as ficwave:
        cabecera = "<4sI4s "
        buffer = ficwave.read(st.calcsize(cabecera))
        chunkID , chunkSize , Format = st.unpack(cabecera,buffer)
        if chunkID != b"RIFF" or Format != b"WAVE":
            raise Exception("Fichero no es Wave") from None
        cabecera = "<4sI2H2I2H"
        buffer = ficwave.read(st.calcsize(cabecera))
        (subchunk1ID, subchunk1size, audioformat, numchannels, samplerate, byterate, blockalign, bitspersamble )= st.unpack(cabecera,buffer)

        cabecera = "<4sI"
        buffer = ficwave.read(st.calcsize(cabecera))
        (subchunk2ID, subchunk2size ) = st.unpack(cabecera,buffer)
        nummuestras = subchunk2size/blockalign
        formato = f"<{nummuestras}h"
        if numchannels==1:
            cabecera = '<' + str(nummuestras)
        buffer = ficwave.read(st.calcsize(cabecera))
        datos = st.unpack(formato , buffer)


    return (numchannels, samplerate, bitspersamble, datos)
# chunkID , chunkSize , Format, subchunk1ID, subchunk1size, audioformat, numchannels, samplerate, byterate, blockalign, bitspersamble


