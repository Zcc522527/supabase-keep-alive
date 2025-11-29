# Supabase Keep-Alive

🚀 一个轻量级的 Python Serverless 项目，用于保持 Supabase 数据库活跃。

## 功能特点

- 🔒 使用访问密钥保护端点
- 🛠 通过环境变量配置目标表
- 🚀 完全 Serverless，适合 Vercel 托管
- 📦 简单的环境设置

## 快速开始

### 1. 部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/supabase-keep-alive)

1. 点击上方按钮
2. 登录 Vercel
3. 配置以下环境变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `SUPABASE_URL` | Supabase 项目 URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase API Key | `eyJhbGc...` |
| `ACCESS_KEY` | 自定义访问密钥 | `my_secret_123` |
| `TABLE_NAME` | 要查询的表名 | `users` |

4. 点击 Deploy

### 2. 设置定时任务

使用以下任意服务定时触发：

#### 方法 A: GitHub Actions（推荐，完全免费）

在仓库中创建 `.github/workflows/keepalive.yml`：

```yaml
name: Supabase Keepalive

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0点
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Endpoint
        run: |
          curl -f "https://your-project.vercel.app/api?key=${{ secrets.ACCESS_KEY }}" || exit 1
