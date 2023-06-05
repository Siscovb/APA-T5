"""
    APA T5

    Nombre y apellidos: Àlex Mata Barrero

""" 

import struct

def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, 
    y escribe el fichero ficMono, con una señal monofónica.

    """
    with open(ficEste, 'rb') as in_file:
        while True:
            riff_be = in_file.read(4) # RIFF
            chunk = in_file.read(4) # file size
            wave_be = in_file.read(4) # file type (WAVE)
            if (wave_be.decode('ascii') != 'WAVE'): break
            fmt_be = in_file.read(4) # "fmt "
            subchunk_size1_le = in_file.read(4) # subchunk size
            format_le = in_file.read(2) # format (PCM...)
            channels_le = in_file.read(2) # channels
            sample_rate_le = in_file.read(4) # sample rate
            byte_rate_le = in_file.read(4) # byte rate
            block_align_le = in_file.read(2) # block align
            bitsPerSample_le = in_file.read(2) # bits per sample
            data_be = in_file.read(4) # "data"
            size_data_le = in_file.read(4) # subchunk2 size

            bytesPerSample = int(struct.unpack('<H', bitsPerSample_le)[0]/8)
            size = int((struct.unpack('<I', size_data_le)[0])/2 + 36)

            with open(ficMono, 'wb') as out_file:
                out_file.write(riff_be)
                out_file.write(struct.pack('<I', size))
                out_file.write(wave_be)
                out_file.write(fmt_be)
                out_file.write(subchunk_size1_le)
                out_file.write(format_le)
                out_file.write(struct.pack('<H', 1))
                out_file.write(sample_rate_le)
                out_file.write(struct.pack('<I', int((struct.unpack('<I', byte_rate_le)[0])/2)))
                out_file.write(struct.pack('<H', int((struct.unpack('<H', block_align_le)[0])/2)))
                out_file.write(bitsPerSample_le)
                out_file.write(data_be)
                out_file.write(struct.pack('<I', size-36))

                if canal == 0:
                    while True:
                        left = in_file.read(bytesPerSample)
                        in_file.read(bytesPerSample)
                        if not left: break
                        out_file.write(left)

                elif canal == 1:
                    while True:
                        in_file.read(bytesPerSample)
                        right = in_file.read(bytesPerSample)
                        if not right: break
                        out_file.write(right)
                
                elif canal == 2:
                    while True:
                        chunk = in_file.read(2 * bytesPerSample)
                        if not chunk: break
                        left, right = struct.unpack('<hh', chunk)
                        out_file.write(struct.pack('<h', int((left + right) / 2)))

                elif canal == 3:
                    while True:
                        chunk = in_file.read(2 * bytesPerSample)
                        if not chunk: break
                        left, right = struct.unpack('<hh', chunk)
                        out_file.write(struct.pack('<h', int((left - right) / 2)))

                else: break
                
            break

def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq, 'rb') as in_file, open(ficDer, 'rb') as in_file_r:
        while True:
            riff_be = in_file.read(4) # RIFF
            chunk = in_file.read(4) # file size
            wave_be = in_file.read(4) # file type (WAVE)
            if (wave_be.decode('ascii') != 'WAVE'): break
            fmt_be = in_file.read(4) # "fmt "
            subchunk_size1_le = in_file.read(4) # subchunk size
            format_le = in_file.read(2) # format (PCM...)
            channels_le = in_file.read(2) # channels
            sample_rate_le = in_file.read(4) # sample rate
            byte_rate_le = in_file.read(4) # byte rate
            block_align_le = in_file.read(2) # block align
            bitsPerSample_le = in_file.read(2) # bits per sample
            data_be = in_file.read(4) # "data"
            size_data_le = in_file.read(4) # subchunk2 size

            bytesPerSample = int(struct.unpack('<H', bitsPerSample_le)[0]/8)
            size = int((struct.unpack('<I', size_data_le)[0])*2 + 36)

            with open(ficEste, 'wb') as out_file:
                out_file.write(riff_be)
                out_file.write(struct.pack('<I', size))
                out_file.write(wave_be)
                out_file.write(fmt_be)
                out_file.write(subchunk_size1_le)
                out_file.write(format_le)
                out_file.write(struct.pack('<H', 2))
                out_file.write(sample_rate_le)
                out_file.write(struct.pack('<I', int((struct.unpack('<I', byte_rate_le)[0])*2)))
                out_file.write(struct.pack('<H', int((struct.unpack('<H', block_align_le)[0])*2)))
                out_file.write(bitsPerSample_le)
                out_file.write(data_be)
                out_file.write(struct.pack('<I', size-36))
                in_file_r.read(44)
                while True:
                    left = in_file.read(bytesPerSample)
                    right = in_file_r.read(bytesPerSample)
                    if not left or not right: break
                    out_file.write(left)
                    out_file.write(right)
            break

def codEstereo(ficEste, ficCod)