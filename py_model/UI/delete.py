from PIL import Image
import os

# 이미지 변환 및 삭제 함수
def convert_and_delete_image(filepath):
    # 원본 이미지 삭제
    os.remove(filepath)
for filename in os.listdir("hairstyles"):
    if filename.endswith(".jpg"):
        filepath = os.path.join("hairstyles", filename)
        convert_and_delete_image(filepath)