import cv2
from firebase_admin import credentials, firestore, initialize_app, storage
from PIL import Image,ImageTk
import tempfile
import numpy as np
import pybase64 as base64
import io

def Capture(win):
    ret,frame = win.cap.read()
    frame = cv2.flip(frame, 1)
    return frame


def ShowFeed(win):
    # Capturing frame by frame
    ret, frame = win.cap.read()
    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)
        # Displaying date and time on the feed
        # cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
        # Changing the frame color from BGR to RGB
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
        win.cameraLabel.after(10, lambda:ShowFeed(win))
    else:
        # Configuring the label to display the frame
        win.cameraLabel.configure(image='')
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
        # 이미지를 Firebase Storage에 업로드
        imgByteArr = io.BytesIO()
        # image.save expects a file-like as a argument
        image.save(imgByteArr, format='JPEG')
        # Turn the BytesIO object back into a bytes object
        imgByteArr = imgByteArr.getvalue()
        blob = bucket.blob(f'customers/{name}_photo.jpg')
        blob.upload_from_string(imgByteArr)
        print("사진이 성공적으로 첨부되었습니다.")
    else:
        print("파일 없습니다.")


if __name__ == "__main__":
    cred = credentials.Certificate('../UI/easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
    firebase_app = initialize_app(cred, { 'storageBucket': 'easylogin-58c28.appspot.com'})
    db = firestore.client()
    bucket = storage.bucket(app=firebase_app)
    img = Image.open("test.png")
    # print(img.format)
    # attach_photo(bucket,"dongjin",img)
    img = imageBrowse(bucket,"dongjin")
    img.save("test1.png")