故障排除
========

本指南提供常见问题的解决方案。

常见问题
--------

ChromeDriver 问题
~~~~~~~~~~~~~~~~~~

**症状**: "ChromeDriver not found" 或版本不匹配

**解决方案**:

1. 让它自动下载（默认行为）
2. 或手动安装：

   * 从 https://chromedriver.chromium.org/ 下载
   * 匹配您的 Chrome 版本
   * 在 ``config.py`` 中更新路径

Selenium 超时
~~~~~~~~~~~~~

**症状**: "Timeout waiting for page elements"

**原因**: 网络慢、服务器负载重

**解决方案**:

* 在 selenium_scraper.py 中增加超时时间（``wait_time`` 参数）
* 检查网络连接
* 如果 ACS 服务器较慢，稍后重试

任务失败并显示 "No papers found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**原因**:

* 无效的期刊 URL
* 期刊页面结构已更改
* 网络问题

**解决方案**:

* 验证 URL 格式: ``https://pubs.acs.org/toc/CODE/current``
* 检查 URL 在浏览器中是否有效
* 如果结构已更改，请报告问题

端口已被占用
~~~~~~~~~~~~

**症状**: "Address already in use"

**解决方案**: 在 ``run.py`` 中更改端口::

    uvicorn.run(app, host="0.0.0.0", port=8080)

数据库被锁定
~~~~~~~~~~~~

**症状**: "database is locked"

**原因**: 多个进程访问数据库

**解决方案**: 确保只运行一个实例

多个任务失败
~~~~~~~~~~~~

**症状**: 第二个任务总是失败

**原因**: Selenium 驱动程序变得过时

**解决方案**: （已在 v0.2.0 中修复）驱动程序在每个任务之前重新初始化

调试
----

启用调试日志
~~~~~~~~~~~~

在 ``config.py`` 中::

    LOG_LEVEL = "DEBUG"

检查 ``logs/acs_crawler.log`` 中的日志

检查数据库
~~~~~~~~~~

::

    sqlite3 data/acs_papers.db
    SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5;
    SELECT COUNT(*) FROM papers;

手动测试 Selenium
~~~~~~~~~~~~~~~~~

::

    python -m acs_crawler.scrapers.selenium_scraper

获取帮助
--------

* 查看 :doc:`installation` 了解详细安装说明
* 查看日志文件 ``logs/`` 目录
* 在 GitHub Issues 上报告 bug
* 在 GitHub Discussions 中提问
