import os
import pyaudio
import numpy as np
from itertools import groupby, chain


class DWN:
    def __init__(self):
        self.node_list = list()
        self.max_frame_size = 128
        self.sound_duration = 130

    def sound(self, frequency, duration=0):
        duration = self.sound_duration
        os.system('play -n -q synth %s sin %s' % (duration / 1000, frequency))  # todo add -q Make SoX not show output

    def send(self, data):
        # data_to_bits : seria un pasar a lista de 1 y 0
        data = list(chain(*data))#[item for sublist in data for item in sublist]
        start_frequency = 22000
        split_frequency = 17000
        # self.sound(start_frequency) # comentar si no es un while true
        for i in data:
            if i:
                frequency = 20000
                self.sound(frequency)
            else:
                frequency = 15000
                self.sound(frequency)
            self.sound(split_frequency)
        self.sound(start_frequency)

    def listen(self):
        data = []
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
        while listening:
            data_ = np.fromstring(stream.read(chunk_size), dtype=np.int16)
            data_ = data_ * np.hanning(len(data_))
            fft = abs(np.fft.fft(data_).real)
            fft = fft[:int(len(fft) / 2)]
            frequency = np.fft.fftfreq(chunk_size, 1.0 / rate)
            frequency = frequency[:int(len(frequency) / 2)]
            frequency_top = frequency[np.where(fft == np.max(fft))[0][0]] + 1
            if frequency_top > 14900:
                print(frequency_top)
                if 19500 < frequency_top < 20500:
                    data.append(1)
                if 16500 < frequency_top < 17500:
                    data.append(2)
                if 14500 < frequency_top < 15500:
                    data.append(0)
                if 21500 < frequency_top < 22500:
                    listening = False
        data = self.clean_frequency(data)
        print(data)
        # bits_to_data
        '''result = []
        for byte in range(0,128,8):
            result.append(data[byte:byte+8])
        print(result)
        exit()
        return result'''
        return data

    def clean_frequency(self, data):
        result = []
        for element in groupby(data):
            if element[0] != 2:
                result.append(element[0])
        return result
