import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import time
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from utils.img_send import img_send

def on_escape(event=None):
    print("escaped")
    root.destroy()

    def quit(self):
        """Quit the Tcl interpreter. All widgets will be destroyed."""
        self.tk.quit()

#1. 첫번째 페이지- 시작하기
# root = tk.Tk()
# root.title("메인")
# tk.Button(root, text="회원가입하기 또는 로그인하기", command=open_win1).pack(pady=10)

#2. 회원가입, 로그인 버튼
def open_win1():
    global win1
    win1 = tk.Toplevel()
    win1.geometry("600x960")
    win1.title("횐가입/로긴")
    win1.bind("<Escape>", on_escape)
    tk.Button(win1, text="뒤로가기", command=lambda:[win1.destroy(),root.deiconify()]).pack(padx=10,pady=10, side="top", anchor="ne")
    tk.Button(win1, text="회원가입하기", width=15, height=5, command=lambda:[win1.withdraw(),open_win2()]).pack(pady=10)
    tk.Button(win1, text="로그인하기", width=15, height=5, command=lambda:[win1.withdraw(),open_win3()]).pack(pady=10)
    
#3-1. 회원가입 페이지
def open_win2():
    global win2
    var =IntVar()
    cb = IntVar()
    def selection():
        global m
        choice = var.get()
        if choice == 1:
            m = '남자'
        elif choice == 2:
            m = '여자'
        return m

    def submit():
        global name
        try:
            name = name_Tf.get()
            m = selection()
            return messagebox.showinfo('PythonGuides', f'{m} {name}, 회원가입이 완료되었습니다.')
        except Exception as ep:
            return messagebox.showwarning('PythonGuides', 'Please provide valid input')

    def termsCheck():
        if cb.get() == 1:
            submit_btn['state'] = NORMAL
        else:
            submit_btn['state'] = DISABLED

    win2 =tk.Toplevel()
    win2.geometry("600x960")
    win2.title('sign up')
    win2.bind("<Escape>", on_escape)
    frame1 = Label(win2, bg='#dddddd')
    frame1.pack()
    frame2 = LabelFrame(frame1, text='Gender', padx=30, pady=10)

    var =IntVar()
    cb = IntVar()

    tk.Button(win2, text="뒤로가기", command=lambda:[win2.destroy(),win1.deiconify()]).pack(padx=10,pady=10, side="top", anchor="ne")
    Label(frame1, text='이름').grid(row=0, column=0, padx=5, pady=5)
    Label(frame1, text='전화번호').grid(row=1, column=0, padx=5, pady=5)
    Label(frame1, text='비밀번호').grid(row=2, column=0, padx=5, pady=5)
    Radiobutton(frame2, text='남자', variable=var, value=1,command=selection).pack()
    Radiobutton(frame2, text='여자', variable=var, value=2,command=selection).pack(anchor=W)
    name_Tf = Entry(frame1)
    name_Tf.grid(row=0, column=2)
    Entry(frame1).grid(row=1, column=2)
    Entry(frame1, show="*").grid(row=2, column=2)
    frame2.grid(row=3, columnspan=3,padx=30)
    Checkbutton(frame1, text='Accept the terms & conditions', variable=cb, onvalue=1, offvalue=0,command=termsCheck).grid(row=4, columnspan=4, pady=5)
    submit_btn = Button(frame1, text="Submit", command=lambda:[submit(),open_win1(),win2.withdraw()], padx=50, pady=5, state=DISABLED)
    submit_btn.grid(row=5, columnspan=4, pady=2)

#3-2. 로그인 페이지
def open_win3():
    global win3
    win3 = tk.Toplevel()
    win3.geometry("600x960")
    win3.title("로그인")
    win3.bind("<Escape>", on_escape)
    frame1 = Frame(win3)
    frame1.pack()
    Label(frame1, text='전화번호 뒤 네자리').grid(row=1, column=0, padx=5, pady=5)
    Label(frame1, text='비밀번호').grid(row=2, column=0, padx=5, pady=5)
    Entry(frame1).grid(row=1, column=1)
    Entry(frame1, show="*").grid(row=2, column=1)
    Button(frame1, text="뒤로가기", command=lambda:[win3.destroy(),win1.deiconify()]).grid(row=0, column=2, padx=10, pady=10, sticky="ne")
    Button(frame1, text="로그인", command=lambda:[win3.withdraw(),open_win4()]).grid(row=3, columnspan=3, padx=10, pady=10, sticky="s")


#4. 카메라 실행/ 예약(-> #12), 헤어스타일 선택(-> #5) 버튼
def open_win4():
    global win4
    global isBaro
    isBaro=False
    win4 = tk.Toplevel()
    win4.geometry("600x960")
    win4.title("카메라")
    win4.bind("<Escape>", on_escape)
    tk.Button(win4, text="뒤로가기", command=lambda:[win4.destroy(),win3.deiconify()]).pack(padx=10,pady=10, side="top", anchor="ne")
    tk.Button(win4, text="바로 예약하기", command=lambda:[baro(),win4.withdraw(),open_win12()]).pack(side="left", padx=20,pady=10)
    tk.Button(win4, text="헤어스타일 합성", command=lambda:[win4.withdraw(),open_win5()]).pack(side="right", padx=20, pady=10)

# 바로 예약
def baro():
    global isBaro
    isBaro=True 
    
#5. 사진 촬영(5초 타이머) or 사진 가져오기(-> 팝업창)
def open_win5():
    global win5
    win5 = tk.Toplevel()
    win5.geometry("600x960")
    win5.title("사진 촬영")
    #뒤로 갔다가 돌아오면 웹캠 안뜨는 오류 해결 못함
    tk.Button(win5, text="뒤로가기", command=lambda:[win5.destroy(),win4.deiconify()]).grid(row=1,column=3)
    tk.Button(win5, text="사진 가져오기", command=lambda:[imageBrowse()]).grid(row=7,column=3)
    tk.Button(win5, text="사진 촬영", command=lambda:[Capture()]).grid(row=8,column=3)
    win5.cameraLabel = Label(win5, bg="steelblue", borderwidth=3, relief="groove")
    win5.cameraLabel.grid(row=3,column=2, padx=10, pady=10, columnspan=2)
    win5.imageLabel = Label(win5, bg="steelblue", borderwidth=3, relief="groove")
    win5.imageLabel.grid(row=6,column=2, padx=10, pady=10, columnspan=2)
    # Creating object of class VideoCapture with webcam index
    win5.cap = cv2.VideoCapture(0)

    # Setting width and height
    width, height =320, 240
    win5.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    win5.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    win5.bind("<Escape>", on_escape)

    ShowFeed()

def ShowFeed():
    # Capturing frame by frame
    ret, frame = win5.cap.read()
    # print(ret)
    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)
        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)
        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image = videoImg)
        # Configuring the label to display the frame
        win5.cameraLabel.configure(image=imgtk)
        # Keeping a reference
        win5.cameraLabel.imgtk = imgtk
        # Calling the function after 10 milliseconds
        win5.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        win5.cameraLabel.configure(image='')


# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture():
    destD="/home/lee/4-1/EMB/project_UI/photos"
    destPath.set(destD)
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    # print("dest path: "+destPath.get())
    # If the user has selected the destination directory, then get the directory and save it in image_path
    if destPath.get() != '':
        image_path = destPath.get()
    # If the user has not selected any destination directory, then set the image_path to default directory
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")
    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"
    imagePath.set(imgName)
    # Capturing the frame
    ret,frame = win5.cap.read()
    # Displaying date and time on the frame
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)    
    img_send(frame)
    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)
    saved_image_array = saved_image
    
    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)
    # Configuring the label to display the frame
    win5.imageLabel.config(image=saved_image)
    # Keeping a reference
    win5.imageLabel.photo = saved_image
    # Displaying messagebox
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)
    tk.Button(win5, text="다시 찍기", command=Capture).grid(row=8,column=3)    
    tk.Button(win5, text="사진 선택", command=lambda:[win5.withdraw(),open_win6()]).grid(row=9,column=3)


def imageBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
    # Displaying the directory in the directory textbox
    imagePath.set(openDirectory)
    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(openDirectory)
    # Resizing the image using Image.resize()
    imageResize = imageView.resize((320, 240), resample=Image.LANCZOS)
    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)
    # Configuring the label to display the frame
    win5.imageLabel.config(image=imageDisplay)
    # Keeping a reference
    win5.imageLabel.photo = imageDisplay
    tk.Button(win5, text="사진 선택", command=lambda:[win5.withdraw(),open_win6()]).grid(row=9,column=3)

#7. 헤어스타일 선택
# 범위 벗어난 인덱스에 대한 오류 처리 x
button_dict9 = {}
num9=2
button_dict15 = {}
num15=2
m='여자'
def open_win6():
    global win6,img_list9,button_list9,button_dict9,img_list15,button_list15,button_dict15,m
    button_dict9 = {}
    button_dict15 = {}
    win6 = tk.Toplevel()
    win6.geometry("600x960")
    win6.title("헤어스타일 선택")
    win6.bind("<Escape>", on_escape)
    
    #cmd 실행 안됨!!!!!!!
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
    backgrounds = ["spring.png", "summer.png", "autumn.png", "winter.png"]
    # 전경 이미지 파일 경로
    foreground = Image.open("test.png")
    # 배경 이미지를 원하는 크기로 조정
    labels = []
    background_images = []
    for bg_path in backgrounds:
        background = Image.open(bg_path)
        resized_background = background.resize((100, 120))
        background_images.append(resized_background)

    def progress_bar():
        frame_progress = tk.LabelFrame(win6, text="진행상황")
        frame_progress.grid(row=18, column=1, sticky="ew", padx=10, pady=10,columnspan=6)
        p_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
        progress_bar.pack(fill="x", padx=5, pady=5, ipady=5)

        for i in range(100):
            time.sleep(0.005)
            p_var.set(i)
            progress_bar.update()
        win6.after(100,lambda:[frame_progress.grid_remove(),progress_bar.pack_forget(),win6.withdraw(),open_win11()])
    
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

    tk.Button(win6, text="뒤로가기", command=lambda:[win6.destroy(),win5.deiconify()]).grid(row=0, column=6)
    tk.Button(win6, text="헤어스타일 선택", command=progress_bar).grid(row=17, column=3)
    tk.Button(win6, text="◀", command=forward_image9).grid(row=9, column=1)
    tk.Button(win6, text="▶", command=next_image9).grid(row=9, column=6)
    tk.Button(win6, text="◀", command=forward_image15).grid(row=15, column=1)
    tk.Button(win6, text="▶", command=next_image15).grid(row=15, column=6)
    tk.Label(win6,text='간소화된 퍼스널컬러 자가진단: 선택 시 추천 컬러가 바뀝니다.').grid(row=2, column=2,columnspan=3)
    tk.Label(win6,text='얼굴형에 따른 추천 헤어스타일').grid(row=5, column=2,columnspan=3)
    tk.Label(win6,text='전체 헤어스타일').grid(row=8, column=3)
    tk.Label(win6,text='퍼스널컬러에 따른 추천 염색 컬러').grid(row=11, column=2, columnspan=3)
    tk.Label(win6,text='전체 염색 컬러').grid(row=14, column=3)

    var=IntVar()
    var.set(1)
    # 전경 이미지를 윈도우 크기로 조정
    resized_foreground = foreground.resize((100, 120))

    for i, background_image in enumerate(background_images):
        composite_image = Image.alpha_composite(background_image, resized_foreground)
        # ImageTk 객체 생성
        photo = ImageTk.PhotoImage(composite_image)
        # 합성 이미지를 표시할 라벨 생성
        label = tk.Label(win6, image=photo)
        label.grid(row=3, column=i+2)
        # 라벨을 리스트에 추가
        labels.append(label)
        # ImageTk 객체에 대한 참조 유지
        label.image = photo
        image_name = backgrounds[i].split(".")[0]  # 이미지 파일 이름 (확장자 제외)
        name_label = tk.Radiobutton(win6, text=image_name,variable=var, value=i,command=personal_cmd())
        name_label.grid(row=4, column=i+2)

    if m=='여자':
        dir_path9 = "hairstyles"
    elif m=='남자':
        dir_path9 = "hairstyles_men"
    dir_path15="colors"
    img_path9 = [os.path.join(dir_path9, f) for f in os.listdir(dir_path9) if f.endswith(".png")]
    img_path15 = [os.path.join(dir_path15, f) for f in os.listdir(dir_path15) if f.endswith(".png")]
    img_size = (100, 100)

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
            button = tk.Button(win6, image=None)
            button.grid(row=3*i+6, column=j+2, padx=5, pady=5)  # 추가 간격 설정
            row_list.append(button)
            label=tk.Label(win6,text='')
            label.grid(row=3*i+7, column=j+2, padx=5, pady=5)
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
            button = tk.Button(win6, image=None)
            button.grid(row=3*i+12, column=j+2, padx=5, pady=5)  # 추가 간격 설정
            row_list.append(button)
            label=tk.Label(win6,text='')
            label.grid(row=3*i+13, column=j+2, padx=5, pady=5)
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

#11. 결과 출력/ 다시 찍기(-> #5), 헤어스타일 재선택(-> #7), 예약하기(-> #12) 버튼
def open_win11():
    global win11
    win11 = tk.Toplevel()
    win11.geometry("600x960")
    win11.title("결과")
    win11.bind("<Escape>", on_escape)
    result_path="./result/result.jpg"
    if os.path.exists(result_path):
        result_img = Image.open(result_path)
        result_img = result_img.resize((320,240))  # 이미지 크기 조절        
        photo = ImageTk.PhotoImage(result_img)
        label = tk.Label(win11, image=photo)
        label.image = photo  # 이미지 객체 유지
        label.grid(row=2, column=1)
    else:
        print("이미지 파일이 존재하지 않습니다.")

    tk.Button(win11, text="뒤로가기", command=lambda:[win11.destroy(),win6.deiconify()]).grid(row=0,column=3)
    tk.Button(win11, text="다시 찍기", command=lambda:[win11.withdraw(),win5.deiconify()]).grid(row=3,column=1)
    tk.Button(win11, text="헤어스타일 재선택", command=lambda:[win11.withdraw(),win6.deiconify()]).grid(row=4,column=1)
    tk.Button(win11, text="예약하기", command=lambda:[win11.withdraw(),open_win12()]).grid(row=5,column=1)
    tk.Button(win11, text="뒤로가기", command=lambda:[win11.destroy(),win6.deiconify()]).grid(row=1,column=3)
    tk.Button(win11, text="다시 찍기", command=lambda:[win11.withdraw(),win5.deiconify()]).grid(row=3,column=2)
    tk.Button(win11, text="헤어스타일 재선택", command=lambda:[win11.withdraw(),win6.deiconify()]).grid(row=4,column=2)
    tk.Button(win11, text="예약하기", command=lambda:[win11.withdraw(),open_win12()]).grid(row=5,column=2)

#12. 예약하기/ 디자이너 사진 + 스케줄, 완료 버튼
def open_win12():
    global win12
    win12 = tk.Toplevel()
    win12.geometry("600x960")
    win12.title("예약")
    win12.bind("<Escape>", on_escape)

    tk.Button(win12, text="뒤로가기", command=BaroGoback()).pack(pady=10)
    tk.Button(win12, text="예약하기", command=lambda:[win12.withdraw(),open_win13()]).pack(pady=10)

def BaroGoback():
    # print(isBaro)
    if(isBaro==True):
        # print("뒤로가기")
        return lambda:[win12.destroy(),win4.deiconify()]
    else:
        return lambda:[win12.destroy(),win11.deiconify()]

#13. 예약 완료 텍스트 or 확인 팝업창
def open_win13():
    global win13
    win13 = tk.Toplevel()
    win13.geometry("600x960")
    win13.title("완료")
    win13.bind("<Escape>", on_escape)
    tk.Label(win13, text=name + "님 예약이 완료되었습니다.").pack(pady=10)

root = tk.Tk()
root.geometry("600x960")
root.title("메인")
tk.Button(root, text="시작하기", width=16, height=7, command=lambda:[root.withdraw(),open_win1()]).pack(anchor="center",pady=200)

# Creating tkinter variables
destPath = StringVar()
destP=StringVar()
imagePath = StringVar()

# close window with key `ESC`
root.bind("<Escape>", on_escape)

root.mainloop()
