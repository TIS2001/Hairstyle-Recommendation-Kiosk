import socket
import cv2
import threading
import numpy
import pybase64 as base64
from PIL import Image

class ServerSocket:
    def __init__(self, ip='172.17.0.4', port=8080):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        
        # self.socketClose()
        # self.receiveThread = threading.Thread(target=self.receiveImages)
        # self.receiveThread.start()
        # not multi thread
                
    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        
    def receiveImages(self):
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')
        try:
            length = self.recvall(self.conn, 64)
            length1 = length.decode('utf-8')
            stringData = self.recvall(self.conn, int(length1))
            data = numpy.frombuffer(base64.b64decode(stringData), dtype = numpy.uint8)
            decimg = cv2.imdecode(data, 1)
            imageRGB = cv2.cvtColor(decimg , cv2.COLOR_BGR2RGB)
            return imageRGB       
        except Exception as e:
            print(e)
            self.receiveImages()


    def sendImages(self,img):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, frame = cv2.imencode(".jpg",img,encode_param)
        data = numpy.array(frame)
        stringData = base64.b64encode(data)
        
        length = str(len(stringData))
        # print(length)
        self.conn.send(length.encode('utf-8').ljust(64))
        self.conn.send(stringData)
        print('send images')
        # self.connectServer()
        # self.sendImages()
    
    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

def main():
    server = ServerSocket('172.17.0.4', 8080)
    server.receiveImages()

if __name__ == "__main__":
    main()