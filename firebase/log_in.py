import tkinter as tk
from firebase_admin import credentials, firestore, initialize_app, storage
from tkinter import messagebox
from PIL import ImageTk, Image

# Firebase 초기화
cred = credentials.Certificate('./easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
firebase_app = initialize_app(cred, {
    'storageBucket': 'easylogin-58c28.appspot.com'
})
db = firestore.client()

# GUI 생성
window = tk.Tk()
window.title("로그인")

# 아이디와 비밀번호 입력 필드
id_label = tk.Label(window, text="아이디:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.pack()

password_label = tk.Label(window, text="비밀번호:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# 로그인 함수
def login():
    id = id_entry.get()
    password = password_entry.get()

    if id and password:
        # Firebase에서 사용자 데이터 조회
        doc_ref = db.collection('customers').document(id)
        doc = doc_ref.get()

        if doc.exists:
            customer_data = doc.to_dict()
            # 비밀번호 일치 확인
            if password == customer_data['password']:
                messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
                # 로그인 성공 후 사용자 사진 표시
                display_customer_photo(id)
            else:
                messagebox.showerror("로그인 실패", "비밀번호가 일치하지 않습니다.")
        else:
            messagebox.showerror("로그인 실패", "해당 아이디가 존재하지 않습니다.")
    else:
        messagebox.showwarning("경고", "아이디와 비밀번호를 입력해주세요.")

# 사용자 사진 표시 함수
def display_customer_photo(id):
    # Firebase Storage에서 사진 다운로드
    bucket = storage.bucket(app=firebase_app)
    blob = bucket.blob('customers/{0}_photo.jpg'.format(id))
    image_path = './temp.jpg'
    blob.download_to_filename(image_path)

    # 이미지 로드 및 표시
    image = Image.open(image_path)
    image = image.resize((200, 200))  # 이미지 크기 조절
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(window, image=photo)
    image_label.image = photo  # 참조 유지
    image_label.pack()

# 로그인 버튼
login_button = tk.Button(window, text="로그인", command=login)
login_button.pack()

# GUI 실행
window.mainloop()
