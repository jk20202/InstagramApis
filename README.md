<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
    </a>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688" alt="FastAPI">
    </a>
</div>

# 📸 Instagram Platform

**✨ 专业的 Instagram 数据采集解决方案，支持用户信息、作品列表与全量评论抓取**

当你需要让 AI Agent 感知 Instagram 内容生态——自动采集评论舆论、分析用户作品、驱动内容运营策略——第一道墙往往不是模型能力，而是**平台数据获取能力的缺失**。

本项目做的事很简单：把这道墙拆掉。

**⚠️ 严禁用于爬取用户隐私、违规商业用途！本项目仅供学习与技术研究使用，后果自负。**

## 🌟 功能特性

- ✅ **用户信息采集**
  - 获取用户主页基础信息（user_id、XIgAppId、HomeDocID）
  - 获取用户详细 Profile 数据
- 📹 **作品列表采集**
  - 自动翻页，获取用户全部作品 URL
- 💬 **评论全量采集**
  - 支持一级评论（外层评论）全量抓取
  - 支持二级评论（楼中楼回复）递归抓取
  - 自动翻页，获取全部评论
- 🔍 **作品详情获取**
  - 通过作品 URL 获取帖子/Reel 完整详情数据
- 🚀 **高性能服务**
  - 基于 FastAPI + Uvicorn 异步服务
  - 支持 Docker 一键部署

## 🛠️ 快速开始

### ⛳ 运行环境

- Python 3.10+

### 🎯 本地安装

```bash
pip install -r requirements.txt
```

### 🚀 运行项目

```bash
python App.py
```

服务启动后访问 http://localhost:5005/docs 查看交互式 API 文档。

### 🎨 Cookie 配置

在浏览器中打开 [www.instagram.com](https://www.instagram.com)，**登录账号**后按 `F12` 打开开发者工具，点击「网络」→ 找任意一个 API 请求 → 复制请求头中的 `Cookie` 字段值。

> ⚠️ 注意：必须登录后获取的 Cookie 才有效，缺失将导致请求失败。

将获取到的 Cookie 字符串作为 `cookies_str` 参数传入接口，格式如下：

```
sessionid=xxx; csrftoken=xxx; ds_user_id=xxx; ...
```

## 📡 接口说明

### POST `/get_info`

获取目标用户的基础信息（**调用其他用户相关接口前必须先调用此接口**）。

**请求参数**

| 字段       | 类型  | 必填 | 说明             |
|----------|-----|----|----------------|
| username | str | 是  | Instagram 用户名  |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_info \
  -H "Content-Type: application/json" \
  -d '{"username": "daniel_xueyx"}'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "user_name": "daniel_xueyx",
    "user_id": "123456789",
    "XIgAppId": "936619743392459",
    "HomeDocID": "abc123def456"
  }
}
```

---

### POST `/get_user_info`

获取用户的详细 Profile 信息。

**请求参数**

| 字段          | 类型  | 必填 | 说明                          |
|-------------|-----|----|-------------------------------|
| username    | str | 是  | Instagram 用户名               |
| XIgAppId    | str | 是  | 由 `/get_info` 返回的 XIgAppId  |
| cookies_str | str | 是  | Instagram 登录 Cookie 字符串    |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_user_info \
  -H "Content-Type: application/json" \
  -d '{
    "username": "daniel_xueyx",
    "XIgAppId": "936619743392459",
    "cookies_str": "sessionid=xxx; csrftoken=xxx"
  }'
```

---

### POST `/get_user_all_videos`

获取用户的全部作品 URL 列表（自动翻页）。

**请求参数**

| 字段          | 类型  | 必填 | 说明                         |
|-------------|-----|----|------------------------------|
| user_id     | str | 是  | 由 `/get_info` 返回的 user_id  |
| DocID       | str | 是  | 由 `/get_info` 返回的 HomeDocID |
| cookies_str | str | 是  | Instagram 登录 Cookie 字符串   |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_user_all_videos \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123456789",
    "DocID": "abc123def456",
    "cookies_str": "sessionid=xxx; csrftoken=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": [
    "https://www.instagram.com/reel/C56MpyPrO_3/",
    "https://www.instagram.com/reel/C4xxxxxABC/"
  ]
}
```

---

### POST `/get_inswork_info`

通过作品 URL 获取帖子或 Reel 的完整详情数据（含 media_id、点赞数、描述等）。

**请求参数**

| 字段          | 类型  | 必填 | 说明                    |
|-------------|-----|----|-------------------------|
| url         | str | 是  | 作品的完整 URL            |
| cookies_str | str | 是  | Instagram 登录 Cookie 字符串 |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_inswork_info \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.instagram.com/reel/C56MpyPrO_3/",
    "cookies_str": "sessionid=xxx; csrftoken=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "pk": "3354xxxxxxxx",
    "code": "C56MpyPrO_3",
    "like_count": 1024,
    "comment_count": 88,
    "caption": { "text": "作品描述文字..." }
  }
}
```

---

### POST `/get_WorkCommentDocID`

获取指定作品的评论 DocID（**调用评论接口前必须先调用此接口，每个作品的 DocID 不同**）。

**请求参数**

| 字段          | 类型  | 必填 | 说明                    |
|-------------|-----|----|-------------------------|
| url         | str | 是  | 作品的完整 URL            |
| cookies_str | str | 是  | Instagram 登录 Cookie 字符串 |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_WorkCommentDocID \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.instagram.com/reel/C56MpyPrO_3/",
    "cookies_str": "sessionid=xxx; csrftoken=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "DocIDV1": "7xxxxxxxxxxxxxxx",
    "DocIDV2": "8xxxxxxxxxxxxxxx"
  }
}
```

---

### POST `/get_work_all_comments`

获取指定作品的**全部评论**（含所有楼中楼二级回复，自动翻页）。

**请求参数**

| 字段            | 类型   | 必填 | 说明                                         |
|---------------|------|----|----------------------------------------------|
| CommentDocID  | dict | 是  | 由 `/get_WorkCommentDocID` 返回的 DocID 对象   |
| mediaID       | str  | 是  | 由 `/get_inswork_info` 返回的作品 pk（media_id）|
| cookies_str   | str  | 是  | Instagram 登录 Cookie 字符串                   |

**请求示例**

```bash
curl -X POST http://localhost:5005/get_work_all_comments \
  -H "Content-Type: application/json" \
  -d '{
    "CommentDocID": {"DocIDV1": "7xxx", "DocIDV2": "8xxx"},
    "mediaID": "3354xxxxxxxx",
    "cookies_str": "sessionid=xxx; csrftoken=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": [
    {
      "node": {
        "pk": "17xxxxxxxxx",
        "text": "评论内容",
        "created_at": 1712000000,
        "owner": { "username": "用户名" },
        "child_comment_count": 2,
        "sub_comments": [
          {
            "node": {
              "pk": "17yyyyyyyyy",
              "text": "回复内容",
              "owner": { "username": "回复用户" }
            }
          }
        ]
      }
    }
  ]
}
```

## 🔗 典型调用流程

### 获取作品全部评论（完整流程）

```
1. POST /get_inswork_info   → 获取 media_id (pk)
2. POST /get_WorkCommentDocID → 获取 CommentDocID (DocIDV1, DocIDV2)
3. POST /get_work_all_comments → 获取全部评论
```

### 获取用户全部作品（完整流程）

```
1. POST /get_info           → 获取 user_id、HomeDocID
2. POST /get_user_all_videos → 获取全部作品 URL 列表
```

## 🐳 Docker 部署

```bash
docker build -t ins-platform .
docker run -d -p 5005:5005 ins-platform
```

## 🍥 日志

| 日期       | 说明                                                         |
|----------|--------------------------------------------------------------|
| 26/04/10 | 项目初始化，完成用户信息、作品列表、评论全量抓取（含楼中楼）API 封装 |

## 🤝 欢迎贡献 PR

本项目欢迎任何形式的贡献！如果你有新功能想法、Bug 修复或文档改进，欢迎提交 PR。

- Fork 本仓库并在新分支上开发
- 保持代码风格与现有代码一致
- PR 描述中请简要说明改动内容和目的
- 也欢迎通过 Issue 提出建议或报告问题

## 🧸 额外说明
1. 感谢 star⭐ 和 follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~

## 🍔 交流群

如果你对爬虫和 AI Agent 感兴趣，请加作者主页 wx 通过邀请加入群聊

ps: 请加群，人满或者过期 issue | wx 提醒

| group-1 | group-2 | group-3 |
|:--:|:--:|:--:|
| <img width="280" alt="group1" src="https://cvcat.site/assets/group1.jpg" /> | <img width="280" alt="group2" src="https://cvcat.site/assets/group2.jpg" /> | <img width="280" alt="group3" src="https://cvcat.site/assets/group3.jpg" /> |
