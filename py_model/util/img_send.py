import socket
import time
import numpy
import cv2
import sys
import pybase64 as base64

class ClientVideoSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.img = None

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
        except Exception as e:
            print(e)
            time.sleep(1)
            self.connectServer()
    def sendImages(self,img):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, frame = cv2.imencode(".jpg",img,encode_param)
        data = numpy.array(frame)
        stringData = base64.b64encode(data)
        length = str(len(stringData))
        self.sock.sendall(length.encode('utf-8').ljust(64))
        self.sock.send(stringData)
        print('send images')
        time.sleep(0.02)
        self.sock.close()
        time.sleep(1)
        # self.connectServer()
        # self.sendImages()

def img_send(img):
    TCP_IP = "211.243.232.32"
    TCP_PORT = 7100
    client = ClientVideoSocket(TCP_IP, TCP_PORT)
    client.connectServer(img)


if __name__ == "__main__":
    img_send()
