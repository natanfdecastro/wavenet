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

import sys
import socket
from concurrent.futures import ThreadPoolExecutor
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s : %(message)s \n')

'''
Comprovación de argumentos
'''
argv = sys.argv
if '-n' in argv and '-p' in argv and len(argv) == 6:
    print('Use: python3  Server.py −p [ puerto ] −n [ numero_hilos ]')

'''
Asignación de variables y constantes globales
'''
nodes = {}  # Diccionario donde se guarda la dirección IP del nodo y su llave pública
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(argv[2])
socket.bind(('', port))
thread_n = int(argv[4])
socket.listen()


def convert_list_to_string(org_list, split=' '):
    """
    Función que se encarga de retornar una cadena de texto que contiene
    a todos los elementos de la lista recibida con separaciones entre
    cada uno de un espacio.
    :param org_list: lista de strings
    :param split: caracter a unir
    :return: valores de la lista concatenados
    """
    return split.join(org_list)


def routing(source, destine):
    """
    Función que se encarga de defifir la ruta que seguirán los paquetes en
    la red mesh. Trabaja al emplear funciones que retornan valores random
    para definir la cantidad de saltos en medio de nodos (que se harán entre
    el destinatario y el remitente) y para definir el orden de los nodos que se seguirá.
    :param source: string dirección IP de origen
    :param destine: string dirección IP de destino
    :return: lista con llaves públicas de nodos por los que se enviaran los datos
    """
    logging.info(">>> Routing", source, destine)
    if not nodes.get(destine):
        return "Destine is not register"
    MAX = 2
    MIN = 2
    keys = []
    hops = random.randint(MIN, MAX)
    hops_list = list(nodes.items())
    hops_count = (len(hops_list) - 2)
    last_hops = None
    while hops and hops < hops_count:
        address, key = random.choice(hops_list)
        if last_hops != address or address != destine or address != source:
            keys.append(key)
            keys.append('|')
            hops -= 1
    keys.append(nodes.get(destine))
    return convert_list_to_string(keys)


def generate_response(connection, address):
    """
    Función encargada de recibir nuevas conexiones en el servidor.
    Se encarga de registrar a cada uno de los clientes mediante su dirección IP,
    junto con la llave pública que este envía. Además, se encarga de atender a las
    solicitudes de enrutamiento que son emitidas por el cliente.
    :param connection:
    :param address:
    :return:
    """
    connection.send('Welcome to WaveNET. Thank you for connecting'.encode())
    data = connection.recv(1024)
    nodes[address[0]] = data.decode('UTF-8')
    while True:
        data = connection.recv(1024)
        data = data.decode('UTF-8')
        if not data:
            break
        logging.info(f'{address[0]} received: {data}')
        data = data.split()
        if 'send' == data[0]:
            keys = routing(address[0], data[1])
            connection.send(bytes(keys, 'UTF-8'))
            logging.info(f'{address[0]} send: host public keys, size {len(keys)}')
    nodes.pop(address[0])
    logging.info(f"{address[0]} disconnected")
    connection.close()  # Close the connection


logging.info('>>> Server running')

with ThreadPoolExecutor(max_workers=thread_n) as executor:
    """
    Pool de Threads, por cada conexión realizada se asigna un hilo para las tareas
    """
    while True:
        connection, address = socket.accept()
        logging.info(f'>>> New connection from: {address}')
        try:
            result = executor.submit(generate_response, connection, address)
        except KeyboardInterrupt:
            connection.close()
