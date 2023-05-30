import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import os
import math
from tkinter import messagebox

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
        if frame is not None:
            for widget in frame.winfo_children():
                widget.destroy()


    def open_win6(self):
        self.win6 = tk.Frame(self, relief="flat", bg="white")
        self.win6.place(x=0, y=0, width=800, height=1280)
        self.dict1 = {}
        self.dict2 = {}
        self.page1 = 0
        self.page2 = 0
        self.frame1 = tk.Frame(self.win6, bg='#dddddd')
        self.frame1.place(x=50, y=50)
        self.frame2 = tk.Frame(self.win6, bg='#dddddd')
        self.frame2.place(x=50, y=250)
        self.frame3 = tk.Frame(self.win6, bg='#dddddd')
        self.frame3.place(x=10, y=450,width=780)
        self.frame4 = tk.Frame(self.win6, bg='#dddddd')
        self.frame4.place(x=50, y=650)
        self.frame5 = tk.Frame(self.win6, bg='#dddddd')
        self.frame5.place(x=10, y=850,width=780)
        self.make_btn(self.frame3, [os.path.join("UI/colors/전체", f) for f in os.listdir("UI/colors/전체") if f.endswith(".JPG")],0)
        self.make_btn(self.frame4, [os.path.join("UI/hairstyles", f) for f in os.listdir("UI/hairstyles") if f.endswith(".png")],0)
        self.make_btn(self.frame5, [os.path.join("UI/hairstyles_men", f) for f in os.listdir("UI/hairstyles_men") if f.endswith(".png")],0)
        self.select_personal()

        # def forward_image(self,btn):
        #     page = 0
        #     dict={}            
        #     dir_path=""
        #     format=""
        #     parent_frame = btn.winfo_parent()  # button의 부모 프레임을 찾음
        #     if parent_frame == str(self.frame3) :  
        #         page = self.page1
        #         dict=self.dict1
        #         dir_path="UI/colors/전체"
        #         format=".JPG"
        #     elif parent_frame == str(self.frame5) :  
        #         page = self.page2
        #         dict=self.dict2
        #         dir_path="UI/hairstyles"
        #         format=".png"
        #     page=page-1
        #     if page>=0:
        #        self.make_btn(parent_frame, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(format)],page)

        #     if page in dict.keys():           
        #         dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")

        # def next_image(self,frame):
        #     page = 0
        #     dict={}            
        #     dir_path=""
        #     format=""
        #     print(frame)

        #     if frame == str(self.frame3) :  
        #         print(frame)
        #         page = self.page1
        #         dict=self.dict1
        #         dir_path="UI/colors/전체"
        #         format=".JPG"
        #     elif frame == str(self.frame5) :  
        #         print(frame)
        #         page = self.page2
        #         dict=self.dict2
        #         dir_path="UI/hairstyles"
        #         format=".png"
        #     page+=1
        #     if page>=0:
        #        self.make_btn(frame, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(format)],page)

        #     if page in dict.keys():           
        #         dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")

        tk.Button(self.win6, font=("Arial",15), text="뒤로가기", command=lambda:[self.win5.tkraise()]).place(x=680, y=0)
        # tk.Button(self.win6, font=("Arial",15), text="헤어스타일 선택", command=self.progress_bar).grid(row=17, column=3)
        # self.button1 = tk.Button(self.frame3, font=("Arial", 15), text="◀", command=lambda direction="prev": self.navi_click(self.frame3,direction))
        # self.button1.grid(row=1, column=0, padx=5)

        # button2 = tk.Button(self.frame3, font=("Arial", 15), text="▶", command=lambda direction="next": self.navi_click(self.frame3,direction))
        # button2.grid(row=1, column=5, padx=5)

        # button3 = tk.Button(self.frame5, font=("Arial", 15), text="◀", command=lambda: self.forward_image(button3))
        # button3.grid(row=1, column=0, padx=5)

        # button4 = tk.Button(self.frame5, font=("Arial", 15), text="▶", command=lambda: self.next_image(self.frame5))
        # button4.grid(row=1, column=5, padx=5)

        # tk.Label(self.win6,text='간소화된 퍼스널컬러 자가진단: 선택 시 추천 컬러가 바뀝니다.',height=1).grid(row=2, column=2,columnspan=3)
        # tk.Label(self.win6,text='얼굴형에 따른 추천 헤어스타일',height=1).grid(row=5, column=2,columnspan=3)
        # tk.Label(self.win6,text='전체 헤어스타일',height=1).grid(row=8, column=3)
        # tk.Label(self.win6,text='퍼스널컬러에 따른 추천 염색 컬러',height=1).grid(row=11, column=2, columnspan=3)
        # tk.Label(self.win6,text='전체 염색 컬러',height=1).grid(row=14, column=3)

    # def forward_image(self,btn):
    #     page = 0
    #     dict={}            
    #     dir_path=""
    #     format=""
    #     parent_frame = btn.winfo_parent()  # button의 부모 프레임을 찾음
    #     if parent_frame == str(self.frame3) :  
    #         page = self.page1
    #         dict=self.dict1
    #         dir_path="UI/colors/전체"
    #         format=".JPG"
    #     elif parent_frame == str(self.frame5) :  
    #         page = self.page2
    #         dict=self.dict2
    #         dir_path="UI/hairstyles"
    #         format=".png"
    #     page=page-1
    #     if page>=0:
    #         self.make_btn(parent_frame, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(format)],page)
    #     else:
    #         print("처음 페이지 입니다.")
    #     if page in dict.keys():           
    #         dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")

    # def next_image(self,frame):
    #     page = 0
    #     dict={}            
    #     dir_path=""
    #     format=""
    #     if frame == self.frame3 :  
    #         page = self.page1
    #         dict=self.dict1
    #         dir_path="UI/colors/전체"
    #         format=".JPG"
    #     elif frame == str(self.frame5) :  
    #         print(frame)
    #         page = self.page2
    #         dict=self.dict2
    #         dir_path="UI/hairstyles"
    #         format=".png"
    #     page+=1
    #     if page>=0:
    #         self.make_btn(frame, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(format)],page)
    #         self.button1.tkraise()
    #     if page in dict.keys():           
    #         dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")

    def navi_click(self,frame,dir):
        # # page = 0
        # dict={}            
        # dir_path=""
        # format=""
        if frame == self.frame3 :  
            if dir=="prev":
                self.page1-=1
            elif dir=="next":
                self.page1+=1
            page = self.page1
            dict=self.dict1
            dir_path="UI/colors/전체"
            format=".JPG"
        elif frame == self.frame5 :  
            if dir=="prev":
                self.page2-=1
            elif dir=="next":
                self.page2+=1            
            page = self.page2
            dict=self.dict2
            dir_path="UI/hairstyles"
            format=".png"
        img_path=[os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(format)]
        if page<0:
            messagebox.showwarning('페이지 범위 오류', '처음 페이지입니다.')
            if frame == self.frame3 :
                self.page1+=1
            elif frame == self.frame5 :   
                self.page2+=1  
        elif page>((len(img_path)//4)-1):
            messagebox.showwarning('페이지 범위 오류', '마지막 페이지입니다.')            
            if frame == self.frame3 :
                self.page1-=1
            elif frame == self.frame5 :   
                self.page2-=1
        else:
            self.make_btn(frame, img_path,page)
            # print(f"frmae={frame},page: {page}")
        if page in dict.keys():           
            dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")

    def make_btn(self, frame, img_path,page):           
        
        self.clear_frame(frame)
        img_name = []
        img_size = (150, 150)
        buttons = []     
        for i in range(4):
            idx=4*page+i
            if idx==0 and (frame == self.frame3 or frame == self.frame5):
                button = tk.Button(frame, text="X", width=10,height=5, fg="red", font=("Arial", 15))  
                             
                button.configure(command=lambda btn=button: self.toggle_border(btn))
                button.grid(row=1, column=1, padx=5)
                img_name.append("적용하지 않음")

            else:
                if idx==0 and (frame == self.frame3 or frame == self.frame5):
                    continue
                path = img_path[idx]
                img = Image.open(path)
                img = img.resize(img_size)
                photo_img = ImageTk.PhotoImage(img)
                button = tk.Button(frame, image=photo_img)
                buttons.append(button)
                self.img_list.append(photo_img)
                img_name.append(img_path[idx].split('/')[-1].split('.')[0])

                button.configure(command=lambda btn=button: self.toggle_border(btn))
                button.grid(row=1, column=i+1, padx=5)
            label = tk.Label(frame, text=img_name[i])
            label.grid(row=2, column=i+1, padx=5)

        if frame == self.frame3 :  
            self.button1 = tk.Button(self.frame3, font=("Arial", 15), text="◀", command=lambda direction="prev": self.navi_click(self.frame3,direction))
            self.button1.grid(row=1, column=0, padx=5)

            button2 = tk.Button(self.frame3, font=("Arial", 15), text="▶", command=lambda direction="next": self.navi_click(self.frame3,direction))
            button2.grid(row=1, column=5, padx=5)

        elif frame == self.frame5 :  
            button3 = tk.Button(self.frame5, font=("Arial", 15), text="◀", command=lambda direction="prev": self.navi_click(self.frame5,direction))
            button3.grid(row=1, column=0, padx=5)

            button4 = tk.Button(self.frame5, font=("Arial", 15), text="▶", command=lambda direction="next": self.navi_click(self.frame5,direction))
            button4.grid(row=1, column=5, padx=5) 


    def toggle_border(self, button):
        # print(button)
        parent_frame = button.winfo_parent()  # button의 부모 프레임을 찾음
        if parent_frame == str(self.frame2) or parent_frame == str(self.frame3): 
            dict_var = self.dict1
            page=self.page1
        elif parent_frame == str(self.frame4) or parent_frame == str(self.frame5):  
            dict_var = self.dict2
            page=self.page2
        else:
            dict_var = {}
        
        if button.cget("relief") == "solid":
            button.config(relief="flat", highlightthickness=0)
            dict_var.clear()
        else:
            if bool(dict_var):
                int_keys = [k for k in dict_var.keys() if isinstance(k, int)]
                dict_var[int_keys[0]].config(relief="flat", highlightthickness=0)         
                dict_var.clear()
            
            button.config(relief="solid", highlightthickness=2, highlightbackground="red")
            dict_var[page] = button

    def personal_cmd(self):
        selected_image = self.var.get()
        if selected_image == 1:
            dir_path = "UI/colors/봄웜"
        elif selected_image == 2:
            dir_path = "UI/colors/여쿨"
        elif selected_image == 3:
            dir_path = "UI/colors/갈웜"
        elif selected_image == 4:
            dir_path = "UI/colors/겨쿨"
        
        self.make_btn(self.frame2, [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".JPG")],0)
        self.dict1={}


    def select_personal(self):
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
        self.var=tk.IntVar(value=-1)

        for i, background_image in enumerate(background_images):
            composite_image = Image.alpha_composite(background_image, resized_foreground)
            # ImageTk 객체 생성
            photo = ImageTk.PhotoImage(composite_image)
            # 합성 이미지를 표시할 라벨 생성
            label = tk.Label(self.frame1, image=photo)
            label.grid(row=3, column=i+2,padx=5)
            # 라벨을 리스트에 추가
            labels.append(label)
            # ImageTk 객체에 대한 참조 유지
            label.image = photo
            image_name = backgrounds[i].split(".")[0]  # 이미지 파일 이름 (확장자 제외)
            name_label = tk.Radiobutton(self.frame1, font=("Arial", 15), text=image_name, variable=self.var, value=i+1,
                            command=lambda:self.personal_cmd())
            name_label.grid(row=4, column=i+2,padx=5)

if __name__ == "__main__":
    UI = MainUI()
