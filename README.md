设置消息推送

在 “设置” - “机密和变量” - “操作” - “仓库机密” - “新建仓库机密”

#配置推送服务

##推送渠道1：PushPlus
访问 https://www.pushplus.plus
微信扫码登录
在"一对一推送"页面复制你的token
在GitHub仓库中：
Settings > Secrets > actions > New repository secret
名称：PUSHPLUS_TOKEN
值：粘贴复制的token

##推送渠道2：Server酱（方糖）
免费账号，每日限制5条消息
访问 https://sct.ftqq.com
微信扫码登录
在"Key&API"页面复制SendKey
GitHub仓库添加secret：
名称：SERVERCHAN_TOKEN
值：你的SendKey

##推送渠道3：钉钉机器人
在钉钉群中：
右上角群设置 > 智能群助手 > 添加机器人 > 自定义
设置机器人名称，安全设置选择"自定义关键词"，填写  双色球  
复制生成的Webhook URL（包含access_token=参数的部分）
GitHub仓库添加secret：
名称：DINGDING_WEBHOOK
值：你的token

##推送渠道4：飞书机器人
在飞书群中：
群设置 > 添加机器人 > 自定义机器人
设置机器人名称，勾选所需权限
安全设置选择"自定义关键词"，填写  双色球  
复制生成的Webhook URL
GitHub仓库添加secret：
名称：FEISHU_WEBHOOK
值：复制的Webhook URL




#根据代码
if len(common_elements) == 1  
严格限制必须有且只有1个重号，每组红球必须包含且仅包含1个与上期开奖号码相同的红球
