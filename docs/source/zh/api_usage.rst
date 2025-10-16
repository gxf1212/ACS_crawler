API 使用指南
=============

本指南介绍如何使用 RESTful API 进行程序化访问。

API 概述
--------

应用程序在 http://localhost:8000/api 提供 RESTful API

交互式文档访问地址：http://localhost:8000/docs

身份验证
--------

目前，API 不需要身份验证。所有端点都可以在没有令牌的情况下访问。

任务 API
--------

列出所有任务
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/jobs

响应::

    [
      {
        "job_id": "job_20250112_123456_abc123",
        "journal_url": "https://pubs.acs.org/toc/jacsat/current",
        "status": "completed",
        "papers_crawled": 25,
        "total_papers": 25,
        "created_at": "2025-01-12T12:34:56",
        "completed_at": "2025-01-12T12:45:30"
      }
    ]

获取任务详情
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/jobs/{job_id}

创建新任务
~~~~~~~~~~

::

    curl -X POST http://localhost:8000/api/jobs \
      -H "Content-Type: application/json" \
      -d '{
        "journal_url": "https://pubs.acs.org/toc/jacsat/current",
        "max_results": 10
      }'

参数：

* ``journal_url`` (必需): ACS 期刊 URL
* ``max_results`` (可选): 限制爬取的论文数量

取消任务
~~~~~~~~

::

    curl -X DELETE http://localhost:8000/api/jobs/{job_id}

论文 API
--------

列出所有论文
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers

查询参数：

* ``search``: 在标题/作者/摘要中搜索
* ``journal``: 按期刊名称筛选
* ``year``: 按发表年份筛选
* ``has_abstract``: true/false

带筛选器的示例::

    curl "http://localhost:8000/api/papers?journal=JACS&year=2025&has_abstract=true"

获取论文详情
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers/{doi}

将 {doi} 替换为 URL 编码的 DOI（例如 ``10.1021/jacs.1c00001``）。

导出为 Excel
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers/export/xlsx -o papers.xlsx

这将所有论文下载为 Excel (XLSX) 文件，包含：

* 专业格式的表头（带颜色样式）
* 自动调整列宽以提高可读性
* 原生 Excel 兼容性
* 正确处理逗号分隔值（作者、关键词）

统计 API
--------

获取统计信息
~~~~~~~~~~~~

::

    curl http://localhost:8000/api/stats

响应::

    {
      "total_papers": 1250,
      "total_jobs": 45,
      "completed_jobs": 40,
      "papers_by_journal": {
        "JACS": 320,
        "Org. Lett.": 180
      }
    }

Python 示例
-----------

使用 requests 库::

    import requests

    # 创建爬取任务
    response = requests.post(
        "http://localhost:8000/api/jobs",
        json={
            "journal_url": "https://pubs.acs.org/toc/jacsat/current",
            "max_results": 10
        }
    )
    job = response.json()
    print(f"已创建任务: {job['job_id']}")

    # 检查任务状态
    status = requests.get(f"http://localhost:8000/api/jobs/{job['job_id']}")
    print(status.json())

    # 列出论文
    papers = requests.get("http://localhost:8000/api/papers")
    for paper in papers.json():
        print(f"{paper['title']} - {paper['journal']}")

错误处理
--------

API 返回标准 HTTP 状态码：

* **200**: 成功
* **201**: 已创建
* **400**: 错误请求（无效参数）
* **404**: 未找到
* **500**: 内部服务器错误

错误响应格式::

    {
      "detail": "错误信息"
    }

速率限制
--------

没有强制的速率限制，但请：

* 间隔创建任务（不要同时创建许多任务）
* 遵守 ACS 的服务条款
* 使用 ``max_results`` 进行测试

完整 API 参考
-------------

有关所有端点、参数和响应模式的完整 API 文档：

访问 http://localhost:8000/docs（FastAPI 自动生成的 Swagger UI）

或查看 :doc:`api` 以获取详细参考。
