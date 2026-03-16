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

### 2. 本地运行

```bash
# 方式一：直接传参
python sign.py --token "eyJ0eXAi..."

# 方式二：设置环境变量
export DAWU_TOKEN="eyJ0eXAi..."
python sign.py
```

### 3. GitHub Actions 自动签到

#### 3.1 推送代码到 GitHub

```bash
git init
git add .
git commit -m "feat: 大物是也自动签到脚本"
git remote add origin https://github.com/你的用户名/dawushiye-checkin.git
git push -u origin main
```

#### 3.2 配置 Secret

在 GitHub 仓库页面：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 填写：
   - **Name**: `DAWU_TOKEN`
   - **Secret**: 你抓包获取的 JWT Token（`eyJ0eXAi...` 开头）
4. 点击 **Add secret**

#### 3.3 运行

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

## 注意事项

### Token 过期

JWT Token 有过期时间（通常几个月），过期后需要重新抓包：

1. 重新抓包获取新的 `Authorization` 值
2. 更新 GitHub Secret 中的 `DAWU_TOKEN`

可以用以下命令检查 Token 到期时间：

```bash
python3 -c "
import base64, json, datetime
token = '你的token'
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
data = json.loads(base64.b64decode(payload))
print('到期时间:', datetime.datetime.fromtimestamp(data['exp']).strftime('%Y-%m-%d %H:%M:%S'))
"
```

### 修改定时时间

编辑 `.github/workflows/sign.yml` 中的 cron 表达式：

```yaml
schedule:
  # 每天北京时间 09:30 运行（UTC 01:30）
  - cron: "30 1 * * *"
```

**注意**：cron 使用 UTC 时间，北京时间 = UTC + 8

| 北京时间 | UTC 时间 | cron 表达式 |
|---------|---------|------------|
| 08:00   | 00:00   | `0 0 * * *` |
| 09:30   | 01:30   | `30 1 * * *` |
| 12:00   | 04:00   | `0 4 * * *` |

## 项目结构

```
.
├── sign.py                    # 主签到脚本
├── requirements.txt           # Python 依赖
├── .github/
│   └── workflows/
│       └── sign.yml          # GitHub Actions 工作流
├── .gitignore
└── README.md
```

## 常见问题

### Q: 为什么签到失败？

**A:** 可能原因：
1. Token 已过期 → 重新抓包获取新 Token
2. 网络问题 → 检查网络连接
3. 接口变更 → 提 Issue 反馈

### Q: 如何查看 Actions 运行日志？

**A:** 进入仓库 **Actions** 页面 → 点击对应的运行记录 → 查看 **Run sign script** 步骤的输出

### Q: 可以多账号签到吗？

**A:** 可以，有两种方式：
1. Fork 多个仓库，每个仓库配置不同的 `DAWU_TOKEN`
2. 修改脚本支持多账号（需自行实现）

## License

MIT License
