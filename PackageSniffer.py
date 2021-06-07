import scapy.all as scapy
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s : %(message)s \n')
TCP = 0
RAW = 3


def sniff_package():
    package = scapy.sniff(filter='port 6667', count=1)
    tcp = package[TCP]
    logging.info(tcp[RAW])
    return tcp[RAW]


thread_n = 5
i = 15000
executor = ThreadPoolExecutor(max_workers=thread_n)
with ThreadPoolExecutor(max_workers=thread_n):
    while i:
        i -= 1
        result = executor.submit(sniff_package)

