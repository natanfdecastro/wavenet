import scapy.all as scapy

# Parte de la versión?
version_bytes = 2  # VER_BYTES
destiny_bytes = 8  # VER_BYTES
source_bytes = 8  # VER_BYTES
chksum_bytes = 4  # VER_BYTES
length_bytes = 2  # VER_BYTES
max_data_len = 104


class WaveNetPacket(scapy.Packet):
    name = "WaveNetPacket"

    '''
    ShortField -> 2 bytes
    XByteField -> 1 byte, por la X prefiere la representación hex
    IntField
    StrLenField("Omer", "", None)
    '''

    fields_desc = [scapy.ShortField("version", 1),
                   scapy.LongField("dst_id", 8888),
                   scapy.LongField("src_id", 8888),
                   scapy.XIntField("checksum", None),  # Puede ser x o None
                   scapy.ShortField("len", None),  # Realmente el largo cabe en un byte
                   scapy.StrLenField("data", "")]  # Tamaño max_data_len


'''
2 + 4 + 4 + 4 + 2

16 bytes
Total = 128
'''


# a = WaveNetPacket(dst_id=12, checksum=12234, len=7, data="abcdf12")
# b = scapy.raw(a)

# print(f"Packet {a.show()}")
# print(f"Raw {b}")

# def decode_bytes(bin_packet):

# 	to_return = WaveNetPacket
# 	return to_return

def caesar_cipher(key, bin_data):
    new_data = bytearray()
    for elem in bin_data:
        new_data.append((elem + key) % 255)
    return new_data


def caesar_decipher(key, bin_data):
    new_data = bytearray()
    for elem in bin_data:
        new_data.append((elem - key) % 255)
    return new_data


# print(list(bytes(string,"ascii")))
# print(list(file.read()))

# byte a string

# Pasar el message a array binario?
# def create_bin_packets(source, destiny, message, version = 1): # Message is a list of bytes

# 	length = len(message)

# 	packets_list = []
# 	while(length > 0):

# 		current_length = length if length<=max_data_len else max_data_len # Definir el tamaño del data en constante
# 		new_packet = WaveNetPacket(version = version, src_id = source, dst_id = destiny, 
# 			checksum = None, len = current_length, data = bytearray(message[:max_data_len]))#''.join(map(chr, message[:max_data_len])))

# 		# Calcular y ponerle checksum

# 		binaries = scapy.raw(new_packet)
# 		packets_list.append([[int(n) for n in bin(byte)[2:].zfill(8)] for byte in binaries])

# 		message = message[max_data_len:]
# 		length -= max_data_len

# 	return packets_list

def send_file(source, destiny, file_path, version=1):  # create packets from file

    file = open(file_path, "rb")
    message = list(file.read())  # if message is string list(bytes(string,"ascii"))

    file.close()
    return create_bin_packets(source, destiny, message, version=1)


def create_bin_packets(source, destiny, bins, version=1):  # bins is a list of bytes

    print(bins)
    length = len(bins)
    print('length', length)

    packets_list = []
    while (length > 0):
        current_length = length if length <= max_data_len else max_data_len  # Definir el tamaño del data en constante
        new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                                   checksum=None, len=current_length, data=bins[:max_data_len])  # ''.join(map(chr, bins[:max_data_len])))

        # Calcular y ponerle checksum
        new_packet.show()
        binaries = scapy.raw(new_packet)
        packets_list.append([[int(n) for n in bin(byte)[2:].zfill(8)] for byte in binaries])

        bins = bins[max_data_len:]
        length -= max_data_len

    return packets_list


# Crear paquetes un arreglo de bits
def create_packets_from_bins(source, destiny, bins, version=1):  # Message is a list of bytes

    length = len(bins)

    packets_list = b''

    current_length = length if length <= max_data_len else max_data_len  # Definir el tamaño del data en constante
    new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                               checksum=None, len=length, data=bins)  # ''.join(map(chr, bins[:max_data_len])))
    new_packet.show()
    # Calcular y ponerle checksum

    binaries = scapy.raw(new_packet)
    packets_list += binaries

    # bins = bins[max_data_len:]
    # length -= max_data_len

    return packets_list


def get_file_binaries(file_path):  # create bitarray from file

    file = open(file_path, "rb")
    message = file.read()  # if message is string list(bytes(string,"ascii"))

    file.close()
    return message


# bin_packets = create_bin_packets(1, 2, 'mensaje prueba', 1)
# print('', *bin_packets[0], sep='\n')

# bin_packets = create_bin_packets(1, 2, 
# 	"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\
# 	1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111", 1)
# print("Bin packet", *bin_packets, sep='\n')




def decode_packets(bin_packets_list):
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

        # if version not in diccionario versiones?

        destiny = 0
        left_index = right_index
        right_index = left_index + destiny_bytes
        for byte in packet[left_index:right_index]:

            for bit in byte:
                destiny = (destiny << 1) | bit

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

        new_packet = WaveNetPacket(version=version, src_id=source, dst_id=destiny,
                                   checksum=None, len=length, data=message)

        '''
		if calcularchecksum() != checksum
			Errors correction
	
		'''

        packets_list.append(new_packet)
    return packets_list


def decode_bins(bin_from_packet):
    left_index = 0
    right_index = version_bytes

    version = int.from_bytes(bin_from_packet[:right_index], "big")

    # if version not in diccionario versiones?

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
    '''
	if calcularchecksum() != checksum
		Errors correction

	'''

    # packets_list.append(new_packet)
    return new_packet


def data_to_bits(data):
    return bin(int(''.join(map(str, data)), 2) << 1)


'''
byte_arr = [65,66,67,68] 
some_bytes = bytearray(byte_arr)

immutable_bytes = bytes(some_bytes)
with open("my_file.txt", "wb") as binary_file: # Abrir el archivo como la hora
    binary_file.write(immutable_bytes)
'''

import time


def receive_file(packets):
    # packets = decode_packets(bin_packets_list)
    file = open(time.strftime("%Y-%m-%d_%H:%M:%S"), "wb")

    for elem in packets:
        file.write(elem)

    file.close()


# return packets

'''
arr = get_file_binaries('prueba.txt')
arr2 = create_packets_from_bins(1, 2, arr, version=1)

# print(arr2)
arr3 = create_bin_packets(1, 2, arr2, version=1)

# print(arr3)
# arr3[0][0].show()

decoded_packets_list = decode_packets(arr3)

l = []
for elem in decoded_packets_list:
    elem.show()
    print(elem.data)
    l.append(decode_bins(elem.data))

print(l)'''

# bin_packets = send_file(1, 2, '2021-06-03_14-43_1.png', 1)

# decoded_packets_list = receive_file(bin_packets)

# for elem in decoded_packets_list:
# 	print(f"Paquete: {elem.show()}")

'''
Función para unir los mensajes?

'''

'''

Pasar de bin a bits
[int(n) for n in bin(b[1])[2:].zfill(8)]
[int(n) for y in b for n in bin(y)[2:].zfill(8)]

[[int(n) for n in bin(y)[2:].zfill(8)] for y in b]

'''

# def send_packet(destiny, dst_port, src_port, message, retry): # Message is a string

# 	addr = ('255.255.255.255', src_port)  # 255. is the broadcast IP for UDP
# 	send_socket = socket(AF_INET, SOCK_DGRAM)
#     try:
#         send_socket.sendto(message, addr)
#     except Exception as e:
#         print("Link failed to send packet over socket %s" % e)
#         sleep(0.2)
#         if retry:
#             send_packet(destiny, dst_port, src_port, message, retry=False)

# def send_packet2(destiny, dst_port, src_port, message):

# 	packet=IP(dst=destiny)/TCP()/message
# 	send(packet)

# def receive_package():
