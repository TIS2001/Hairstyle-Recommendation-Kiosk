from model_main import Img_model
from utils.tcp_server import ServerSocket
from utils.shape_predictor import face_predicter


if __name__ == "__main__":
    dat = "utils/dat/shape_predictor_81_face_landmarks.dat"
    mesh = face_predicter(dat)
    model = Img_model()
    server = ServerSocket()
    while 1:
        img = server.receiveImages()
        img = mesh.run(img) ## output : PIL
        
        img = model.img_maker(img)
        
        dying_img = model.dying_main(img)
        # server.sendImages(dying_img)
        server.conn.close()
