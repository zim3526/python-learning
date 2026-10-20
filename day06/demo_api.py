# ===== 演示：用 Python 调用一个公开 API =====
# 运行：py D:\aistudy\day06\demo_api.py
# 这个 API 不需要 Key，纯粹用来理解"请求 → 响应"的流程

import requests

# ① URL：要访问的地址
url = "https://jsonplaceholder.typicode.com/todos/1"

print("=" * 60)
print("① 发出请求")
print("=" * 60)
print(f"  URL: {url}")
print(f"  方法: GET（读取数据）")

# ② 发请求（相当于"打电话"）
response = requests.get(url, timeout=10)

print()
print("=" * 60)
print("② 收到响应")
print("=" * 60)
print(f"  状态码: {response.status_code}    （200 = 成功）")
print(f"  数据类型: {response.headers.get('Content-Type')}")

print()
print("=" * 60)
print("③ 响应体（原始文本）")
print("=" * 60)
print(f"  {response.text}")

print()
print("=" * 60)
print("④ 解析成 Python 字典")
print("=" * 60)
data = response.json()          # 把 JSON 文本变成字典
print(f"  type(data) = {type(data)}")
print(f"  data        = {data}")
print()
print(f"  取字段：")
print(f"    data['title']     = {data['title']}")
print(f"    data['completed'] = {data['completed']}")

print()
print("=" * 60)
print("⑤ 状态码对照表")
print("=" * 60)
print("  200  成功")
print("  400  请求格式错")
print("  401  没权限（Key 错或没给）")
print("  402  余额不足")
print("  404  地址不存在")
print("  429  请求太频繁")
print("  500  服务器内部错误")
