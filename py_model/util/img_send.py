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

    def connectServer(self,img):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
            self.sendImages(img)
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            time.sleep(1)
            self.connectServer()

    def sendImages(self,img):
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, frame = cv2.imencode(".jpg",img,encode_param)
        data = numpy.array(frame)
        numpy.save("data",data)
        stringData = base64.b64encode(data)
        length = str(len(stringData))
        self.sock.sendall(length.encode('utf-8').ljust(64))
        self.sock.send(stringData)
        print('send images')
        time.sleep(0.02)
        
        self.sock.close()
        time.sleep(1)
        self.connectServer()
        self.sendImages()

def main():
    TCP_IP = 1234
    TCP_PORT = 1234
    client = ClientVideoSocket(TCP_IP, TCP_PORT)
    client.connectServer(img)

if __name__ == "__main__":
    main()