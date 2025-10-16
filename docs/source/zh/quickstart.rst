快速开始
========

本指南将在几分钟内让您开始使用 ACS Paper Crawler。

前提条件
--------

**方式一：Docker（推荐）**

* Docker 20.10 或更高版本
* Docker Compose 2.0 或更高版本

**方式二：本地安装**

* Python 3.9 或更高版本
* Chrome 浏览器
* pip 包管理器

安装
----

方式一：Docker（推荐）
~~~~~~~~~~~~~~~~~~~~~~

1. 克隆仓库::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

2. 使用 Docker Compose 启动::

    docker compose up -d

3. 打开浏览器::

    http://localhost:8000

就是这样！Docker 会自动安装 Chrome、ChromeDriver 和所有依赖项。

方式二：通过 Conda 本地安装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 克隆仓库::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

2. 创建 conda 环境::

    conda create -n acs_crawler python=3.9
    conda activate acs_crawler

3. 安装依赖::

    pip install -r requirements.txt

4. 运行应用::

    python run.py

5. 打开浏览器::

    http://localhost:8000

您应该看到带有统计和图表的仪表板。

第一次爬取
----------

1. 在仪表板上，从下拉菜单选择期刊（例如，"JACS - Journal of the American Chemical Society"）
2. 点击"Start Crawling"
3. 在 Jobs 页面监控进度
4. 在 Papers 页面查看已爬取的论文

下一步
------

* 阅读 :doc:`installation` 了解详细设置选项
* 了解 :doc:`web_usage` 和 :doc:`api_usage` 的高级功能
* 探索 :doc:`api` 进行 API 集成
* 参考 :doc:`troubleshooting` 解决常见问题
