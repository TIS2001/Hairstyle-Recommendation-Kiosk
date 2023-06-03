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
        self.select1={}
        self.select2={}
        self.page1 = 0
        self.page2 = 0
        self.buttons1=[]
        self.buttons2=[]
        self.labels1=[]
        self.labels2=[]
        self.ischeck = 0
        self.img_list = []  # 이미지 리스트 초기화
        self.img_list1=[]
        self.img_list2=[]
        self.img_name1=[]
        self.img_name2=[]
        self.img_path1=[os.path.join("UI/colors/전체", f) for f in os.listdir("UI/colors/전체") if f.endswith(".JPG")]
        self.img_path2=[os.path.join("UI/hairstyles_men", f) for f in os.listdir("UI/hairstyles_men") if f.endswith(".png")]
        self.append_list(self.img_path1,self.img_list1,self.img_name1)
        self.append_list(self.img_path2,self.img_list2,self.img_name2)
        self.frame1 = tk.Frame(self.win6, bg='#dddddd')
        self.frame1.place(x=70, y=50,width=665)
        self.frame2 = tk.Frame(self.win6, bg='#dddddd')
        self.frame2.place(x=70, y=260,width=665)  #250
        self.frame3 = tk.Frame(self.win6, bg='#dddddd')
        self.frame3.place(x=10, y=465,width=780)    #450
        self.frame4 = tk.Frame(self.win6, bg='#dddddd')
        self.frame4.place(x=70, y=695,width=665) #650
        self.frame5 = tk.Frame(self.win6, bg='#dddddd')
        self.frame5.place(x=10, y=900,width=780) #850
        self.make_btn(self.frame3, self.img_path1,0)
        self.make_btn(self.frame4, [os.path.join("UI/hairstyles", f) for f in os.listdir("UI/hairstyles") if f.endswith(".png")],0)
        self.make_btn(self.frame5, self.img_path2,0)
        self.select_personal()
        
        tk.Button(self.win6, font=("Arial",15), text="뒤로가기").place(x=680, y=0)
        tk.Button(self.win6, font=("Arial",15), text="헤어스타일 선택",command=self.print_dict).place(relx=0.5,anchor=tk.CENTER,y=1120,height=50)
        tk.Label(self.win6,font=("Arial",13),text='잘 어울리는 퍼스널컬러를 선택해주세요! 선택 시 추천 컬러가 바뀝니다.').place(relx=0.5,anchor=tk.CENTER,y=30)
        tk.Label(self.win6,font=("Arial",13),text='퍼스널컬러에 따른 추천 염색 컬러').place(relx=0.5,anchor=tk.CENTER,y=245,width=665)
        tk.Label(self.win6,font=("Arial",13),text='전체 염색 컬러').place(relx=0.5,anchor=tk.CENTER,y=450,width=780)
        tk.Label(self.win6,font=("Arial",13),text='얼굴형에 따른 추천 헤어스타일').place(relx=0.5,anchor=tk.CENTER,y=680,width=665)
        tk.Label(self.win6,font=("Arial",13),text='전체 헤어스타일').place(relx=0.5,anchor=tk.CENTER,y=885,width=780)

    def print_dict(self):
        if bool(self.dict1) and bool(self.dict2):
            style=self.dict1[next(iter(self.dict1))].cget("text")
            color=self.dict2[next(iter(self.dict2))].cget("text")
            print(f"style={style}, color={color}")
        else:
            messagebox.showwarning('시술 선택 오류', '헤어스타일과 염색 컬러를 모두 선택해 주세요.')

    def append_list(self,img_path,img_list,img_name):
        img = Image.open("UI/no_apply.jpg")
        img = img.resize((150, 150))
        img_list.append(ImageTk.PhotoImage(img))
        img_name.append("no_apply")
        for i, path in enumerate(img_path):
            img = Image.open(path)
            img = img.resize((150, 150))
            img_list.append(ImageTk.PhotoImage(img))
            img_name.append(img_path[i].split('/')[-1].split('.')[0])

    def navi_click(self,frame,dir):
        if frame == self.frame3 :  
            if dir=="prev":
                self.page1-=1
            elif dir=="next":
                self.page1+=1
            page = self.page1
            dict=self.dict1
            buttons=self.buttons1
            labels=self.labels1
            img_list=self.img_list1
            img_name=self.img_name1
        
        elif frame == self.frame5 :  
            if dir=="prev":
                self.page2-=1
            elif dir=="next":
                self.page2+=1            
            page = self.page2
            dict=self.dict2
            buttons=self.buttons2
            labels=self.labels2
            img_list=self.img_list2
            img_name=self.img_name2

        if page<0:
            messagebox.showwarning('페이지 범위 오류', '첫 페이지입니다.')
            if frame == self.frame3 :
                self.page1+=1
            elif frame == self.frame5 :   
                self.page2+=1  
            return
        elif page>(math.ceil(len(img_list)/4)-1):
            messagebox.showwarning('페이지 범위 오류', '마지막 페이지입니다.')            
            if frame == self.frame3 :
                self.page1-=1
            elif frame == self.frame5 :   
                self.page2-=1
            return
        
        for i in range(4):
            idx=4*page+i
            if idx>len(img_list)-1:
                buttons[i].configure(state="disabled")
                labels[i].configure(text="-")
            else:
                buttons[i].configure(text=img_name[idx],state="normal",image=img_list[idx], relief="flat", highlightthickness=0)
                labels[i].configure(text=img_name[idx])
        if page in dict.keys():           
            dict[page].config(relief="solid", highlightthickness=2, highlightbackground="red")        

    def make_btn(self, frame, img_path,page):   
        self.clear_frame(frame)
        img_name = []
        img_size = (150, 150)
        buttons = []

        for i in range(4):
            idx=4*page+i
            if frame == self.frame2 or frame == self.frame4:   
                path = img_path[idx]
                img = Image.open(path)
                img = img.resize(img_size)
                photo_img = ImageTk.PhotoImage(img)
                button = tk.Button(frame, image=photo_img)
                self.img_list.append(photo_img)
                buttons.append(button)
                img_name.append(img_path[idx].split('/')[-1].split('.')[0])
                label = tk.Label(frame, text=img_name[i])   
                button.configure(text=img_name[i],command=lambda btn=button: self.toggle_border(btn))
            else:
                button=tk.Button(frame)
                label = tk.Label(frame)
                button.configure(command=lambda btn=button: self.toggle_border(btn))

            if frame == self.frame3:               
                self.buttons1.append(button)
                self.labels1.append(label)
                self.buttons1[i].configure(text=self.img_name1[idx],image=self.img_list1[idx])
                self.labels1[i].configure(text=self.img_name1[idx])

            elif frame == self.frame5 :
                self.buttons2.append(button)
                self.labels2.append(label)
                self.buttons2[i].configure(text=self.img_name2[idx],image=self.img_list2[idx])
                self.labels2[i].configure(text=self.img_name2[idx])

            button.grid(row=1,column=i+1,padx=5)
            label.grid(row=2,column=i+1,padx=5)

        if frame == self.frame3 or frame == self.frame5:  
            button1 = tk.Button(frame, font=("Arial", 15), text="◀", command=lambda direction="prev": self.navi_click(frame,direction))
            button1.grid(row=1, column=0, padx=5)

            button2 = tk.Button(frame, font=("Arial", 15), text="▶", command=lambda direction="next": self.navi_click(frame,direction))
            button2.grid(row=1, column=5, padx=5)        

        # for label in self.labels1:
        #     print(label.cget("text"))

    def toggle_border(self,button):
        # print(button.cget("text"))
        parent_frame = button.winfo_parent()  # button의 부모 프레임을 찾음
        if parent_frame == str(self.frame2) or parent_frame == str(self.frame3): 
            dict_var = self.dict1
            page=self.page1
        elif parent_frame == str(self.frame4) or parent_frame == str(self.frame5):  
            dict_var = self.dict2
            page=self.page2
        self.toggle_change(button,dict_var,page) 

    def toggle_change(self,button,dict_var,page):
        self.ischeck=0    
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
            if button.winfo_parent() == str(self.frame2):
                self.ischeck=1

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
        if self.ischeck==1:
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
            name_label = tk.Radiobutton(self.frame1, font=("Arial", 13), text=image_name, variable=self.var, value=i+1,
                            command=lambda:self.personal_cmd())
            name_label.grid(row=4, column=i+2,padx=5)


if __name__ == "__main__":
    UI = MainUI()
