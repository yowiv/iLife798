# 慧生活798积分签到

因闲鱼代挂恶臭环境，我自己抓包公开此脚本。

## 功能说明

- 自动签到领取积分
- 查询当前积分
- 日志记录功能
- 配置文件管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

1. 复制配置文件模板：

```bash
cp config.example.json config.json
```

2. 编辑 `config.json` 填入你的信息：

```json
{
  "phone": "你的手机号",
  "token": "你的token（通过抓包获取）",
  "user_agent": "你的User-Agent"
}
```

### 如何获取配置信息

1. 使用抓包工具（如Charles、Fiddler、HTTP Toolkit等）
2. 在手机/浏览器上登录慧生活798
3. 进行一次签到操作
4. 在抓包工具中找到签到请求
5. 复制请求中的 token 和其他必要参数

## 使用方法

```bash
python check_in.py
```

## 自动化运行

### Linux/Mac (使用crontab)

每天早上8点自动签到：

```bash
crontab -e
```

添加以下内容：

```
0 8 * * * cd /path/to/-798 && python check_in.py
```

### Windows (使用任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为每天执行
4. 操作设置为运行程序：`python.exe`
5. 参数填写：`check_in.py`
6. 起始于目录填写脚本所在目录

## 注意事项

⚠️ **重要提示**：

- 本脚本仅供学习交流使用
- 请遵守相关服务条款
- 不要频繁请求接口，避免给服务器造成压力
- Token具有时效性，过期后需重新抓包获取
- 请勿将包含真实Token的config.json提交到公共仓库

## 免责声明

本项目仅供学习研究使用，使用本项目所造成的一切后果由使用者自行承担，与开发者无关。

## License

MIT
