# 家桥 · HearthBridge

这是一个围绕“中国式家庭沟通”场景的产品原型，核心目标是用温暖、低打扰的方式把家人重新连接起来：不做监控、不做社交平台，只做“轻量的关心入口”和“可被理解的家庭表达”。

当前仓库包含：
- 前端交互原型：`jq.html`（核心功能演示）
- 宣传海报：`poster.html`（9:16 海报）
- Python 后端：`backend/server.py`（对接 Qwen3-VL 多模态模型）

## 功能概览（jq.html）
- 随地聊：气球话题入口，点击后话题飞入聊天框自动生成对话；支持手动编辑发送。
- 个人拾光区：随手拍记录生活；拍摄后可选照片并分享给家庭共鸣空间。
- 家庭共鸣空间：共享照片以气泡形式呈现，可一键预览全部，并查看时光总结（AI 生成）。
- 家庭成员总结：爸爸 / 妈妈 / 我最近十天的照片与总结（AI 生成）。
- 平安铃铛：轻触报平安，展示家庭成员打卡状态。

## 项目结构
```
hack_bjzgca/
├─ jq.html                # 主交互页面
├─ poster.html            # 9:16 海报
├─ static/                # 家庭共鸣空间图片
├─ personal_context/      # 个人拾光区图片
├─ jst/                   # 随地聊气球图 & 相机取景图
└─ backend/
   ├─ server.py           # Python API 服务（Qwen3-VL）
   └─ requirements.txt    # 依赖
```

## 启动方式

### 1) 启动后端（Python）
需要 Python 3.10+（建议）

```bash
cd backend
python -m pip install -r requirements.txt
```

配置环境变量（任选其一）：
- Windows PowerShell
```powershell
$env:DASHSCOPE_API_KEY="你的API Key"
```

如需指定地域可选：
```powershell
$env:DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

启动服务：
```bash
python server.py
```
默认监听：`http://localhost:8000`

### 2) 启动前端（静态服务）
由于页面会通过 `fetch` 读取本地图片并转换为 DataURL，请不要用 `file://` 打开，需用本地静态服务器。

在项目根目录执行：
```bash
python -m http.server 5173
```

浏览器打开：
- `http://localhost:5173/jq.html`
- `http://localhost:5173/poster.html`

## API 说明
前端默认调用：
- `POST /api/vision`

请求体示例：
```json
{
  "prompt": "你的提示词",
  "image_urls": ["data:image/jpeg;base64,..."]
}
```

前端已内置“家桥”场景的 system prompt，用于提升家庭场景总结质量；成员总结/家庭共鸣/分享总结会自动附加上下文提示。

## 常见问题
- 看不到 AI 总结：请确认后端已启动、`DASHSCOPE_API_KEY` 正确，以及前端在本地服务器中打开。
- 图片读取失败：请确保通过 `http://localhost:5173` 打开页面，而不是本地文件路径。

## 备注
本仓库为原型与演示用途，便于展示产品方向与交互体验。
