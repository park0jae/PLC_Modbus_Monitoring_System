# PLC_Modbus_Monitoring_System

**Environments**
<br>
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

**Developments**
<br>
<img src="https://img.shields.io/badge/PYTHON-6DB33F?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF12?style=for-the-badge&logo=javascript&logoColor=white">

<br>

# Project 🔍
- 프로젝트명 : 산업 분야에서 사용하는 PLC 통신 프로토콜 분석 및 자동 탐지 시스템
- 개발 환경 : ubuntu 22.04
- 개발 언어 : Python, HTML5, CSS3, Javascript
- 사용 툴 : Elasticsearch, Kibana , XG 5000 (LS산전사의 PLC 소프트웨어)
- 사용 장비 : XBC-DN32U(LS 산전), ipTIME_N104E_Plus, RaspberryPi4

<br>

# Guide 🔍

### Diagram
![](https://velog.velcdn.com/images/okvv26/post/ef4668d6-2eb9-48b8-a85a-a8225f95dcdb/image.png)

<br>

### Requirements
For building and running this project you need : 
- elasticsearch 7.16.2
- kibana 7.16.2
- python 3.10.x
  - scapy 2.5.0
  - pymodbus 3.3.1

<br>

### Installation
```
$ git clone https://github.com/park0jae/PLC_Modbus_Monitoring_System.git
$ cd PLC_Modbus_Monitoring_System
```

<br>

### Run
```
// Web : "호스트주소:포트번호/index.html"을 통해 브라우저 열면, 키바나 화면을 보여주고 통신을 통해 오류값을 모니터링하여 토스트메시지 출력
// PLC : Hash_Client.py와 Modbus_Hash_Client.py 코드를 실행하기 위해 Hash_Server.py 코드를 통해 서버를 먼저 열어준다.
1. python Hash_Server.py 실행
2. Hash_Client.py , Modbus_Hash_Client.py 실행
3. Capture_Packet.py 실행
4. Modbus_Hash_Client.py 코드를 통해 패킷 전송
- 명령어 : q(읽기,read), w(위조), e(잘못된 요청) , r(변조) 
5. Capture_Packet.py 를 통해 캡쳐된 패킷을 Elasticsearch로 인덱싱 후 Kibana로 시각화
```

<br>


# 화면 구성

[ 정상 요청 흐름 ]
![](https://velog.velcdn.com/images/okvv26/post/ea0f2c8a-5296-47d8-a3d4-a8e4a9daa2dc/image.png)

[ 잘못된 요청  ]
![](https://velog.velcdn.com/images/okvv26/post/c3301869-9402-4f8f-9f95-9e0be0e66edc/image.png)


[ 해시 검증 오류 ]
![](https://velog.velcdn.com/images/okvv26/post/41a86370-cebe-408b-a5e0-2bf8d5f3fe2a/image.png)

<br>

📍 잘못된 요청이나 해시 검증 오류가 발생하면, 사용자의 이메일로도 경고 메일이 발송됩니다.
![](https://velog.velcdn.com/images/okvv26/post/217fa2e3-0c7d-4cf9-8387-09b264f13ba9/image.png)


