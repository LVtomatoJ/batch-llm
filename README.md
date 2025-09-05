## 批量提问小助手（Batch LLM）

一个用于“批量与 AI 对话”的轻量 Web 应用，基于 NiceGUI 构建。你可以一次性输入多组变量（如品牌、产品名等），系统会将这些变量自动替换进统一问题模板，批量向模型发起对话，并以 Markdown 预览与结果列表展示，支持一键导出为 Excel。

### 主要特性
- 输入多行变量，使用形如 `how to buy {var}` 的问题模板批量提问
- 选择模型并填写 API Key，即可快速开始
- 支持导出结果为 Excel（列：变量、结果）

### 快速开始
1. 安装依赖
```bash
uv sync
```
2. 运行服务
```bash
uv run -m app.main
```
3. 访问界面
打开浏览器访问 `http://127.0.0.1:8080/batch_llm`

### 使用说明
1. 在“创建任务”卡片中：
   - 在“替换的文本变量，一行一个☝️”输入区，逐行填写变量，例如：
     ```
     nike
     adidas
     ```
   - 在“Question with {var}”中输入问题模板（会用每行变量替换 `{var}`）
   - 选择模型、填写 OpenAI API Key
   - 点击“试一次”或“全部运行”
2. 页面底部展示批量结果：
   - 每一行变量对应一个 Markdown 结果卡片
   - 所有任务完成后，可点击“导出 Excel”下载两列表格（变量、结果）

### 配置
- 在 `.env` 中配置默认的 `OPENAI_API_KEY`（或在界面直接填写）

### 目录结构
```text
app/
  main.py                  # UI 和交互
  core/config.py           # 配置加载
  services/
    llm_service.py         # 与模型交互
    task_service.py        # 任务模型/状态
    export_service.py      # 导出 Excel
```

### 路线图 / TODO
1. 支持更多平台模型与自定义参数（温度、最大 tokens、系统提示、web搜索等）
2. 导出支持 HTML等格式（保留 Markdown 样式、可离线查看）
3. 数据库支持：保存历史任务与结果，支持检索与随时查看
4. 消息队列支持：后台异步任务调度与并发控制
