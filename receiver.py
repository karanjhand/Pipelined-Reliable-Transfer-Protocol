import socket
import struct

MAX_SEQ_NUM = 256
SYN = 1
ACK = 2
FIN = 3

def create_ack_packet(ack_num, packet_type):
    ack_num = ack_num % MAX_SEQ_NUM
    checksum = ack_num  
    return struct.pack('!B B H', packet_type, ack_num, checksum)

def compute_checksum(seq_num, payload):
    checksum = seq_num + sum(payload)
    return checksum & 0xFFFF

def is_corrupt(packet):
    if len(packet) < 4:
        return True
    packet_type, seq_num, checksum = struct.unpack('!B B H', packet[:4])
    payload = packet[4:]
    return checksum != compute_checksum(seq_num, payload)

def parse_packet(packet):
    packet_type, seq_num = struct.unpack('!B B', packet[:2])
    payload = packet[4:]
    return packet_type, seq_num, payload

def rdt_receive(sock, expected_seq_num):
    while True:
        try:
            packet, addr = sock.recvfrom(1024)
            if is_corrupt(packet):
                print("Corrupt packet received")
                continue

            packet_type, seq_num, payload = parse_packet(packet)
            if packet_type == SYN:
                # Send SYN-ACK
                syn_ack_packet = create_ack_packet(seq_num, SYN)
                sock.sendto(syn_ack_packet, addr)
            elif packet_type == FIN:
                # Send FIN-ACK
                fin_ack_packet = create_ack_packet(seq_num, FIN)
                sock.sendto(fin_ack_packet, addr)
                break
            else:
                if seq_num == expected_seq_num:
                    print(f"Received: {payload.decode()}")
                    expected_seq_num = (expected_seq_num + 1) % MAX_SEQ_NUM
                    ack_packet = create_ack_packet(seq_num, ACK)
                    sock.sendto(ack_packet, addr)
                elif seq_num < expected_seq_num:
                    print(f"Received duplicate packet: {seq_num}")
                    ack_packet = create_ack_packet(seq_num, ACK)
                    sock.sendto(ack_packet, addr)
            
            
            
        except OSError as e:
            print(f"Socket error: {e}")
            break

if __name__ == "__main__":
    server_address = ('localhost', 12345)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    packet, addr = sock.recvfrom(1024)
    if is_corrupt(packet):
        print("Corrupt packet received")
       

    packet_type, seq_num, payload = parse_packet(packet)
    if packet_type == SYN:
        # Send SYN-ACK
        syn_ack_packet = create_ack_packet(seq_num, SYN)
        sock.sendto(syn_ack_packet, addr)
        print("Connection established")
    rdt_receive(sock, 0)
    
    sock.close()
