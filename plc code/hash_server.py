# 해시 처리 서버(호스트1)

from elasticsearch import Elasticsearch
import socket
import threading
import time
from datetime import datetime,timezone, timedelta


# Elasticsearch 설정
es = Elasticsearch(['호스트 및 포트 지정'])

# 첫번째 호스트의 주소와 포트 정의
host = '0.0.0.0'
port = 8989 

# TCP/IP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 포트에 바인드
server_address = (host, port)
sock.bind(server_address)

# 들어오는 연결을 대기
sock.listen(2)

hashes_received_host2 = []
hashes_received_host3 = []

client_counter=0

def handle_client_connection(client_socket, host_number):
    print(f"클라이언트 {host_number} 연결 완료")
    while True:
        # 소켓에서 데이터 수신
        data = client_socket.recv(1024)
        if data:
            hash_received = data.decode()
            
            # 호스트에 따라 해시를 해당 리스트에 추가
            if host_number == 2:
                hashes_received_host2.append(hash_received)
            else:
                hashes_received_host3.append(hash_received)
        else:
            break

    client_socket.close()

def send_to_elasticsearch(hash2, hash3, match_status):
    # 현재 시간을 YYYYMMDDHHMMSS 형식으로 가져오기

    datetime_utc = datetime.utcnow()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_kst = datetime_utc.astimezone(timezone_kst)
    
    current_time = datetime_kst.strftime('%Y-%m-%d_%H%M')

    # Elasticsearch로 해시 전송
    es.index(index=f'hash-{current_time}', body={"hash_host2": hash2, "hash_host3": hash3, "match_status": "Matched" if match_status else "Mismatch", 'timestamp': datetime_kst.isoformat()})

def compare_hashes(hash1, hash2):
    # 두 해시 값을 비교하고 결과 출력
    match = hash1 == hash2
    if match:
        print(f"두 해시 값이 일치합니다.\n Hash1: {hash1},\n Hash2: {hash2}")
    else:
        print(f"두 해시 값이 일치하지 않습니다.\n Hash1: {hash1},\n Hash2: {hash2}")
    return match


def listen_hashes():
    while True:
        time.sleep(0.1)
        
        # 두 해시 값을 비교 (두 호스트로부터 각각 해시가 도착하면)
        print(len(hashes_received_host2), len(hashes_received_host3))

        if len(hashes_received_host2) > 0 and len(hashes_received_host3) > 0:
            match_status = compare_hashes(hashes_received_host2[0], hashes_received_host3[0])

            # 받은 해시를 Elasticsearch로 전송
            es_thread = threading.Thread(target=send_to_elasticsearch, args=(hashes_received_host2[0], hashes_received_host3[0], match_status))
            es_thread.start()

            # 비교한 두 해시 값을 리스트에서 제거
            hashes_received_host2.pop(0)
            hashes_received_host3.pop(0)

        if len(hashes_received_host2) != len(hashes_received_host3):
            while True:
                if len(hashes_received_host2)==0:
                    break
                hashes_received_host2.pop(0)
            while True:
                if len(hashes_received_host3)==0:
                    break
                hashes_received_host3.pop(0)

listen_thread = threading.Thread(target=listen_hashes)
listen_thread.start()

while True:
    try:
        # 연결 대기
        print('연결을 대기 중입니다')
        client_socket, client_address = sock.accept()

        # 첫 번째 연결이 호스트2로, 두 번째 연결이 호스트3로 가정합니다.
        host_number = client_counter % 2 + 2
        client_counter += 1
        
        # 각 클라이언트 소켓을 처리하는 스레드 생성
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, host_number))
        client_thread.start()
    except KeyboardInterrupt:
        print("프로그램이 강제로 종료되었습니다.")
        sock.close()
        break
    except Exception as e:
        print(f"예기치 못한 오류가 발생했습니다: {e}")
        sock.close()
        break