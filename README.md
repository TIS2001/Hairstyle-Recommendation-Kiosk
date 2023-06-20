# 2023ESE - 머리문제가 아니조
UOS_MIE Embedded Project<br/>


라즈베리파이를 활용한 미용실 전용 키오스크 **'프린세스 메이커'** 제작

# 프로젝트 개요
## 프로젝트 요약
사용자에게 헤어스타일을 추천해주고 미리 체험 가능한 미용실에서 사용할 수 있는 키오스크인 '프린세스 메이커'를 제작한다. 프린세스메이커는 연결된 카메라를 통해 사용자 얼굴을 인식하고 AI모델이 사용자의 얼굴형을 판단하여 얼굴형에 따라 맞춤 헤어스타일을 추천해주는 역할을 한다. 또한 사용자가 터치스크린을 통해 헤어스타일을 선택하면 이를 AI모델이 사용자의 얼굴과 자연스럽게 합성하여 미리 결과물을 볼 수 있게 화면에 표시하여 사용자의 헤어스타일 선택에 도움을 준다. 이후에는 예약 가능한 시간에 디자이너를 정하여 예약을 할 수 있고 예약이 완료되면 디자이너에게 카카오톡으로 예약 내역을 전송하여 사용자와 디자이너에게 간편하게 예약 시스템을 제공한다.

## 전체 시나리오
![시나리오](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/bc31a450-9591-4e4d-bc31-95f971a2c281)
![목적계통도](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/fc7aa11b-20c1-4194-ab92-71a94cfd558e)

# 구현 내용
## 하드웨어 설계 및 UI 화면 구성
### 키오스크 하우징
25.6cm * 16.8cm의 키오스크 모니터를 보호, 지지해주기 위해 키오스크의 하우징은 총 크기를 35cm * 20cm로 설계하였고, 전면부 2개, 후면부 2개 총 4개의 part로 나누어서 설계했다. 

나누어진 총 4개의 part는 아래와 같다. <br/>
![338px-2023_hk_ft](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/35af277f-4760-4e1f-806a-9874440c90b1)
![270px-2023_hk_fb](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/a2ed476f-62c8-4186-b6e1-4695d7526f19)
![270px-2023_hk_bt](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/2ffef8b8-de86-42eb-8b6c-956dabe5ed8b)
![338px-2023_hk_bb](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/90cb16f9-1989-4ff8-933c-42ce36c9f63a)


위의 part들을 각각 출력하여 완성된 키오스크의 모습은 아래와 같다.

![413px-2023_hk_front](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/0e200d0d-4392-4083-87f2-cc1fca95a02b)
![272px-2023_hk_side](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/1a87a251-0a3f-4456-9e4b-04682b291118)

## UI 화면 구성
main 내에서 MainUI 클래스를 호출하여 UI 인스턴스를 생성한다. 특정 페이지는 초기화 작업 중에 프레임을 미리 생성하고, 프레임을 불러올 때 tkinter 모듈에서 제공하는 tkraise()를 호출하여 가장 앞 화면으로 올라오게 된다. 사용자가 입력, 선택, 받기를 수행하는 프레임은 미리 생성하지 않고, 순차적으로 진행함에 따라 실행하게 된다. 각 프레임의 동작과 설명은 주로 사용자 인터페이스를 구성하는 데 사용되는 메서드, 함수, 라이브러리의 API 호출, UI 위젯의 생성 및 설정, 이벤트 핸들러 함수 등은 아래와 같다. 

### Frame_init 메서드: 프레임 초기 설정
* 카메라 초기화, 스타트 프레임, 로그인 프레임, 서비스 선택 프레임을 시작한다.
* 스타트 프레임을 가장 위에 띄운다.

### open_win1 메서드: 로그인과 회원가입 선택 페이지
*회원가입 버튼을 클릭하면 open_win2을, 로그인 버튼을 클릭하면 open_win3을 실행한다.

### open_win2 메서드: 회원가입 페이지
* onboard 키보드 띄우기 : 한글 출력은 되지만, 입력이 안되는 오류 발생했다. 대안으로 키가 눌릴 때마다 영어->한글로 변환하는 함수 실행하고, 프레임이 생성되고 커서가 입력 부분에 갈 수 있도록 focus_set() 설정하여 사용자가 이름 입력에 헷갈리지 않도록 함.
* check_duplicate_id 함수: ID 중복 확인
* submit 함수: 사용자로부터 이름, ID, 비밀번호, 전화번호, 성별을 입력받아 데이터베이스에 고객 정보를 저장하고, ID로 고객을 판별하고 firebase에 고객 정보 업로드
* 개인정보 동의 항목이 체크 되면 submit 버튼 활성화
* 회원가입 완료하면 onboard 키보드 종료

### open_win3 메서드: 로그인 페이지
* onboard 키보드 띄우기
* self.db.collection('customers').document(id) 리턴값을 get() 하여 doc 변수에 저장
* 로그인 시도시 빈칸 입력 시 오류 출력 후 페이지 넘어가지 않음
* 로그인 시도시 FIrebase Database에 저장된 고객의 정보와 비교, 저장된 고객 데이터의 아이디와 비밀번호가 일치하는지 확인
* 로그인이 되면 고객 이름을 카카오톡 채팅 목록에서 검색하여 윈도우 전환하고 프레임 destroy()

### open_win4 메서드: 서비스 선택 페이지
* button_reg을 누르면 baro()를 호출하여 self.isBaro를 참으로 바꾼 뒤 바로 예약 페이지 메서드를 호출
* self.isBaro가 참으로 설정될 시 사진 합성 과정을 생략하기에 이후 카카오톡 메세지 전송 환경에서 사진을 따로 보내지 않음
* button_login을 누르면 사진 촬영 페이지 메서드를 호출

### open_win5 메서드: 사진 촬영 페이지
* 이 프레임을 시작하면 self.Baro = False로 변경
* count_down(num), Capture(win,picam), AfterCapture(frame), Showfeed() 함수를 사용해서 picam으로부터 프레임을 읽어들여 사진 촬영 후 레이블에 이미지로 표시
* imageBrowse(bucket,name), AfterBrowse(image) 함수를 사용해서 Firebase Storage로부터 고객 사진을 다운로드 받아 레이블에 이미지로 표시
* tg_img(label,btn) 함수로부터 선택한 버튼에 따라 정의된 모드 속성과 이미지 속성을 바꾸고, 리스트 속성에 선택한 버튼 저장
* AfterSelect(mode,image_name,image) 함수에서 리스트 속성이 있을 경우 모드와 이미지 속성을 서버로 전송 
* 서버에서 사용자의 얼굴형을 파악하여 Firebase에 업로드하면 헤어스타일 선택 페이지 메서드 호출 후 프레임 종료

### open_win6 메서드: 헤어스타일 선택 페이지
* select_personal(self,img) 메서드를 통해 전송했던 서버로부터 사진의 배경이 지워진 사진을 받아 퍼스널컬러를 확인해볼 수 있는 4가지 배경에 붙여서 이미지 라벨에 추가
* append_list(self,img_path,img_list,img_name) 메서드, select_personal(self,img) 메서드, make_btn(self, frame, img_path,page) 메서드, recommend_style 메서드를 사용해 각 이미지 프레임별로 원하는 사진 버튼을 배열하고 구축
* 이미지 버튼을 클릭할 때 toggle_border(self, button)에서 변수를 결정하고 이를 인자로 받는 toggle_change(self,button,dict_var,page) 메서드로 컬러와 헤어스타일이 한 개씩만 선택될 수 있도록 설정
* send_styles 메서드로 선택된 style은 self.dict1 딕셔너리에 저장된 첫 번재 키에 해당한 값의 text, color는 self.dict2 딕셔너리에 저장된 첫 번재 키에 해당한 값의 text를 받아 [style, color] 리스트를 서버에게 전송한다. 이후 합성 결과 확인 페이지 메서드 호출

### open_win11 메서드: 합성 결과 확인 페이지
* 서버로부터 받은 합성 결과 이미지를 라벨에 표시
* 결과가 마음에 들지 않는다면 관련 버튼을 눌러 다시 촬영을 시도 (다시 찍기)
* 전 페이지로 돌아가 헤어스타일을 재선택 (헤어스타일 재선택) 
* 이 경우 서버에게 동작 페이지를 알려주기 위해 5나 6을 모드로 전송 
* 합성된 결과대로 시술을 예약하고 싶다면 예약하기 버튼을 클릭하여 미용사 선택 페이지로 이동

### open_win12 메서드: 예약 페이지
* designer 클래쓰를 통해 미용사 인스턴스를 생성하고, 미용사별로 read_reservation(self,db) 메서드로 Firebase Storage로부터 예약 내역을 확인하여 버튼을 생성
* make_reservation(designer_list) 함수로 예약 정보를 Firestore에 저장하며, 여러 시간, 여러 미용사를 선택하지 않도록 함
* 선택된 미용사와 고객 이름을 바탕으로 예약 내역과 합성 결과 이미지를 카카오톡 전송 후 예약 완료 알림 페이지 호출

### open_win13 메서드: 종료 페이지
* 예약이 완료되었다는 텍스트를 보여주고 2초 뒤에 초기 화면으로 돌아가며 이전 프레임은 종료하여 키오스크 초기화

## 소프트웨어 설계 및 구현
### 헤어스타일 합성 모델

헤어스타일 합성은 아래와 같은 방법으로 진행된다.

![1050px-헤어스타일모델](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/d3d4784b-f2c2-4235-afc7-e02208343597)


#### 얼굴형 인식
* 얼굴형 인식을 할 경우 dlib의 landmark 기능을 사용하여 진행하였다.
* 진행을 위해 얼굴형에 따른 랜드마크 대조군이 필요했는데 이를 구성하기 위하여 명확한 기준을 정하여 얼굴형 별로 분류한 데이터셋을 생성하였다.

얼굴형은 남자 여자 모두 둥근형, 각진형, 계란형, 긴얼굴형 4가지로 하여 기준을 정하였다. 얼굴형에 대한 기준은 황금비율 마스크를 사용해서 정하였고 아래와 같다.

![300px-81_landmakr](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/1c048664-cd5b-4c79-924d-e46f0095187b)
![450px-황금비율마스크](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/4b90671e-7697-43cf-8848-26845472cb96)


* 둥근형 :  황금비율 마스크 바깥쪽으로 턱 바로 옆에서 볼까지 돌출된 형상이 둥금.
* 각진형 : 하관이 두드러지고 광대뼈도 튀어나옴. 황금비율 마스크에 제일 잘 맞음.
* 계란형 : 전체적으로 마스크 바깥쪽으로 나와있지만 둥글고 부드럽게 나와있음.
* 긴얼굴형 : 마스크 바깥으로 턱이 살짝 돌출된 얼굴형이면서 마스크에 빈공간이 많음.


기준에 맞는 얼굴 사진 중 정면을 보고 있는 사진을 선별하여 얼굴형 별로 20장씩 데이터셋을 구성하였다.
만든 데이터셋으로 사진을 Align 기능을 이용하여 같은 크기로 만들어주고 얼굴 외각 landmark를 추출하여 각 랜드마크를 평균을 내어 대조군을 완성하였다. 
이 대조군의landmark와 사용자사진의 landmark의 차를 error로 정의하고 가장 error가 작은 얼굴형이 output이 되도록 설계하였다.

#### Style-your-hair
"Style Your Hair: Latent Optimization for Pose-Invariant Hairstyle Transfer via Local-Style-Aware Hair Alignment (ECCV 2022)"에서 사용된 모델로 source image의 얼굴과 target style의 머리스타일을 합성한 결과를 보여주는 모델로 BiseNet과 Style Gan2를 응용하여 만들어졌다. 프린세스 메이커 프로젝트는 고객의 사진을 사용하여 실시간으로 고객에게 결과를 보여주는 프로젝트로 보안과 속도가 매우 중요한 요인중 하나이다. 하지만 Style-your-hair 모델은 Realtime이 목적이 아니라 source와 target 이미지로 좋은 퀄리티 사진을 만들어 내는것에 초점을 두어서 초기 시간이 RTX-3090 환경에서 Inference time이 약 6분 이상 걸리는 문제가 존재하였다. 또한 코드가 합성을 할때 파일을 저장하고 이를 불러오는 방식으로 대부분 구성이 되어있어 고객의 정보가 Server에 그대로 저장되었다.

![900px-Style-your-hair](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/93685a22-a87f-4951-a99a-c2f6d7861629)


이 문제점을 해결하기 위하여 여러가지 방법을 활용하였다.


**SYH_해결 방안 1) 임베딩 과정**

Style-your-hair는 Image generation 모델이 입력받은 이미지를 생성할 수 있도록 weight를 수정해주는 Embedding 과정이 존재한다. 5분중 이 Embedding 시간이 6분이상을 차지하고 이후 합성 시간은 20초 내외에 불가하다는 점을 발견하였다. 따라서 Embedding에 걸리는 시간을 줄이는 것이 필수적이였다. 먼저 Style은 이미 정해진 사진을 사용자에게 합성하는 과정이므로 미리 Embedding을 진행하여 DB에 저장해두었다. 사용자가 만약 스타일을 선택하게 된다면 DB에서 Embedding 데이터를 가져와 사용하게 된다. 이러한 방식으로 Embedding 시간을 절반으로 줄일 수 있었다. 

또한 Embedding 과정을 살펴본 결과 300회 이상 학습이 되는 경우 이후 사진은 비슷한 품질을 보여주는 것을 확인하여 기존 1900회로 설정되어있던 Embedding parameter를 수정하였다.

아래는 기존 Embedding 결과와 수정 후 Embedding 결과를 비교한 사진이다.

![1050px-Embedding](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/36ee193b-817d-405d-9bd2-53cccee578a8)


수정전에 Embedding 시간은 총 3분 10초가 소요되었지만 수정후에는 30초로 시간을 크게 줄이면서 비슷한 퀄리티의 사진을 받을 수 있게 되었다.


**SYH_해결 방안 2)  파일 저장**

::Style-your-hair는 대부분의 과정이 파일을 직접 저장하고 저장한 파일을 불러오는 방식으로 동작하게 되어있다. 파일을 저장하지 않아도 동작하도록 코드를 수정하여 고객의 개인정보가 서버에 남아있지 않도록 수정해주었다.


### 염색

::염색을 하는 과정은 BiseNet과 Opencv를 활용하여 진행하였다. 합성 이미지를 BiseNet에 넣어서 Segmentation data를 받고 이중 Hair 부분만 opencv로 염색을 진행하였다.

![1050px-Dying](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/841dcbd2-0944-4730-bfa1-26c329470ae0)


### 데이터 베이스
Firebase Cloud Service를 이용하여 고객의 데이터, 미용사의 예약시간, 헤어 스타일 정보, 염색 정보등 프로젝트와 관련된 데이터를 정리한다.

**Collection: customers** <br/>

|Document|Field|설명|형식|
|---|---|---|---|
|고객의 ID|gender|고객의 성별 지정<br/>'남자' 혹은 '여자' 값만 저장|string|
|-|id|고객의 ID<br/>중복 허용하지 않음|string|
|-|name|고객의 이름 저장|string|
|-|password|고객의 password 저장|string|
|-|phoneNumber|고객의 전화번호 저장|string|
|-|shape|고객의 얼굴형 저장<br/>이는 사진 촬영 후 분석 후에 저장된다.|string|

'customers' collection은 키오스크 사용에 있어서 전체 고객의 데이터를 저장한다. 이는 추후에 '회원가입', '로그인' 기능 뿐만 아니라 키오스크 사용에 있어서 고객의 정보를 가져올 때 다양하게 사용된다.

**Collection: hairdresser** <br/>

|Document|Field|설명|형식|
|---|---|---|---|
|미용사의 이름|reservation_time|고객이 선택한 예약시간 저장|배열|


'hairdresser' collection은 '미용사 예약하기' 기능 사용에 활용되며, 예약시간 중복이나 이미 지나간 시간에 대해 비활성화할 때 사용된다.


![Cloud_FireStore](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/a5d7e502-9c02-44f5-8c26-954f5a128a85)

**Storage**
Storage에는 남성/여성의 헤어스타일 정보와 염색 정보를 저장한다.

![PM_Storage](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/5073b925-f4d1-4be6-93fe-4ecb315bde10)
![PM_Storage2](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/ce382a01-78df-4d8d-b194-30f92d59e31c)


### 카카오톡 전송
:예약시스템을 완성 시키기 위해서는 예약 내역과 고객이 선택한 헤어스타일이 합성된 사진을 고객과 미용사에게 전송해야 했고, 이를 카카오톡으로 전송하기로 하였다. 카카오톡 전송은 python의 selenium모듈을 통한 웹크롤링을 통하여 구현하였다. "프린세스메이커" 전용 플러스친구 채널을 따로 만들어 사용자들이 이 채널을 친구추가 하면 채널을 통해 카카오톡 전송이 가능하게 하였다. 고객이 키오스크를 통해 로그인을 하면 데이터베이스에서 받아온 고객의 이름을 통하여 플러스친구의 고객 명단에서 사용자의 이름을 검색하고 고객이 원하는 헤어스타일을 적용한 후에 예약을 하면 헤어스타일이 합성된 사진과 예약 시간을 각각 첨부하여 고객에게 전송하였고, 이를 선택한 디자이너에게도 보낼 수 있게 하였다.


![1050px-2023_hk_kakaotalk_main](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/d56e8c55-d826-4b02-9697-cead793f6874)

![375px-2023_hk_kakaotalk2](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/88767c35-5396-4a97-9595-d2ace3dc029a)
![365px-2023_hk_kakaotalk1](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/886d3ce8-3210-4e4c-9e1a-6dc568141628)

![600px-PM_Start_Frame](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/d919e464-36d3-484c-b8e0-52a0f8b11c3b)
![600px-PM_Open_win1](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/10aa6948-d245-4bd6-9f0c-2620615042a5)
![600px-PM_Open_win2](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/4d876da0-00a5-4960-9972-fd6b29210036)
![600px-PM_Open_win3_000](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/74bc752c-7b00-4407-afe3-4b4f62405f48)
![600px-PM_Open_win4](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/3de2fc47-8a0a-4f7b-b27d-62e4a799ea10)
![600px-PM_Open_win5](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/81f13f62-4cf3-48e6-be07-b8a57ab98ae0)
![600px-PM_Open_win6](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/2bed2648-b582-44f2-ba47-16f0f4fa6f22)
![600px-PM_Open_win11](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/30a84a1e-3db6-466f-8524-5873d75d3933)
![600px-PM_Open_win12](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/5e61e27a-eee8-4636-bedc-10af9affcee7)
![600px-PM_Open_win13](https://github.com/TIS2001/Hairstyle-Recommendation-Kiosk/assets/94544462/160d0eca-05f2-4971-bd95-13d42edfd1c8)

