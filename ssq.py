import random
import requests
from lxml import html
from collections import Counter
import os
import json

# 实时获取区间比、奇偶的概率
def ssq_interval_parity_data():
    # 请求网页
    url = "https://m.cz89.com/zst/ssq?pagesize=120"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # 解析HTML
    tree = html.fromstring(response.text)

    # 定义XPath表达式
    interval_xpath = "/html/body/div[2]/div/div/div[2]/div[2]/table/tbody[1]/tr[{}]/td[60]"
    parity_xpath = "/html/body/div[2]/div/div/div[2]/div[2]/table/tbody[1]/tr[{}]/td[61]"

    # 提取数据
    data = []
    second_data = []
    for i in range(1, 121):
        path = interval_xpath.format(i)
        second_path = parity_xpath.format(i)
        value = tree.xpath(path)
        second_value = tree.xpath(second_path)
        if value and second_value:
            data.append(value[0].text_content().strip())
            second_data.append(second_value[0].text_content().strip())

    # 统计处理
    counter = Counter(data)
    second_counter = Counter(second_data)

    total = sum(counter.values())
    second_total = sum(second_counter.values())

    items_str = []
    percentages = []
    second_items_str = []
    second_percentages = []

    for item, count in counter.items():
        items_str.append(item)
        percentages.append(count / total)

    for second_item, second_count in second_counter.items():
        second_items_str.append(second_item)
        second_percentages.append(second_count / second_total)

    items_int = [list(map(int, item.split(':'))) for item in items_str]
    second_items_int = [list(map(int, item.split(':'))) for item in second_items_str]

    sorted_results = sorted(zip(items_int, percentages), key=lambda x: x[0])
    items_sorted, percentages_sorted = zip(*sorted_results)

    second_sorted_results = sorted(zip(second_items_int, second_percentages), key=lambda x: x[0])
    second_items_sorted, second_percentages_sorted = zip(*second_sorted_results)

    return [list(items_sorted), list(percentages_sorted)], [list(second_items_sorted), list(second_percentages_sorted)]

# 获取最新开奖结果
def fetch_latest_result():
    """获取最新开奖结果（含红球、蓝球、期号）"""
    url = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart=&dayEnd=&pageNo=1&pageSize=30&week=&systemType=PC"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            latest = data['result'][0]
            return {
                'red': [int(ball) for ball in latest['red'].split(',')],
                'blue': latest['blue'],
                'issue': latest['issue']
            }
        return None
    except Exception as e:
        print(f"获取开奖结果失败: {str(e)}")
        return None

# 生成红球号码
def generate_numbers(items_sorted, percentages_sorted, second_items_sorted, second_percentages_sorted):
    sections = [(1, 11), (12, 22), (23, 33)]
    ratios = random.choices(items_sorted, weights=percentages_sorted, k=1)[0]
    picked_numbers = []
    total_sum = 0
    odd_even_ratio = random.choices(second_items_sorted, weights=second_percentages_sorted, k=1)[0]
    required_odds, required_evens = odd_even_ratio
    
    total_sum_list = [(40, 149)]  # 简化总和范围
    total_sum_weights = [1]
    total_sum_result = random.choices(total_sum_list, weights=total_sum_weights, k=1)[0]
    start, end = total_sum_result
    
    attempt = 0
    while not (start <= total_sum <= end) or \
          len([num for num in picked_numbers if num % 2 != 0]) != required_odds or \
          len([num for num in picked_numbers if num % 2 == 0]) != required_evens:
        picked_numbers = []
        total_sum = 0
        if attempt == 500:
            break
        for ratio, section in zip(ratios, sections):
            for _ in range(ratio):
                candidates = []
                if len([num for num in picked_numbers if num % 2 != 0]) < required_odds:
                    candidates = [n for n in range(section[0], section[1]+1) if n % 2 != 0 and n not in picked_numbers]
                if not candidates:
                    candidates = [n for n in range(section[0], section[1]+1) if n % 2 == 0 and n not in picked_numbers]
                if candidates:
                    num = random.choice(candidates)
                    picked_numbers.append(num)
                    total_sum += num
        attempt += 1
    return picked_numbers, total_sum, ratios, odd_even_ratio

# 获取蓝球数据
def ssq_blue_data():
    url = "https://m.cz89.com/zst/ssq/lqzs.htm?pagesize=120"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tree = html.fromstring(response.text)
    interval_xpath = "/html/body/div[2]/div/div/div[2]/div[2]/table/tbody[1]/tr[{}]/td[11]"

    data = []
    for i in range(1, 121):
        path = interval_xpath.format(i)
        value = tree.xpath(path)
        if value:
            data.append(value[0].text_content().strip())

    counter = Counter(data)
    total = sum(counter.values())
    
    items_str = []
    percentages = []
    for item, count in counter.items():
        items_str.append(item)
        percentages.append(count / total)

    items_int = [list(map(int, item.split(':'))) for item in items_str]
    sorted_results = sorted(zip(items_int, percentages), key=lambda x: x[0])
    items_sorted, percentages_sorted = zip(*sorted_results)
    return [list(items_sorted), list(percentages_sorted)]

# 蓝球生成
def back_random_nums(blue_proportion, interval_weights):
    return random.choices(blue_proportion, weights=interval_weights, k=1)[0]

# 推送功能
def send_pushplus(content):
    token = os.getenv('PUSHPLUS_TOKEN')
    if not token:
        return
    url = 'https://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": "双色球预测结果",
        "content": content
    }
    requests.post(url, json=data)

def send_serverchan(content):
    token = os.getenv('SERVERCHAN_TOKEN')
    if not token:
        return
    url = f'https://sctapi.ftqq.com/{token}.send'
    data = {
        "title": "双色球预测结果",
        "desp": content
    }
    requests.post(url, data=data)

def send_dingding(content):
    webhook = os.getenv('DINGDING_WEBHOOK')
    if not webhook:
        return
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {"content": f"双色球预测结果：\n{content}"}
    }
    requests.post(webhook, headers=headers, json=data)

def send_feishu(content):
    webhook = os.getenv('FEISHU_WEBHOOK')
    if not webhook:
        return
    headers = {"Content-Type": "application/json"}
    data = {
        "msg_type": "text",
        "content": {"text": f"双色球预测结果：\n{content}"}
    }
    requests.post(webhook, headers=headers, json=data)

# 主程序
if __name__ == "__main__":
    # 初始化数据
    interval_data, parity_data = ssq_interval_parity_data()
    items_sorted, percentages_sorted = interval_data
    second_items_sorted, second_percentages_sorted = parity_data
    blue_proportion, interval_weights = ssq_blue_data()
    
    # 获取最新开奖结果
    latest_result = fetch_latest_result()  # 确保使用新函数名
    
    # 生成推送内容
    content = "双色球预测结果：\n\n"
    if latest_result:
        content += f"最新开奖：\n🔴 红球：{sorted(latest_result['red'])}\n🔵 蓝球：{latest_result['blue']}\n期号：{latest_result['issue']}\n\n"
    else:
        content += "⚠️ 最新开奖数据获取失败\n\n"
    
    # 生成预测结果
    count = 0
    while count < 10:
        try:
            back = back_random_nums([item[0] for item in blue_proportion], interval_weights)
            numbers, total_sum, ratios, odd_even_ratio = generate_numbers(
                items_sorted, percentages_sorted, 
                second_items_sorted, second_percentages_sorted
            )
            numbers_sorted = sorted(numbers)
            if len(set(numbers_sorted) & set(latest_result['red'])) == 1:
                line = f"第 {count+1} 组：\n红球：{numbers_sorted}\n蓝球：{back}\n"
                line += f"总和：{total_sum} | 奇偶比：{odd_even_ratio}\n"
                content += line + "\n"
                count += 1
        except Exception as e:
            print(f"生成出错：{str(e)}")
            continue
    
    content += "------\n预祝您中大奖！"
    
    # 发送推送
    send_pushplus(content)
    send_serverchan(content)
    send_dingding(content)
    send_feishu(content)

    # 发送推送
    send_pushplus(content)
    send_serverchan(content)
    send_dingding(content)
    send_feishu(content)
