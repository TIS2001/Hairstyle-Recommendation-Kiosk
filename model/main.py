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
from rembg import remove
import time
from tqdm import tqdm

class Database:
    def __init__(self):
        self.cred = credentials.Certificate('./princess-maker-1f45e-firebase-adminsdk-dwlbp-74b3b65023.json')
        self.firebase_app = initialize_app(self.cred, { 'storageBucket': 'princess-maker-1f45e.appspot.com'})
        self.bucket = storage.bucket(app=self.firebase_app)
        self.db = firestore.client()
        self.shape_name = {0:"각진형",1:"둥근형",2:"계란형",3:"긴얼굴형"}
        
    def get_info(self,id):
        self.doc_ref = self.db.collection('customers').document(id)
        doc = self.doc_ref.get()
        self.customer_data = doc.to_dict()
        if self.customer_data["gender"]=="여자":
            self.customer_data["gender"]=0
        else:
            self.customer_data["gender"]=1
        
    def shape_update(self,shape):
        self.customer_data["shape"] = self.shape_name[shape]
        if self.customer_data["gender"]==0:
            self.customer_data["gender"]="여자"
        else:
            self.customer_data["gender"]="남자"
                
        self.doc_ref.set(self.customer_data)

    def download_npy_file(self,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(file_name)
            blob.download_to_file(stream)
            stream.seek(0)
            file_ = np.load(stream)
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

    def get_HSV_from_Image(self,file_name):
        img = self.download_image_file(file_name)
        img = np.array(img)
        hsvImage = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
        hsvImage = np.float32(hsvImage)
        # 채널로 분리하는 함수  ( 다차원일 경우 사용)
        H, S, V = cv2.split(hsvImage)
        return H[0][0],S[0][0],V[0][0]

    def upload_img_file(self,f,file_name):
        with io.BytesIO() as stream:
            blob = self.bucket.blob(f'hairstyles_man/{file_name}')
            # np.savez(stream, latent_in=f["latent_in"], latent_F=f["latent_F"])
            f.save(stream,format='JPEG')
            stream.seek(0)
            blob.upload_from_file(stream)
    
        

if __name__ == "__main__":
    pre = "utils/dat/shape_predictor_81_face_landmarks.dat"
    det = "utils/dat/mmod_human_face_detector.dat"
    face_pre = face_predicter(pre,det)
    model = Img_model()
    server = ServerSocket()
    db = Database()
    gender_path = {"여자":"hairstyles_woman","남자":"hairstyles_man"}
    
    styel_path = "/workspace/princess_maker/Hairstyle-Recommendation-Kiosk/py_model/UI/hairstyles/female/추가/"
    while True:
        server.conn , server.addr = server.sock.accept()
        print("Connected")
        re_select = 5
        while re_select==5:
            try:
                mode = int(server.conn.recv(1).decode('utf-8'))
                image_name = server.conn.recv(64).decode('utf-8')
                info = db.get_info(image_name)
                img = db.download_image_file(f"customers/{image_name}.jpg")
                output = remove(img)
                server.sendImages_png(output)
                img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
                img = face_pre.run(img)
                shape = face_pre.face_shape(img,db.customer_data["gender"])
                db.shape_update(shape)

                if mode: 
                    ## 얼굴형 판단 후 고객 정보에 저장 구현 필요
                    img = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(img)
                    target_numpy =  model.img_maker(img) ## [0] latent_in [1] latent_FS
                    db.upload_npz_file(target_numpy[0],f"customers_npz/{image_name}.npz")
                    db.upload_npy_file(target_numpy[1],f"customers_npy/{image_name}.npy")
                else:
                    latent_FS = db.download_npz_file(f"customers_npz/{image_name}.npz")
                    latent_W = db.download_npy_file(f"customers_npy/{image_name}.npy")
                    target_numpy =  [latent_FS,latent_W]
                re_select=6
                while re_select==6:
                    style_color = server.conn.recv(64).decode('utf-8').split('/')
                    style, color = style_color
                    if style == "no_apply":
                        style_numpy = target_numpy
                    else:
                        style_img = db.download_image_file(f'{gender_path[db.customer_data["gender"]]}/{style}.jpg')
                        latent_FS = db.download_npz_file(f'{gender_path[db.customer_data["gender"]]}/{style}.npz')
                        latent_W = db.download_npy_file(f'{gender_path[db.customer_data["gender"]]}/{style}.npy')
                        style_numpy = [latent_FS,latent_W]

                    res_img = model.align.align_images(img, style_img,target_numpy,style_numpy, "fidelity", align_more_region=False, smooth=5)

                    if color == "no_apply":
                        color = None
                    else:
                        color = db.get_HSV_from_Image(f'color/{color}.JPG')
                        res_img = model.dying_main(res_img,color)

                    res_img_test = cv2.cvtColor(res_img , cv2.COLOR_RGB2BGR)
                    server.sendImages(res_img)
                    re_select = int(server.conn.recv(1).decode('utf-8'))
                    print("re_select:",re_select)
            except Exception as e: 
                print(e)
                re_select = 0
        server.conn.close()
