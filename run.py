from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
import requests
import os
import concurrent.futures
from threading import Lock
import time
from tqdm import tqdm, tqdm_notebook

lock = Lock()

def fetch_image(image_url, save_directory, image_filename, max_attempts=3, delay=5, error_log=None):
    for attempt in range(max_attempts):
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                image_data = response.content
                with lock:
                    image_path = os.path.join(save_directory, image_filename)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_data)
                return
            else:
                error_message = f"Failed to download {image_filename}, status code: {response.status_code}, attempt: {attempt + 1}"
                record_error(error_message, error_log)
        except Exception as e:
            error_message = f"Exception occurred while downloading {image_filename} on attempt {attempt + 1}: {e}"
            record_error(error_message, error_log)
        time.sleep(delay)
    error_message = f"Failed to download {image_filename} after {max_attempts} attempts"
    record_error(error_message, error_log)

def record_error(message, error_log):
    with lock:
        error_log.append(message)
        tqdm.write(message)

def fetch_images_from_url(url, webdriver_path=r"G:\edgedriver_win64\msedgedriver.exe"):
    # 设置Edge WebDriver服务
    service = EdgeService(executable_path=webdriver_path)

    # 初始化Edge WebDriver
    options = EdgeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    driver = webdriver.Edge(service=service, options=options)

    # 打开网页
    driver.get(url)

    # 获取标题和作者信息
    title_element = driver.find_element(By.CSS_SELECTOR, 'h1.post__title span')
    author_element = driver.find_element(By.CSS_SELECTOR, 'a.post__user-name')

    title = title_element.text
    author = author_element.text

    # 创建存储图片的文件夹
    save_directory = os.path.join('images', f'[{author}] {title}')
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # 找到所有具有特定class的div标签
    div_tags = driver.find_elements(By.CLASS_NAME, 'post__thumbnail')

    # 准备下载任务列表
    tasks = []
    for i, div_tag in enumerate(div_tags):
        try:
            # 找到div中的a标签
            a_tag = div_tag.find_element(By.TAG_NAME, 'a')
            # 获取原图URL
            image_url = a_tag.get_attribute('href')
            if image_url:
                # 定义图片文件名
                image_filename = f'{i+1}.jpg'
                # 将下载任务添加到任务列表
                tasks.append((image_url, save_directory, image_filename))
        except Exception as e:
            record_error(f"Failed to prepare download task for image {i+1}: {e}")

    # 使用多线程下载图片，并添加进度条
    error_log = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_image, task[0], task[1], task[2], error_log=error_log) for task in tasks]
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Downloading images"):
            pass

    # 关闭WebDriver
    driver.quit()

    # 最后输出所有错误信息
    if error_log:
        print("\nErrors encountered:")
        for error in error_log:
            print(error)

# 示例使用
if __name__ == "__main__":
    url = input("请输入需要下载图片的链接: ")
    webdriver_path = input("请输入WebDriver的路径(默认为G:\\edgedriver_win64\\msedgedriver.exe): ") or r"G:\edgedriver_win64\msedgedriver.exe"
    fetch_images_from_url(url, webdriver_path)
