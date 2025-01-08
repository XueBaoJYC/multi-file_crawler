# Multi-file_Crawler

## Introduction

This is an automated robot for general multi-file type crawling, downloading, and dataset generation based on Edge browser and Bing search engine. It contains two modules, link crawling module and link downloading module. In the crawling module, you can customize the file type and keywords, and the crawled links will be classified and stored in .txt files. In the downloading module, the downloaded files will be stored in a folder according to the hash table name, and then a .csv file with two columns, file_name and label, will be generated.


## Fuctions

- 1. Automatically crawl keyword-related links, classify them and store them in .txt files, and count the number of links in each category and the total number.

- 2. Parse URL redirection links, automatically complete downloads, organize data sets, and generate .csv files.


## Usage

- 1. Clone the repository

```python
git clone https://github.com/XueBaoJYC/multi-file_crawler.git
```

- 2. Requirements

Make sure you have the latest version of Edge installed
```python
pip install -r requirements.txt
```
- 3. Set up a proxy (required)
In the crawler file, modify proxies to your proxy address and enter it in the format of IP address: port.

```python
proxies = {
    "http": "your ip:prot",
    "https": "your ip:prot",
}
```


- 4. Configuring Configuration File Types and Keywords

In the crawler, change the file type (filetype: your filetype) to the file type you need to obtain, such as ppt, doc, pdf, and modify the category and keyword (the example is docx file).

```python
search_url = f"https://www.bing.com/search?q=filetype:docx {term}"
            driver.get(search_url)

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
```


- 5. Run crawler.py and download.py

It supports multi-threaded parallel downloading. The maximum number of threads can be modified in the area shown in the code. It also supports breakpoint resume function.

```python
with ThreadPoolExecutor(max_workers=10) as executor:  
    futures = []
    for txt_file in txt_files:
```


