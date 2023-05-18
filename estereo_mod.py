import wave
import struct
from docopt import docopt

"""
    Quinta tarea de APA - Sonido estéreo y ficheros WAVE
    Nombre y apellidos: Victor Ceballos Fouces
"""



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


USAGE= """
estereo_mod.py

Usage:
  estereo_mod.py [mono] [options] <ficL> [<ficR>] <ficEste>
  estereo_mod.py --help
  estereo_mod.py --version

Options:
  --left, -l    Usa el canal izquierdo de la señal estereo [default: False]
  --right, -r   Usa el canal derecho de la señal estereo  [default: False]
  --suma, -s    Usa la semi-suma de los dos canales [default: False]
  --diferencia, -d   Usa la semi-diferencia de los dos canales [default: False]
"""


def main():
    args = docopt(USAGE, version="estereo_mod.py - Victor Ceballos Fouces, 2023")
    
    # Procesamiento de los argumentos y opciones
    ficL = args['<ficL>']
    ficR = args['<ficR>']
    ficEste = args['<ficEste>']
    ficMono = args['<ficMono>']
    canal = 0

    if args['mono']:
        # Lógica para procesar el caso de conversión de estéreo a mono
        if args['--left']:
            canal = 0
        elif args['--right']:
            canal = 1
        elif args['--suma']:
            canal = 2
        elif args['--diferencia']:
            canal = 3

        # Llamada a la función estereo2mono
        estereo2mono(ficEste, ficMono, canal)
    else:
        # Lógica para procesar el caso de conversión de mono a estéreo
        # Llamada a la función mono2estereo
        mono2estereo(ficL, ficR, ficEste)

if __name__ == '__main__':
    main()




