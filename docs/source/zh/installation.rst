安装指南
========

本指南提供了针对不同操作系统的详细安装说明。

系统要求
--------

**通用要求：**

* **内存**: 最少 4GB RAM（推荐 8GB）
* **磁盘空间**: 应用程序和数据库至少需要 500MB
* **网络**: 用于下载依赖项和爬取

**Docker 安装：**

* **Docker**: 20.10 或更高版本
* **Docker Compose**: 2.0 或更高版本

**本地安装：**

* **Python**: 3.9 或更高版本
* **Chrome 浏览器**: 最新稳定版本
* **Conda/Mamba**: 推荐用于环境管理

Docker 安装（推荐）
-------------------

Docker 提供了一个隔离的、可重现的环境，Chrome、ChromeDriver 和所有依赖项都已预安装。

**步骤 1：安装 Docker**

按照官方 Docker 安装指南安装：

* Linux: https://docs.docker.com/engine/install/
* macOS: https://docs.docker.com/desktop/install/mac-install/
* Windows: https://docs.docker.com/desktop/install/windows-install/

**步骤 2：克隆并启动**::

    # 克隆仓库
    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

    # 启动应用程序
    docker compose up -d

    # 查看日志
    docker compose logs -f

**步骤 3：访问应用程序**

在浏览器中打开 http://localhost:8000

**Docker 的作用：**

* 自动安装 Chrome 和 ChromeDriver
* 为数据和日志创建持久卷
* 在端口 8000 上启动容器
* 失败时自动重启
* 资源限制（2GB RAM，2 个 CPU）

**管理 Docker 容器**::

    # 停止应用程序
    docker compose down

    # 重启
    docker compose restart

    # 查看日志
    docker compose logs -f

通过 Conda 本地安装
--------------------

适合希望完全控制环境的用户。

步骤 1: 安装前置要求
~~~~~~~~~~~~~~~~~~~~

**Python 3.9+**

* Ubuntu/Debian: ``sudo apt install python3.9 python3-pip``
* macOS: ``brew install python@3.9``
* Windows: 从 https://www.python.org/downloads/ 下载

**Chrome 浏览器**

* Ubuntu/Debian: ``sudo apt install google-chrome-stable``
* macOS: ``brew install --cask google-chrome``
* Windows: 从 https://www.google.com/chrome/ 下载

**Conda/Mamba**（推荐用于环境管理）

* 下载 Miniconda: https://docs.conda.io/en/latest/miniconda.html
* 或安装 Mamba（更快）: ``conda install mamba -n base -c conda-forge``

步骤 2: 克隆并设置
~~~~~~~~~~~~~~~~~~

**克隆仓库**::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

**创建 conda 环境**::

    conda create -n acs_crawler python=3.9
    conda activate acs_crawler

**安装依赖**::

    pip install -r requirements.txt

这将安装 FastAPI、Selenium、BeautifulSoup4、SQLite 和 Uvicorn。

**注意**: ChromeDriver 由 webdriver-manager 自动下载。无需手动设置！

步骤 3: 运行应用程序
~~~~~~~~~~~~~~~~~~~~

启动服务器::

    python run.py

预期输出::

    INFO:     Started server process [12345]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

在浏览器中访问 http://localhost:8000

您应该看到统计仪表板、交互式图表和期刊选择。

平台特定说明
~~~~~~~~~~~~

Ubuntu/Debian
^^^^^^^^^^^^^

**安装所有前置要求**::

    # 系统包
    sudo apt update
    sudo apt install python3.9 python3-pip google-chrome-stable

    # 无头服务器
    sudo apt install xvfb

**安装 Conda/Mamba**::

    # Miniconda
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

    # Mamba（通过 conda-forge）
    conda install mamba -n base -c conda-forge

macOS
^^^^^

**使用 Homebrew**::

    # 安装 Homebrew（如果未安装）
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # 安装前置要求
    brew install python@3.9 google-chrome

    # 安装 Conda
    brew install --cask miniconda

Windows
^^^^^^^

1. **安装 Python**: 从 https://www.python.org/ 下载
2. **安装 Chrome**: 从 https://www.google.com/chrome/ 下载
3. **安装 Conda**: 从 https://docs.conda.io/en/latest/miniconda.html 下载 Miniconda

**PowerShell 命令**::

    # 克隆仓库
    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

    # 创建 conda 环境
    conda create -n acs_crawler python=3.9
    conda activate acs_crawler

    # 安装依赖
    pip install -r requirements.txt

    # 运行应用程序
    python run.py

已知限制
--------

**不支持搜索 URL 爬取**

ACS 搜索页面（``/action/doSearch``）受 Cloudflare Turnstile 验证码保护，阻止所有自动化访问：

* **被阻止的工具**: Selenium、undetected-chromedriver、curl 等所有自动化工具
* **原因**: 基于 JavaScript 的挑战需要人工交互
* **解决方法**: 使用期刊页面 URL（``/toc/`` 页面），完美工作

**替代方案**:

无需爬取搜索结果，您可以：

1. 浏览与您研究相关的特定期刊
2. 爬取符合您时间范围的期刊刊期
3. 爬取后在论文界面进行本地关键词过滤

示例::

    # 代替搜索 "SARS-CoV-2"
    # 爬取相关期刊，例如：
    - Journal of Medicinal Chemistry（药物化学杂志）
    - ACS Infectious Diseases（ACS 传染病）
    # 然后在论文界面过滤

论文页面的本地过滤支持搜索：

* 论文标题
* 作者姓名
* 摘要
* 关键词

常见问题排除
------------

**ChromeDriver 问题**

* 让它自动下载（默认行为）
* 或从 https://chromedriver.chromium.org/ 手动安装

**Selenium 超时**

* 增加超时时间
* 检查网络连接

**端口已被占用**

在 ``run.py`` 中更改端口::

    uvicorn.run(app, host="0.0.0.0", port=8080)

**数据库被锁定**

确保只运行一个实例

获取帮助
~~~~~~~~

* 🐛 `报告问题 <https://github.com/gxf1212/ACS_crawler/issues>`_
* 💬 `在讨论区提问 <https://github.com/gxf1212/ACS_crawler/discussions>`_
