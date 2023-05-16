# Sonido estéreo y ficheros WAVE

## Nom i cognoms: Pau Péralvarez Casasampere

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI.

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda, y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.

### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Es la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

________________________________

- PARA COMPROBAR EL FUNCIONAMIENTO DE LAS FUNCIONES SE HAN CREADO LAS DIFERENTES VERSIONES DE 'KOMM.WAV' PARA CADA UNO DE LOS CASOS.
  - mono0.wav es del la función estereo2mono() para el canal 0, y igual con los otros tres con los otros.
  - stereo.wav es de la función mono2estereo()
  - kommCod.wav es de la función codEstereo()
  - kommDecod.wav es de la función decEstereo() 

- La primera función funciona perfectamente, mientras que mono2estereo() solo lee hasta la mitad de la canción (y no se como arreglarlo), y es por esto que las dos ultimas funciones tampoco funcionan de manera correcta.

_________________________________
#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `abrirWAVE()` y `creaCabeceraWAVE()`
```python
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
```

##### Código de `estereo2mono()`
```python
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
```


##### Código de `mono2estereo()`
```python
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
```


##### Código de `codEstereo()`
```python
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
```



##### Código de `decEstereo()`
```python
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
```



#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
