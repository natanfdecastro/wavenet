import sys
import socket  # Import socket module
from concurrent.futures import ThreadPoolExecutor
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s : %(message)s \n')

argv = sys.argv
nodes = {}
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
port = int(argv[2])  # Reserve a port for your service.
socket.bind(('', port))  # Bind to the port
thread_n = int(argv[4])
socket.listen()  # Now wait for client connection.


def convert_list_to_string(org_list, split=' '):
    return split.join(org_list)


def routing(source, destine):
    # todo validar si existe el destino saludos
    print("Routing", source, destine)
    MAX = 2
    MIN = 2
    keys = []
    hops = random.randint(MIN, MAX)
    hops_list = list(nodes.items())
    hops_count = (len(hops_list) - 2)
    last_hops = None
    while hops:  # and hops < hops_count
        address, key = random.choice(hops_list)
        if last_hops != address and address != destine:
            keys.append(key)
            keys.append('|')
            hops -= 1
    print(nodes.get(destine))
    keys.append(nodes.get(destine))
    print(keys)
    return convert_list_to_string(keys)


def generate_response(connection, address):
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
            logging.info(f"{len(bytes(keys, 'UTF-8'))}")
            logging.info(f'{address[0]} send: host public keys')
    nodes.pop(address[0])
    print("F para", address[0])
    connection.close()  # Close the connection


with ThreadPoolExecutor(max_workers=thread_n) as executor:
    while True:
        connection, address = socket.accept()  # Establish connection with client.
        logging.info(f'New connection from: {address}')
        try:
            result = executor.submit(generate_response, connection, address)
        except KeyboardInterrupt:
            connection.close()
