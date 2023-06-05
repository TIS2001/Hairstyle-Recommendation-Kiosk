import cv2
from firebase_admin import credentials, firestore, initialize_app, storage
from PIL import Image,ImageTk
import tempfile
import numpy as np
import pybase64 as base64
import io

def Capture(win,picam):
    if picam:   
        frame = win.cap.capture_array(name="main")
        frame = cv2.flip(frame, 0)
    else:
        _,frame = win.cap.read()
        frame = cv2.flip(frame, 1)
    return frame


def ShowFeed(win,picam):
    # Capturing frame by frame
    if picam:
        frame = win.cap.capture_array(name="main")
        frame = cv2.flip(frame, 0)

    else:
        _,frame = win.cap.read()
        frame = cv2.flip(frame, 1)
    
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_frame = cv2.resize(cv2image, (512, 512), interpolation=cv2.INTER_AREA)
    # Creating an image memory from the above frame exporting array interface
    videoImg = Image.fromarray(resized_frame)
    # Creating object of PhotoImage() class to display the frame
    imgtk = ImageTk.PhotoImage(image = videoImg)
    # Configuring the label to display the frame
    win.cameraLabel.configure(image=imgtk)
    # Keeping a reference
    win.cameraLabel.imgtk = imgtk
        # Calling the function after 10 milliseconds
        # win.cameraLabel.after(10, lambda:ShowFeed(win,cam))

    win.cameraLabel.after(10, lambda:ShowFeed(win,picam))
    # Configuring the label to display the frame

    # Displaying messagebox
    # if success :
    #     messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)
    
    
    
def imageBrowse(bucket,name):
    # Firebase Storage에서 사진 다운로드
    blob = bucket.blob(f'customers/{name}_photo.jpg')
    str = blob.download_as_bytes()
    return Image.open(io.BytesIO(str))
    # Configuring the label to display the frame
    
    
def attach_photo(bucket,name, image):
    
    if image:
        with io.BytesIO() as stream:
        # 이미지를 Firebase Storage에 업로드
        # imgByteArr = io.BytesIO()
        # image.save expects a file-like as a argument
            image.save(stream, format='JPEG')
            # Turn the BytesIO object back into a bytes object
            # imgByteArr = imgByteArr.getvalue()
            stream.seek(0)
            blob = bucket.blob(f'customers/{name}_photo.jpg')
            blob.upload_from_file(stream)
            print("사진이 성공적으로 첨부되었습니다.")
    else:
        print("파일 없습니다.")


if __name__ == "__main__":
    cred = credentials.Certificate('../UI/princess-maker-1f45e-firebase-adminsdk-dwlbp-74b3b65023.json')
    firebase_app = initialize_app(cred, { 'storageBucket': 'princess-maker-1f45e.appspot.com'})
    db = firestore.client()
    bucket = storage.bucket(app=firebase_app)
    image = Image.open("test.png")
    with io.BytesIO() as imgByteArr:
    # image.save expects a file-like as a argument
        image.save(imgByteArr, format='JPEG')
        # Turn the BytesIO object back into a bytes object
        # imgByteArr = imgByteArr.getvalue()
        blob = bucket.blob(f'customers/test_photo.jpg')
        imgByteArr.seek(0)
        blob.upload_from_file(imgByteArr)
    # img = Image.open("test.png")
    # print(img.format)
    # attach_photo(bucket,"dongjin",img)    
    # print(bucket.blob(f'customers/'))
