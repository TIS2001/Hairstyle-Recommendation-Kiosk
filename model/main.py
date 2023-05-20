from model_main import model_main
from utils.tcp_server import ServerSocket


if __name__ == "__main__":
    while 1:
        server = ServerSocket()
        img = server.receiveImages()
        ## 사진 받는것 까진 완료 하지만 다시 나가는게 안됨.
        ## 정 안되면 여기서 firebase에 올려서 그걸 받는 방법으로 해야될 수도 있음.
        ## firebase 구현
        res_img = model_main(img)
        res_img.save("test.png")
        # server.sock.send("length".encode('utf-8').ljust(64))
        # server.sendImages(res_img)
        server.socketClose()