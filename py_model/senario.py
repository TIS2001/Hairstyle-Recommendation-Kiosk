import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import *
import time
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from firebase_admin import credentials, firestore, initialize_app, storage
from util.img_send import ClientVideoSocket
from util.image_util import Capture, ShowFeed, attach_photo, imageBrowse
import numpy as np
from threading import Thread


class MainUI(tk.Tk):
    def __init__(self,picam=False,server_open=False):
        tk.Tk.__init__(self)
        self.pycam = picam
        self.server_open=server_open
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
        if self.pycam:
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
        
        button_start = tk.Button(self.StartFrame, text="시작하기", width=16, height=7, command=lambda:[self.win1.tkraise()])
        button_start.pack(anchor="center",pady=200)
        button_start.configure(font=(20))
        
        self.StartFrame.bind("<Escape>", self.on_escape)
        
    def img_thread(self,img):
        if self.server_open:
            self.server_tk = self.after(0,self.connect_server,img)
        else:
            pass
    
    def connect_server(self,img):
        self.server = ClientVideoSocket("211.243.232.32",7100)
        self.server.connectServer()
        self.server.sendImages(img)
        self.img = self.server.receiveImages()
        # self.img.save("test.png")

    def firebase_init(self):
        cred = credentials.Certificate('./UI/easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
        self.firebase_app = initialize_app(cred, { 'storageBucket': 'easylogin-58c28.appspot.com'})
        self.db = firestore.client()
    
    
    #2. 회원가입, 로그인 버튼    
    def open_win1(self):
        self.win1 = tk.Frame(self, relief="flat",bg="white")
        self.win1.place(x=0,y=0,width=800,height=1280)
        self.win1.bind("<Escape>", self.on_escape)
        button_back = tk.Button(self.win1, text="뒤로가기", command=lambda:[self.StartFrame.tkraise()])
        button_back.configure(font=(20))
        button_back.place(x=670, y=10)
        
        button_reg = tk.Button(self.win1, text="회원가입하기", width=15, height=5, command=lambda:[self.win2.tkraise()])
        button_reg.configure(font=(20))
        button_reg.place(x=150, y=100)
        
        button_login = tk.Button(self.win1, text="로그인하기", width=15, height=5, command=lambda:[self.win3.tkraise()])
        button_login.configure(font=(20))
        button_login.place(x=450, y=100)
    
    
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
        button_back = tk.Button(self.win2, text="뒤로가기", command=lambda:[self.win1.tkraise()])
        button_back.configure(font=(20))
        button_back.place(x=670, y=10)
        
        frame1 = Label(self.win2, bg='#dddddd')
        # frame1.config(width=600, height=600)
        frame1.place(x=100, y=100)
        frame2 = LabelFrame(frame1, text='성별 (Gender)', padx=50, pady=10)
        frame2.configure(font=(30))

        # 라벨 설정
        label_name = Label(frame1, text='이름 (Name)')
        label_name.configure(font=(30))
        label_name.grid(row=0, column=0, padx=20, pady=15, sticky=W)
        
        label_id = Label(frame1, text='아이디 (Id)')
        label_id.configure(font=(30))
        label_id.grid(row=1, column=0, padx=20, pady=15, sticky=W)
        
        label_password = Label(frame1, text='비밀번호 (Password)')
        label_password.configure(font=(30))
        label_password.grid(row=2, column=0, padx=20, pady=15, sticky=W)
        
        label_phone = Label(frame1, text='전화번호 (PhoneNumber)')
        label_phone.configure(font=(30))
        label_phone.grid(row=3, column=0, padx=20, pady=15, sticky=W)
        
        var.set(None)
        # frame 2 내의 버튼
        button_man = Radiobutton(frame2, text='남자', variable=var, value='남자')
        button_man.configure(font=(30))
        button_man.grid(row=0, column=0, padx=30)
        
        button_woman = Radiobutton(frame2, text='여자', variable=var, value='여자')
        button_woman.configure(font=(30))
        button_woman.grid(row=0, column=1, padx=30)
        
        # 입력창 관련
        name_Tf = Entry(frame1)
        name_Tf.configure(font=(30))
        name_Tf.grid(row=0, column=2, padx=20, pady=10)
        
        id_Tf = Entry(frame1)
        id_Tf.configure(font=(30))
        id_Tf.grid(row=1, column=2,padx=20, pady=10)
        
        password_Tf = Entry(frame1, show="*") # 비밀번호 보안을 위한 show='*'
        password_Tf.configure(font=(30))
        password_Tf.grid(row=2, column=2, padx=20, pady=10)
        
        phoneNumber_Tf = Entry(frame1)
        phoneNumber_Tf.configure(font=(30))
        phoneNumber_Tf.grid(row=3, column=2, padx=20, pady=10)
        
        frame2.grid(row=4, columnspan=3,padx=30)
        
        check_btn = Checkbutton(frame1, text='Accept the terms & conditions', variable=cb, onvalue=1, offvalue=0,command=termsCheck)
        check_btn.configure(font=(30))
        check_btn.grid(row=5, columnspan=4, pady=15)
        
        submit_btn = Button(frame1, text="Submit", command=submit, padx=50, pady=5, state=DISABLED)
        submit_btn.configure(font=(30))
        submit_btn.grid(row=6, columnspan=4, pady=15)
    
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


        button_back = Button(self.win3, text="뒤로가기", command=lambda:[self.win1.tkraise()])
        button_back.configure(font=(20))
        button_back.place(x=670, y=10)
        
        frame1 = Label(self.win3, bg='#dddddd')
        frame1.place(x=100, y=100)
        
        # 라벨 설정
        label_id = Label(frame1, text='아이디 (Id)')
        label_id.configure(font=(30))
        label_id.grid(row=1, column=0, padx=20, pady=15, sticky=W)
            
        label_pw = Label(frame1, text='비밀번호 (Password)')
        label_pw.configure(font=(30))
        label_pw.grid(row=2, column=0, padx=20, pady=15, sticky=W)
        
        # 입력칸 설정
        id_entry = Entry(frame1)
        id_entry.configure(font=(30))
        id_entry.grid(row=1, column=1, padx=20, pady=15)
        
        password_entry = Entry(frame1, show="*")
        password_entry.configure(font=(30))
        password_entry.grid(row=2, column=1, padx=20, pady=15)
        
        # 로그인 버튼
        button_login = Button(frame1, text="로그인", command=login)
        button_login.configure(font=(30))
        button_login.grid(row=4, columnspan=3, padx=10, pady=30, sticky="s")

    #4. 카메라 실행/ 예약(-> #12), 헤어스타일 선택(-> #5) 버튼
    def open_win4(self):
        self.isBaro=False
        self.win4 = tk.Frame(self, relief="flat",bg="white")
        self.win4.place(x=0,y=0,width=800,height=1280)
        self.win4.bind("<Escape>", self.on_escape)
        
        # 바로 예약
        def baro():
            self.isBaro=True
            # print(self.isBaro)
            
        tk.Button(self.win4, text="뒤로가기", command=lambda:[self.win3.tkraise()]).pack(padx=10,pady=10, side="top", anchor="ne")
        tk.Button(self.win4, text="바로 예약하기", width=15, height=5, command=lambda:[baro(),self.win12.tkraise()]).pack(pady=10)
        tk.Button(self.win4, text="헤어스타일 합성", width=15, height=5, command=lambda:[self.camera.start(),self.open_win5(),self.win5.tkraise()]).pack(pady=10)

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
            tk.Button(self.win5, text="다시 찍기", command=lambda:[AfterCapture(Capture(self.win5,self.picam))]).place(x=350,y=630,width=100,height=40)    
            # tk.Button(self.win5, text="사진 선택", command=lambda:[self.server.sendImages(frame),self.win5.withdraw(),self.open_win6()]).grid(row=9,column=3)
            tk.Button(self.win5, text="사진 선택", command=lambda:[attach_photo(self.bucket,self.user_info["name"],image),self.open_win6(),self.win6.tkraise(),self.img_thread(frame)]).place(x=350,y=680,width=100,height=40)
        
        def AfterBrowse(image):
            frame = np.array(image)
            resizedImg = image.resize((200,200), Image.LANCZOS)
            saved_image=ImageTk.PhotoImage(resizedImg)
            self.win5.imageLabel.config(image=saved_image)
            # Keeping a reference
            self.win5.imageLabel.photo = saved_image
            browse_bt.destroy()
            # tk.Button(win5, text="사진 선택", command=lambda:[self.server.sendImages(frame),attach_photo(),win5.withdraw(),open_win6()]).grid(row=9,column=3)
            tk.Button(self.win5, text="사진 선택", command=lambda:[attach_photo(self.bucket,self.user_info["name"],image),self.open_win6(),self.win6.tkraise(),self.img_thread(frame)]).place(x=350,y=580,width=100,height=40)

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
    
    
    
    def open_win6(self):
        global img_list9,button_list9,button_dict9,img_list15,button_list15,button_dict15

        self.num9=2
        self.num15=2
        button_dict9 = {}
        button_dict15 = {}

        self.win6 = tk.Frame(self, relief="flat",bg="white")
        self.win6.place(x=0,y=0,width=800,height=1280)
        self.win6.bind("<Escape>", self.on_escape)
        
        ##cmd 실행 안됨!!!!!!!
        def personal_cmd():
            selected_image = var.get()
            if selected_image == 1:
                # 첫 번째 이미지에 대한 cmd 명령어 실행
                print("봄웜")
            elif selected_image == 2:
                # 두 번째 이미지에 대한 cmd 명령어 실행
                print("여쿨")
            elif selected_image == 3:
                # 세 번째 이미지에 대한 cmd 명령어 실행
                print("갈웜")
            elif selected_image == 4:
                # 네 번째 이미지에 대한 cmd 명령어 실행
                print("겨쿨")

        # 배경 이미지 파일 경로
        backgrounds = ["UI/spring.png", "UI/summer.png", "UI/autumn.png", "UI/winter.png"]
        # 전경 이미지 파일 경로
        foreground = Image.open("UI/test.png")  ##이미지 받아오기!!!
        # 배경 이미지를 원하는 크기로 조정
        labels = []
        background_images = []
        for bg_path in backgrounds:
            background = Image.open(bg_path)
            resized_background = background.resize((80, 96))
            background_images.append(resized_background)

        def progress_bar():
            frame_progress = tk.LabelFrame(self.win6, text="진행상황")
            frame_progress.grid(row=18, column=1, sticky="ew", padx=10, pady=10,columnspan=6)
            p_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
            progress_bar.pack(fill="x", padx=5, pady=5, ipady=5)

            for i in range(100):
                time.sleep(0.005)
                p_var.set(i)
                progress_bar.update()
            self.win6.after(100,lambda:[frame_progress.grid_remove(),progress_bar.pack_forget(),self.open_win11(),self.win11.tkraise()])
        
        def toggle_border9(button):
            global num9,button_dict9
            if button.cget("relief") == "solid":
                button.config(relief="flat", highlightthickness=0)
                button_dict9 = {}
            else:
                if bool(button_dict9):
                    int_keys = [k for k in button_dict9.keys() if isinstance(k, int)]
                    button_dict9[int_keys[0]].config(relief="flat", highlightthickness=0)         
                    button_dict9 = {}
                button.config(relief="solid", highlightthickness=2, highlightbackground="red")
                button_dict9[num9] = button

        def forward_image9():
            global num9,button_dict9
            num9 = num9 - 1
            for j in range(4):
                idx = num9 * 4 + j
                if (idx>=0 and idx < len(img_list9) and idx < len(img_name9)):
                    button_list9[1][j].configure(image=img_list9[idx], relief="flat", highlightthickness=0)
                    name_list9[1][j].configure(text=img_name9[idx])
            if num9 in button_dict9.keys():           
                button_dict9[num9].config(relief="solid", highlightthickness=2, highlightbackground="red")

        def next_image9():
            global num9,button_dict9
            num9 = num9 + 1
            for j in range(4):
                idx = num9 * 4 + j
                if (idx>=0 and idx < len(img_list9) and idx < len(img_name9)):
                    button_list9[1][j].configure(image=img_list9[idx], relief="flat", highlightthickness=0)
                    name_list9[1][j].configure(text=img_name9[idx])

            if num9 in button_dict9.keys():           
                button_dict9[num9].config(relief="solid", highlightthickness=2, highlightbackground="red")

        def toggle_border15(button):
            global num15,button_dict15
            if button.cget("relief") == "solid":
                button.config(relief="flat", highlightthickness=0)
                button_dict15 = {}
            else:
                if bool(button_dict15):
                    int_keys = [k for k in button_dict15.keys() if isinstance(k, int)]
                    button_dict15[int_keys[0]].config(relief="flat", highlightthickness=0)         
                    button_dict15 = {}
                button.config(relief="solid", highlightthickness=2, highlightbackground="red")
                button_dict15[num15] = button
            
        def forward_image15():
            global num15,button_dict15
            num15 = num15 - 1
            for j in range(4):
                idx = num15 * 4 + j
                if (idx>=0 and idx < len(img_list15) and idx < len(img_name15)):
                    button_list15[1][j].configure(image=img_list15[idx], relief="flat", highlightthickness=0)
                    name_list15[1][j].configure(text=img_name15[idx])

            if num15 in button_dict15.keys():           
                button_dict15[num15].config(relief="solid", highlightthickness=2, highlightbackground="red")
                
        def next_image15():
            global num15,button_dict15
            num15 = num15 + 1
            for j in range(4):
                idx = num15 * 4 + j
                if (idx>=0 and idx < len(img_list15) and idx < len(img_name15)):
                    button_list15[1][j].configure(image=img_list15[idx], relief="flat", highlightthickness=0)
                    name_list15[1][j].configure(text=img_name15[idx])
            if num15 in button_dict15.keys():           
                button_dict15[num15].config(relief="solid", highlightthickness=2, highlightbackground="red")

        tk.Button(self.win6, text="뒤로가기", command=lambda:[self.win5.tkraise()]).grid(row=0, column=6)
        tk.Button(self.win6, text="헤어스타일 선택", command=progress_bar).grid(row=17, column=3)
        tk.Button(self.win6, text="◀", command=forward_image9).grid(row=9, column=1)
        tk.Button(self.win6, text="▶", command=next_image9).grid(row=9, column=6)
        tk.Button(self.win6, text="◀", command=forward_image15).grid(row=15, column=1)
        tk.Button(self.win6, text="▶", command=next_image15).grid(row=15, column=6)
        tk.Label(self.win6,text='간소화된 퍼스널컬러 자가진단: 선택 시 추천 컬러가 바뀝니다.',height=1).grid(row=2, column=2,columnspan=3)
        tk.Label(self.win6,text='얼굴형에 따른 추천 헤어스타일',height=1).grid(row=5, column=2,columnspan=3)
        tk.Label(self.win6,text='전체 헤어스타일',height=1).grid(row=8, column=3)
        tk.Label(self.win6,text='퍼스널컬러에 따른 추천 염색 컬러',height=1).grid(row=11, column=2, columnspan=3)
        tk.Label(self.win6,text='전체 염색 컬러',height=1).grid(row=14, column=3)

        var=IntVar()
        var.set(1)
        # 전경 이미지를 윈도우 크기로 조정
        resized_foreground = foreground.resize((80, 96))

        for i, background_image in enumerate(background_images):
            composite_image = Image.alpha_composite(background_image, resized_foreground)
            # ImageTk 객체 생성
            photo = ImageTk.PhotoImage(composite_image)
            # 합성 이미지를 표시할 라벨 생성
            label = tk.Label(self.win6, image=photo)
            label.grid(row=3, column=i+2)
            # 라벨을 리스트에 추가
            labels.append(label)
            # ImageTk 객체에 대한 참조 유지
            label.image = photo
            image_name = backgrounds[i].split(".")[0]  # 이미지 파일 이름 (확장자 제외)
            name_label = tk.Radiobutton(self.win6, text=image_name,variable=var, value=i+1,command=personal_cmd)
            name_label.grid(row=4, column=i+2)

        if self.user_info["gender"]=='여자':
            dir_path9 = "UI/hairstyles"
        elif self.user_info["gender"]=='남자':
            dir_path9 = "UI/hairstyles_men"
        dir_path15="UI/colors"
        img_path9 = [os.path.join(dir_path9, f) for f in os.listdir(dir_path9) if f.endswith(".png")]
        img_path15 = [os.path.join(dir_path15, f) for f in os.listdir(dir_path15) if f.endswith(".png")]
        img_size = (80, 80)

        # 이미지 로드 및 크기 조정
        img_list9 = []
        img_name9=[]
        for i, path in enumerate(img_path9):
            img = Image.open(path)
            img = img.resize(img_size)
            img_list9.append(ImageTk.PhotoImage(img))
            img_name9.append(img_path9[i].split('/')[-1].split('.')[0])  # 경로에서 마지막 부분(파일 이름) 추출
            
        # 이미지를 표시할 버튼 생성
        button_list9 = []
        name_list9=[]
        for i in range(2):
            row_list = []
            row_list2=[]
            for j in range(4):
                button = tk.Button(self.win6, image=None)
                button.grid(row=3*i+6, column=j+2, padx=5)  # 추가 간격 설정
                row_list.append(button)
                label=tk.Label(self.win6,text='')
                label.grid(row=3*i+7, column=j+2, padx=5)
                row_list2.append(label)
            button_list9.append(row_list)
            name_list9.append(row_list2)

        # 이미지를 버튼에 할당
        for i in range(2):
            for j in range(4):
                idx = i * 4 + j
                if idx < len(img_list9):
                    button_list9[i][j].configure(image=img_list9[idx],command=lambda i=i, j=j: toggle_border9(button_list9[i][j]))
                    name_list9[i][j].configure(text=img_name9[idx])
        
        # 이미지 로드 및 크기 조정
        img_list15 = []
        img_name15=[]
        for i,path in enumerate(img_path15):
            img = Image.open(path)
            img = img.resize(img_size)
            img_list15.append(ImageTk.PhotoImage(img))
            img_name15.append(img_path15[i].split('/')[-1].split('.')[0])  # 경로에서 마지막 부분(파일 이름) 추출print(img)

        # 이미지를 표시할 버튼 생성
        button_list15 = []
        name_list15=[]
        for i in range(2):
            row_list = []
            row_list2=[]
            for j in range(4):
                button = tk.Button(self.win6, image=None)
                button.grid(row=3*i+12, column=j+2, padx=5)  # 추가 간격 설정
                row_list.append(button)
                label=tk.Label(self.win6,text='')
                label.grid(row=3*i+13, column=j+2, padx=5)
                row_list2.append(label)
            button_list15.append(row_list)
            name_list15.append(row_list2)

        # 이미지를 버튼에 할당
        for i in range(2):
            for j in range(4):
                idx = i * 4 + j
                if idx < len(img_list15):
                    button_list15[i][j].configure(image=img_list15[idx],command=lambda i=i, j=j: toggle_border15(button_list15[i][j]))
                    name_list15[i][j].configure(text=img_name15[idx])


    def open_win11(self):
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
        tk.Button(self.win11, text="예약하기", command=lambda:[self.win12.tkraise()]).grid(row=5,column=1)
        
    #12. 예약하기/ 디자이너 사진 + 스케줄, 완료 버튼
    def open_win12(self):
        self.win12 = tk.Frame(self, relief="flat",bg="white")
        self.win12.place(x=0,y=0,width=800,height=1280)
        self.win12.bind("<Escape>", self.on_escape)
        self.reservation_buttons = []
        class designer():
            def __init__(self,name,win,y):
                self.name=name
                self.reservation_buttons = list()
                self.frame1 = tk.LabelFrame(win, text=name, width=200, height=200)
                self.frame1.place(x=75, y=y)
                self.frame2 = tk.Frame(win, width=400, height=200)
                self.frame2.place(x=300, y=y)
           
            def toggle_reservation(self,index):
                # 버튼의 선택 상태를 변경하는 함수
                if self.reservation_buttons[index]["relief"] == "sunken":
                    self.reservation_buttons[index]["relief"] = "raised"
                else:
                    self.reservation_buttons[index]["relief"] = "sunken"    
            
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
                    if time in saved_times:
                        btn_state = tk.DISABLED
                
                    row = index // 4  # 버튼이 배치될 행 인덱스
                    col = index % 4  # 버튼이 배치될 열 인덱스
                    
                    btn = tk.Button(self.frame2, text=time, state=btn_state, command=lambda i=index: self.toggle_reservation(i))
                    btn.grid(row=row, column=col, padx=10, pady=30)
                    self.reservation_buttons.append(btn) 
       
        times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]  # 예약 가능한 시간 리스트
        
        def make_reservation(designer_list):
                # 예약 정보 저장 및 Firestore에 전달하는 함수
                reservation_time = []
                for designer in designer_list:
                    for index, btn in enumerate(designer.reservation_buttons):
                        if btn["relief"] == "sunken":
                            reservation_time.append(times[index])   
                    # 예약 정보와 기타 필요한 정보를 수집하여 Firestore에 저장
                    data = {
                        "reservation_time": reservation_time,
                        # 추가 필드 필요시 여기에 정보 입력
                    }
                    # Firestore에 예약 정보 저장
                    hairdresser_ref = self.db.collection("hairdresser").document(designer.name)
                    hairdresser_ref.set(data)
                print("예약이 완료되었습니다.")   
                
        def download_image(filename):
            bucket = storage.bucket()
            blob = bucket.blob("stylist/" + filename)
            image_path = "temp.jpg"  # 다운로드 받은 이미지를 임시로 저장할 경로
            blob.download_to_filename(image_path)
            return image_path
        
        def show_image(frame, filename):
            # 이미지를 다운로드하여 해당 프레임에 출력하는 함수
            image_path = download_image(filename)
            img = Image.open(image_path)
            img = img.resize((132, 170), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=img_tk)
            label.image = img_tk
            label.pack()
            
        
        # 페이지 스타트 
        # button_back = tk.Button(self.win12, text="뒤로가기", command=self.BaroGoback())
        button_back = tk.Button(self.win12, text="뒤로가기", command=lambda:[self.win4.tkraise()])
        button_back.configure(font=(20))
        button_back.place(x=670, y=10)
        
        designer1 = designer("김이발",self.win12, y=75)
        filename1 = "이승현님 여권 .jpg"
        show_image(designer1.frame1, filename1)  
        designer1.read_reservation(self.db)

        designer2 = designer("최이발", self.win12, y=300)
        filename2 = "이승현님 여권 .jpg"
        show_image(designer2.frame1, filename2)
        designer2.read_reservation(self.db)
        
        designer3 = designer("동이발", self.win12, y=525)
        filename3 = "이승현님 여권 .jpg"
        show_image(designer3.frame1, filename3)
        designer3.read_reservation(self.db)
        
        # open_win 함수에서 커스터마이징가능하게 만들어야함
        self.designer_list = [designer1,designer2,designer3]
        # 예약하기 버튼 생성
        tk.Button(self.win12, text="예약하기", command=lambda:[make_reservation(self.designer_list), self.open_win13(),self.win13.tkraise()]).place(x=375, y=750)

    def BaroGoback(self):
        # print(self.isBaro)
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




#7. 헤어스타일 선택
# 범위 벗어난 인덱스에 대한 오류 처리 x
# button_dict9 = {}
# num9=2
# button_dict15 = {}
# num15=2
# m='여자'

    

# #11. 결과 출력/ 다시 찍기(-> #5), 헤어스타일 재선택(-> #7), 예약하기(-> #12) 버튼

# # Creating tkinter variables

# close window with key `ESC`

if __name__ == "__main__":
    UI = MainUI()
