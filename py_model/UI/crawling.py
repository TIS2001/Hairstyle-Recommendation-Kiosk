import requests
from bs4 import BeautifulSoup
import os

search_url = "https://www.google.com/search?q=%EC%97%AC%EC%9E%90+%EB%A8%B8%EB%A6%AC&tbm=isch&ved=2ahUKEwjC7qbQ7fj-AhXWVd4KHT0NB3IQ2-cCegQIABAA&oq=%EC%97%AC%EC%9E%90+%EB%A8%B8%EB%A6%AC&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoICAAQgAQQsQM6BAgAEB46BwgjEOoCECc6CAgAELEDEIMBOgsIABCABBCxAxCDAVCqB1iWImC0ImgMcAB4BYABuQKIAYwVkgEIMS4xNS4xLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=G_NiZIL1K9ar-Qa9mpyQBw&bih=933&biw=1848"
response = requests.get(search_url)
soup = BeautifulSoup(response.content, 'html.parser')
images = soup.find_all('img')
image_urls = [image.get('src') if image.get('src') else image.get('data-src') for image in images]
save_folder = "new_hairstyles"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

for i, url in enumerate(image_urls[:50]):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(f"{save_folder}/new_hairstyle_{i+1}.jpg", "wb") as f:
            f.write(response.content)
        print(f"Successfully saved image {i+1}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        continue
    except Exception as err:
        print(f"Other error occurred: {err}")
        continue
