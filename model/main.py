from model_main import Img_model
from utils.tcp_server import ServerSocket
from utils.shape_predictor import face_predicter
import cv2
import numpy as np

if __name__ == "__main__":
    pre = "utils/dat/shape_predictor_81_face_landmarks.dat"
    det = "utils/dat/mmod_human_face_detector.dat"
    mesh = face_predicter(pre,det)
    model = Img_model()
    server = ServerSocket()
    # cred = credentials.Certificate('easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
    # firebase_app = initialize_app(cred, { 'storageBucket': 'easylogin-58c28.appspot.com'})
    # db = firestore.client()
    # while 1:
    for i in range(1):
        conn , addr = server.sock.accept()
        mode = conn.recv(64)
        print(mode.decode('utf-8'))
        image_name = conn.recv(64)
        print(image_name.decode('utf-8'))
        # if int(mode):
        #     npy = get_numpy_from_db(image_name)
        # else:
        #     img = get_image_from_db(image_name)
            
        
        # cv2.imwrite("in.jpg",img)
        # print(img)
        # img = cv2.imread("test.jpg")
        # try:s
        # img = mesh.run(img) ## output : PIL
        style = conn.recv(64)
        print(style.decode('utf-8'))
        color = conn.recv(64)
        print(color.decode('utf-8'))
        # model.img_maker(img)
        # res_img = model.align.align_images(img, style, "fidelity", align_more_region=False, smooth=5)
        # dying_img = model.dying_main(img,color)
        # server.sendImages(dying_img)
        conn.close()
        # except:
            # pass
