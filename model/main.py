from model_main import Img_model
from utils.tcp_server import ServerSocket
from utils.shape_predictor import face_predicter
from firebase_admin import credentials, firestore, initialize_app, storage
import os
import cv2
import numpy as np
import pybase64 as base64
import io
from PIL import Image

class Database:
    def __init__(self):
        self.cred = credentials.Certificate('./princess-maker-1f45e-firebase-adminsdk-dwlbp-74b3b65023.json')
        self.firebase_app = initialize_app(self.cred, { 'storageBucket': 'princess-maker-1f45e.appspot.com'})
        self.bucket = storage.bucket(app=self.firebase_app)

    def download_npy_file(self,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            blob.download_to_file(stream)
            stream.seek(0)
            file_ = np.load(stream)
            # file_ = np.array(file_)
            # print(file_)
        return file_

    def download_npz_file(self,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            blob.download_to_file(stream)
            stream.seek(0)
            file_ = np.load(stream)
            file_ = {"latent_in": np.array(file_["latent_in"]), "latent_F":np.array(file_["latent_F"])}
        return file_

    def download_image_file(self,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            blob.download_to_file(stream)
            stream.seek(0)
            # print(stream)
            file_ = Image.open(stream).copy()
            # file_ = cv2.imdecode(stream,cv2.IMREAD_COLOR)
        return file_

    def upload_npy_file(self,f,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            np.save(stream,f)
            stream.seek(0)
            blob.upload_from_file(stream)
        
    def upload_npz_file(self,f,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            np.savez(stream, latent_in=f["latent_in"], latent_F=f["latent_F"])
            stream.seek(0)
            blob.upload_from_file(stream)


if __name__ == "__main__":
    pre = "utils/dat/shape_predictor_81_face_landmarks.dat"
    det = "utils/dat/mmod_human_face_detector.dat"
    mesh = face_predicter(pre,det)
    model = Img_model()
    # server = ServerSocket()
    db = Database()
    
    for i in range(1):
        # conn , addr = server.sock.accept()
        # mode = conn.recv(1).decode('utf-8')
        # image_name = conn.recv(64).decode('utf-8')

        mode = 0
        image_name = "선동진_photo"
        img = db.download_image_file(f"customers/{image_name}.jpg")
        
        
        img = mesh.run(np.array(img))
        if mode: 
            ## 얼굴형 판단 후 고객 정보에 저장 구현 필요
            target_numpy =  model.img_maker(img) ## [0] latent_in [1] latent_FS
            db.upload_npz_file(target_numpy[0],f"customers_npz/{image_name}.npz")
            db.upload_npy_file(target_numpy[1],f"customers_npy/{image_name}.npy")
        else:
            latent_FS = db.download_npz_file(f"customers_npz/{image_name}.npz")
            latent_W = db.download_npy_file(f"customers_npy/{image_name}.npy")
            target_numpy =  [latent_FS,latent_W]

        # style = conn.recv(64).decode('utf-8').split('\\')
        # # style npz 불러오기
        style_img = db.download_image_file(f'{style[0]}/{style[1]}.jpg')
        latent_FS = db.download_npz_file(f'{style[0]}/{style[1]}.npz')
        latent_W = db.download_npy_file(f'{style[0]}/{style[1]}.npy')
        style_numpy = [latent_FS,latent_W]
        # color = conn.recv(64)
        # print(color.decode('utf-8'))
        
        res_img = model.align.align_images(img, style_img,target_numpy,style_numpy, "fidelity", align_more_region=False, smooth=5)
        # cv2.imwrite("test4.jpg",res_img)
        # dying_img = model.dying_main(res_img,color)
        server.sendImages(dying_img)
        conn.close()
        # except:
            # pass
