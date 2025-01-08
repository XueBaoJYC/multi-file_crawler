# Multi-file_Crawler

## Introduction

This is an automated robot for general multi-file type crawling, downloading, and dataset generation based on Edge browser and Bing search engine. It contains two modules, link crawling module and link downloading module. In the crawling module, you can customize the file type and keywords, and the crawled links will be classified and stored in .txt files. In the downloading module, the downloaded files will be stored in a folder according to the hash table name, and then a .csv file with two columns, file_name and label, will be generated.

---
## Fuctions

1.自动爬取关键词相关链接，并分类存储到.txt文件中，计数每个类别链接数量和总数量。

2.解析URL重定向链接，自动完成下载、数据集整理并生成.csv文件

---
## 安装步骤  

1.克隆仓库

