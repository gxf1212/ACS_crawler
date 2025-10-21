# ACS Paper Crawler / ACS 论文爬虫

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)
[![Documentation](https://readthedocs.org/projects/acs-crawler/badge/?version=latest)](https://acs-crawler.readthedocs.io/)

A professional web-based crawler for American Chemical Society (ACS) papers with modern dashboard and analytics.

专业的 ACS（美国化学会）论文网络爬虫，具有现代化仪表板和分析功能。

[English](#english) | [中文](#中文) | [📚 Documentation](https://acs-crawler.readthedocs.io/)

---

<a name="english"></a>

## English

### Features

- **43 Built-in Journals**: Pre-configured ACS journal list
- **Real-time Crawling**: Extract papers from ACS Publications
- **Complete Metadata**: Title, DOI, authors, abstract, keywords, citation info
- **Modern Dashboard**: Interactive charts and statistics
- **Advanced Filtering**: Search by title, author, journal, year
- **Background Jobs**: Async crawling with progress tracking
- **RESTful API**: Full API documentation at `/docs`

### Quick Start

**Option 1: Docker (Recommended)**

```bash
# Start with Docker Compose
docker compose up -d

# Access at http://localhost:8000

# Stop
docker compose down
```

**Option 2: Local Installation**

```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Configure ChromeDriver path
# Copy .env.example to .env and set CHROMEDRIVER_PATH if needed
cp .env.example .env
# Edit .env to set your ChromeDriver path (Windows users especially)

# Run the application
python run.py

# Open browser
http://localhost:8000
```

**Option 3: Install from PyPI** (Coming soon)

```bash
pip install acs-crawler

# Run the web interface
python -m uvicorn acs_crawler.api.main:app --host 0.0.0.0 --port 8000
```

### Requirements

- **Docker**: 20.10+ (for Docker installation), OR
- **Python**: 3.9+ (for local installation)
- **Chrome browser**: Latest stable version
- **ChromeDriver**: Auto-downloaded by webdriver-manager (or configure manually)

### Configuration

**ChromeDriver Path** (Optional)

By default, ChromeDriver is automatically downloaded. If you want to use your own ChromeDriver:

1. Copy `.env.example` to `.env`
2. Set `CHROMEDRIVER_PATH` to your ChromeDriver executable path

Examples:
```bash
# Windows
CHROMEDRIVER_PATH=C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe

# Linux/Mac
CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# WSL (Windows path from WSL)
CHROMEDRIVER_PATH=/mnt/c/Program Files/Google/Chrome/Application/chromedriver-win64/chromedriver.exe
```

### Known Limitations

- **No Search URL Crawling**: ACS search pages are protected by Cloudflare Turnstile CAPTCHA
  - Automated tools (Selenium, curl, etc.) are blocked
  - **Workaround**: Use journal issue URLs which work perfectly
  - Local filtering available in Papers UI after crawling
- **Performance**: Selenium-based (slower than HTTP-only crawlers, ~3-5s startup per job)
- **Rate Limiting**: No automatic limits - space out jobs manually (1-2 concurrent max)
- **Data Extraction**: Only public metadata (no paywalled content, no author affiliations)
- **Scalability**: Sequential job processing, SQLite storage (not for production)
- **ACS Only**: Designed for ACS journals, relies on current page structure
- **Legal**: Users responsible for complying with ACS Terms of Service

See [full documentation](https://acs-crawler.readthedocs.io/) for workarounds and best practices.

### Documentation

Full documentation available in the `docs/` directory:

```bash
cd docs
make html
# Open docs/_build/html/index.html
```

Or read online: [Documentation](https://acs-crawler.readthedocs.io/)

### Screenshots

<div align="center">

![Dashboard](screenshots/index.png)
*Dashboard with statistics and charts*

![Papers](screenshots/papers.png)
*Advanced paper filtering*

![Paper Detail](screenshots/paper_detail.png)
*Detailed paper view*

![Jobs](screenshots/jobs.png)
*Job management with cancellation*

</div>

### License & Copyright

**Copyright (c) 2025 ACS Paper Crawler Contributors**

This software is for **educational and research purposes only**.

- ✅ Academic & Educational Use
- ✅ Research & Study
- ❌ Commercial Use (requires permission)
- ⚠️ Respect ACS Terms of Service

See [LICENSE](LICENSE) and [full documentation](https://acs-crawler.readthedocs.io/) for details.

---

<a name="中文"></a>

## 中文

### 功能特性

- **43 个内置期刊**：预配置的 ACS 期刊列表
- **实时爬取**：从 ACS Publications 提取论文
- **完整元数据**：标题、DOI、作者、摘要、关键词、引用信息
- **现代化仪表板**：交互式图表和统计
- **高级过滤**：按标题、作者、期刊、年份搜索
- **后台任务**：异步爬取，进度追踪
- **RESTful API**：完整 API 文档位于 `/docs`

### 快速开始

**方式一：Docker（推荐）**

```bash
# 使用 Docker Compose 启动
docker compose up -d

# 访问 http://localhost:8000

# 停止
docker compose down
```

**方式二：本地安装**

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py

# 打开浏览器
http://localhost:8000
```

### 环境要求

- **Docker**: 20.10+（Docker 安装方式），或
- **Python**: 3.9+（本地安装方式）
- **Chrome 浏览器**: 最新稳定版
- **ChromeDriver**: 由 webdriver-manager 自动下载

### 已知限制

- **无法爬取搜索 URL**：ACS 搜索页面受 Cloudflare Turnstile 验证码保护
  - 自动化工具（Selenium、curl 等）被阻止
  - **解决方法**：使用期刊页面 URL，完美工作
  - 爬取后可在论文界面进行本地过滤
- **性能**：基于 Selenium（比纯 HTTP 爬虫慢，每个任务启动约 3-5 秒）
- **速率限制**：无自动限制 - 需手动间隔任务（最多 1-2 个并发）
- **数据提取**：仅公开元数据（无付费内容，无作者单位）
- **可扩展性**：顺序任务处理，SQLite 存储（不适用于生产环境）
- **仅限 ACS**：专为 ACS 期刊设计，依赖当前页面结构
- **法律**：用户需自行遵守 ACS 服务条款

详见[完整文档](https://acs-crawler.readthedocs.io/)获取解决方法和最佳实践。

### 文档

完整文档位于 `docs/` 目录：

```bash
cd docs
make html
# 打开 docs/_build/html/index.html
```

或在线阅读：[文档](https://acs-crawler.readthedocs.io/)

### 截图

<div align="center">

![仪表板](screenshots/index.png)
*带统计和图表的仪表板*

![论文](screenshots/papers.png)
*高级论文过滤*

![论文详情](screenshots/paper_detail.png)
*详细的论文视图*

![任务](screenshots/jobs.png)
*带取消功能的任务管理*

</div>

### 许可证与版权

**版权所有 (c) 2025 ACS Paper Crawler 贡献者**

本软件仅用于**教育和研究目的**。

- ✅ 学术与教育用途
- ✅ 研究与学习
- ❌ 商业用途（需要许可）
- ⚠️ 遵守 ACS 服务条款

详见[许可证](LICENSE)和[完整文档](https://acs-crawler.readthedocs.io/)。

---

## Project Structure / 项目结构

```
ACS_crawler/
├── src/acs_crawler/      # Source code / 源代码
├── docs/                 # Documentation / 文档
├── data/                 # Database / 数据库
├── logs/                 # Logs / 日志
├── run.py               # Entry point / 入口
└── README.md            # This file / 本文件
```

## Technology Stack / 技术栈

**Backend**: FastAPI, SQLite, Selenium, BeautifulSoup4
**Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript

---

## Contributing / 贡献

Contributions welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md)

欢迎贡献！请查看[贡献指南](docs/CONTRIBUTING.md)

## Support / 支持

- 📚 [Documentation](https://acs-crawler.readthedocs.io/)
- 🐛 [Report Issues](https://github.com/gxf1212/ACS_crawler/issues)
- 💬 [Discussions](https://github.com/gxf1212/ACS_crawler/discussions)

---

**Happy Crawling! / 爬取愉快！** 🚀
