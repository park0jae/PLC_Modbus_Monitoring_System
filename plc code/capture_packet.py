from scapy.all import sniff, TCP, Ether, IP
from modbus import *
from elasticsearch import Elasticsearch
from datetime import datetime, timezone, timedelta

# Elasticsearch 연결 설정
es = Elasticsearch(['호스트 및 포트 지정'])  # Elasticsearch 호스트 및 포트를 변경하세요

# TCP 502 포트에 Modbus 프로토콜 바인딩
bind_layers(TCP, ModbusADURequest, dport=502)
bind_layers(TCP, ModbusADUResponse, sport=502)
cnt = 1

def packet_info(packet):

    eth_layer = packet.getlayer(Ether)
    ip_layer = packet.getlayer(IP)
    tcp_layer = packet.getlayer(TCP)
    modbus_layer = packet.getlayer(ModbusADURequest) or packet.getlayer(ModbusADUResponse)
    modbus_function_code = modbus_layer.funcCode if modbus_layer else None

    print("modbus_layer=", modbus_layer)
    print("modbus_function_code=",modbus_function_code)

    # modbus_layer 는 두 부분으로 나뉘어짐, 앞에가 info, 뒤가 function_code_info
    modbus_layer_remove = str(modbus_layer).replace(" ", "")
    modbus_info = modbus_layer_remove.split("/")  

    modbus_layer_info = modbus_info[0][9:]
    modbus_funcCode_info = modbus_info[1]

    if "Unknown" in modbus_funcCode_info:
        search_str = "Unknown"
        index = modbus_funcCode_info.index(search_str) + len(search_str)
        new_str = modbus_funcCode_info[index:]
    else :
        new_str = modbus_funcCode_info[11:]

    print("new_str = ", new_str);

    if "Error" in str(new_str):
        print("FAILED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        suc_or_fail = "Failed"
    else:
        suc_or_fail = "Success"

    print("suc_or_fail=", suc_or_fail)      
    print("-----------------------------------")

    datetime_utc = datetime.utcnow()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_kst = datetime_utc.astimezone(timezone_kst)

    packet_dict = {
        'suc_or_fail': suc_or_fail,
        'eth_src': eth_layer.src if eth_layer else None,
        'eth_dst': eth_layer.dst if eth_layer else None,
        'ip_src': ip_layer.src if ip_layer else None,
        'ip_dst': ip_layer.dst if ip_layer else None,
        'tcp_sport': tcp_layer.sport if tcp_layer else None,
        'tcp_dport': tcp_layer.dport if tcp_layer else None,
        'modbus_func_type': modbus_layer_info,
        'modbus_func_code': modbus_function_code,
        'modbus_func_info': new_str,
        'timestamp': datetime_utc.isoformat()
    }

    print(packet_dict)

    return packet_dict

def send_to_elastic(packet_dict):
    # if packet_dict['suc_or_fail'] == 'Success':
        #datetime_utc = datetime.utcnow()

        #timezone_kst = timezone(timedelta(hours=9))
        #datetime_kst = datetime_utc.astimezone(timezone_kst)

        #current_time = datetime_kst.strftime('%Y-%m-%d_%H%M')
        now = datetime.now()
        current_time = now.strftime('%Y-%m-%d_%H%M')


        # 인덱스 이름 설정
        index_name = f"packets-{current_time}"

        res = es.index(index=index_name, body=packet_dict)
        print("-------------------")
        print("result =", res['result'])
        print("-------------------")
        if res['result'] == 'created':
            print(f"Elasticsearch로 패킷 전송 성공: {packet_dict}")
        else:
            print(f"Elasticsearch로 패킷 전송 실패: {packet_dict}")

def process_packet(packet):
    if packet.haslayer(ModbusADUResponse) or packet.haslayer(ModbusADURequest):
        packet_dict = packet_info(packet)
        print("packet_dict",packet_dict);
        send_to_elastic(packet_dict)
    else:
        print(packet.summary())



if __name__ == '__main__':
    sniff(prn=process_packet, iface='인터페이스 이름')


