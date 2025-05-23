from scanner.base_module import ScannerModule
from scanner.utils import get_popular_ports
from urllib.parse import urlparse
from scapy.all import IP, TCP, sr1, sr, send, sniff
import socket

class PortScanner (ScannerModule):
    def __init__(self, scan_mode='stelth'):
        self.scan_mode = scan_mode

    def get_destination_ip(self, url):
        try:
            print(f"[*] Получаем IP-адрес цели")
            parsed_url = urlparse(url)
            domain = parsed_url.netloc 
            destination_ip = socket.gethostbyname(domain)
            print(f"[OK] IP-адрес цели: {destination_ip}") 
            return destination_ip
        except socket.gaierror as e:
            print(f"[!] Ошибка при получении IP-адреса цели: {e}")
    
    def craft_tcp_syn_packet(self, destination_ip, port):
        return IP(dst=destination_ip)/TCP(dport=port, flags='S')
    
    def tcp_response_handler(self, response):
        print(response)

    def packet_callback(pkt):
        if pkt.haslayer(IP):
            pkt.show()

    def scan_ports(self, url):
        destination_ip = self.get_destination_ip(url)
        popular_ports = get_popular_ports()
        
        for port in popular_ports:
            syn_tcp = self.craft_tcp_syn_packet(destination_ip, port)
            answered, unanswered = send(syn_tcp, timeout=2, verbose=1)
            sniff(filter=f"host {destination_ip}", timeout=3, prn=self.packet_callback)
            
    def run(self, url):
        self.scan_ports(url)