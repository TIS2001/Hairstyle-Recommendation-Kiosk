from tkinter import *
from PIL import Image, ImageTk
import os

num = 0
def forward_image():
    global num
    num = num - 1
    label_Img.configure(image=images[num])
    
def next_image():
    global num
    num = num + 1
    label_Img.configure(image=images[num])

root = Tk()
root.geometry("400x400")

#
# jpg 파일이 저장된 폴더 경로
folder_path = 'hairstyles/'

# 폴더 내 jpg 파일 리스트
jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

# jpg 파일을 png 파일로 변환하여 리스트에 저장
png_files = []
for jpg_file in jpg_files:
    # jpg 파일 열기
    img = Image.open(os.path.join(folder_path, jpg_file))

    # png 파일로 변환하여 저장
    png_file = os.path.splitext(jpg_file)[0] + '.png'
    img.save(os.path.join(folder_path, png_file), 'PNG')
    png_files.append(png_file)

# png 파일을 PhotoImage로 변환하여 리스트에 저장
images = []
for png_file in png_files:
    photo = ImageTk.PhotoImage(Image.open(os.path.join(folder_path, png_file)))
    images.append(photo)

os.remove(os.path.join(folder_path, jpg_file))
# # 이미지 경로를 PhotoImage 객체로 변환하여 리스트에 저장하기
# images = []
# for path in images:
#     image = PhotoImage(file=path)
#     images.append(image)


# 이미지를 보여줄 라벨

label_Img = Label(root, image=images[0])
label_Img.pack()

button = Button(root, text="이전", command=forward_image)
button.pack()

button = Button(root, text="다음", command=next_image)
button.pack()

root.mainloop()
