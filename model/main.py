from model_main import Img_model
from utils.tcp_server import ServerSocket
from utils.shape_predictor import face_predicter
import cv2

if __name__ == "__main__":
    pre = "utils/dat/shape_predictor_81_face_landmarks.dat"
    det = "utils/dat/mmod_human_face_detector.dat"
    mesh = face_predicter(pre,det)
    model = Img_model()
    server = ServerSocket()
    # while 1:
    for i in range(1):
        img = server.receiveImages()
        cv2.imwrite("in.jpg",img)
        # img = cv2.imread("test.jpg")
        # try:
        img = mesh.run(img) ## output : PIL
        img = model.img_maker(img)
        
        dying_img = model.dying_main(img)
        server.sendImages(dying_img)
        server.conn.close()
        # except:
            # pass
