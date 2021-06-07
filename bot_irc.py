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
import socket
import time
import sys

def connect_bot_to_IRC(server, port, channel, bot_nick, bot_pass):
    '''
    Función que se encarga de conectar a un bot en un canal del 
    servidor IRC. Es necesario especificar la dirección IP del 
    servidor, el puerto por el que recibe conexiones, el nombre 
    del canal al que se desea conectar, un nombre para el bot y 
    la contraseña del servidor (por si fuera necesaria).
    '''
    
    # Definición del socket
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to: {server} {port}")
    new_socket.connect((server, port))
    
    # Autentificación
    new_socket.send(bytes("USER " + bot_nick + " " + bot_nick +" " + bot_nick + " :Python bot\n", "UTF-8"))
    new_socket.send(bytes("NICK " + bot_nick + "\n", "UTF-8"))
    new_socket.send(bytes("NICKSERV IDENTIFY " + bot_nick + " " + bot_pass + "\n", "UTF-8"))
    time.sleep(5)
    
    # Unirse al canal
    new_socket.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    print(f"Joined the channel {channel}")

    files_links = []

    # Función del bot
    try:
        while True:

            # Recibe mensaje
            resp = new_socket.recv(2040).decode("UTF-8")
            print(f"Received message: {resp}")

            if resp.find("PING") != -1:                      
                new_socket.send(bytes("PONG " + resp.split()[1] + '\r\n', "UTF-8")) 

            # Agregar un archivo
            if "http" in resp and channel in resp and "file" in resp:
                
                user = resp.partition("!")[0]
                file = resp[resp.index("http"):-2]
                log = "File:" + file + "  ---  Uploaded by" + user

                files_links.append(log)

                to_send_message = "PRIVMSG " + channel + " " + "Received file: " + file + "\n"
                print(f"Sending message: {to_send_message}")
                new_socket.send(bytes(to_send_message, "UTF-8"))

            # Mostrar los links de archivos
            elif "list_files" in resp.lower():
                if files_links == []:
                    to_send_message = "PRIVMSG " + channel + " " + "No files uploaded" + "\n"
                    print(f"Sending message: {to_send_message}")
                    new_socket.send(bytes(to_send_message, "UTF-8"))
                else:
                    to_send_message = "PRIVMSG " + channel + " " + "Saved files:" + "\n"
                    print(f"Sending message: {to_send_message}")
                    new_socket.send(bytes(to_send_message, "UTF-8"))

                    for elem in files_links:
                        to_send_message = "PRIVMSG " + channel + " " + elem + "\n"
                        print(f"Sending message: {to_send_message}")
                        new_socket.send(bytes(to_send_message, "UTF-8"))

            time.sleep(3)

    except(KeyboardInterrupt):
        new_socket.close()

argv = sys.argv
if not ("-h" in argv and "-p" in argv and "-c" in argv and 
    "-b" in argv and "-p" in argv):
    print('Usage: python3 bot_irc.py -h host -p port -c channel -b bot_nick -p password')

server   = argv[argv.index("-h") + 1]
port     = int(argv[argv.index("-p") + 1])
channel  = "#" + argv[argv.index("-c") + 1]
bot_nick = argv[argv.index("-b") + 1]
bot_pass = argv[argv.index("-p") + 1]

connect_bot_to_IRC(server, port, channel, bot_nick, bot_pass)