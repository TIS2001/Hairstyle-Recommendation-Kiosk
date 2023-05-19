from model_main import model_main
from utils.tcp_server import ServerSocket

if __name__ == "__main__":
    server = ServerSocket()
    img = server.img
    model_main(img)