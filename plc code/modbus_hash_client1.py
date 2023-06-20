# 모드 버스 전송 클라이언트(전송 및 해시 호스트2)

import hashlib
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.pdu import ModbusRequest
from pymodbus.transaction import ModbusBinaryFramer
import struct
import socket
import threading
from scapy.all import sniff, Raw
from scapy.layers.inet import TCP, IP
from scapy.contrib.modbus import ModbusADURequest, ModbusADUResponse

# 세번째 호스트와 첫번째 호스트의 주소와 포트 정의
host_3rd = '호스트 주소'
host_1st = '호스트 주소'
port = 8989

# Modbus 클라이언트 초기화
client = ModbusTcpClient(host_3rd, 502)

# 첫번째 호스트로 TCP 통신을 위한 소켓 생성
sock_1st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_1st.connect((host_1st, port))

def send_modbus_command(client):
    # 세번째 호스트로 Modbus 명령을 보냄
    request = client.read_holding_registers(1,10)
def send_modbus_wrong(client):
    sock_1st.sendall("aaa6058b56e50e7239df12b4a181a912550861fbf4ca7635b30b105e5d0818d0".encode())
    request = client.read_holding_registers(1,10)
class CustomModbusRequest(ModbusRequest):
    function_code = 0x81  # 이 값을 원하는 함수 코드로 변경

    def __init__(self, address=None, count=None, **kwargs):
        ModbusRequest.__init__(self, **kwargs)
        self.address = address
        self.count = count

    def encode(self):
        return struct.pack('>BHH', self.function_code, self.address, self.count)

    def decode(self, data):
        self.function_code, self.address, self.count = struct.unpack('>BHH', data)

def send_modbus_error(client):
    print("error")
    request = CustomModbusRequest(1,10)
    response = client.execute(request)

    print(response)


def packet_callback(packet):
    if TCP in packet:
        try:
            tcp_payload = packet[TCP].payload

            # Modbus 패킷인지 확인합니다.
            if ModbusADURequest in tcp_payload or ModbusADUResponse in tcp_payload:
                # TCP payload를 추출하고 해싱합니다.
                hash_payload = hashlib.sha256(str(tcp_payload).encode()).hexdigest()

                # 해싱된 payload를 첫번째 호스트에게 TCP 통신으로 전달합니다.
                sock_1st.sendall(hash_payload.encode())

                # 해시 값 출력
                print("해시 값: ", hash_payload)
                
        except Exception as e:
            print("TCP payload 해싱 에러: ", e)

def user_input():
    while True:
        user_command = input("Enter 's' to send a Modbus command: ")
        if user_command.lower() == 's':
            send_modbus_command(client)
        elif user_command.lower() == 'w':
            send_modbus_wrong(client)
        elif user_command.lower() == 'e':
            send_modbus_error(client)
# Scapy 스니핑 스레드 생성 및 시작
sniff_thread = threading.Thread(target=sniff, kwargs={'iface' : '인터페이스 이름' , 'filter': 'tcp port 502', 'prn': packet_callback})
sniff_thread.start()

# 사용자 입력 처리 스레드 생성 및 시작
input_thread = threading.Thread(target=user_input)
input_thread.start()

# 스레드들이 완전히 종료될 때까지 기다립니다.
sniff_thread.join()
input_thread.join()

# 종료된 후에만 클라이언트와 소켓을 닫습니다.
client.close()
sock_1st.close()