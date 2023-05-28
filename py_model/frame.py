import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import os


class MainUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.title("Princess_maker")

        self.img_list = []  # 이미지 리스트 초기화
        self.open_win6()
        self.mainloop()

    def clear_frame(self, frame):
        for widget in  frame.winfo_children():
                widget.destroy()

    def open_win6(self):
        # self.img_name = []
        self.win6 = tk.Frame(self, relief="flat", bg="white")
        self.win6.place(x=0, y=0, width=800, height=1280)

        
        def make_btn(frame, img_path):
            self.clear_frame(frame)
            img_name = []
            img_size = (150, 150)
            for i in range(4):
                path = img_path[i]
                img = Image.open(path)
                img = img.resize(img_size)
                photo_img = ImageTk.PhotoImage(img)
                button = tk.Button(frame, image=photo_img)
                button.grid(row=1, column=i, padx=5)
                self.img_list.append(photo_img)
                img_name.append(img_path[i].split('/')[-1].split('.')[0])
                label = tk.Label(frame, text=img_name[i])
                label.grid(row=2, column=i, padx=5)

        def personal_cmd():
            selected_image = var.get()
            if selected_image == 1:
                dir_path="UI/colors/봄웜"
                print("봄웜")
            elif selected_image == 2:
                dir_path="UI/colors/여쿨"
                print("여쿨")
            elif selected_image == 3:
                dir_path="UI/colors/갈웜"
                print("갈웜")
            elif selected_image == 4: 
                dir_path="UI/colors/겨쿨"
                print("겨쿨")
            make_btn(frame3, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".JPG")])


        frame1 = tk.Frame(self.win6, bg='#dddddd')
        frame1.place(x=50, y=100)
        # make_btn(frame1, [os.path.join("UI/hairstyles", f) for f in os.listdir("UI/hairstyles") if f.endswith(".png")])
       
        frame2 = tk.Frame(self.win6, bg='#dddddd')
        frame2.place(x=50, y=500)
        make_btn(frame2, [os.path.join("UI/hairstyles_men", f) for f in os.listdir("UI/hairstyles_men") if f.endswith(".png")])

        frame3 = tk.Frame(self.win6, bg='#dddddd')
        frame3.place(x=50, y=800)
        # make_btn(frame3, ...)
        # 배경 이미지 파일 경로
        backgrounds = ["UI/spring.png", "UI/summer.png", "UI/autumn.png", "UI/winter.png"]
        # 전경 이미지 파일 경로
        foreground = Image.open("UI/test.png")  ##이미지 받아오기!!!
        # 배경 이미지를 원하는 크기로 조정
        labels = []
        background_images = []
        for bg_path in backgrounds:
            background = Image.open(bg_path)
            resized_background = background.resize((150, 150))
            background_images.append(resized_background)
        
        # 전경 이미지를 윈도우 크기로 조정
        resized_foreground = foreground.resize((150, 150))
        var=tk.IntVar(value=-1)

        for i, background_image in enumerate(background_images):
            composite_image = Image.alpha_composite(background_image, resized_foreground)
            # ImageTk 객체 생성
            photo = ImageTk.PhotoImage(composite_image)
            # 합성 이미지를 표시할 라벨 생성
            label = tk.Label(frame1, image=photo)
            label.grid(row=3, column=i+2)
            # 라벨을 리스트에 추가
            labels.append(label)
            # ImageTk 객체에 대한 참조 유지
            label.image = photo
            image_name = backgrounds[i].split(".")[0]  # 이미지 파일 이름 (확장자 제외)
            name_label = tk.Radiobutton(frame1, font=("Arial", 15), text=image_name, variable=var, value=i+1,
                            command=lambda:personal_cmd())
            name_label.grid(row=4, column=i+2)

if __name__ == "__main__":
    UI = MainUI()
