#해시 전송 클라이언트(호스트3)

import hashlib
from scapy.all import sniff, TCP
import socket
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse

# 첫번째 호스트와의 통신을 위한 TCP 소켓을 생성합니다.
host_1st = 'localhost'
port = 8989
sock_1st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_1st.connect((host_1st, port))

def packet_callback(packet):
    if TCP in packet:
        try:
            # TCP payload를 추출하고 해싱합니다.
            tcp_payload = packet[TCP].payload
            if ModbusADURequest in tcp_payload or ModbusADUResponse in tcp_payload:
                  hash_payload = hashlib.sha256(str(tcp_payload).encode()).hexdigest()
                  # 출력: 해시된 payload
                  print("Hashed Payload: ", hash_payload)

                  # 해싱된 payload를 첫번째 호스트에게 TCP 통신으로 전달합니다.
                  sock_1st.sendall(hash_payload.encode())

        except Exception as e:
            print("TCP payload 해싱 에러: ", e)

# TCP 패킷을 캡처합니다.
sniff(iface='인터페이스 이름', filter="tcp and port 502", prn=packet_callback)