import numpy as np
import PIL
import PIL.Image as Image
import scipy
import scipy.ndimage
import dlib
from pathlib import Path
import torchvision
import cv2
import os
"""
brief: face alignment with FFHQ method (https://github.com/NVlabs/ffhq-dataset)
author: lzhbrian (https://lzhbrian.me)
date: 2020.1.5
note: code is heavily borrowed from
    https://github.com/NVlabs/ffhq-dataset
    http://dlib.net/face_landmark_detection.py.html

requirements:
    apt install cmake
    conda install Pillow numpy scipy
    pip install dlib
    # download face landmark model from:
    # http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
"""
class face_predicter:
    def __init__(self,pre,det):
        self.predictor = dlib.shape_predictor(pre)
        self.detector = dlib.cnn_face_detection_model_v1(det)
        self.shape_init("./dat")
    
    def shape_init(self,path):
        self.shape_numpy = {"man":[],"woman":[]}
        paths = ["man","woman"]
        for j in paths:
            for i in os.listdir(os.path.join(path,j)):
                if os.path.splitext(i)[1] != ".npy":
                    continue ## 에러처리해야댐
                # print(i)
                np_path = os.path.join(path,j,i)
                self.shape_numpy[j].append(np.load(np_path))
            
    def get_landmark(self,img):
        """get landmark with dlib
        :return: np.array shape=(68, 2)
        """
        # self.detector = dlib.cnn_face_detection_model_v1(det)
        # print(type(img))
        det = self.detector(img, 1)[0].rect
        shape = self.predictor(img, det)

        lm = np.array([[tt.x, tt.y] for tt in shape.parts()])

        return lm

    def face_shape(self,img,gender=1): # PIL
        img = np.array(img)
        target_landmark = self.get_landmark(img)
        target_landmark = np.concatenate([target_landmark[0: 17],target_landmark[68:]])
        # print(target_landmark)
        if gender:
            shape_dat = self.shape_numpy["man"]
        else:
            shape_dat = self.shape_numpy["woman"]
        gb_error = float("inf")
        for i,shape_landmark in enumerate(shape_dat):
            # print(np.abs(shape_landmark - target_landmark))
            error = sum(sum(np.abs(shape_landmark - target_landmark)))
            print(error)
            # print(error)
            if gb_error > error :
                gb_error = error
                shape = i
        return shape

        



    def align_face(self,img):
        """
        :param filepath: str
        :return: list of PIL Images
        """

        lm = self.get_landmark(img)

        lm_chin = lm[0: 17]  # left-right
        lm_eyebrow_left = lm[17: 22]  # left-right
        lm_eyebrow_right = lm[22: 27]  # left-right
        lm_nose = lm[27: 31]  # top-down
        lm_nostrils = lm[31: 36]  # top-down
        lm_eye_left = lm[36: 42]  # left-clockwise
        lm_eye_right = lm[42: 48]  # left-clockwise
        lm_mouth_outer = lm[48: 60]  # left-clockwise
        lm_mouth_inner = lm[60: 68]  # left-clockwise
        fore_head = lm[68:81]

        # Calculate auxiliary vectors.
        eye_left = np.mean(lm_eye_left, axis=0)
        eye_right = np.mean(lm_eye_right, axis=0)
        eye_avg = (eye_left + eye_right) * 0.5
        eye_to_eye = eye_right - eye_left
        mouth_left = lm_mouth_outer[0]
        mouth_right = lm_mouth_outer[6]
        mouth_avg = (mouth_left + mouth_right) * 0.5
        eye_to_mouth = mouth_avg - eye_avg

        # Choose oriented crop rectangle.
        x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
        x /= np.hypot(*x)
        x *= max(np.hypot(*eye_to_eye) * 2.0, np.hypot(*eye_to_mouth) * 1.8)
        y = np.flipud(x) * [-1, 1]
        c = eye_avg + eye_to_mouth * 0.1
        quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
        qsize = np.hypot(*x) * 2

        output_size = 1024
        # output_size = 256
        transform_size = 4096
        enable_padding = True
        img = Image.fromarray(img)
        # Shrink.
        shrink = int(np.floor(qsize / output_size * 0.5))
        if shrink > 1:
            rsize = (int(np.rint(float(img.size[0]) / shrink)), int(np.rint(float(img.size[1]) / shrink)))
            img = img.resize(rsize, PIL.Image.LANCZOS)
            quad /= shrink
            qsize /= shrink

        # Crop.
        border = max(int(np.rint(qsize * 0.1)), 3)
        crop = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
                int(np.ceil(max(quad[:, 1]))))
        crop = (max(crop[0] - border, 0), max(crop[1] - border, 0), min(crop[2] + border, img.size[0]),
                min(crop[3] + border, img.size[1]))
        if crop[2] - crop[0] < img.size[0] or crop[3] - crop[1] < img.size[1]:
            img = img.crop(crop)
            quad -= crop[0:2]

        # Pad.
        pad = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
            int(np.ceil(max(quad[:, 1]))))
        pad = (max(-pad[0] + border, 0), max(-pad[1] + border, 0), max(pad[2] - img.size[0] + border, 0),
            max(pad[3] - img.size[1] + border, 0))
        if enable_padding and max(pad) > border - 4:
            pad = np.maximum(pad, int(np.rint(qsize * 0.3)))
            img = np.pad(np.float32(img), ((pad[1], pad[3]), (pad[0], pad[2]), (0, 0)), 'reflect')
            # print(img)
            # print(img.shape)
            h, w, _ = img.shape
            y, x, _ = np.ogrid[:h, :w, :1]
            mask = np.maximum(1.0 - np.minimum(np.float32(x) / pad[0], np.float32(w - 1 - x) / pad[2]),
                            1.0 - np.minimum(np.float32(y) / pad[1], np.float32(h - 1 - y) / pad[3]))
            blur = qsize * 0.02
            img += (scipy.ndimage.gaussian_filter(img, [blur, blur, 0]) - img) * np.clip(mask * 3.0 + 1.0, 0.0, 1.0)
            img += (np.median(img, axis=(0, 1)) - img) * np.clip(mask, 0.0, 1.0)
            # img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            img = PIL.Image.fromarray(np.uint8(np.clip(np.rint(img), 0, 255)),'RGB')
            quad += pad[:2]

        # Transform.
        img = img.transform((transform_size, transform_size), PIL.Image.QUAD, (quad + 0.5).flatten(),
                            PIL.Image.BILINEAR)
        if output_size < transform_size:
            img = img.resize((output_size, output_size), PIL.Image.LANCZOS)
        # img.save('align1.png')
        return img
    
    def run(self,img):
        face = self.align_face(img)
        face_tensor = torchvision.transforms.ToTensor()(face).unsqueeze(0).cuda()
        face_tensor_lr = face_tensor[0].cpu().detach().clamp(0, 1)
        face = torchvision.transforms.ToPILImage()(face_tensor_lr)
        face = face.resize((1024, 1024), PIL.Image.LANCZOS)
        return face
    
    
if __name__=="__main__":
    pre = "dat/shape_predictor_81_face_landmarks.dat"
    det = "dat/mmod_human_face_detector.dat"
    mesh = face_predicter(pre,det)
    # img_shape = "long"
    
    # img_dir = "./test/woman/"+img_shape
    img_path = "./test/woman/egg/다운로드2.jpg"
    # circle = []
    # for i in os.listdir(img_dir):
    #     img_path = os.path.join(img_dir,i)
    #     if os.path.splitext(img_path)[1] ==".npy":
    #         continue 
    #     img = dlib.load_rgb_image(img_path)
    #     img = mesh.align_face(img)
    #     img = np.array(img)
    #     lan = mesh.get_landmark(img)
    #     lan = np.concatenate([lan[0:17],lan[68:]])
    #     circle.append(lan)
    # circle = np.array(circle)
    # circle = np.mean(circle,axis = 0)
    # np.save(os.path.join(img_dir,img_shape),circle)
    
    
    img = dlib.load_rgb_image(img_path)
    img = mesh.align_face(img)
    img = np.array(img)
    lan = mesh.get_landmark(img)
    lan = np.concatenate([lan[0:17],lan[68:]])
    shape = mesh.face_shape(img,0)

    print(shape)


    # print(circle)
    # print(circle.shape)

    # img.save("align1.png")
    
    # img = cv2.imread("test.jpg")
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(img.shape)
    # print(type(img))


    # img = mesh.align_face(img)
    # img.save("align2.png")

    # print(type(img))
    # img = pre.run(img)
    # img = np.array(img)
    
    # 
    # img.save('test.png')
    
    