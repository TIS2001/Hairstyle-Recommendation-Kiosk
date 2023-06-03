import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import math
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from firebase_admin import credentials, firestore, initialize_app, storage
from util.img_send import ClientVideoSocket
from util.image_util import Capture, ShowFeed, attach_photo, imageBrowse
import numpy as np
from multiprocessing import Process, Pipe

class MainUI(tk.Tk):
    def __init__(self,p,picam=True):
        tk.Tk.__init__(self)
        self.picam = picam
        self.p = p
        self.firebase_init()
        self.bucket = storage.bucket(app=self.firebase_app)
        self.geometry("800x1280")        
        self.title("Princess_maker")
        self.Frame_init()
        self.mainloop()
        
        
    #1. 첫번째 페이지- 시작하기
    def Frame_init(self):
        self.camera_init()
        self.Start_Frame()
        self.open_win1()
        self.open_win2()
        self.open_win3()
        self.open_win4()
        self.open_win12()
        self.StartFrame.tkraise()
    
    def camera_init(self):
        if self.picam:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            width,height = 1024,1024
            video_config= self.camera.create_still_configuration(main={"size":(width,height), "format":"RGB888"},buffer_count=1)
            self.camera.configure(video_config)
        else:
            self.camera = cv2.VideoCapture(0)

    def Start_Frame(self):
        self.StartFrame = tk.Frame(self, relief="flat",bg="white")
        self.StartFrame.place(x=0,y=0,width=800,height=1280)
        tk.Button(self.StartFrame, text="시작하기", width=16, height=7, command=lambda:[self.win1.tkraise()]).pack(anchor="center",pady=200)
        self.StartFrame.bind("<Escape>", self.on_escape)
        
    def firebase_init(self):
        cred = credentials.Certificate('./UI/easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
        self.firebase_app = initialize_app(cred, { 'storageBucket': 'easylogin-58c28.appspot.com'})
        self.db = firestore.client()
    
    #2. 회원가입, 로그인 버튼    
    def open_win1(self):
        self.win1 = tk.Frame(self, relief="flat",bg="white")
        self.win1.place(x=0,y=0,width=800,height=1280)
        self.win1.bind("<Escape>", self.on_escape)
        tk.Button(self.win1, text="뒤로가기", command=lambda:self.StartFrame.tkraise).pack(padx=10,pady=10, side="top", anchor="ne")
        tk.Button(self.win1, text="회원가입하기", width=15, height=5, command=lambda:[self.win2.tkraise()]).pack(pady=10)
        tk.Button(self.win1, text="로그인하기", width=15, height=5, command=lambda:[self.win3.tkraise()]).pack(pady=10)
    
    #3-1. 회원가입 페이지
    def open_win2(self):
        var = StringVar()
        cb = IntVar()
        
        # def selection():
        #     ## global selection이 무슨 의민지 모르겠음
        #     self.m = var.get()
        
        def check_duplicate_id(id):
            customer_ref = self.db.collection('customers')
            query = customer_ref.where('id', '==', id).limit(1).get()
            return len(query) > 0

        def submit():
            name = name_Tf.get()
            id = id_Tf.get()
            password = password_Tf.get()
            phoneNumber = phoneNumber_Tf.get()
            gender = var.get()

            
            if not name or not id or not password or not phoneNumber or not gender:
                messagebox.showwarning('회원가입 실패', '모든 필드를 입력해주세요.')
                return
            
            if check_duplicate_id(id):
                messagebox.showwarning('회원가입 실패', '이미 사용 중인 아이디입니다.')
                return
        
            try:
                # Firebase에 고객 정보 저장
                doc_ref = self.db.collection('customers').document(id)
                self.user_info = {
                    'name': name,
                    'id': id,
                    'password': password,
                    'phoneNumber': phoneNumber,
                    'gender' : gender
                }
                doc_ref.set(self.user_info)
                
                # 저장 후 필드 초기화
                name_Tf.delete(0, tk.END)
                id_Tf.delete(0, tk.END)
                password_Tf.delete(0, tk.END)
                phoneNumber_Tf.delete(0, tk.END)
                var.set(None)
                
                messagebox.showinfo('회원가입 성공', f'{name}님, 회원가입이 완료되었습니다.')
                
                self.open_win1()
                self.win2.withdraw()
            except Exception as ep:
                messagebox.showwarning('회원가입 실패', '형식에 맞는 입력을 넣어주세요.')
                
        def termsCheck():
            if cb.get() == 1:
                submit_btn['state'] = NORMAL
            else:
                submit_btn['state'] = DISABLED

        self.win2 = tk.Frame(self, relief="flat",bg="white")
        self.win2.place(x=0,y=0,width=800,height=1280)
        self.win2.bind("<Escape>", self.on_escape)
        
        # 뒤로가기 버튼 왼쪽 위에 생성
        tk.Button(self.win2, text="뒤로가기", command=lambda:[self.win1.tkraise()]).pack(padx=10,pady=10, side="top", anchor="ne")
        
        frame1 = Label(self.win2, bg='#dddddd')
        frame1.pack()
        frame2 = LabelFrame(frame1, text='Gender', padx=50, pady=10)

        Label(frame1, text='이름').grid(row=0, column=0, padx=5, pady=5)
        Label(frame1, text='아이디').grid(row=1, column=0, padx=5, pady=5)
        Label(frame1, text='비밀번호').grid(row=2, column=0, padx=5, pady=5)
        Label(frame1, text='전화번호').grid(row=3, column=0, padx=5, pady=5)
        
        var.set(None)
        Radiobutton(frame2, text='남자', variable=var, value='남자').grid(row=0, column=0)
        Radiobutton(frame2, text='여자', variable=var, value='여자').grid(row=0, column=1)
        
        name_Tf = Entry(frame1)
        name_Tf.grid(row=0, column=2)
        
        id_Tf = Entry(frame1)
        id_Tf.grid(row=1, column=2)
        
        password_Tf = Entry(frame1, show="*") # 비밀번호 보안을 위한 show='*'
        password_Tf.grid(row=2, column=2)
        
        phoneNumber_Tf = Entry(frame1)
        phoneNumber_Tf.grid(row=3, column=2)
        
        frame2.grid(row=4, columnspan=3,padx=30)
        
        check_btn = Checkbutton(frame1, text='Accept the terms & conditions', variable=cb, onvalue=1, offvalue=0,command=termsCheck)
        check_btn.grid(row=5, columnspan=4, pady=5)
        
        submit_btn = Button(frame1, text="Submit", command=submit, padx=50, pady=5, state=DISABLED)
        submit_btn.grid(row=6, columnspan=4, pady=2)
    
    #3-2. 로그인 페이지 
    def open_win3(self):
        self.win3 = tk.Frame(self, relief="flat",bg="white")
        self.win3.place(x=0,y=0,width=800,height=1280)
        self.win3.bind("<Escape>", self.on_escape)
        
        def login():
            id = id_entry.get()
            password = password_entry.get()        

            if id and password:
                # Firebase에서 사용자 데이터 조회
                doc_ref = self.db.collection('customers').document(id)
                doc = doc_ref.get()

                if doc.exists:
                    customer_data = doc.to_dict()
                    # 비밀번호 일치 확인
                    if password == customer_data['password']:
                        self.user_info = customer_data
                        messagebox.showinfo("로그인 성공", f'어서오세요, {self.user_info["name"]}님.')
                        self.win4.tkraise()
                    else:
                        messagebox.showerror("로그인 실패", "비밀번호가 일치하지 않습니다.")
                else:
                    messagebox.showerror("로그인 실패", "해당 아이디가 존재하지 않습니다.")
            else:
                messagebox.showwarning("로그인 실패", "아이디와 비밀번호를 입력해주세요.")


        Button(self.win3, text="뒤로가기", command=lambda:[self.win1.tkraise()]).grid(row=0, column=2, padx=10, pady=10, sticky="ne")
        Label(self.win3, text='아이디').grid(row=1, column=0, padx=5, pady=5)    
        Label(self.win3, text='비밀번호').grid(row=2, column=0, padx=5, pady=5)
        id_entry = Entry(self.win3)
        id_entry.grid(row=1, column=1)
        password_entry = Entry(self.win3, show="*")
        password_entry.grid(row=2, column=1)
        Button(self.win3, text="로그인", command=login).grid(row=4, columnspan=3, padx=10, pady=10, sticky="s")

    #4. 카메라 실행/ 예약(-> #12), 헤어스타일 선택(-> #5) 버튼
    def open_win4(self):
        self.isBaro=False
        self.win4 = tk.Frame(self, relief="flat",bg="white")
        self.win4.place(x=0,y=0,width=800,height=1280)
        self.win4.bind("<Escape>", self.on_escape)
        
        # 바로 예약
        def baro():
            self.isBaro=True
            
        tk.Button(self.win4, text="뒤로가기", command=lambda:[self.win3.tkraise()]).pack(padx=10,pady=10, side="top", anchor="ne")
        tk.Button(self.win4, text="바로 예약하기", width=15, height=5, command=lambda:[baro(),self.win12.tkraise()]).pack(pady=10)
        if self.picam:
            tk.Button(self.win4, text="헤어스타일 합성", width=15, height=5, command=lambda:[self.camera.start(),self.open_win5(),self.win5.tkraise()]).pack(pady=10)
        else:
            tk.Button(self.win4, text="헤어스타일 합성", width=15, height=5, command=lambda:[self.open_win5(),self.win5.tkraise()]).pack(pady=10)
    #5. 사진 촬영(5초 타이머) or 사진 가져오기(-> 팝업창)
    def open_win5(self):
        self.win5 = tk.Frame(self, relief="flat",bg="white")
        self.win5.place(x=0,y=0,width=800,height=1280)
        self.win5.bind("<Escape>", self.on_escape)
        
        def AfterCapture(frame):
            frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            resizedImg = image.resize((200,200), Image.LANCZOS)
            resizedImg = ImageTk.PhotoImage(resizedImg)
            self.win5.imageLabel.config(image=resizedImg)
            self.win5.imageLabel.photo = resizedImg
            takePhoto_bt.destroy()
            image_name = f"{self.user_info['name']}_photo.jpg"
            tk.Button(self.win5, text="다시 찍기", command=lambda:[AfterCapture(Capture(self.win5,self.picam))]).place(x=350,y=630,width=100,height=40)    
            # tk.Button(self.win5, text="사진 선택", command=lambda:[self.server.sendImages(frame),self.win5.withdraw(),self.open_win6()]).grid(row=9,column=3)
            tk.Button(self.win5, text="사진 선택", command=lambda:[self.p.send(1),self.p.send(image_name),attach_photo(self.bucket,self.user_info["name"],image),self.open_win6(),self.win6.tkraise(),self.img_thread(frame)]).place(x=350,y=680,width=100,height=40)
        
        def AfterBrowse(image):
            frame = np.array(image)
            resizedImg = image.resize((200,200), Image.LANCZOS)
            saved_image=ImageTk.PhotoImage(resizedImg)
            self.win5.imageLabel.config(image=saved_image)
            # Keeping a reference
            self.win5.imageLabel.photo = saved_image
            browse_bt.destroy()
            image_name = f"{self.user_info['name']}_photo.jpg"
            # tk.Button(win5, text="사진 선택", command=lambda:[self.server.sendImages(frame),attach_photo(),win5.withdraw(),open_win6()]).grid(row=9,column=3)
            tk.Button(self.win5, text="사진 선택", command=lambda:[self.p.send(0),self.p.send(image_name),attach_photo(self.bucket,self.user_info["name"],image),self.open_win6(),self.win6.tkraise()]).place(x=350,y=580,width=100,height=40)

        #뒤로 갔다가 돌아오면 웹캠 안뜨는 오류 해결 못함
        tk.Button(self.win5, text="뒤로가기", command=lambda:[self.win4.tkraise()]).place(x=700,y=1200,width=40,height=20)
        browse_bt=tk.Button(self.win5, text="사진 가져오기", command=lambda:[AfterBrowse(imageBrowse(self.bucket,self.user_info["name"]))])
        browse_bt.place(x=350,y=580,width=100,height=40)
        takePhoto_bt=tk.Button(self.win5, text="사진 촬영", command=lambda:[AfterCapture(Capture(self.win5,self.picam))])
        takePhoto_bt.place(x=350,y=630,width=100,height=40)
        
        self.win5.cameraLabel = Label(self.win5, bg="steelblue", borderwidth=3, relief="groove")
        self.win5.cameraLabel.place(x=144,y=50)
        self.win5.imageLabel = Label(self.win5, bg="steelblue", borderwidth=3, relief="groove")
        self.win5.imageLabel.place(x=300,y=700)
        # Creating object of class VideoCapture with webcam index
        self.win5.cap = self.camera
        # Setting width and height
        self.win5.bind("<Escape>", self.on_escape)

        ShowFeed(self.win5,self.picam)
    
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
        tk.Button(self.win6, font=("Arial",15), text="헤어스타일 선택",command=lambda: self.send_styles()).place(relx=0.5,anchor=tk.CENTER,y=1120,height=50)
        tk.Label(self.win6,font=("Arial",13),text='잘 어울리는 퍼스널컬러를 선택해주세요! 선택 시 추천 컬러가 바뀝니다.').place(relx=0.5,anchor=tk.CENTER,y=30)
        tk.Label(self.win6,font=("Arial",13),text='퍼스널컬러에 따른 추천 염색 컬러').place(relx=0.5,anchor=tk.CENTER,y=245,width=665)
        tk.Label(self.win6,font=("Arial",13),text='전체 염색 컬러').place(relx=0.5,anchor=tk.CENTER,y=450,width=780)
        tk.Label(self.win6,font=("Arial",13),text='얼굴형에 따른 추천 헤어스타일').place(relx=0.5,anchor=tk.CENTER,y=680,width=665)
        tk.Label(self.win6,font=("Arial",13),text='전체 헤어스타일').place(relx=0.5,anchor=tk.CENTER,y=885,width=780)

    def send_styles(self):
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
                button.configure(command=lambda btn=button: self.toggle_border(btn))
                label = tk.Label(frame)

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


    def toggle_border(self, button):
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












        # global img_list9,button_list9,button_dict9,img_list15,button_list15,button_dict15

        # self.num9=2
        # self.num15=2
        # button_dict9 = {}
        # button_dict15 = {}

        # self.win6 = tk.Frame(self, relief="flat",bg="white")
        # self.win6.place(x=0,y=0,width=800,height=1280)
        # self.win6.bind("<Escape>", self.on_escape)
        
        # ##cmd 실행 안됨!!!!!!!
        # def personal_cmd():
        #     selected_image = var.get()
        #     if selected_image == 1:
        #         # 첫 번째 이미지에 대한 cmd 명령어 실행
        #         print("봄웜")
        #     elif selected_image == 2:
        #         # 두 번째 이미지에 대한 cmd 명령어 실행
        #         print("여쿨")
        #     elif selected_image == 3:
        #         # 세 번째 이미지에 대한 cmd 명령어 실행
        #         print("갈웜")
        #     elif selected_image == 4:
        #         # 네 번째 이미지에 대한 cmd 명령어 실행
        #         print("겨쿨")

        # # 배경 이미지 파일 경로
        # backgrounds = ["UI/spring.png", "UI/summer.png", "UI/autumn.png", "UI/winter.png"]
        # # 전경 이미지 파일 경로
        # foreground = Image.open("UI/test.png")  ##이미지 받아오기!!!
        # # 배경 이미지를 원하는 크기로 조정
        # labels = []
        # background_images = []
        # for bg_path in backgrounds:
        #     background = Image.open(bg_path)
        #     resized_background = background.resize((80, 96))
        #     background_images.append(resized_background)

        # def progress_bar():
        #     frame_progress = tk.LabelFrame(self.win6, text="진행상황")
        #     frame_progress.grid(row=18, column=1, sticky="ew", padx=10, pady=10,columnspan=6)
        #     p_var = tk.DoubleVar()
        #     progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
        #     progress_bar.pack(fill="x", padx=5, pady=5, ipady=5)
        #     self.p.send((self.style,self.color))
        #     for i in range(100):
        #         time.sleep(0.005)
        #         p_var.set(i)
        #         progress_bar.update()
        #     self.win6.after(100,lambda:[frame_progress.grid_remove(),progress_bar.pack_forget(),self.open_win11(),self.win11.tkraise()])
        
        # def toggle_border9(button):
        #     global num9,button_dict9
        #     if button.cget("relief") == "solid":
        #         button.config(relief="flat", highlightthickness=0)
        #         button_dict9 = {}
        #     else:
        #         if bool(button_dict9):
        #             int_keys = [k for k in button_dict9.keys() if isinstance(k, int)]
        #             button_dict9[int_keys[0]].config(relief="flat", highlightthickness=0)         
        #             button_dict9 = {}
        #         button.config(relief="solid", highlightthickness=2, highlightbackground="red")
        #         button_dict9[self.num9] = button
        #         self.style = str(button.cget("text"))

        # def forward_image9():
        #     global button_dict9
        #     self.num9 = self.num9 - 1
        #     for j in range(4):
        #         idx = num9 * 4
        #         if (idx>=0 and idx < len(img_list9) and idx < len(img_name9)):
        #             button_list9[1][j].configure(image=img_list9[idx], relief="flat", highlightthickness=0)
        #             name_list9[1][j].configure(text=img_name9[idx])
        #     if self.num9 in button_dict9.keys():           
        #         button_dict9[self.num9].config(relief="solid", highlightthickness=2, highlightbackground="red")

        # def next_image9():
        #     global button_dict9
        #     self.num9 = self.num9 + 1
        #     for j in range(4):
        #         idx = self.num9 * 4 + j
        #         if (idx>=0 and idx < len(img_list9) and idx < len(img_name9)):
        #             button_list9[1][j].configure(image=img_list9[idx], relief="flat", highlightthickness=0)
        #             name_list9[1][j].configure(text=img_name9[idx])

        #     if self.num9 in button_dict9.keys():           
        #         button_dict9[self.num9].config(relief="solid", highlightthickness=2, highlightbackground="red")

        # def toggle_border15(button):
        #     global button_dict15
        #     if button.cget("relief") == "solid":
        #         button.config(relief="flat", highlightthickness=0)
        #         button_dict15 = {}
        #         # self.color = str(button.cget("image"))
        #     else:
        #         if bool(button_dict15):
        #             int_keys = [k for k in button_dict15.keys() if isinstance(k, int)]
        #             button_dict15[int_keys[0]].config(relief="flat", highlightthickness=0)         
        #             button_dict15 = {}
        #         button.config(relief="solid", highlightthickness=2, highlightbackground="red")
        #         self.color = str(button.cget("text"))
        #         button_dict15[self.num15] = button
            
        # def forward_image15():
        #     global button_dict15
        #     self.num15 = self.num15 - 1
        #     for j in range(4):
        #         idx = self.num15 * 4 + j
        #         if (idx>=0 and idx < len(img_list15) and idx < len(img_name15)):
        #             button_list15[1][j].configure(image=img_list15[idx], relief="flat", highlightthickness=0)
        #             name_list15[1][j].configure(text=img_name15[idx])

        #     if self.num15 in button_dict15.keys():           
        #         button_dict15[self.num15].config(relief="solid", highlightthickness=2, highlightbackground="red")
                
        # def next_image15():
        #     global button_dict15
        #     self.num15 = self.num15 + 1
        #     for j in range(4):
        #         idx = self.num15 * 4 + j
        #         if (idx>=0 and idx < len(img_list15) and idx < len(img_name15)):
        #             button_list15[1][j].configure(image=img_list15[idx], relief="flat", highlightthickness=0)
        #             name_list15[1][j].configure(text=img_name15[idx])
        #     if self.num15 in button_dict15.keys():           
        #         button_dict15[self.num15].config(relief="solid", highlightthickness=2, highlightbackground="red")

        # tk.Button(self.win6, text="뒤로가기", command=lambda:[self.win5.tkraise()]).grid(row=0, column=6)
        # tk.Button(self.win6, text="헤어스타일 선택", command=progress_bar).grid(row=17, column=3)
        # tk.Button(self.win6, text="◀", command=forward_image9).grid(row=9, column=1)
        # tk.Button(self.win6, text="▶", command=next_image9).grid(row=9, column=6)
        # tk.Button(self.win6, text="◀", command=forward_image15).grid(row=15, column=1)
        # tk.Button(self.win6, text="▶", command=next_image15).grid(row=15, column=6)
        # tk.Label(self.win6,text='간소화된 퍼스널컬러 자가진단: 선택 시 추천 컬러가 바뀝니다.',height=1).grid(row=2, column=2,columnspan=3)
        # tk.Label(self.win6,text='얼굴형에 따른 추천 헤어스타일',height=1).grid(row=5, column=2,columnspan=3)
        # tk.Label(self.win6,text='전체 헤어스타일',height=1).grid(row=8, column=3)
        # tk.Label(self.win6,text='퍼스널컬러에 따른 추천 염색 컬러',height=1).grid(row=11, column=2, columnspan=3)
        # tk.Label(self.win6,text='전체 염색 컬러',height=1).grid(row=14, column=3)

        # var=IntVar()
        # var.set(1)
        # # 전경 이미지를 윈도우 크기로 조정
        # resized_foreground = foreground.resize((80, 96))

        # for i, background_image in enumerate(background_images):
        #     composite_image = Image.alpha_composite(background_image, resized_foreground)
        #     # ImageTk 객체 생성
        #     photo = ImageTk.PhotoImage(composite_image)
        #     # 합성 이미지를 표시할 라벨 생성
        #     label = tk.Label(self.win6, image=photo)
        #     label.grid(row=3, column=i+2)
        #     # 라벨을 리스트에 추가
        #     labels.append(label)
        #     # ImageTk 객체에 대한 참조 유지
        #     label.image = photo
        #     image_name = backgrounds[i].split(".")[0]  # 이미지 파일 이름 (확장자 제외)
        #     name_label = tk.Radiobutton(self.win6, text=image_name,variable=var, value=i+1,command=personal_cmd)
        #     name_label.grid(row=4, column=i+2)

        # if self.user_info["gender"]=='여자':
        #     dir_path9 = "UI/hairstyles"
        # elif self.user_info["gender"]=='남자':
        #     dir_path9 = "UI/hairstyles_men"
        # dir_path15="UI/colors"
        # img_path9 = [os.path.join(dir_path9, f) for f in os.listdir(dir_path9) if f.endswith(".png")]
        # img_path15 = [os.path.join(dir_path15, f) for f in os.listdir(dir_path15) if f.endswith(".png")]
        # img_size = (80, 80)

        # # 이미지 로드 및 크기 조정
        # img_list9 = []
        # img_name9=[]
        # for i, path in enumerate(img_path9):
        #     img = Image.open(path)
        #     img = img.resize(img_size)
        #     img_list9.append(ImageTk.PhotoImage(img))
        #     img_name9.append(img_path9[i].split('/')[-1].split('.')[0])  # 경로에서 마지막 부분(파일 이름) 추출
            
        # # 이미지를 표시할 버튼 생성
        # button_list9 = []
        # name_list9=[]
        # for i in range(2):
        #     row_list = []
        #     row_list2=[]
        #     for j in range(4):
        #         button = tk.Button(self.win6, image=None)
        #         button.grid(row=3*i+6, column=j+2, padx=5)  # 추가 간격 설정
        #         row_list.append(button)
        #         label=tk.Label(self.win6,text='')
        #         label.grid(row=3*i+7, column=j+2, padx=5)
        #         row_list2.append(label)
        #     button_list9.append(row_list)
        #     name_list9.append(row_list2)

        # # 이미지를 버튼에 할당
        # for i in range(2):
        #     for j in range(4):
        #         idx = i * 4 + j
        #         if idx < len(img_list9):
        #             button_list9[i][j].configure(text=img_name9[idx],image=img_list9[idx],command=lambda i=i, j=j: toggle_border9(button_list9[i][j]))
        #             name_list9[i][j].configure(text=img_name9[idx])
        
        # # 이미지 로드 및 크기 조정
        # img_list15 = []
        # img_name15=[]
        # for i,path in enumerate(img_path15):
        #     img = Image.open(path)
        #     img = img.resize(img_size)
        #     img_list15.append(ImageTk.PhotoImage(img))
        #     img_name15.append(img_path15[i].split('/')[-1].split('.')[0])  # 경로에서 마지막 부분(파일 이름) 추출print(img)

        # # 이미지를 표시할 버튼 생성
        # button_list15 = []
        # name_list15=[]
        # for i in range(2):
        #     row_list = []
        #     row_list2=[]
        #     for j in range(4):
        #         button = tk.Button(self.win6, image=None)
        #         button.grid(row=3*i+12, column=j+2, padx=5)  # 추가 간격 설정
        #         row_list.append(button)
        #         label=tk.Label(self.win6,text='')
        #         label.grid(row=3*i+13, column=j+2, padx=5)
        #         row_list2.append(label)
        #     button_list15.append(row_list)
        #     name_list15.append(row_list2)

        # # 이미지를 버튼에 할당
        # for i in range(2):
        #     for j in range(4):
        #         idx = i * 4 + j
        #         if idx < len(img_list15):
        #             button_list15[i][j].configure(text=img_name15[idx],image=img_list15[idx],command=lambda i=i, j=j: toggle_border15(button_list15[i][j]))
        #             name_list15[i][j].configure(text=img_name15[idx])


    def open_win11(self):
        self.img = self.p.recv()
        self.win11 = tk.Frame(self, relief="flat",bg="white")
        self.win11.place(x=0,y=0,width=800,height=1280)
        self.win11.bind("<Escape>", self.on_escape)
        
        self.img = self.img.resize((320,240))  # 이미지 크기 조절        
        photo = ImageTk.PhotoImage(self.img)
        label = tk.Label(self.win11, image=photo)
        label.image = photo  # 이미지 객체 유지
        label.grid(row=2, column=1)

        tk.Button(self.win11, text="뒤로가기", command=lambda:[self.win6.tkraise()]).grid(row=0,column=3)
        tk.Button(self.win11, text="다시 찍기", command=lambda:[self.win5.tkraise()]).grid(row=3,column=1)
        tk.Button(self.win11, text="헤어스타일 재선택", command=lambda:[self.win6.tkraise()]).grid(row=4,column=1)
        tk.Button(self.win11, text="예약하기", command=lambda:[self.win12.tkrais()]).grid(row=5,column=1)
        
    #12. 예약하기/ 디자이너 사진 + 스케줄, 완료 버튼
    def open_win12(self):
        self.win12 = tk.Frame(self, relief="flat",bg="white")
        self.win12.place(x=0,y=0,width=800,height=1280)
        self.win12.bind("<Escape>", self.on_escape)

        tk.Button(self.win12, text="뒤로가기", command=self.BaroGoback()).pack(pady=10)
        tk.Button(self.win12, text="예약하기", command=lambda:[self.open_win13(),self.win13.tkraise()]).pack(pady=10)

    def BaroGoback(self):
        # print(isBaro)
        if(self.isBaro==True):
            # print("뒤로가기")
            return lambda:[self.win4.tkraise()]
        else:
            return lambda:[self.win11.tkraise()]

    #13. 예약 완료 텍스트 or 확인 팝업창
    def open_win13(self):
        self.win13 = tk.Frame(self, relief="flat",bg="white")
        self.win13.place(x=0,y=0,width=800,height=1280)
        self.win13.bind("<Escape>", self.on_escape)
        tk.Label(self.win13, text=self.user_info["name"] + "님 예약이 완료되었습니다.").pack(pady=10)
    # esc 누르면 화면이 꺼지게 만드는 기능

    def on_escape(self,event=None):
        print("escaped")
        self.destroy()

        def quit(self):
            """Quit the Tcl interpreter. All widgets will be destroyed."""
            self.tk.quit()


def main(p):
    UI = MainUI(p)

def server(p):
    server = ClientVideoSocket("211.243.232.32",7100)
    server.connectServer()
    mode= p.recv()
    print(mode)
    server.sock.send(str(mode).encode('utf-8'))
    image_name = p.recv()
    print(image_name)
    server.sock.send(image_name.encode('utf-8'))
    style,color = p.recv()
    print(style,color)
    server.sock.send(style.encode('utf-8'))
    server.sock.send(color.encode('utf-8'))        
    # cv2.imwrite("test.png",img)
    # print(type(img))
    # img.save("test.png")    
    # img = server.receiveImages()
    # p.send(img)
    

if __name__ == "__main__":
    p,q = Pipe()
    p1 = Process(target=main,args=(p,))
    p2 = Process(target=server,args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    
