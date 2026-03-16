# 大物是也微信小程序自动签到

自动签到脚本，支持 GitHub Actions 定时运行，每天自动完成「大物是也」小程序的签到任务。

## 功能特性

- ✅ 自动签到，获取每日积分
- ✅ 支持 GitHub Actions 定时任务（每天北京时间 08:00）
- ✅ 智能识别已签到状态，避免重复签到
- ✅ Token 通过环境变量安全传递，不会泄露

## 快速开始

### 1. 获取 Token

使用 Charles 或 Fiddler 抓包获取 JWT Token：

1. 打开 **Charles**（或 Fiddler）
2. 配置 HTTPS 解密：`Help` → `SSL Proxying` → `Install Charles Root Certificate`
3. 打开微信 PC 版，进入「大物是也」小程序
4. 在小程序中随便点击一个功能（如查看签到记录）
5. 在 Charles 中找到 `api.dawushiye.com` 的请求
6. 复制请求头中的 `Authorization` 字段值（以 `eyJ0eXAi...` 开头的 JWT）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 本地运行

```bash
# 方式一：直接传参
python sign.py --token "eyJ0eXAi..."

# 方式二：设置环境变量
export DAWU_TOKEN="eyJ0eXAi..."
python sign.py
```

### 4. GitHub Actions 自动签到

#### 4.1 推送代码到 GitHub

```bash
git init
git add .
git commit -m "feat: 大物是也自动签到脚本"
git remote add origin https://github.com/你的用户名/dawushiye-checkin.git
git push -u origin main
```

#### 4.2 配置 Secret

在 GitHub 仓库页面：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 填写：
   - **Name**: `DAWU_TOKEN`
   - **Secret**: 你抓包获取的 JWT Token（`eyJ0eXAi...` 开头）
4. 点击 **Add secret**

#### 4.3 运行

- **自动运行**：每天北京时间 08:00 自动执行
- **手动触发**：进入 **Actions** 页面 → 选择 **大物是也自动签到** → **Run workflow**

## 运行结果示例

### 签到成功

```
==================================================
  大物是也 自动签到  |  2026-03-15 08:00:00
==================================================

[1/2] 查询签到状态...
      响应: {"data": {...}, "resultCode": 0, ...}

[2/2] 执行签到...
      响应: {"data": {"integral": 2, ...}, "resultCode": 0, ...}

[OK] 签到成功！，获得 2 积分

==================================================
```

### 已签到

```
[2/2] 执行签到...
      响应: {"data": null, "resultCode": -1, "errorMessage": "已签到成功！请勿重复签到哦"}

[OK] 今日已签到，无需重复签到

==================================================
```

## 项目结构

```
.
├── sign.py                    # 主签到脚本
├── requirements.txt           # Python 依赖（requests）
├── .github/
│   └── workflows/
│       └── sign.yml          # GitHub Actions 工作流
└── README.md                 # 项目说明文档
```

## 注意事项

### Token 过期

JWT Token 有过期时间（通常几个月），过期后需要重新抓包：

1. 重新抓包获取新的 `Authorization` 值
2. 更新 GitHub Secret 中的 `DAWU_TOKEN`