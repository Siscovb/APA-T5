def estereo2mono (ficEste, ficMono, canal=2):
    señal = bytearray()
    fichero = open(ficEste, mode='rb', buffering=0)
    if canal == 0:
        i=0
        while fichero:
            fichero.seek(i)
            señal=fichero.read(2)
            i+=4
    elif canal == 1:
        i=2
        while fichero:
            fichero.seek(i)
            señal=fichero.read(2)
            i+=4
    with open(ficMono, 'wb') as output_file:
        output_file.write('\n'.join(map(str, señal)))
    #elif canal == 2:
    #    while fichero:
    #        fichero.seek(i)
    #        señalL=(float(fichero.read(1)) + float(fichero.read(2)))/2
    #        i+=4
    #elif canal == 3:
    #    while fichero:
    #        i=0
    #        fichero.seek(i)
    #        señal=fichero.read(2)
    #        i+=4
