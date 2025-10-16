安装指南
========

本指南提供了针对不同操作系统的详细安装说明。

系统要求
--------

* **Python**: 3.9 或更高版本
* **Chrome 浏览器**: 最新稳定版本
* **内存**: 最少 4GB RAM（推荐 8GB）
* **磁盘空间**: 应用程序和数据库至少需要 500MB

步骤 1: 安装 Python
-------------------

**Ubuntu/Debian**::

    sudo apt update
    sudo apt install python3.9 python3-pip

**macOS**::

    # 使用 Homebrew
    brew install python@3.9

**Windows**:

从 https://www.python.org/downloads/ 下载并运行安装程序。
安装过程中请确保勾选"Add Python to PATH"。

步骤 2: 安装 ACS Crawler
-------------------------

克隆仓库
~~~~~~~~

::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

创建虚拟环境
~~~~~~~~~~~~

**方式一: 使用 Conda（推荐）**::

    # 创建环境
    conda create -n acs_crawler python=3.9

    # 激活环境
    conda activate acs_crawler

    # 安装依赖
    pip install -r requirements.txt

**方式二: 使用 Mamba（更快）**::

    # 创建环境
    mamba create -n acs_crawler python=3.9

    # 激活环境
    mamba activate acs_crawler

    # 安装依赖
    pip install -r requirements.txt

安装依赖
~~~~~~~~

::

    pip install -r requirements.txt

这将安装以下组件：

* **FastAPI**: Web 框架
* **Selenium**: 浏览器自动化
* **BeautifulSoup4**: HTML 解析
* **SQLite**: 数据库（Python 内置）
* **Uvicorn**: ASGI 服务器

步骤 3: 安装 Chrome 浏览器
---------------------------

应用程序需要 Chrome 浏览器进行网页爬取。

**Ubuntu/Debian**::

    # 下载 Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

    # 安装 Chrome
    sudo apt install ./google-chrome-stable_current_amd64.deb

    # 验证安装
    google-chrome --version

**CentOS/RHEL/Fedora**::

    # 添加 Google Chrome 仓库
    sudo dnf install fedora-workstation-repositories
    sudo dnf config-manager --set-enabled google-chrome

    # 安装 Chrome
    sudo dnf install google-chrome-stable

**macOS**::

    # 使用 Homebrew Cask
    brew install --cask google-chrome

**Windows**:

从 https://www.google.com/chrome/ 下载并安装

**无头 Linux 服务器**:

对于没有显示器的服务器（如云虚拟机），需要安装 X11 库::

    # Ubuntu/Debian
    sudo apt install xvfb libxi6 libgconf-2-4

步骤 4: ChromeDriver 设置
--------------------------

ChromeDriver 由 ``webdriver-manager`` 自动下载。无需手动设置！

**手动配置（可选）**:

如果您希望手动管理 ChromeDriver：

1. 从以下地址下载与您的 Chrome 版本匹配的 ChromeDriver：
   https://chromedriver.chromium.org/downloads

2. 解压并安装

3. 编辑 ``src/acs_crawler/config.py`` 设置路径

步骤 5: 验证安装
----------------

运行应用程序
~~~~~~~~~~~~

::

    python run.py

预期输出::

    INFO:     Started server process [12345]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

访问仪表板
~~~~~~~~~~

在浏览器中访问：http://localhost:8000

您应该看到统计仪表板、交互式图表、期刊选择下拉菜单等。

Docker 安装（替代方案）
------------------------

Docker 提供了一个隔离的、可重现的环境，所有依赖项都已预安装。

使用 Docker Compose（推荐）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # 克隆仓库
    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

    # 启动应用程序
    docker-compose up -d

    # 查看日志
    docker-compose logs -f

    # 停止应用程序
    docker-compose down

**访问应用程序**：在浏览器中打开 http://localhost:8000

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
