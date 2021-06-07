import os
from time import sleep

import pyaudio
import numpy as np
from itertools import groupby, chain


class DWN:
    """
    Clase que se encarga de manejar la información en un dispositivo wavenet.
    La cual tiene como atributos la lista de nodos, el tamaño máximo de un paquete
    y la duración de un sonido de 1 segundo (1000 ms)
    """
    def __init__(self):
        """
        Constructor de la clase
        """
        self.node_list = list()
        self.max_frame_size = 128
        self.sound_duration = 200

    def sound(self, frequency, duration=0):
        """
        Función que se encarga de reproducir sonidos dentro de la red,
        recive una frecuencia y el tiempo por el que se va a emitir el sonido,
        se realiza una llamada al sistema para hacer uso de la bilioteca SoX (Sound eXchange),
        la cual permite emitir sonidos en el sistema Linux.
        :param frequency: valor de frecuencia
        :param duration: tiempo que se emite el sonido
        :return:
        """
        duration = self.sound_duration
        os.system('play -n -q synth %s sin %s' % (duration / 1000, frequency))  # todo add -q Make SoX not show output

    def send(self, data):
        """
        Función que se encarga de escuchar por frecuencias que puedan coincidir con las
        definidas para representar bits en el programa y frecuencias especiales (de separación
        y de finalización). Guarda en una lista el resultado de los símbolos recuperados.
        :param data: lista de 1 y 0
        """
        data = list(chain(*data))#[item for sublist in data for item in sublist]
        start_frequency = 16000
        split_frequency = 13000
        # self.sound(start_frequency) # comentar si no es un while true
        print(f"******************************************************************{len(data)}******************************************************************")
        for i in data:
            if i:
                frequency = 15000
                self.sound(frequency)
            else:
                frequency = 11000
                self.sound(frequency)
            sleep(0.1)
            self.sound(split_frequency)
        sleep(0.1)
        self.sound(start_frequency, 2000)

    def listen(self):
        """
        Función que se encarga de limpiar los resultados obtenidos de la
        lista de datos recividos, recibe una lista con valores de: 1, 0 y
        2, donde [2] es para diferenciar el inicio y fin de un bit
        :return: lista de 1 y 0
        """
        print(">>> [Listening for WaveNET package...]")
        data = []
        result = []
        chunk_size = 4096
        rate = 44100
        channel_number = 1
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=channel_number,
                            rate=rate,
                            frames_per_buffer=chunk_size,
                            input=True)
        listening = True
        try:
            while listening:
                data_ = np.fromstring(stream.read(chunk_size), dtype=np.int16)
                data_ = data_ * np.hanning(len(data_))
                fft = abs(np.fft.fft(data_).real)
                fft = fft[:int(len(fft) / 2)]
                frequency = np.fft.fftfreq(chunk_size, 1.0 / rate)
                frequency = frequency[:int(len(frequency) / 2)]
                frequency_top = frequency[np.where(fft == np.max(fft))[0][0]] + 1
                print(frequency_top)
                if frequency_top > 10500:
                    if 14500 < frequency_top < 15500:
                        data.append(1)
                        print(1)
                    if 12500 < frequency_top < 13500:
                        data.append(2)
                        print(2)
                    if 10500 < frequency_top < 11500:
                        data.append(0)
                        print(0)
                    if 15500 < frequency_top < 16500:
                        listening = False
                        print('break')
            data = self.clean_frequency(data)
            print(data)
            # bits_to_data
            for i in range(0, len(data), 8):
                result.append(data[i:i * 8])
            return data, result
        except KeyboardInterrupt:
            data = self.clean_frequency(data)
            return data, result

    def clean_frequency(self, data):
        """
        Función que se encarga de limpiar los resultados obtenidos de la lista
        de datos recividos, recibe una lista con valores de: 1, 0 y 2, donde [2]
        es para diferenciar el inicio y fin de un bit.
        :param data:
        :return:
        """
        result = []
        for element in groupby(data):
            if element[0] != 2:
                result.append(element[0])
        return result
