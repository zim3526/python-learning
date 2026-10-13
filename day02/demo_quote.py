# 演示：f-string 里变量名加不加引号，区别巨大
# 运行：py D:\aistudy\day02\demo_quote.py

scores = {"张三": 85, "李四": 92}
name = "张三"          # 这是一个变量，它的值是字符串 "张三"

print("=" * 50)
print("正确写法：{scores[name]}   —— name 是变量，取它的值")
print("=" * 50)
print(f"{name}的成绩是{scores[name]}")
print()

print("=" * 50)
print("错误写法：{scores['name']}  —— 'name' 被当成字典的键")
print("=" * 50)
print("字典里所有的键是：", list(scores.keys()))
print("注意：里面没有 'name' 这个键！")
print()
print("所以下面这行会报 KeyError：")
print("    scores['name']")
print()

# 故意触发错误，让你看到报错的样子
print("现在执行错误写法，观察报错：")
print("-" * 50)
print(f"{name}的成绩是{scores['name']}")
