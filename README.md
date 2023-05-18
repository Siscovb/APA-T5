# Sonido estéreo y ficheros WAVE

## Nom i cognoms: Victor Ceballos Fouces

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

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`
```python
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Convierte un archivo WAVE estéreo a mono utilizando uno de los canales.

    Args:
        ficEste (str): Nombre del archivo de entrada WAVE estéreo.
        ficMono (str): Nombre del archivo de salida WAVE mono.
        canal (int): Canal a utilizar (0 = izquierdo, 1 = derecho, 2 = semisuma, 3 = semidiferencia).

    Raises:
        ValueError: Si el archivo de entrada no es estéreo o si el canal especificado no es válido.

    """
    # Canal a utilizar
    if canal < 0 or canal > 3:
        raise ValueError("Canal inválido.")
    
    # Abre el archivo estéreo
    with wave.open(ficEste, 'rb') as fEste:
        # Comprueba que el archivo de entrada es estéreo
        if fEste.getnchannels() != 2:
            raise ValueError("El archivo de entrada no es estéreo.")

        # Lee los parámetros del archivo de entrada
        nframes = fEste.getnframes()
        framerate = fEste.getframerate()
        sampwidth = fEste.getsampwidth()
        nchannels = 1
        
        # Abre el archivo de salida
        with wave.open(ficMono, 'wb') as fMono:
            # Establece los parámetros del archivo de salida
            fMono.setnchannels(nchannels)
            fMono.setsampwidth(sampwidth)
            fMono.setframerate(framerate)
            fMono.setnframes(nframes)

            # Lee y escribe las muestras
            for i in range(nframes):
                # Lee una muestra estéreo
                muestra = fEste.readframes(1)
                L, R = struct.unpack("<hh", muestra)

                # Elige el canal a utilizar
                if canal == 0:
                    muestraMono = struct.pack("<h", L)
                elif canal == 1:
                    muestraMono = struct.pack("<h", R)
                elif canal == 2:
                    muestraMono = struct.pack("<h", (L+R)//2)
                else:
                    muestraMono = struct.pack("<h", (L-R)//2)

                # Escribe la muestra mono
                fMono.writeframes(muestraMono)
```

##### Código de `mono2estereo()`
```python
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Convierte dos ficheros de audio monofónicos en un fichero de audio estéreo.

    :param ficIzq: Ruta del fichero de audio con el canal izquierdo.
    :param ficDer: Ruta del fichero de audio con el canal derecho.
    :param ficEste: Ruta del fichero de audio estéreo resultante.
    """
    # Abrir los ficheros de entrada y salida
    with open(ficIzq, 'rb') as f_izq, open(ficDer, 'rb') as f_der, open(ficEste, 'wb') as f_est:
        # Leer las cabeceras de los ficheros de entrada
        cabecera_izq = f_izq.read(44)
        cabecera_der = f_der.read(44)

        # Comprobar que los ficheros de entrada son válidos
        if cabecera_izq[:4] != b'RIFF' or cabecera_der[:4] != b'RIFF':
            raise ValueError('Los ficheros de entrada no son archivos WAVE')

        if cabecera_izq[22:24] != b'\x01\x00' or cabecera_der[22:24] != b'\x01\x00':
            raise ValueError('Los ficheros de entrada no son archivos de audio PCM')

        if cabecera_izq[34:36] != cabecera_der[34:36]:
            raise ValueError('Los ficheros de entrada tienen distinta frecuencia de muestreo')

        if cabecera_izq[40:44] != cabecera_der[40:44]:
            raise ValueError('Los ficheros de entrada tienen distinto número de bytes por segundo')

        # Escribir la cabecera del fichero de salida
        f_est.write(cabecera_izq)

        # Leer los datos de los ficheros de entrada
        data_izq = f_izq.read()
        data_der = f_der.read()

        # Comprobar que los datos de los ficheros de entrada tienen la misma longitud
        if len(data_izq) != len(data_der):
            raise ValueError('Los ficheros de entrada tienen distinta longitud de datos')

        # Empaquetar los datos de los canales izquierdo y derecho
        izq = struct.unpack(f'{len(data_izq)//2}h', data_izq)
        der = struct.unpack(f'{len(data_der)//2}h', data_der)

        # Mezclar los canales y empaquetar la señal estéreo
        est = bytearray()
        for i in range(len(izq)):
            est.extend(struct.pack('h', izq[i]))
            est.extend(struct.pack('h', der[i]))

        # Escribir los datos de la señal estéreo en el fichero de salida
        f_est.write(est)
```

##### Código de `codEstereo()`
```python
def codEstereo(ficEste, ficCod):
    """
    Codifica un archivo de audio estéreo en un archivo de audio mono utilizando el método de codificación "L + R / 2" y "L - R / 2".

    :param ficEste: Nombre del archivo de entrada con formato de audio estéreo.
    :type ficEste: str
    :param ficCod: Nombre del archivo de salida con formato de audio mono codificado.
    :type ficCod: str
    """
    with open(ficEste, 'rb') as f_in, open(ficCod, 'wb') as f_out:
        # Leemos la cabecera del archivo de entrada
        cabecera = f_in.read(44)
        f_out.write(cabecera)  # Escribimos la misma cabecera en el archivo de salida
        
        while True:
            # Leemos dos muestras de 2 bytes cada una, correspondientes a los canales izquierdo y derecho
            muestra_izq = f_in.read(2)
            muestra_der = f_in.read(2)
            
            # Si hemos llegado al final del archivo, salimos del bucle
            if not muestra_der:
                break
            
            # Convertimos las muestras a enteros de 16 bits
            izq = int.from_bytes(muestra_izq, byteorder='little', signed=True)
            der = int.from_bytes(muestra_der, byteorder='little', signed=True)
            
            # Calculamos la semisuma y la semidiferencia de las muestras
            semisuma = (izq + der) // 2
            semidif = (izq - der) // 2
            
            # Convertimos la semisuma y la semidiferencia a enteros de 32 bits
            semisuma32 = semisuma << 16
            semisuma32 &= 0x7FFF0000
            semidif32 = semidif & 0xFFFF
            semidif32 &= 0x7FFF0000
            
            # Escribimos los enteros de 32 bits en el archivo de salida
            f_out.write(semisuma32.to_bytes(4, byteorder='little', signed=False))
            f_out.write(semidif32.to_bytes(4, byteorder='little', signed=False))
            
    print('Codificación estéreo completada.')
```

##### Código de `decEstereo()`
```python
def decEstereo(ficCod, ficEste):
    """
    La función decEstereo(ficCod, ficEste) toma como entrada un archivo de audio codificado en
    formato PCM lineal de 32 bits, donde los 16 bits más significativos contienen la semisuma de
    los dos canales de una señal estéreo y los 16 bits menos significativos contienen la semidiferencia.
    Luego, decodifica la señal y escribe el archivo de audio estéreo resultante en formato de archivo WAV
    en ficEste. La función no modifica el archivo de entrada y solo utiliza la información de los canales
    para generar una nueva señal estéreo.

    """
    # Abrimos el archivo de entrada en modo lectura binaria
    with open(ficCod, 'rb') as f_in:
        # Leemos los primeros 44 bytes, que corresponden a la cabecera del archivo WAV
        cabecera = f_in.read(44)

        # Obtenemos los valores necesarios de la cabecera para escribir la nueva cabecera del archivo estéreo
        tamano = len(f_in.read())
        num_canales = 2
        frec_muestreo = struct.unpack('<I', cabecera[24:28])[0]
        bytes_por_muestra = 2
        tamano_cabecera = 36

        # Abrimos el archivo de salida en modo escritura binaria y escribimos la nueva cabecera
        with open(ficEste, 'wb') as f_out:
            f_out.write(struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', tamano + tamano_cabecera - 8, b'WAVE',
                                    b'fmt ', tamano_cabecera - 8, 1, num_canales, frec_muestreo,
                                    frec_muestreo * num_canales * bytes_por_muestra,
                                    num_canales * bytes_por_muestra, bytes_por_muestra * 8, b'data', tamano))

            # Volvemos al principio del archivo de entrada para leer los datos de audio
            f_in.seek(44)

            while True:
                # Leemos dos enteros de 32 bits cada uno del archivo de entrada
                semisuma_bytes = f_in.read(4)
                semidif_bytes = f_in.read(4)

                # Si hemos llegado al final del archivo, salimos del bucle
                if not semidif_bytes:
                    break

                # Convertimos los enteros de 32 bits a semisuma y semidiferencia
                semisuma = int.from_bytes(semisuma_bytes, byteorder='little', signed=False) >> 16
                semidif = int.from_bytes(semidif_bytes, byteorder='little', signed=False) & 0xFFFF

                # Calculamos las muestras izquierda y derecha
                izq = semisuma + semidif
                der = semisuma - semidif

                # Escribimos las muestras izquierda y derecha en el archivo de salida
                f_out.write(izq.to_bytes(2, byteorder='little', signed=True))
                f_out.write(der.to_bytes(2, byteorder='little', signed=True))

    print('Decodificación estéreo completada.')
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
