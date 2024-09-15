from scapy.all import PcapReader as ScapyPcapReader, RawPcapReader, IP, TCP
from typing import Generator
from dataclasses import dataclass

@dataclass
class Packet:
    id: str
    timestamp: float
    length: int

class PcapReader:
    def __init__(self, file):
        self.pcap_file = file
        self.start_time=None
        
        pcap_reader = ScapyPcapReader(self.pcap_file)
        try:
            for packet in pcap_reader:
                self.start_time=float(packet.time)
                break
        finally:
            pcap_reader.close()
        
        
        

    def stream_reader(self) -> Generator[Packet, None, None]:
        pcap_reader = ScapyPcapReader(self.pcap_file)
        try:
            for packet in pcap_reader:
                if IP in packet and TCP in packet:
                    yield Packet(
                        timestamp=float(packet.time),
                        id=f'{packet[IP].src}_{packet[IP].dst}',
                        length=packet.wirelen
                    )
        finally:
            pcap_reader.close()

# reader = PcapReader("data_capture\\traffic\\capture-2024-06-27_17-49-07.pcap")

# for packet in reader.stream_reader():
#     print(f"Timestamp: {packet.timestamp}, id: {packet.id}, Length: {packet.length}")
#     break
