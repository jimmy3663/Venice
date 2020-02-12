# server.py : 연결해 1 보낼 수 있음.
import socket
import Manager #무호흡 계산을 위한 놈
import pcm2wav
import mysqlprac as msp
import mysql4login as m4log
import Apnea_dB


def decode_rcv_message(v):
   temp = v.decode()
   val = ""
   if len(temp) >= 2:
      for i in range(2,len(temp)):
         val += temp[i]
   return val


def make_apnea_info_send_message(v):
   
   temp = v[0]+"+"+v[1]+"+"+v[2]+"+"+v[3]
   length = len(temp)
   val = bytearray(b'\x00')
   val.append(length)
   val.extend(temp.encode('utf-8'))
   return val

def make_Login_info_send_message(v):
   if v >= 1:
      val = bytearray(b'\x00\x011')
   else:
      val = (b'\x00\x010')
   return val
   

host = '192.168.2.1' # 호스트 ip를 적어주세요
port = 9998            # 포트번호를 임의로 설정해주세요

#소켓 생성, IPv4, TCP
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#WinError 10048해결을위한(포트 사용중이라 연결할수없음) -->더 알아보기
#server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

server_sock.bind((host, port))
server_sock.listen()

print("기다리는 중")

flag = 0
data = b''

while True:
   client_sock, addr = server_sock.accept()
   newbuf = client_sock.recv(17620)
   print("연결은 됐고")
   print(newbuf[2])
   if not newbuf:
      break
   if newbuf == b'\x00\x06Search':
      #val = Manager.Manager()
      print("Search")
      val = Apnea_dB.Find_dB_value();
      send = make_apnea_info_send_message(val)
      print(send)
      client_sock.sendall(send)
      client_sock.close()
      data = b''
      continue
   elif newbuf[2] == 82:
      print("Register")
      message = newbuf
      if msp.mysqlcon(message.decode('utf-8')) == 1:
         send = make_Login_info_send_message(1)
         client_sock.sendall(send)
      else:
         send = make_Login_info_send_message(0)
         client_sock.sendall(send)
      client_sock.close()
      data = b''
      continue
   elif newbuf[2] == 76:
      print("login!")
      message = newbuf
      if m4log.mysql4login(message.decode('utf-8')) == 1:
         send = make_Login_info_send_message(1)
         client_sock.sendall(send)
         print("login success!!")
      else:
         send = make_Login_info_send_message(0)
         client_sock.sendall(send)
      client_sock.close()
      data = b''
   else:
      while True:
         print("Recording")
         newbuf = client_sock.recv(17620)
         if not newbuf:
            break
         data += newbuf
      break
if data != b'':
   pcm2wav.pcm2wav(data,'test_set.wav',1,16,44100)
   val = Manager.Manager('test_set.wav')
   Apnea_dB.Insert_dB_value(val)

client_sock.close()
server_sock.close()
