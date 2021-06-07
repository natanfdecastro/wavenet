"""
======================================================================
Copyright (C) 2021 Brandon, Walter Bytes, Natan & Kenny
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/.

    Instituto Tecnologico de Costa Rica
    Redes Locales - IC-7602

    WaveNET (wavenet)
    Disponible en: https://github.com/natanfdecastro/wavenet

    Natan Fernandez de Castro - 2017105774
    Kenneth Rodriguez Murillo - 2018132752
    Brandon Josué Ledezma Fernández - 2018185574
    Walter Antonio Morales Vásquez - 2018212846
========================================================================
"""

import scapy.all as scapy
import time

version_bytes = 2
destiny_bytes = 8
source_bytes = 8
chksum_bytes = 4
length_bytes = 2
max_data_len = 104


class WaveNetPacket(scapy.Packet):
    """
    Tiene los atributos de la lista de una lista con la descripción de un
    paquete, la cual contiene: (version), id del destino (dst_id),  id del origen (src_id),
    suma de comprobación (checksum), largo (len) y la información (data)
    """
    name = "WaveNetPacket"
    fields_desc = [scapy.ShortField("version", 1),
                   scapy.LongField("dst_id", 8888),
                   scapy.LongField("src_id", 8888),
                   scapy.XIntField("checksum", None),
                   scapy.ShortField("len", None),
                   scapy.StrLenField("data", "")]


def send_file(source, destiny, file_path, version=1):  # create packets from file
    """
    Función que se encarga de crear los paquetes a partir de un archivo,
    el cual lo abre, lee la información (data) y le agrega la descripción
    con la nueva información al paquete.
    :param source: direccion origen
    :param destiny: direccion destino
    :param file_path: ruta de un archivo
    :param version: versión del paquete
    :return: binarios del archivo
    """
    file = open(file_path, "rb")
    message = list(file.read())  # si el mensaje es string list(bytes(string,"ascii"))
    file.close()
    return create_bin_packets(source, destiny, message, version=1)


def create_bin_packets(source, destiny, bins, version=1):
    """
     Función que se encarga de crear un paquete en  binario según
     la información suministrada por parámetro. Retornando una lista de unos y ceros.
    :param source: direccion origen
    :param destiny: direccion destino
    :param bins: datos binarios
    :param version: versión del paquete
    :return: WaveNetPacket
    """
    length = len(bins)
    packets_list = []
    while (length > 0):
        current_length = length if length <= max_data_len else max_data_len  # Definir el tamaño del data en constante
        new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                                   checksum=None, len=current_length,
                                   data=bins[:max_data_len])  # ''.join(map(chr, bins[:max_data_len])))

        # Calcular y ponerle checksum
        new_packet.show()
        binaries = scapy.raw(new_packet)
        packets_list.append([[int(n) for n in bin(byte)[2:].zfill(8)] for byte in binaries])

        bins = bins[max_data_len:]
        length -= max_data_len

    return packets_list


def create_packets_from_bins(source, destiny, bins, version=1):
    """
    Función que se encarga de crear un paquete, lo convierte a binario y luego lo retorna
    :param source: direccion origen
    :param destiny: direccion destino
    :param bins: datos binarios
    :param version: versión del paquete
    :return: paquetes
    """
    length = len(bins)

    packets_list = b''

    current_length = length if length <= max_data_len else max_data_len
    new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                               checksum=None, len=length, data=bins)
    new_packet.show()

    binaries = scapy.raw(new_packet)
    packets_list += binaries

    return packets_list


def get_file_binaries(file_path):
    """
    Función utilizada para obtener los binarios de un archivo para enviarlo a otro nodo de la red.
    :param file_path: ruta del archivo
    :return: binario del archivo
    """
    file = open(file_path, "rb")
    message = file.read()

    file.close()
    return message


def decode_packets(bin_packets_list):
    """
    Función que recibe una lista de unos y ceros que para cada paquete
    se encarga de generar un paquete de WaveNetPacket por cada 128 bits.
    :param bin_packets_list:
    :return:
    """
    packets_list = []
    print('bin_packets_list', bin_packets_list)
    for packet in bin_packets_list:

        print('packet', packet)
        version = 0
        left_index = 0
        right_index = version_bytes
        for byte in packet[:right_index]:

            for bit in byte:
                version = (version << 1) | bit
        destine = 0
        left_index = right_index
        right_index = left_index + destiny_bytes
        for byte in packet[left_index:right_index]:

            for bit in byte:
                destiny = (destine << 1) | bit

        source = 0
        left_index = right_index
        right_index = left_index + source_bytes
        for byte in packet[left_index:right_index]:

            for bit in byte:
                source = (source << 1) | bit

        chksum = 0
        left_index = right_index
        right_index = left_index + chksum_bytes
        for byte in packet[left_index:right_index]:

            for bit in byte:
                chksum = (chksum << 1) | bit

        length = 0
        left_index = right_index
        right_index = left_index + length_bytes
        for byte in packet[left_index:right_index]:

            for bit in byte:
                length = (length << 1) | bit

        message = bytearray()
        left_index = right_index
        right_index = left_index + length
        for byte in packet[left_index:right_index]:

            temp = 0
            for bit in byte:
                temp = (temp << 1) | bit
            message.append(temp)

        new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destine,
                                   checksum=None, len=length, data=message)

        '''
        if calcularchecksum() != checksum
         Errors correction
        '''

        packets_list.append(new_packet)
    return packets_list


def decode_bins(bin_from_packet):
    """
     Función utilizada para crear un paquete con la información recibida en los parametros obtenidos.
    :param bin_from_packet:
    :return:
    """
    left_index = 0
    right_index = version_bytes

    version = int.from_bytes(bin_from_packet[:right_index], "big")

    left_index = right_index
    right_index = left_index + destiny_bytes
    destiny = int.from_bytes(bin_from_packet[left_index:right_index], "big")

    left_index = right_index
    right_index = left_index + source_bytes
    source = int.from_bytes(bin_from_packet[left_index:right_index], "big")

    left_index = right_index
    right_index = left_index + chksum_bytes
    chksum = int.from_bytes(bin_from_packet[left_index:right_index], "big")

    left_index = right_index
    right_index = left_index + length_bytes
    length = int.from_bytes(bin_from_packet[left_index:right_index], "big")

    left_index = right_index
    right_index = left_index + length
    message = bin_from_packet[left_index:right_index]

    new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                               checksum=None, len=length, data=message)

    return new_packet


def data_to_bits(data):
    """
    Función encargada de convertir una lista compuesta de 1 y 0
    con el fin de convertir su contenido en un dato binario.
    :param data: lista de 1 y 0
    :return: dato en binario
    """
    return bin(int(''.join(map(str, data)), 2) << 1)


def receive_file(packets):
    """
     Función que se encarga de crear un nuevo archivo con los datos binarios
     que recibe. es creado con la fecha y hora del momento en que esta función es llamada.
    :param packets: lista de WaveNetPacket
    """
    file = open(time.strftime("%Y-%m-%d_%H:%M:%S"), "wb")

    for elem in packets:
        file.write(elem)

    file.close()
