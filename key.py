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
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

key_length = 1024


def generate_keys():
    """
    Función encargada de generar las llaves publicas y privadas de cada usuario en la red.
    Se utiliza la biblioteca de Python Crypto, la cual contiene una clase para generar claves
    de RSA de N bits.
    :return Llave privada y pública del cliente
    """
    private_key = RSA.generate(key_length)
    public_key = private_key.publickey()
    print(type(private_key), type(public_key))
    private_pem = private_key.exportKey().decode()
    public_pem = public_key.export_key().decode()
    return private_pem, public_pem


def cipher_data(data, key):
    """
    Función que se encarga de cifrar la información por medio de el
    cifrador asimétrico PKCS#1 OAEP basado en RSA.
    :param data: binarios a firmar
    :param key: llave pública RSA
    :return: datos binarios cifrados
    """
    cipher = PKCS1_OAEP.new(key=key)
    cipher_data = b''
    for i in range(0, len(data), key_length):
        cipher_data += (cipher.encrypt(data[i:i * key_length]))
    print(cipher_data)
    return cipher_data


def decipher_data(data, key):
    """
    Función que se encarga de descifrar la información por medio
    de el cifrador asimétrico PKCS#1 OAEP basado en RSA.
    :param data: binarios a descifrar
    :param key: llave privada PSA
    :return:
    """
    decrypt = PKCS1_OAEP.new(key=key)
    decrypted_data = b''
    for i in range(0, len(data), key_length):
        decrypted_data += (decrypt.decrypt(data[i:i * key_length]))
    print(decrypted_data)
    return decrypted_data