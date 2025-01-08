import os
import time
import csv
import hashlib
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义路径
links_dir = "/home/CJY/PycharmProjects/NLP/crawler"  # 存放txt文件的目录
base_dir = "/home/CJY/PycharmProjects/NLP/crawler/data"  # 主下载目录
csv_file_path = "/home/CJY/PycharmProjects/NLP/crawler/data.csv"  # CSV文件路径
downloaded_files_path = "/home/CJY/PycharmProjects/NLP/crawler/downloaded_files.txt"  # 记录已下载文件的路径

# 创建主目录
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 初始化CSV文件（如果不存在则创建）
if not os.path.exists(csv_file_path):
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_name", "label"])  # 写入表头

# 初始化已下载文件记录（如果不存在则创建）
if not os.path.exists(downloaded_files_path):
    with open(downloaded_files_path, "w", encoding="utf-8") as f:
        pass  # 创建一个空文件

# 清理未完成的下载文件
def cleanup_incomplete_downloads(download_dir):
    for f in os.listdir(download_dir):
        if f.endswith(".crdownload"):
            os.remove(os.path.join(download_dir, f))
            print(f"Removed incomplete download: {f}")

# 生成唯一文件名
def generate_unique_filename(link):
    hash_object = hashlib.md5(link.encode())
    return f"{hash_object.hexdigest()}.pptx"

# 检查文件是否已下载
def is_file_downloaded(file_name):
    if os.path.exists(os.path.join(base_dir, file_name)):
        return True
    with open(downloaded_files_path, "r", encoding="utf-8") as f:
        return file_name in f.read()

# 记录已下载的文件
def mark_file_as_downloaded(file_name):
    with open(downloaded_files_path, "a", encoding="utf-8") as f:
        f.write(file_name + "\n")

# 下载单个文件的函数（支持断点续传）
def download_file(link, category):
    file_name = generate_unique_filename(link)

    # 检查文件是否已下载
    if is_file_downloaded(file_name):
        print(f"File already exists: {file_name}")
        return

    # 设置Edge无头模式
    edge_options = Options()
    edge_options.add_argument("--headless")  # 启用无头模式
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")

    # 设置下载目录
    prefs = {
        "download.default_directory": base_dir,  # 下载到主目录
        "download.prompt_for_download": False,  # 禁用下载提示
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    edge_options.add_experimental_option("prefs", prefs)

    # 初始化Edge WebDriver（增加重试机制）
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 自动下载并管理 EdgeDriver
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
            break  # 成功启动浏览器，跳出重试循环
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to start EdgeDriver after {max_retries} attempts.")
                return  # 跳过当前链接
            time.sleep(5)  # 等待 5 秒后重试

    try:
        # 清理未完成的下载文件
        cleanup_incomplete_downloads(base_dir)

        # 设置页面加载超时
        driver.set_page_load_timeout(30)

        # 访问下载链接
        print(f"Downloading {link}...")
        driver.get(link)
        time.sleep(10)  # 等待页面加载

        # 获取最终的重定向 URL
        final_url = driver.current_url
        print(f"Final URL: {final_url}")

        # 使用 requests 库直接下载文件（支持断点续传）
        file_path = os.path.join(base_dir, file_name)
        if os.path.exists(file_path):
            # 如果文件已部分下载，获取已下载的文件大小
            downloaded_size = os.path.getsize(file_path)
            headers = {"Range": f"bytes={downloaded_size}-"}
        else:
            downloaded_size = 0
            headers = {}

        response = requests.get(final_url, headers=headers, stream=True)
        if response.status_code == 200 or response.status_code == 206:  # 206 表示部分内容
            with open(file_path, "ab" if downloaded_size else "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Successfully downloaded: {file_name}")

            # 记录到CSV文件
            with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([file_name, category])

            # 标记文件为已下载
            mark_file_as_downloaded(file_name)
        else:
            print(f"Failed to download {final_url}: Status code {response.status_code}")

    except Exception as e:
        print(f"Error downloading {link}: {e}")
    finally:
        # 关闭浏览器
        driver.quit()

# 获取所有txt文件并排序
txt_files = sorted([f for f in os.listdir(links_dir) if f.endswith(".txt")])

# 使用线程池并行下载
with ThreadPoolExecutor(max_workers=10) as executor:  # 设置最大线程数
    futures = []
    for txt_file in txt_files:
        # 获取类别名称（去掉.txt后缀）
        category = os.path.splitext(txt_file)[0]

        # 读取txt文件中的链接
        with open(os.path.join(links_dir, txt_file), "r", encoding="utf-8") as file:
            links = file.read().splitlines()

        # 提交下载任务到线程池
        for link in links:
            futures.append(executor.submit(download_file, link, category))

    # 等待所有任务完成
    for future in as_completed(futures):
        try:
            future.result()  # 获取任务结果（如果有异常会抛出）
        except Exception as e:
            print(f"Error in download task: {e}")