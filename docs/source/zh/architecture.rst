架构设计
========

本文档描述 ACS Paper Crawler 的系统架构和设计决策。

系统概述
--------

ACS Paper Crawler 采用模块化架构，主要组件包括：

* **Web 服务器** (FastAPI) - RESTful API 和 Web 界面
* **爬虫引擎** (Selenium) - 浏览器自动化和数据提取
* **数据存储** (SQLite) - 论文和任务数据持久化
* **任务调度** - 后台异步任务处理

核心模块
--------

API 层
~~~~~~

基于 FastAPI 框架，提供：

* RESTful API 端点
* 自动生成的 API 文档
* 请求验证和错误处理
* 静态文件服务（Web 界面）

爬虫层
~~~~~~

基于 Selenium WebDriver：

* 智能等待和页面加载检测
* 反爬虫检测绕过
* 元数据提取和解析
* 错误处理和重试机制

存储层
~~~~~~

SQLite 数据库：

* 论文表（papers）
* 任务表（jobs）
* 作者表（authors）
* 关键词表（keywords）
* 全文搜索索引

数据流
------

1. 用户通过 Web 界面或 API 创建爬取任务
2. 任务进入后台队列
3. 爬虫引擎处理任务：

   * 加载期刊页面
   * 提取论文列表
   * 逐个爬取论文详情
   * 保存到数据库

4. 用户通过 Web 界面或 API 查看结果

技术栈
------

* **后端**: Python 3.9+, FastAPI, Uvicorn
* **爬虫**: Selenium WebDriver, BeautifulSoup4
* **数据库**: SQLite3
* **前端**: Bootstrap 5, Chart.js, Vanilla JavaScript

设计决策
--------

**为什么使用 Selenium 而不是 requests？**

ACS 网站使用 JavaScript 动态加载内容，需要真实的浏览器环境。

**为什么使用 SQLite 而不是 PostgreSQL/MySQL？**

SQLite 简单易用，无需额外的服务器配置，适合中小规模应用。

**为什么使用 FastAPI？**

FastAPI 提供自动 API 文档、类型验证和高性能异步支持。

扩展性
------

系统可以通过以下方式扩展：

* 添加更多期刊支持
* 实现分布式爬取
* 添加数据导出格式
* 集成其他分析工具

详细信息请查看源代码中的注释和文档字符串。
