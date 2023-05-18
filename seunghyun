import tkinter as tk
from tkinter import filedialog
from firebase_admin import credentials, firestore, initialize_app, storage
from PIL import Image

# Firebase 초기화
cred = credentials.Certificate('./easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
firebase_app = initialize_app(cred, {
    'storageBucket': 'easylogin-58c28.appspot.com'
})
db = firestore.client()

# GUI 생성
window = tk.Tk()
window.title("고객 정보 관리")

# 고객 정보 입력 필드
name_label = tk.Label(window, text="이름:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

id_label = tk.Label(window, text="아이디:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.pack()

password_label = tk.Label(window, text="비밀번호:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# 고객 정보 저장 함수
def save_customer_info():
    name = name_entry.get()
    id = id_entry.get()
    password = password_entry.get()

    if name and id and password:
        # Firebase에 고객 정보 저장
        doc_ref = db.collection('customers').document(id)
        doc_ref.set({
            'name': name,
            'id': id,
            'password': password
        })
        # 저장 후 필드 초기화
        name_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        print("고객 정보가 성공적으로 저장되었습니다.")
    else:
        print("모든 필드를 입력해주세요.")
        
# 고객 정보 읽기 함수
def read_customer_info():
    id = id_entry.get()
    if id:
        # Firebase에서 고객 정보 읽기
        doc_ref = db.collection('customers').document(id)
        doc = doc_ref.get()
        if doc.exists:
            customer_data = doc.to_dict()
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, customer_data['name'])
            password_entry.delete(0, tk.END)
            password_entry.insert(tk.END, customer_data['password'])
            print("고객 정보를 성공적으로 불러왔습니다.")
        else:
            print("해당 아이디의 고객 정보가 존재하지 않습니다.")
    else:
        print("아이디를 입력해주세요.")

# 사진 첨부 함수
def attach_photo():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        # 이미지를 Firebase Storage에 업로드
        bucket = storage.bucket(app=firebase_app)
        blob = bucket.blob('customers/{0}_photo.jpg'.format(name_entry.get()))
        blob.upload_from_filename(file_path)
        print("사진이 성공적으로 첨부되었습니다.")
    else:
        print("파일 선택이 취소되었습니다.")

# 사진 첨부 버튼
attach_button = tk.Button(window, text="사진 첨부", command=attach_photo)
attach_button.pack()

# 저장 버튼
save_button = tk.Button(window, text="저장", command=save_customer_info)
save_button.pack()

# # 읽기 버튼
# read_button = tk.Button(window, text="읽기", command=read_customer_info)
# read_button.pack()

# GUI 실행
window.mainloop()
