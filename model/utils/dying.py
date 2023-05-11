import cv2
import numpy as np


def dying(img,seg, color)
    img = cv2.imread(img)
    img = cv2.resize(img,(512,512))
    img_seg = cv2.imread(seg)

    h,w,_ = img_seg.shape
    img_seg_ = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            if int(img_seg[i,j,1])==102:
                img_seg_[i,j] = 1
        
    hsvImage = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    hsvImage = np.float32(hsvImage)

    # 채널로 분리하는 함수  ( 다차원일 경우 사용)
    H, S, V = cv2.split(hsvImage)    # 분리됨


    hue_code = color

    H = np.where(img_seg_==1,hue_code[0]/2,H)
    S = np.where(img_seg_==1,hue_code[1]/100*255,S)
    V = np.where(img_seg_==1,hue_code[2]/105*255,V)

    
    hsvImage = cv2.merge( [ H,S,V ] )

    hsvImage = np.uint8(hsvImage)

    
    imgBgr = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)

    alpha=0.7
    final=cv2.addWeighted(img, alpha, imgBgr, 1-alpha, 0)
    return final
    
if __name__ == "__main__":
    test_img = dying("source6.png","0_erased_src_seg.png")
    cv2.imwrite('test_img.png',test_img)    
