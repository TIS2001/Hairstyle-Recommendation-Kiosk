import tkinter as tk
from firebase_admin import credentials, firestore, initialize_app
from tkinter import messagebox

# Firebase 초기화
cred = credentials.Certificate('./easylogin-58c28-firebase-adminsdk-lz9v2-4c02999507.json')
firebase_app = initialize_app(cred, {
    'databaseURL': 'https://easylogin-58c28.firebaseio.com'
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
                # 로그인 성공 후 수행할 작업 추가
            else:
                messagebox.showerror("로그인 실패", "비밀번호가 일치하지 않습니다.")
        else:
            messagebox.showerror("로그인 실패", "해당 아이디가 존재하지 않습니다.")
    else:
        messagebox.showwarning("경고", "아이디와 비밀번호를 입력해주세요.")

# 로그인 버튼
login_button = tk.Button(window, text="로그인", command=login)
login_button.pack()

# GUI 실행
window.mainloop()
