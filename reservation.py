

import tkinter as tk

def button_click(number):
    reservation = []   #지역변수 초기화
    # db에서 받아온 디자이너의 예약된 리스트 designer_res[]
    designer_res = [11, 13] #임의 지정
    for i in range(len(designer_res)):
        reservation.append(designer_res[i]) #비교를 위한 reservation에 예약된 시간 추가
    input_int = int(number) #시간 버튼을 누르면 int타입으로 받아서 input_int변수로 저장
    print(reservation)

    for i in reservation :
        if input_int not in reservation: #예약 가능한 시간이면 designer_res에 갱신
            designer_res.append(input_int)
            break
        
        else: #이미 예약된 시간일 경우
            print("이미 예약된 시간입니다.")

    #designer_res리스트 db갱신(승현이가 해줘)
    print(designer_res)
    

root = tk.Tk()

button1 = tk.Button(root, text="10", command=lambda: button_click(10))
button1.pack()

button2 = tk.Button(root, text="11", command=lambda: button_click(11))
button2.pack()

button3 = tk.Button(root, text="12", command=lambda: button_click(12))
button3.pack()

button4 = tk.Button(root, text="13", command=lambda: button_click(13))
button4.pack()

button5 = tk.Button(root, text="14", command=lambda: button_click(14))
button5.pack()

root.mainloop()


# doc_ref = db.collection('Designers').document(name)
#             doc_ref.set({
#                 'name': name,
#                 'reservation': time,
#             })