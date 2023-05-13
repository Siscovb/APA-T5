from waves import *
##exec(open('waves.py').read())

def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, con una señal monofónica.
    El tipo concreto de señal que se almacenará en ficMono depende del argumento canal.
    """
    with open(ficEste,'rb') as fwave:
        format = '<4sI4s'
        buffer = fwave.read(st.calcsize(format))
        chunkid,chunksize,fmttwave = st.unpack(format, buffer)
        if chunkid != b'RIFF' or fmttwave != b'WAVE':
            raise Exception('Error en el fichero no tiene formato valido') 
        format = '<4sI2H2I2H'
        buffer = fwave.read(st.calcsize(format))
        schunk1ID, schunk1size, aformat, nchannels, srate, bitrate, blockAlign , bitPerSample = st.unpack(format, buffer)
        format = '<4sI'
        buffer = fwave.read(st.calcsize(format))
        schunk2ID, schunk2size = st.unpack(format, buffer)
        numMuestras = schunk2size // blockAlign
        format = f'<{numMuestras}h'
        buffer = fwave.read(st.calcsize(format))
        data = st.unpack(format, buffer)
    
        audio = []
        if canal == 2: # Mono
          audio = data[:,0] /2 + data[:,1] /2 #(L+R)/2
        elif canal == 1: #Right chanel R
          audio = data[:,1]
        elif canal == 0: #Left chanel L
          audio = data[:,0]
        elif canal == 3: #Side (L-R/2)
          audio = (data[:,0]-data[:,1])//2
        else:
           raise ValueError("Error canal")
     
        format ='<2h' 
        dat = st.pack(format, audio)
        ficMono = fwave.write(dat)  
        return ficMono
       

def mono2estereo(ficIzq, ficDer, ficEste):
     """
     Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales izquierdo y derecho, 
     respectivamente, y construye con ellas una señal estéreo que almacena en el fichero ficEste.
     """
     with open(ficIzq,'rb') as fwaveL, open(ficDer,'rb') as fwaveR, open(ficEste, 'wb') as fwaveout:
        format = '<4sI4s'
        buffer = fwaveL.read(st.calcsize(format))
        chunkid,chunksize,fmttwave = st.unpack(format, buffer)
        if chunkid != b'RIFF' or fmttwave != b'WAVE':
            raise Exception('Error en el fichero no tiene formato valido') 
        format = '<4sI2H2I2H'
        buffer = fwaveL.read(st.calcsize(format))
        schunk1ID, schunk1size, aformat, nchannels, srate, bitrate, blockAlign , bitPerSample = st.unpack(format, buffer)
        format = '<4sI'
        buffer = fwaveL.read(st.calcsize(format))
        schunk2ID, schunk2size = st.unpack(format, buffer)
        numMuestras = schunk2size // blockAlign
        format = f'<{numMuestras}h'
        buffer = fwaveL.read(st.calcsize(format))
        data = st.unpack(format, buffer)

        format = f'<{numMuestras}h'
        buffer = fwaveR.read(st.calcsize(format))
        data2 = st.unpack(format, buffer)
        audio = data[:]/2 + data2[:]/2
        formatOut = '<2h'
        dat= st.pack(formatOut,audio)
        ficEste= fwaveout.write(dat)
        return len(ficEste)
        
    
def codEstereo(ficEste, ficCod):
    """
     Lee el fichero ficEste, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
     y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas monofónicos como por sistemas estéreo preparados para ello.
    """
   
    with open(ficEste,'r+b') as fwave:
        format = '<4sI4s'
        buffer = fwave.read(st.calcsize(format))
        chunkid,chunksize,fmttwave = st.unpack(format, buffer)
        if chunkid != b'RIFF' or fmttwave != b'WAVE':
            raise Exception('Error en el fichero no tiene formato valido') 
        format = '<4sI2H2I2H'
        buffer = fwave.read(st.calcsize(format))
        schunk1ID, schunk1size, aformat, nchannels, srate, bitrate, blockAlign , bitPerSample = st.unpack(format, buffer)
        format = '<4sI'
        buffer = fwave.read(st.calcsize(format))
        schunk2ID, schunk2size = st.unpack(format, buffer)
        numMuestras = schunk2size // blockAlign
        format = f'<{numMuestras}h'#h
        buffer = fwave.read(st.calcsize(format))
        data = st.unpack(format, buffer)

        if nchannels == 2 and bitPerSample == 16:

         dataAudioMono = [data[:,0] /2 + data[:,1] /2]  #L+r/2
         #Intercalar muestras
         datafin = dataAudioMono + data
         datafin[::2] = dataAudioMono  #Coge muestras Mono slice 2 en 2
         datafin[1::2] = data  #estereo
         formatcod = '>i'   #Big endian 4bytes*8=32 bits
         dat= st.pack(formatcod, datafin)
         ficCod = fwave.write(dat)
         return len(ficCod)
        else:
           raise ValueError("El archivo entrante no es estereo o no es de 16 bits.")



    

def decEstereo(ficCod, ficEste):
   
   """
  Lee el fichero ficCod con una señal monofónica de 32 bits en la que los 16 bits más significativos contienen la semisuma de los dos canales de una señal estéreo 
  y los 16 bits menos significativos la semidiferencia, y escribe el fichero ficEste con los dos canales por separado en el formato de los ficheros WAVE estéreo.
   """
   with open(ficCod,'r+b') as fwave:
        format = '<4sI4s'
        buffer = fwave.read(st.calcsize(format))
        chunkid,chunksize,fmttwave = st.unpack(format, buffer)
        if chunkid != b'RIFF' or fmttwave != b'WAVE':
            raise Exception('Error en el fichero no tiene formato valido') 
        format = '<4sI2H2I2H'
        buffer = fwave.read(st.calcsize(format))
        schunk1ID, schunk1size, aformat, nchannels, srate, bitrate, blockAlign , bitPerSample = st.unpack(format, buffer)
        format = '<4sI'
        buffer = fwave.read(st.calcsize(format))
        schunk2ID, schunk2size = st.unpack(format, buffer)
        numMuestras = schunk2size // blockAlign
        format = f'<{numMuestras}h'#h
        buffer = fwave.read(st.calcsize(format))
        data = st.unpack(format, buffer)

        if bitPerSample != 32 or nchannels != 1:
           
           raise ValueError("El archivo no es monofonico o no es de 32 bit.")
        
        audioMono = data[::2] #8+8=16 primeros bits
        audioEst =  data[2::2] #empieza en 16 bits (y coge + 16) = 32 bits  
        
        audiOut =[]
        for Left, Right in zip(audioMono,audioEst):  #Intercala muestras mono y estereo
          audiOut.append(Left)
          audiOut.append(Right)
         
        format = '>h' #Big endian 8 bits
        dat = st.pack(format, audiOut)
        ficEste = fwave.write(dat)
        return len(ficEste)

        

        


     




