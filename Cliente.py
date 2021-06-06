import socket  # Import socket module
import sys

import wavenet
from key import *
from wavenet import *
from DispositivoWaveNET import *


# pasar host y puerto por parametros
argv = sys.argv
if "-p" in argv and '-h' in argv:
    print('Use: python3 Client.py -h host -p port')
print(argv)
socket = socket.socket()  # Create a socket object
host = argv[2]  # Get local machine name
port = int(argv[4])  # Reserve a port for your service.
print("Generic public and private key")
private, public = generate_keys()
print("Connecting to host...")
socket.connect((host, port))
dwn = DWN()



def get_public_keys(socket_, command):
    socket_.send(bytes(command, 'UTF-8'))
    data = socket_.recv(4096)
    print('Largo de la ostia recibida', len(data))
    data = data.decode('UTF-8')
    print("Data: ", data)
    keys = data.split(' | ')
    print(keys)
    public_keys = [RSA.import_key(i) for i in keys]
    '''
    for i in public_keys:
        print(i.export_key().decode())

    print("LEN: ", len( public_keys))
    '''
    return public_keys


def cipher_data (data, key):
    cipher = PKCS1_OAEP.new(key=key)
    cipher_data = cipher.encrypt(data)
    print(cipher_data)
    return cipher_data


def decipher_data(data, key):
    decrypt = PKCS1_OAEP.new(key=key)
    decrypted_data = decrypt.decrypt(data)
    print(cipher_data)
    return decrypted_data


def receive_data():
    print("Escuchando")
    data = dwn.listen()
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
    source = abs(hash(host))
    destination = abs(hash(command[4:]))
    public_keys = get_public_keys(socket_, command)
    for i in public_keys:
        print(type(i))
    file_name = input('File path: ')
    # preguntar si es archivo si se puede
    file_binary = get_file_binaries(file_name)
    init_package = create_packets_from_bins(source, destination, file_binary, 1)
    print("Init: ", init_package)
    init_package = cipher_data(init_package, public_keys[-1])
    for key in public_keys[1:-1]:
        init_package = create_packets_from_bins(source, destination, init_package, 1)
        print('2', init_package)
        # init_package = cipher_data(init_package, key)
        print('3', init_package)
    init_package = create_packets_from_bins(source, destination, init_package, 1)
    print('4', init_package)
    init_package = cipher_data(init_package, public_keys[0])
    print('fin', init_package)
    init_package = [[int(n) for n in bin(byte)[2:].zfill(8)] for byte in init_package]
    # init_package = create_bin_packets(1, 2, init_package, version=1)
    print(init_package)  # enviar a sonar
    dwn.send(init_package)


def cli(socket_):
    command = str(input())
    if command[:4] == 'send':
        send_data(socket_, command)
    if command == 'receive':
        receive_data()

try:
    print(socket.recv(1024))
    print(len(bytes(public, 'UTF-8')))
    socket.send(bytes(public, 'UTF-8'))
    while True:
        cli(socket)
except KeyboardInterrupt:
    socket.close()