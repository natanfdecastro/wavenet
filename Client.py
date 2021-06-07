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

import socket
import sys
from key import *
from wavenet import *
from DispositivoWaveNET import *


print("░██╗░░░░░░░██╗░█████╗░██╗░░░██╗███████╗███╗░░██╗███████╗████████╗")
print("░██║░░██╗░░██║██╔══██╗██║░░░██║██╔════╝████╗░██║██╔════╝╚══██╔══╝")
print("░╚██╗████╗██╔╝███████║╚██╗░██╔╝█████╗░░██╔██╗██║█████╗░░░░░██║░░░")
print("░░████╔═████║░██╔══██║░╚████╔╝░██╔══╝░░██║╚████║██╔══╝░░░░░██║░░░")
print("░░╚██╔╝░╚██╔╝░██║░░██║░░╚██╔╝░░███████╗██║░╚███║███████╗░░░██║░░░")
print("░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚══════╝░░░╚═╝░░░")

'''
Comprobación de argumentos
'''
argv = sys.argv
if not ("-p" in argv) or not ('-h' in argv):
    print('Use: python3 Client.py -h host -p port')
    exit()

'''
Asignación de variables y constantes globales
'''
socket = socket.socket()
host = argv[2]
port = int(argv[4])
print(">>> Generic public and private key")
private, public = generate_keys()
print(">>> Connecting to host...")
socket.connect((host, port))
dwn = DWN()


def get_public_keys(socket_, command):
    """
    Función que se encarga de obtener las llaves RSA públicas de cada
    cliente que se va a hacer el enrutamiento, dividiéndolas por un pipe (|)
    y retornándolas.
    :param socket_: socket de la conexión
    :param command: string con las llaves publicas
    :return: lista de llaves RSA
    """
    socket_.send(bytes(command, 'UTF-8'))
    data = socket_.recv(4096)
    data = data.decode('UTF-8')
    print("Data: ", data)
    keys = data.split(' | ')
    public_keys = [RSA.import_key(i) for i in keys]
    return public_keys


def receive_data():
    """
    Función que se encarga de por instanciar al estado actual de dispositivo
    wavenet y escuchar la información entrante para en dado caso recibir el
    archivo, o en dado caso si el archivo excede en tamaño al paquete dispara
    un error de valor.
    """
    print("Listening...")
    _, data = dwn.listen()
    print(data)
    data = data_to_bits(data)
    try:
        data = decipher_data(data, private)
        package = decode_bins(data)
        receive_file(package.data)
        print('File received')
    except ValueError:
        print("Ciphertext too large")


def send_data(socket_, command):
    """
    Función que se encarga de recibir las llaves públicas de cada
    cliente para la comunicación, recibir la ruta con el nombre del archivo,
    y cifrarla para enviarla a través de la red mesh.
    :param socket_: socket de la conexión
    :param command: commando a enviar al servidor
    """
    source = abs(hash(host))
    destination = abs(hash(command[4:]))
    public_keys = get_public_keys(socket_, command)
    file_name = input('>>> File path: ')

    if os.path.isdir(file_name):
        exit()
    if not (os.path.isdir(file_name) or os.path.isfile(file_name)):
        print("\033[96m {}\033[00m".format("No se ha encontrado el archivo..........."))
        exit()
    file_name = file_name.replace(' ', '\ ')

    file_binary = get_file_binaries(file_name)
    init_package = create_packets_from_bins(source, destination, file_binary, 1)
    print("Init: ", init_package)
    init_package = cipher_data(init_package, public_keys[-1])
    for key in public_keys[1:-1]:
        init_package = create_packets_from_bins(source, destination, init_package, 1)
        print(f'for {key}:', init_package)
        init_package = cipher_data(init_package, key)
        print(f'for cipher', init_package)
    init_package = create_packets_from_bins(source, destination, init_package, 1)
    print('Out for', init_package)
    init_package = cipher_data(init_package, public_keys[0])
    print('End package', init_package)
    init_package = [[int(n) for n in bin(byte)[2:].zfill(8)] for byte in init_package]
    # init_package = create_bin_packets(1, 2, init_package, version=1)
    print(init_package)
    dwn.send(init_package)


def cli(socket_):
    """
    Función que se encarga de recibir comandos a través de la línea de comandos.
    :param socket_: socket de la conexión
    """
    command = str(input())
    if command[:4] == 'send':
        send_data(socket_, command)
    if command == 'receive':
        receive_data()


"""
Se establece la conexión con el servidor
"""
try:
    print(socket.recv(1024).decode('UTF-8'))
    print(">>> Sending public key")
    print("Key length: ", len(bytes(public, 'UTF-8')))
    socket.send(bytes(public, 'UTF-8'))
    while True:
        cli(socket)
except KeyboardInterrupt:
    socket.close()
