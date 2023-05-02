"""
Oriol Garcia Moreiras
Sonido estéreo y ficheros WAVE

A continuación se escribiran  las funciones que permitirán el manejo de los canales de
una señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos

Funciones:


readWave(ficWave):

writeWave(ficWave, /, *, numChannels=2, sampleRate=44100, bitsPerSample=16, data=[]):

estereo2mono(ficEste, ficMono, canal=2):

mono2estereo(ficIzq, ficDer, ficEste):

codEstereo(ficEste, ficCod):

decEstereo(ficCod, ficEste):


"""

