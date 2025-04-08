# 消息推送服务配置指南

## 配置路径
在 GitHub 仓库进行如下操作：  
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

---

## 推送渠道配置说明

### 1. PushPlus 推送
​**​配置步骤：​**​
1. 访问 [PushPlus官网](https://www.pushplus.plus)
2. 使用微信扫码登录
3. 在「一对一推送」页面复制您的 Token
4. 添加 GitHub Secret：
   - ​**​名称​**​：`PUSHPLUS_TOKEN`
   - ​**​值​**​：粘贴复制的 Token

### 2. Server酱（方糖）
​**​注意事项：​**​
⚠️ 免费账号每日限制 5 条消息  
​**​配置步骤：​**​
1. 访问 [Server酱控制台](https://sct.ftqq.com)
2. 使用微信扫码登录
3. 在「Key&API」页面复制 SendKey
4. 添加 GitHub Secret：
   - ​**​名称​**​：`SERVERCHAN_TOKEN`
   - ​**​值​**​：您的 SendKey

### 3. 钉钉机器人
​**​安全设置要求：​**​
🔒 必须设置自定义关键词「双色球」  
​**​配置步骤：​**​
1. 在钉钉群：
   - 群设置 → 智能群助手 → 添加机器人 → 自定义机器人
2. 复制含 `access_token=` 参数的 Webhook URL
3. 添加 GitHub Secret：
   - ​**​名称​**​：`DINGDING_WEBHOOK`
   - ​**​值​**​：完整的 Webhook URL

### 4. 飞书机器人
​**​安全设置要求：​**​
🔒 必须设置自定义关键词「双色球」  
​**​配置步骤：​**​
1. 在飞书群：
   - 群设置 → 添加机器人 → 自定义机器人
2. 勾选「自定义关键词」权限
3. 复制生成的 Webhook URL
4. 添加 GitHub Secret：
   - ​**​名称​**​：`FEISHU_WEBHOOK`
   - ​**​值​**​：复制的 Webhook URL

---

## 核心逻辑验证规则
```python
# 强制校验每组红球必须包含且仅包含 1 个历史开奖重号
if len(common_elements) == 1:
    # 通过验证
else:
    # 触发验证失败处理
