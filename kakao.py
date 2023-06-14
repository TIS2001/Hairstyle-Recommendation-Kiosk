from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from PIL import Image
import time
import configparser
import urllib
from selenium.webdriver.chrome.service import Service


#if ~ 예약이 완료되면:
#알리기
Config = configparser.ConfigParser()

#카카오 아이디, 비번 불러오기
Config.read('./info.conf')
Config = Config['MAIN']

#아이디, 비번
id = Config['kakaoid']
pw = Config['kakaopw']

#카카오메인페이지 지정
KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'

# 미용사에 따라 채팅룸 링크 지정
ChatRoom_LGE = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876826696105085'
ChatRoom_LSH = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876819996735611'
ChatRoom_SDJ = 'https://center-pf.kakao.com/_xgyjyxj/chats/4876819676480609'
options = webdriver.ChromeOptions()
service = Service(executable_path=r'/usr/bin/chromedriver')

#user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.95 Safari/537.36")
#창을 띄우지 않고 실행
# options.add_argument("headless")

#크로니움 드라이버 로드
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

#카카오 메인페이지 로드
driver.get(KaKaoURL)
time.sleep(5)

#로그인
idvar = driver.find_element(By.NAME, "loginKey")
idvar.send_keys(id)
pwvar = driver.find_element(By.NAME, "password")
pwvar.send_keys(pw)
time.sleep(3)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(10)
driver.find_element(By.CLASS_NAME, "tit_invite").click()
time.sleep(1)

#채팅방 로드
driver.get(ChatRoom_LSH)
time.sleep(3)


#메시지 작성
driver.find_element(By.ID, 'chatWrite').send_keys('예약 완료')
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼


# driver.find_element(By.CLASS_NAME, "ico_rocket ico_list").click()
# time.sleep(1)
# links = 
# for link in links:
#     if link.text == "채팅 목록":  # 클릭하고자 하는 링크의 텍스트를 기반으로 조건을 설정합니다
#         link.click()
#         break
while True:
    
    #디자이너 승현
    #if      :
    #채팅방 로드
    # driver.get(ChatRoom_LSH)
    # time.sleep(3)
    # #메시지 작성
    # driver.find_element(By.ID, 'chatWrite').send_keys('예약 완료')
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼

    #디자이너 동진
    #elif      :
    #채팅방 로드
    # driver.get(ChatRoom_SDJ)
    # time.sleep(3)
    # #메시지 작성
    # driver.find_element(By.ID, 'chatWrite').send_keys('예약 완료')
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼

    #디자이너 가은
    #elif      :
    #채팅방 로드
    # driver.get(ChatRoom_LGE)
    # time.sleep(3)
    # #메시지 작성
    # driver.find_element(By.ID, 'chatWrite').send_keys('예약 완료')
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()  #전송버튼




    #else:
        time.sleep(1)
    



# driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
# time.sleep(5)




# driver.quit()
