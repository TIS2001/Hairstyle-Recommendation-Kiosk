import dlib
from pathlib import Path
import argparse
import torchvision
from utils.drive import open_url
from utils.shape_predictor import align_face
import PIL

def align_face(img):
    parser = argparse.ArgumentParser(description='Align_face')

    parser.add_argument('-unprocessed_dir', type=str, default='unprocessed', help='directory with unprocessed images')
    parser.add_argument('-output_dir', type=str, default='input/face', help='output directory')

    parser.add_argument('-output_size', type=int, default=1024, help='size to downscale the input images to, must be power of 2')
    parser.add_argument('-seed', type=int, help='manual seed to use')
    parser.add_argument('-cache_dir', type=str, default='cache', help='cache directory for model weights')

    ###############
    parser.add_argument('-inter_method', type=str, default='bicubic')


    args = parser.parse_args()

    dat = "dat/shape_predictor_81_face_landmarks.dat"
    pre = face_predicter(dat)
    img = dlib.load_rgb_image("/data/test.jpg")
    img = pre.run(img)
    img.save('test.jpg')

    faces = align_face(str(img),predictor)

    for i,face in enumerate(faces):
        if(args.output_size):
            # factor = 1024//args.output_size
            factor = 1024//args.output_size
            assert args.output_size*factor == 1024 # 1024
            face_tensor = torchvision.transforms.ToTensor()(face).unsqueeze(0).cuda()
            face_tensor_lr = face_tensor[0].cpu().detach().clamp(0, 1)
            face = torchvision.transforms.ToPILImage()(face_tensor_lr)
            if factor != 1:
                face = face.resize((args.output_size, args.output_size), PIL.Image.LANCZOS)
        if len(faces) > 1:
            # face.save(Path(args.output_dir) / (im.stem+f"_{i}.png"))
            return face
        else:
            return face
            # face.save(Path(args.output_dir) / (im.stem + f".png"))