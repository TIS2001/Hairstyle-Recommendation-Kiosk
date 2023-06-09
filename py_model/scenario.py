#-*-coding:utf-8-*-
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import customtkinter as ctk
from tkinter import *
import math
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox, filedialog
import time
import os
from firebase_admin import credentials, firestore, initialize_app, storage
from util.img_send import ClientVideoSocket
from util.image_util import Capture, ShowFeed, attach_photo, imageBrowse
from util.keyboard import en2ko
import numpy as np
from multiprocessing import Process, Pipe
import subprocess
import io
## 카카오톡 관련 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from PIL import Image
import time
import configparser
import urllib
from selenium.webdriver.chrome.service import Service

class MainUI(tk.Tk):
    def __init__(self,p,picam=True):
        tk.Tk.__init__(self)
        self.picam = picam
        self.first=True
        self.p = p
        self.firebase_init()
        # os.system("onboard")
        self.img = None
        self.bucket = storage.bucket(app=self.firebase_app)
        self.geometry("800x1280")        
        self.title("Princess_maker")
        self.Kakao_init()  ## 카카오톡 관련 
        self.Frame_init()
        self.mainloop()
        # "SCDream4"= "UI/SCDream4.otf"
        self.large_font=20
        self.small_font=15
        
    #1. 첫번째 페이지- 시작하기
    def Frame_init(self):
        self.camera_init()
        self.Start_Frame()
        self.open_win1()
        # subprocess.Popen(["onboard"])
        # self.open_win2()
        # self.open_win3()
        self.open_win4()    
        self.StartFrame.tkraise()
        
    def Frame_init2(self):
        self.Start_Frame()
        self.open_win1()
        # self.open_win2()
        # self.open_win3()
        self.open_win4()   
        self.StartFrame.tkraise()
    
    ## 카카오톡 관련     
    def Kakao_init(self):
        #알리기
        Config = configparser.ConfigParser()

        #카카오 아이디, 비번 불러오기
        Config.read('../info.conf')
        Config = Config['MAIN']

        #아이디, 비번
        id = Config['kakaoid']
        pw = Config['kakaopw']

        #카카오메인페이지 지정
        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = 'https://center-pf.kakao.com/_xgyjyxj/chats'

        # 미용사에 따라 채팅룸 링크 지정
        self.ChatRoom_LGE = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876826696105085'
        self.ChatRoom_LSH = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876819996735611'
        self.ChatRoom_SDJ = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876819676480609'
        self.ChatRoom_SDH = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876782985684096'
        options = webdriver.ChromeOptions()
        service = Service(executable_path=r'/usr/bin/chromedriver')

        #user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.95 Safari/537.36")
        #창을 띄우지 1않고 실행
        options.add_argument("headless")

        #크로니움 드라이버 로드
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(3)

        #카카오 메인페이지 로드
        self.driver.get(KaKaoURL)
        time.sleep(5)

        #로그인
        idvar = self.driver.find_element(By.NAME, "loginKey")
        idvar.send_keys(id)
        pwvar =  self.driver.find_element(By.NAME, "password")
        pwvar.send_keys(pw)
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(10)
        self.driver.get(ChatRoom)
        time.sleep(3)
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button/span').click() #일주일
        time.sleep(1)

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
        img = Image.open("UI/backgrounds/First_Page.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.StartFrame,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        button_start = tk.Button(self.StartFrame, text="시작하기", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",width=15,height=5,command=lambda:[self.win1.tkraise()])
        button_start.place(relx=0.5,anchor=tk.CENTER, y=700)
        button_start.configure(font=("SCDream4",30))

    def firebase_init(self):
        cred = credentials.Certificate('./UI/princess-maker-1f45e-firebase-adminsdk-dwlbp-74b3b65023.json')
        self.firebase_app = initialize_app(cred, { 'storageBucket': 'princess-maker-1f45e.appspot.com'})
        self.db = firestore.client()
    
    
    #2. 회원가입, 로그인 버튼    
    def open_win1(self):
        self.win1 = tk.Frame(self, relief="flat",bg="white")
        self.win1.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Select_Login.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win1,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        button_back = tk.Button(self.win1, text="뒤로가기", bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2", command=lambda:[self.StartFrame.tkraise()])
        button_back.configure(font=("SCDream4",13))
        button_back.place(x=680, y=10)
        
        button_reg = tk.Button(self.win1, text="회원가입", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", width=15, height=4, command=lambda:[subprocess.Popen(["onboard"]),self.open_win2()])
        button_reg.configure(font=("SCDream4",25))
        button_reg.place(relx=0.5,anchor=tk.CENTER, y=550)
        
        button_login = tk.Button(self.win1, text="로그인", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", width=15, height=4, command=lambda:[subprocess.Popen(["onboard"]),self.open_win3()])
        button_login.configure(font=("SCDream4",25))
        button_login.place(relx=0.5,anchor=tk.CENTER, y=780)
    
    #3-1. 회원가입 페이지
    def open_win2(self):
        var = StringVar()
        cb = IntVar()
        subprocess.Popen(["onboard"])
        
        def check_duplicate_id(id):
            customer_ref = self.db.collection('customers')
            query = customer_ref.where('id', '==', id).limit(1).get()
            return len(query) > 0

        def submit():
            name = name_Ko.get("1.0", "end").strip()
            id = id_Tf.get()
            password = password_Tf.get()
            phoneNumber = phoneNumber_Tf.get()
            gender = var.get()
            shape = None
            
            if not name or not id or not password or not phoneNumber or not gender:
                messagebox.showwarning('회원가입 실패', '모든 필드를 입력해주세요.')
                return
            
            if check_duplicate_id(id):
                messagebox.showwarning('회원가입 실패', '이미 사용 중인 아이디입니다.')
                return
        
            #try:
            # Firebase에 고객 정보 저장
            self.doc_ref = self.db.collection('customers').document(id)
            self.user_info = {
                'name': name,
                'id': id,
                'password': password,
                'phoneNumber': phoneNumber,
                'gender' : gender,
                'shape' : None
            }
            self.doc_ref.set(self.user_info)
            # 저장 후 필드 초기화
            name_En.delete("1.0","end")
            name_Ko.delete("1.0","end")
            id_Tf.delete(0, tk.END)
            password_Tf.delete(0, tk.END)
            phoneNumber_Tf.delete(0, tk.END)
            var.set(None)
            
            messagebox.showinfo('회원가입 성공', f'{name}님, 회원가입이 완료되었습니다.')
            subprocess.call(["pkill","onboard"])
            self.win1.tkraise()
 
        def termsCheck():
            if cb.get() == 1:
                submit_btn['state'] = NORMAL
            else:
                submit_btn['state'] = DISABLED

        self.win2 = tk.Frame(self, relief="flat",bg="white")
        self.win2.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Register_Page.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win2,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        # 뒤로가기 버튼 왼쪽 위에 생성
        button_back = tk.Button(self.win2,text="뒤로가기", bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2", command=lambda:[subprocess.call(["pkill","onboard"]),subprocess.Popen(["onboard"]),self.win1.tkraise()])
        button_back.configure(font=("SCDream4",13))
        button_back.place(x=680, y=10)
        
        frame1 = Label(self.win2,  bg="white", highlightthickness=3, highlightbackground="black")
        frame1.config(width=600, height=600)
        frame1.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        frame2 = LabelFrame(frame1, text='성별 (Gender)', padx=50, pady=10,bg="white")
        frame2.configure(font=("SCDream4",15))

        # 라벨 설정
        label_name = Label(frame1, text='이름 (Name)',bg="white")
        label_name.configure(font=("SCDream4",15))
        label_name.grid(row=0, column=0, padx=20, pady=15, sticky=W)
        
        label_id = Label(frame1, text='아이디 (Id)',bg="white")
        label_id.configure(font=("SCDream4",15))
        label_id.grid(row=1, column=0, padx=20, pady=15, sticky=W)
        
        label_password = Label(frame1, text='비밀번호 (Password)',bg="white")
        label_password.configure(font=("SCDream4",15))
        label_password.grid(row=2, column=0, padx=20, pady=15, sticky=W)
        
        label_phone = Label(frame1, text='전화번호 (PhoneNumber)',bg="white")
        label_phone.configure(font=("SCDream4",15))
        label_phone.grid(row=3, column=0, padx=20, pady=15, sticky=W)
        var.set(None)
        # frame 2 내의 버튼
        button_man = Radiobutton(frame2, text='남자', bg="white",highlightthickness=0,variable=var, value='남자')
        button_man.configure(font=("SCDream4",15))
        button_man.grid(row=0, column=0, padx=30)
        
        button_woman = Radiobutton(frame2, text='여자',bg="white", highlightthickness=0,variable=var, value='여자')
        button_woman.configure(font=("SCDream4",15))
        button_woman.grid(row=0, column=1, padx=30)
        
        # 입력창 관련
        name_En = Text(frame1,width=1, fg="white",height=1)
        name_En.configure(font=("SCDream4",15))
        name_En.grid(row=0, column=2, padx=0, pady=10)
        name_Ko = Text(frame1,width=16, height=1)
        name_Ko.configure(font=("SCDream4",15))
        name_Ko.grid(row=0, column=3, padx=0, pady=10)
        name_En.bind("<Map>",name_En.focus_set())
        
        def handle_key(event):
            frame1.after(1, return_btn)

        def return_btn():
            main_in = name_En.get("1.0", END)
            name_Ko.delete("1.0","end")
            name_Ko.insert(END,en2ko(main_in))

        name_En.bind("<Key>", handle_key)
        id_Tf = Entry(frame1)
        id_Tf.configure(font=("SCDream4",15))
        id_Tf.grid(row=1,columnspan=4,column=2,padx=20, pady=10)
        
        password_Tf = Entry(frame1, show="*") # 비밀번호 보안을 위한 show='*'
        password_Tf.configure(font=("SCDream4",15))
        password_Tf.grid(row=2, columnspan=4,column=2, padx=20, pady=10)
        
        phoneNumber_Tf = Entry(frame1)
        phoneNumber_Tf.configure(font=("SCDream4",15))
        phoneNumber_Tf.grid(row=3, columnspan=4, column=2, padx=20, pady=10)
        
        frame2.grid(row=4, columnspan=4,padx=30)
        
        check_btn = Checkbutton(frame1, text='Accept the terms & conditions',bg="white",highlightthickness=0, variable=cb, onvalue=1, offvalue=0,command=termsCheck)
        check_btn.configure(font=("SCDream4",15))
        check_btn.grid(row=5, columnspan=4, pady=15)
        
        submit_btn = Button(frame1, text="Submit",  bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",command=submit, padx=50, pady=5, state=DISABLED)
        submit_btn.configure(font=("SCDream4",18))
        submit_btn.grid(row=6, columnspan=4, pady=15)

    
    #3-2. 로그인 페이지 
    def open_win3(self):
        subprocess.Popen(["onboard"])
        self.win3 = tk.Frame(self, relief="flat",bg="white")
        self.win3.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Login_Page.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win3,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        font_path = "UI/SCDream4.otf"
        font_size = 18
        def login():
            id = id_entry.get()
            password = password_entry.get()        

            if id and password:
                # Firebase에서 사용자 데이터 조회
                self.doc_ref = self.db.collection('customers').document(id)
                doc = self.doc_ref.get()

                if doc.exists:
                    customer_data = doc.to_dict()
                    # 비밀번호 일치 확인
                    if password == customer_data['password']:
                        self.user_info = customer_data
                        messagebox.showinfo("로그인 성공", f'어서오세요, {self.user_info["name"]}님.')
                        subprocess.call(["pkill","onboard"])
                        ## 카카오톡 관련 
                        self.driver.find_element(By.NAME, 'keyword').send_keys(self.user_info["name"])#사용자 이름 검색
                        time.sleep(1)
                        self.driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[2]/div[1]/div[2]/form/fieldset/div/button/span').click() #검색 클릭
                        time.sleep(1)
                        self.driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[2]/div[3]/div/div/li/a/div').click() #고객 채팅방 입장
                        time.sleep(5)
                        self.original_window = self.driver.current_window_handle
                        self.driver.switch_to.window(self.driver.window_handles[-1]) #팝업창으로 전환
                        ##
                        self.win4.tkraise()
                        self.win3.destroy()
                    else:
                        messagebox.showerror("로그인 실패", "비밀번호가 일치하지 않습니다.")
                else:
                    messagebox.showerror("로그인 실패", "해당 아이디가 존재하지 않습니다.")
            else:
                messagebox.showwarning("로그인 실패", "아이디와 비밀번호를 입력해주세요.")


        button_back = Button(self.win3, text="뒤로가기", bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2", command=lambda:[subprocess.call(["pkill","onboard"]),subprocess.Popen(["onboard"]),self.win1.tkraise()])
        button_back.configure(font=("SCDream4",13))
        button_back.place(x=680, y=10)
        
        frame1 = Label(self.win3, bg="white", highlightthickness=3, highlightbackground="black")
        frame1.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        # 라벨 설정
        label_id = Label(frame1, text='아이디 (Id)',bg="white")
        label_id.configure(font=("SCDream4",15))
        label_id.grid(row=1, column=0, padx=20, pady=15, sticky=W)
        
        label_pw = Label(frame1, text='비밀번호 (Password)',bg="white")
        label_pw.configure(font=("SCDream4",15))
        label_pw.grid(row=2, column=0, padx=20, pady=15, sticky=W)
        
        # 입력칸 설정
        id_entry = Entry(frame1)
        id_entry.configure(font=("SCDream4",15))
        id_entry.grid(row=1, column=1, padx=20, pady=15)
        id_entry.bind("<Map>",id_entry.focus_set())
        
        password_entry = Entry(frame1, show="*")
        password_entry.configure(font=("SCDream4",15))
        password_entry.grid(row=2, column=1, padx=20, pady=15)
        
        # 로그인 버튼
        button_login = Button(frame1, text="로그인",bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", command=login)
        button_login.configure(font=("SCDream4",18))
        button_login.grid(row=4, columnspan=3, padx=10, pady=30, sticky="s")

    #4. 카메라 실행/ 예약(-> #12), 헤어스타일 선택(-> #5) 버튼
    def open_win4(self):
        self.isBaro=False
        self.win4 = tk.Frame(self, relief="flat",bg="white")
        self.win4.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Select_Page2.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win4,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        # 바로 예약
        def baro():
            self.isBaro=True
            # print(self.isBaro)

        button_back = tk.Button(self.win4, text="뒤로가기",  bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2", command=lambda:[self.open_win3()])
        button_back.configure(font=("SCDream4",13))
        button_back.place(x=680, y=10)
        
        button_reg = tk.Button(self.win4, text="바로 예약하기",  bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", width=22, height=6, command=lambda:[baro(),self.open_win12(),self.win12.tkraise(),self.win4.destroy()])
        button_reg.configure(font=("SCDream4",20))
        button_reg.place(relx=0.5,anchor=tk.CENTER, y=550)
        if (self.picam and self.first):
            button_login = tk.Button(self.win4, text="헤어스타일 합성", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", width=22, height=6,command=lambda:[self.camera.start(),self.open_win5(),self.win5.tkraise(),self.win4.destroy()])
        else:
            button_login = tk.Button(self.win4, text="헤어스타일 합성", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", width=22, height=6,command=lambda:[self.open_win5(),self.win5.tkraise(),self.win4.destroy()])
        button_login.configure(font=("SCDream4",20))
        button_login.place(relx=0.5,anchor=tk.CENTER, y=800)

    #5. 사진 촬영(5초 타이머) or 사진 가져오기(-> 팝업창)
    def open_win5(self):
        self.first=False
        self.win5 = tk.Frame(self, relief="flat",bg="white")
        self.win5.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/ScreenShot.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win5,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        self.selected=0
        self.copyImage=0
        self.prevImage=0
        self.selectPhoto=0
        self.presentImage=0
        self.mode=1
        self.mode1=1
        self.mode2=1
        self.list=[]
        def count_down(num):
            # self.win5.countdown_label.place(relx=0.5,y=50,anchor=tk.CENTER)
            self.win5.countdown_label.place(relx=0.5,anchor=tk.CENTER,rely=0.27)
            self.win5.countdown_label.configure(font=("SCDream4",30),text=str(num))
            if num>1:
                self.win5.after(1000,count_down,num-1)
            else:
                self.win5.after(750,lambda:AfterCapture(Capture(self.win5,self.picam)))

        def AfterCapture(frame):
            self.win5.after(500,lambda:[self.win5.countdown_label.place(relx=0.5,rely=0.48,anchor=tk.CENTER),self.win5.countdown_label.configure(font=("SCDream4",16),text="사진 클릭 후 \'사진 선택\' 버튼을 눌러주세요!",bg="white")])
            self.win5.countdown_label.configure(font=("SCDream4",20),text="Cheese!")
            if self.copyImage:
                self.selectPhoto=self.prevImage
                self.win5.imageLabel2.config(image=self.copyImage)
                self.win5.imageLabel2.photo = self.copyImage
                if self.mode2==0:
                    self.mode1=0
                else:
                    self.mode1=1
            frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
            self.presentImage = Image.fromarray(frame_rgb)
            self.prevImage=self.presentImage
            # self.presentImage=img
            resizedImg = self.presentImage.resize((300,300), Image.LANCZOS)
            self.copyImage = ImageTk.PhotoImage(resizedImg)
                        
            self.win5.imageLabel.config(image=self.copyImage)
            self.win5.imageLabel.photo = self.copyImage
            self.win5.takePhoto_bt.configure(text="재촬영")
            self.win5.imageLabel.config(relief="flat", highlightthickness=0)
            self.win5.imageLabel2.config(relief="flat", highlightthickness=0)
            self.list.clear()
            self.mode2=1

        def AfterBrowse(image):
            self.win5.countdown_label.place(relx=0.5,rely=0.48,anchor=tk.CENTER)
            self.win5.countdown_label.configure(font=("SCDream4",16),text="사진 클릭 후 \'사진 선택\' 버튼을 눌러주세요!",bg="white")
            self.presentImage=image
            if self.copyImage:
                # resizedImg = img.resize((100,100),Image.LANCZOS)
                # resized=self.copyImage.resize((100,100), Image.LANCZOS)
                self.selectPhoto=self.prevImage
                self.win5.imageLabel2.config(image=self.copyImage)
                self.win5.imageLabel2.photo = self.copyImage
                if self.mode2==0:
                    self.mode1=0
                else:
                    self.mode1=1
            self.prevImage=image
            resizedImg = image.resize((300,300), Image.LANCZOS)
            self.copyImage=ImageTk.PhotoImage(resizedImg)
            self.win5.imageLabel.config(image=self.copyImage)
            # Keeping a reference
            self.win5.imageLabel.photo = self.copyImage
            self.win5.imageLabel.config(relief="flat", highlightthickness=0)
            self.win5.imageLabel2.config(relief="flat", highlightthickness=0)
            self.list.clear()
            self.mode2=0

        def AfterSelect(mode,image_name,image):
            if bool(self.list):
                if mode==1:                
                    attach_photo(self.bucket,self.user_info["id"],image)
                self.p.send(mode)   #real
                self.p.send(image_name) #real
                while(self.user_info['shape']==None):
                    self.user_info = self.doc_ref.get().to_dict()
                messagebox.showinfo("로딩중", f'사진 전송에 성공했습니다.\n잠시만 기다려주세요 :)')
                self.open_win6()
                self.win6.tkraise()
                self.win5.destroy()
            else:
                messagebox.showwarning('사진 전송 오류', '헤어스타일 합성을 위한 사진을 선택해주세요.')

        def tg_img(label,btn):
            #오른쪽 버튼 선택
            if label==1:
                self.mode=self.mode2
                self.selected=self.presentImage

            elif label==2:
                self.mode=self.mode1
                self.selected=self.selectPhoto
            if btn.cget("relief") == "solid":
                btn.config(relief="flat", highlightthickness=0)
                self.list.clear()
            else:
                if bool(self.list):
                    self.list[0].config(relief="flat", highlightthickness=0)
                    self.list.clear()
                btn.config(relief="solid", highlightthickness=2, highlightbackground="red")
                self.list.append(btn)
                
        tk.Button(self.win5, font=("SCDream4",15),text="뒤로가기",  bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2", command=lambda:[self.open_win4(),self.win5.destroy()]).place(x=680, y=10)
        browse_bt=tk.Button(self.win5,font=("SCDream4",15), text="사진 가져오기", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",command=lambda:[AfterBrowse(imageBrowse(self.bucket,self.user_info["id"]))])
        browse_bt.place(relx=0.5,anchor=tk.CENTER,y=990,width=200,height=70)
        
        self.win5.cameraLabel = Label(self.win5, bg="black", borderwidth=3, relief="groove")
        self.win5.cameraLabel.place(relx=0.5,anchor=tk.CENTER,rely=0.27)
        self.win5.imageLabel = Button(self.win5, bg="black", borderwidth=1, relief="groove")
        self.win5.imageLabel.config(command=lambda btn=self.win5.imageLabel:tg_img(1,btn))
        self.win5.imageLabel.place(relx=0.5,anchor=tk.W,rely=0.6)
        self.win5.imageLabel2 = Button(self.win5, bg="black", borderwidth=1, relief="groove")
        self.win5.imageLabel2.configure(command=lambda btn=self.win5.imageLabel2:tg_img(2,btn))
        self.win5.imageLabel2.place(relx=0.5,anchor=tk.E,rely=0.6)
        self.win5.takePhoto_bt=tk.Button(self.win5,font=("SCDream4",15), text="사진 촬영", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", command=lambda:[count_down(3)])
        self.win5.takePhoto_bt.place(relx=0.5,anchor=tk.CENTER,y=1070,width=200,height=70)
        self.win5.countdown_label=Label(self.win5, text="",font=("SCDream4",36))
        image_name = self.user_info['id']
        select_bt=tk.Button(self.win5,font=("SCDream4",15), text="사진 선택",  bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", \
                                command=lambda:[AfterSelect(self.mode,image_name,self.selected)])
        select_bt.place(relx=0.5,anchor=tk.CENTER,y=1150,width=200,height=70)
        self.win5.cap = self.camera
        # Setting width and height

        ShowFeed(self.win5,self.picam)
    
    def clear_frame(self, frame):
        if frame is not None:
            for widget in frame.winfo_children():
                widget.destroy()

    def open_win6(self,img=None):
        self.win6 = tk.Frame(self, relief="flat", bg="white")
        self.win6.place(x=0, y=0, width=800, height=1280)
        bg_img = Image.open("UI/backgrounds/Final.PNG")
        bg_img=bg_img.resize((800,1280))
        bg_photo=ImageTk.PhotoImage(bg_img)
        bg_label=tk.Label(self.win6,image=bg_photo)
        bg_label.place(x=0,y=0)
        bg_label.configure(image=bg_photo)
        bg_label.image=bg_photo
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
        if self.user_info["gender"]=='여자':
            self.gender="female"
        else:
            self.gender="male"
        self.img_path1=[os.path.join("UI/colors/전체", f) for f in os.listdir("UI/colors/전체") if f.endswith(".JPG")]
        self.img_path2=[os.path.join("UI/hairstyles/"+self.gender+"/전체", f) for f in os.listdir("UI/hairstyles/"+self.gender+"/전체") if f.endswith(".jpg")]
        self.append_list(self.img_path1,self.img_list1,self.img_name1)
        self.append_list(self.img_path2,self.img_list2,self.img_name2)
        self.frame1 = tk.Frame(self.win6,bg="white", relief="flat")
        self.frame1.place(x=70, y=50,width=665)
        self.frame2 = tk.Frame(self.win6,bg="white", relief="flat")
        self.frame2.place(x=70, y=260,width=665)  #250
        self.frame3 = tk.Frame(self.win6, bg="white", relief="flat")
        self.frame3.place(x=10, y=465,width=780)    #450
        self.frame4 = tk.Frame(self.win6, bg="white", relief="flat")
        self.frame4.place(x=70, y=695,width=665) #650
        self.frame5 = tk.Frame(self.win6, bg="white", relief="flat")
        self.frame5.place(x=10, y=900,width=780) #850
        self.make_btn(self.frame3, self.img_path1,0)
        self.recommend_style()  #real
        # self.make_btn(self.frame4, [os.path.join("UI/hairstyles/"+self.gender+"/계란형", f) for f in os.listdir("UI/hairstyles/"+self.gender+"/계란형") if f.endswith(".jpg")],0)   #test
        self.make_btn(self.frame5, self.img_path2,0)
        # img = None
        # while not img:
            # if self.p.poll(timeout=2):
        if not img: #real
            self.tran_img = self.p.recv()
            img = self.tran_img #여기까지
            # else:
            #     self.p.send(1) #not receive img
        # self.p.send(0) #receive img
        self.select_personal(img) #real
        # self.select_personal()  #test
        tk.Button(self.win6, font=("SCDream4",15), text="헤어스타일 선택",bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",\
            command=lambda: [self.send_styles()]).place(relx=0.5,anchor=tk.CENTER,y=1120,height=50)
        tk.Label(self.win6,font=("SCDream4",13),text='1) 잘 어울리는 퍼스널컬러의 라디오버튼을 클릭하세요.',\
            bg="white", relief="flat", highlightthickness=2, highlightbackground="black").place(relx=0.5,anchor=tk.CENTER,y=30,width=665)
        tk.Label(self.win6,font=("SCDream4",13),text='퍼스널컬러에 따른 추천 염색 컬러',\
            bg="white", relief="flat", highlightthickness=2, highlightbackground="black").place(relx=0.5,anchor=tk.CENTER,y=245,width=665)
        tk.Label(self.win6,font=("SCDream4",13),text='전체 염색 컬러',\
            bg="white", relief="flat", highlightthickness=2, highlightbackground="black").place(relx=0.5,anchor=tk.CENTER,y=450,width=665)
        tk.Label(self.win6,font=("SCDream4",13),text=f"2) {self.user_info['shape']} 추천 헤어스타일",\
            bg="white", relief="flat", highlightthickness=2, highlightbackground="black").place(relx=0.5,anchor=tk.CENTER,y=680,width=665)
        tk.Label(self.win6,font=("SCDream4",13),text='전체 헤어스타일',\
            bg="white", relief="flat", highlightthickness=2, highlightbackground="black").place(relx=0.5,anchor=tk.CENTER,y=885,width=665)

    def send_styles(self):
        if bool(self.dict1) and bool(self.dict2):
            selection=[]
            color=self.dict1[next(iter(self.dict1))].cget("text")
            style=self.dict2[next(iter(self.dict2))].cget("text")
            selection.append(style)
            selection.append(color)
            self.p.send(selection)  

            while(self.user_info['shape']==None):
                self.user_info = self.doc_ref.get().to_dict()
            messagebox.showinfo("로딩중", f'헤어스타일 선택에 성공했습니다.\n잠시만 기다려주세요 :)')
            self.open_win11()
            self.win11.tkraise()
            self.win6.destroy()
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
                buttons[i].configure(text=img_name[idx],font=("SCDream4", 12),bg="white",state="normal",image=img_list[idx], relief="flat", highlightthickness=0)
                labels[i].configure(text=img_name[idx],font=("SCDream4", 12),bg="white")
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
                label = tk.Label(frame, text=img_name[i],font=("SCDream4", 11),bg="white")
                button.configure(text=img_name[i],command=lambda btn=button: self.toggle_border(btn),bg="white")
            
            else:
                button=tk.Button(frame)
                button.configure(command=lambda btn=button: self.toggle_border(btn))
                label = tk.Label(frame)

            if frame == self.frame3:               
                self.buttons1.append(button)
                self.labels1.append(label)
                self.buttons1[i].configure(text=self.img_name1[idx],image=self.img_list1[idx],bg="white")
                self.labels1[i].configure(text=self.img_name1[idx],font=("SCDream4", 11),bg="white")

            elif frame == self.frame5 :
                self.buttons2.append(button)
                self.labels2.append(label)
                self.buttons2[i].configure(text=self.img_name2[idx],bg="white",image=self.img_list2[idx])
                self.labels2[i].configure(text=self.img_name2[idx],font=("SCDream4", 11),bg="white")

            button.grid(row=1,column=i+1,padx=5)
            label.grid(row=2,column=i+1,padx=5)

        if frame == self.frame3 or frame == self.frame5:  
            button1 = tk.Button(frame, font=("SCDream4", 15), text="◀", bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2",\
                command=lambda direction="prev": self.navi_click(frame,direction))
            button1.grid(row=1, column=0, padx=5)

            button2 = tk.Button(frame, font=("SCDream4", 15), text="▶", bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2",\
                command=lambda direction="next": self.navi_click(frame,direction))
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
                
    def recommend_style(self):
        self.user_info = self.doc_ref.get().to_dict()
        dir_path="UI/hairstyles/"+self.gender+"/"+self.user_info["shape"]
        self.make_btn(self.frame4,[os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".jpg")],0)
    
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

    # def select_personal(self):  #test
    def select_personal(self,img):    #real
        # 배경 이미지 파일 경로
        backgrounds = ["UI/퍼스널컬러배경/봄웜톤.png", "UI/퍼스널컬러배경/여름쿨톤.png", "UI/퍼스널컬러배경/가을웜톤.png", "UI/퍼스널컬러배경/겨울쿨톤.png"]
        # 전경 이미지 파일 경로
        foreground = img    #real
        # foreground=Image.open("UI/test.png")    #test
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
            image_name = backgrounds[i].split("/")[-1].split(".")[0]  # 이미지 파일 이름 (확장자 제외)

            name_label = tk.Radiobutton(self.frame1, font=("SCDream4", 12),bg="white", text=image_name, variable=self.var, value=i+1,
                            command=lambda:self.personal_cmd())
            name_label.grid(row=4, column=i+2,padx=5)

    def open_win11(self):
        self.win11 = tk.Frame(self, relief="flat",bg="white")
        self.win11.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Result.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win11,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        self.img = None
        # while not self.img:
            # if self.p.poll(timeout=30):
        self.img = self.p.recv()
            # else:
                # self.p.send(0)
        # self.p.send(1)
        
        self.img = self.img.resize((512, 512))  # 이미지 크기 조절        
        photo = ImageTk.PhotoImage(self.img)
        label = tk.Label(self.win11, image=photo,highlightthickness=2, highlightbackground="black")
        label.image = photo  # 이미지 객체 유지
        label.place(relx=0.5,rely=0.35,anchor=tk.CENTER)
        
        # tk.Button(self.win11, font=("SCDream4",15), text="뒤로가기", command=lambda:[self.p.send(6),self.win6.tkraise()]).place(x=680, y=0)
        tk.Button(self.win11, font=("SCDream4",15), text="다시 찍기", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",command=lambda:[self.p.send(7),self.open_win5()]).place(relx=0.5,anchor=tk.CENTER,y=820,width=300,height=80)
        tk.Button(self.win11, font=("SCDream4",15), text="헤어스타일 재선택", bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2", command=lambda:[self.p.send(6),self.open_win6(self.tran_img)]).place(relx=0.5,anchor=tk.CENTER,y=920,width=300,height=80)
        tk.Button(self.win11, font=("SCDream4",15), text="예약하기",  bg="white", relief="flat", highlightthickness=3, highlightbackground="#FF6BA2",command=lambda:[self.open_win12()]).place(relx=0.5,anchor=tk.CENTER,y=1020,width=300,height=80)

    #12. 예약하기/ 디자이너 사진 + 스케줄, 완료 버튼
    def open_win12(self):
        self.win12 = tk.Frame(self, relief="flat",bg="white")
        self.win12.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Reservation_Page.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win12,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        self.reservation_buttons = []
        times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]  # 예약 가능한 시간 리스트
        
        class designer():            
            def __init__(self,name,win,y):
                self.name=name
                self.reservation_buttons = list()
                self.frame1 = tk.LabelFrame(win, text=name,font=("SCDream4",15),labelanchor="n",bg="white", width=200, height=200)
                self.frame1.place(x=75, y=y)
                self.frame2 = tk.Frame(win, bg="white", highlightthickness=2, highlightbackground="black",width=400, height=200)
                self.frame2.place(x=300, y=y)
                self.selected_button = None  # 선택된 버튼을 저장하는 변수            
                                
            def toggle_reservation(self,index):
                # 버튼의 선택 상태를 변경하고, 다른 버튼의 선택 상태를 초기화하는 함수
                for btn in self.reservation_buttons:
                    if btn["relief"] == "sunken":
                        btn["relief"] = "raised"
                        btn.config( highlightbackground="black")

                if self.selected_button == self.reservation_buttons[index]:
                    self.selected_button = None
                else:
                    self.reservation_buttons[index]["relief"] = "sunken"
                    # self.reservation_buttons[index].config(highlightthickness=2, highlightbackground="black",bg="white")
                    self.selected_button = self.reservation_buttons[index]
                    self.selected_button.config(highlightbackground="red")
                        
            def read_reservation(self,db):
                # Firestore에서 예약된 시간 읽어오기
                hairdresser_ref = db.collection("hairdresser").document(self.name)
                doc = hairdresser_ref.get()
                
                if doc.exists:
                    reservation_time = doc.get("reservation_time")
                    saved_times = reservation_time if isinstance(reservation_time, list) else []
                else:
                    saved_times = []        

                for index, time in enumerate(times):
                    btn_state = tk.NORMAL
                    # 인덱스와 시간을 흝으면서, 예약 시간이 이미 잡혀있다면 버튼 비활성화.
                    if time in saved_times or (int(time.split(":")[0]) <= datetime.now().hour):
                        btn_state = tk.DISABLED
                
                    row = index // 5  # 버튼이 배치될 행 인덱스
                    col = index % 5  # 버튼이 배치될 열 인덱스
                    
                    btn = tk.Button(self.frame2, text=time, state=btn_state, bg="white", activeforeground="red",highlightthickness=2, highlightbackground="black",command=lambda i=index: self.toggle_reservation(i))
                    btn.grid(row=row, column=col, padx=10, pady=30)
                    self.reservation_buttons.append(btn) 
                
        def make_reservation(designer_list):
            # 예약 정보 저장 및 Firestore에 전달하는 함수
            all_time = []
            send_time = []
            
            # 버튼이 한개만 눌리게 만들려는 로직
            for designer in designer_list:
                selected_buttons = [btn for btn in designer.reservation_buttons if btn["relief"] == "sunken"]
                
                all_time.extend(selected_buttons)
            
            if len(all_time) != 1:
                    messagebox.showwarning("경고", "하나의 시간대를 선택해야 합니다.")
                    return  # 예약 중단
            
            for designer in designer_list:                
                reservation_time = []

                # 기존 예약 시간 불러오기
                hairdresser_ref = self.db.collection("hairdresser").document(designer.name)
                doc = hairdresser_ref.get()
                
                if doc.exists:
                    reservation_time = doc.get("reservation_time")
                
                # 새로운 예약 시간 추가
                for index, btn in enumerate(designer.reservation_buttons):
                    if btn["relief"] == "sunken":
                        new_time = times[index]
                        if new_time not in reservation_time:  # 중복 확인
                            reservation_time.append(new_time)
                            send_time.append(new_time)
                            # 카카오톡 관련
                            # 선택된 시간의 디자이너에서 전송하도록 설정
                            if designer.name == "이승현":
                                Load_ChattingRoom = self.ChatRoom_LSH
                            elif designer.name == "선동진":
                                Load_ChattingRoom = self.ChatRoom_SDJ
                            elif designer.name == "이가은":
                                Load_ChattingRoom = self.ChatRoom_LGE
                            elif designer.name == "신동훈":
                                Load_ChattingRoom = self.ChatRoom_SDH
                            #
                
                # 예약 정보와 기타 필요한 정보를 수집하여 Firestore에 저장
                data = {
                    "reservation_time": reservation_time,
                    # 추가 필드 정보 입력
                }
                
                # Firestore에 예약 정보 저장
                hairdresser_ref.set(data)
            
            ## 카카오톡 관련
            # 
            # with io.BytesIO() as stream:
                # self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                # self.img = Image.fromarray(self.img)
            self.driver.find_element(By.ID, 'chatWrite').send_keys(self.user_info["name"],'님 ', send_time,' 예약 완료되었습니다.')
            time.sleep(2)  # 수정 필요 (현재 딜레이 고려해 3초 설정)
            self.driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼   
            time.sleep(2)
            self.img.save("result.jpg", format='JPEG')
            if self.isBaro == False:
                self.driver.find_element(By.XPATH, "//input[@class='custom uploadInput']").send_keys("/home/u2018430034/project/Hairstyle-Recommendation-Kiosk/py_model/result.jpg") #고객한테 사진 전송
            time.sleep(2)
            
            #채팅방 로드 (미용사에게 로드)
            self.driver.get(Load_ChattingRoom)  
            time.sleep(3)  # 수정 필요 (현재 딜레이 고려해 3초 설정)
            # 사진전송, 메시지 전송
            self.driver.find_element(By.ID, 'chatWrite').send_keys(self.user_info["name"],'님 ', send_time,' 예약 완료되었습니다.')
            time.sleep(2)  # 수정 필요 (현재 딜레이 고려해 3초 설정)
            self.driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼   
            time.sleep(2)
            if self.isBaro == False: 
                self.driver.find_element(By.XPATH, "//input[@class='custom uploadInput']").send_keys("/home/u2018430034/project/Hairstyle-Recommendation-Kiosk/py_model/result.jpg") 
                time.sleep(2)
             
            # 팝업창 닫기
            self.driver.close()
            self.driver.switch_to.window(self.original_window)
            self.driver.find_element(By.NAME, 'keyword').send_keys(Keys.CONTROL + "a")
            self.driver.find_element(By.NAME, 'keyword').send_keys(Keys.DELETE)
            ##
            self.open_win13() 
            self.win13.tkraise()    
        
        def show_image(frame, filename):
            # 이미지를 다운로드하여 해당 프레임에 출력하는 함수
            # image_path = download_image(filename)
            img = Image.open(filename)
            img = img.resize((132, 170), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=img_tk)
            label.image = img_tk
            label.pack()
            
        # button_back = tk.Button(self.win12, text="뒤로가기", command=self.BaroGoback())
        if(self.isBaro):
            button_back = tk.Button(self.win12, font=("SCDream4",13),  bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2",text="뒤로가기", command=lambda:[self.open_win4()]) 
        else:
            button_back = tk.Button(self.win12, font=("SCDream4",13),  bg="white", relief="flat", highlightthickness=2, highlightbackground="#FF6BA2",text="뒤로가기", command=lambda:self.win11.tkraise())

        button_back.configure(font=("SCDream4",13))
        button_back.place(x=680, y=10)
        
        designer1 = designer("이승현",self.win12, y=165)
        filename1 = "이승현.jpg"
        show_image(designer1.frame1, filename1)  
        designer1.read_reservation(self.db)

        designer2 = designer("선동진", self.win12, y=390)
        filename2 = "선동진.jpg"
        show_image(designer2.frame1, filename2)
        designer2.read_reservation(self.db)
        
        designer3 = designer("이가은", self.win12, y=615)
        filename3 = "이가은.jpg"
        show_image(designer3.frame1, filename3)
        designer3.read_reservation(self.db)
        
        designer4 = designer("신동훈", self.win12, y=840)
        filename4 = "신동훈.jpg"
        show_image(designer4.frame1, filename4)
        designer4.read_reservation(self.db)

        # 생성했던 디자이너 리스트들
        self.designer_list = [designer1,designer2,designer3,designer4]
        
        # 예약하기 버튼 생성
        tk.Button(self.win12, font=("SCDream4",15),text="예약하기", bg="white", relief="flat", \
            highlightthickness=3, highlightbackground="#FF6BA2",width=20,height=3,command=lambda:[make_reservation(self.designer_list)]).place(relx=0.5,rely=0.88,anchor=tk.CENTER)
        if(self.isBaro):
            pass
        else:
            self.p.send(7)

    #13. 예약 완료 텍스트 or 확인 팝업창
    def open_win13(self):
        self.win13 = tk.Frame(self, relief="flat",bg="white")
        self.win13.place(x=0,y=0,width=800,height=1280)
        img = Image.open("UI/backgrounds/Final.PNG")
        img=img.resize((800,1280))
        photo=ImageTk.PhotoImage(img)
        label=tk.Label(self.win13,image=photo)
        label.place(x=0,y=0)
        label.configure(image=photo)
        label.image=photo
        tk.Label(self.win13, bg="white", font=("SCDream4", 27), text=self.user_info["name"] + "님 예약이 완료되었습니다.").place(relx=0.5,rely=0.3,anchor=tk.CENTER)

        self.win13.after(2000,lambda:[self.Frame_init2(),self.win13.destroy()])

        def quit(self):
            """Quit the Tcl interpreter. All widgets will be destroyed."""
            self.tk.quit()

def main(p):
    UI = MainUI(p)

def server(p):
    server = ClientVideoSocket("",)
    server.connectServer()
    # camera
    var1 = 5
    while var1==5 or var1==7:
        # print("var1", var1)
        mode= p.recv()
        # print("mode", mode)
        server.sock.send(str(mode).encode('utf-8'))
        image_name = p.recv()
        # print("name",image_name)
        
        server.sock.send(image_name.encode('utf-8'))
        img = server.receiveImages_png()
        # p.send(img)
        # while p.recv():
        p.send(img)
        # print("5일 때 ",var1)
        var1=6
        while var1==6:  
            style,color = p.recv()
            print(style,color)
            st=style+"/"+color
            server.sock.send(st.encode('utf-8'))
            # time.sleep(1)
            # server.sock.send(color.encode('utf-8'))        
            # cv2.imwrite("test.png",img)
            # print(type(img))
            # img.save("test.png")    
            img = server.receiveImages()
            p.send(img)
            # while p.recv():
                # p.send(img)
            var1 = p.recv() ## if var1 = 6 style 재선택 if var1=5 재촬영
            # print("6일 때 ",var1)
            server.sock.send(str(var1).encode('utf-8'))
    server.sock.close()
    

if __name__ == "__main__":
    p,q = Pipe()
    p1 = Process(target=main,args=(p,))
    p2 = Process(target=server,args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()



