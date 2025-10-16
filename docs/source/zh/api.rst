API 参考
=========

完整的 API 文档请访问：

* **Swagger UI**: http://localhost:8000/docs
* **ReDoc**: http://localhost:8000/redoc

主要端点
--------

任务管理
~~~~~~~~

* ``GET /api/jobs`` - 列出所有任务
* ``POST /api/jobs`` - 创建新任务
* ``GET /api/jobs/{job_id}`` - 获取任务详情
* ``DELETE /api/jobs/{job_id}`` - 取消任务

论文管理
~~~~~~~~

* ``GET /api/papers`` - 列出所有论文
* ``GET /api/papers/{doi}`` - 获取论文详情
* ``GET /api/papers/export/xlsx`` - 导出为 Excel

统计信息
~~~~~~~~

* ``GET /api/stats`` - 获取统计信息

详细文档
--------

访问 http://localhost:8000/docs 查看交互式 API 文档，包含：

* 所有端点的详细说明
* 请求/响应示例
* 参数验证
* 直接在浏览器中测试 API

另请参阅
--------

* :doc:`api_usage` - API 使用指南和示例
