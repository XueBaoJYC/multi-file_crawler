import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import random

# 代理配置
proxies = {
    "http": "your ip:prot",
    "https": "you ip:prot",
}

# 创建链接保存目录
if not os.path.exists("doc_links"):
    os.makedirs("doc_links")

# 初始化Selenium WebDriver
def init_webdriver():
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式
    edge_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    edge_options.add_argument("--no-sandbox")  # 禁用沙盒模式
    edge_options.add_argument("--disable-dev-shm-usage")  # 解决内存不足问题

    # 使用 webdriver-manager 自动管理 EdgeDriver
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

# 使用Selenium提取PPT文件的跳转链接
def extract_ppt_links_with_selenium(driver):
    links = set()  # 使用集合存储链接，自动去重
    items = driver.find_elements(By.CSS_SELECTOR, "a.tilk")  # 筛选 <a class="tilk"> 标签
    for item in items:
        href = item.get_attribute("href")
        if href and href.endswith("=1"):  # 筛选以 "=1" 结尾的链接
            links.add(href)  # 将链接添加到集合中

    # 打印提取到的跳转链接
    print(f"Extracted redirect links: {links}")
    return list(links)  # 将集合转换为列表返回

# 检查是否存在下一页
def has_next_page(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.sb_pagN.sb_pagN_bp.b_widePag.sb_bp")
        return next_button.get_attribute("href") is not None
    except:
        return False

# 跳转到下一页
def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.sb_pagN.sb_pagN_bp.b_widePag.sb_bp")
        next_button.click()
        time.sleep(random.randint(3, 5))  # 随机延时 3 到 5 秒
    except Exception as e:
        print(f"Failed to go to next page: {e}")

# 获取链接并保存到文件
def save_links_to_file(keyword, links, category_count, total_count):
    # 文件名以类别命名
    file_name = f"links/{keyword}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    # 更新计数器
    category_count[keyword] = len(links)
    total_count["total"] += len(links)

# 目标关键词（20个类别）
# 目标关键词（20个类别，每个类别扩展多个关键词）
keywords = {
    "博客文章": ["技术博客", "生活博客", "旅行博客", "美食博客", "个人博客"],
    "财务报告": ["财务报表", "财务分析", "财务预算", "年度财务报告", "季度财务报告"],
    "产品说明书": ["产品功能", "使用指南", "产品规格", "安装说明", "维护手册"],
    "合同": ["租赁合同", "劳动合同", "销售合同", "服务合同", "合作协议"],
    "技术文档": ["API文档", "开发指南", "技术规范", "系统架构", "用户手册"],
    "简历": ["个人简历", "求职简历", "简历模板", "简历优化", "简历设计"],
    "旅游攻略": ["旅行指南", "景点推荐", "美食推荐", "交通攻略", "住宿推荐"],
    "培训材料": ["培训PPT", "培训手册", "培训视频", "培训课程", "培训计划"],
    "社交媒体": ["微博", "微信", "抖音", "Instagram", "Facebook"],
    "食谱": ["家常菜谱", "烘焙食谱", "健康食谱", "快手菜谱", "地方特色菜"],
    "市场报告": ["市场分析", "市场趋势", "市场规模", "市场调研", "竞争分析"],
    "文学作品": ["小说", "散文", "诗歌", "剧本", "随笔"],
    "用户手册": ["产品手册", "操作指南", "安装手册", "维护手册", "故障排除"],
    "政府文件": ["政策文件", "法律法规", "通知公告", "工作报告", "白皮书"]
}

# 初始化计数器
category_count = {keyword: 0 for keyword in keywords}
total_count = {"total": 0}

# 初始化Selenium WebDriver
driver = init_webdriver()

try:
    # 遍历所有关键词
    for keyword, search_terms in keywords.items():
        all_links = []  # 存储当前类别的所有链接

        # 遍历每个搜索关键词
        for term in search_terms:
            # 打开搜索页面
            search_url = f"https://www.bing.com/search?q=filetype:docx {term}"
            driver.get(search_url)
            time.sleep(5)  # 等待页面加载

        # 提取当前页面的链接
        all_links = []
        while True:
            # 提取当前页面的链接
            links = extract_ppt_links_with_selenium(driver)
            all_links.extend(links)

            # 检查是否存在下一页
            if not has_next_page(driver):
                break

            # 跳转到下一页
            go_to_next_page(driver)

        # 保存链接到文件并更新计数器
        save_links_to_file(keyword, all_links, category_count, total_count)

        # 打印当前类别的链接数
        print(f"Saved {category_count[keyword]} links for keyword: {keyword}")

    # 打印总链接数
    print(f"Total links saved: {total_count['total']}")
finally:
    # 关闭WebDriver
    driver.quit()