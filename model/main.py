from model_main import model_init, img_maker
from utils.tcp_server import ServerSocket
from models.Alignment import Alignment
from utils.shape_predictor import face_predicter

if __name__ == "__main__":
    dat = "utils/dat/shape_predictor_81_face_landmarks.dat"
    mesh = face_predicter(dat)
    args = model_init()
    align = Alignment(args)
    server = ServerSocket()
    while 1:
        img = server.receiveImages()
        ## 사진 받는것 까진 완료 하지만 다시 나가는게 안됨.
        ## 정 안되면 여기서 firebase에 올려서 그걸 받는 방법으로 해야될 수도 있음.
        ## firebase 구현
        # print(type(img))
        img = mesh.run(img)
        # img.save("test.png")
        img_maker(args,img,align)
    # img = np.array(img)
        # res_img = 
        # res_img.save("test.png")
        # # server.sock.send("length".encode('utf-8').ljust(64))
        # # server.sendImages(res_img)
        # server.socketClose()