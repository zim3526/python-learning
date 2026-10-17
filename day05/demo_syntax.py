# ===== 演示：values() / list() / 生成器表达式 =====
# 运行：py D:\aistudy\day05\demo_syntax.py

scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 45, "钱七": 66, "孙八": 100}
data = list(scores.values())

print("=" * 60)
print("【1】scores.values() 返回什么？")
print("=" * 60)
print(f"  type(scores.values())      = {type(scores.values())}")
print(f"  scores.values()            = {scores.values()}")
print(f"  list(scores.values())      = {list(scores.values())}")
print(f"  type(list(scores.values()))= {type(list(scores.values()))}")
print()
print("  能索引吗？")
try:
    print(f"  scores.values()[0] = {scores.values()[0]}")
except TypeError as e:
    print(f"  失败: {type(e).__name__}: {e}")
print("  → 所以视图不能索引，要用 list() 转成列表才能 data[0]")
print(f"  data[0] = {data[0]}  OK")

print()
print("=" * 60)
print("【2】视图是'实时'的，列表是'快照'")
print("=" * 60)
view = scores.values()
snapshot = list(scores.values())
scores["新同学"] = 88
print(f"  加了新同学后，视图 view     = {view}")
print(f"  加了新同学后，列表 snapshot = {snapshot}")
print("  → 视图跟着变，列表没变（它是拷贝）")
del scores["新同学"]
data = list(scores.values())

print()
print("=" * 60)
print("【3】is_pass 对每个分数的判定")
print("=" * 60)
for s in data:
    print(f"  {s:3d} 分 -> is_pass = {s >= 60}")
print(f"  → 一共 {sum(1 for s in data if s >= 60)} 个及格")

print()
print("=" * 60)
print("【4】生成器表达式到底产出了什么（逐个打印）")
print("=" * 60)

def is_pass(score):
    return score >= 60

gen = (1 for s in data if is_pass(s))
print(f"  生成器对象本身：{gen}")
print("  逐个取出（用 next() 一个一个拿）：")
try:
    while True:
        print(f"    next() = {next(gen)}")
except StopIteration:
    print("    取完了（StopIteration）")
print("  → 它产出了一串 1，数量正好等于及格人数")

print()
print("=" * 60)
print("【5】四种写法算同一个结果")
print("=" * 60)

# 写法一：传统 for 循环（最好懂）
count1 = 0
for s in data:
    if is_pass(s):
        count1 += 1
print(f"  for 循环            : {count1}")

# 写法二：生成器表达式（今天学的）
count2 = sum(1 for s in data if is_pass(s))
print(f"  生成器表达式        : {count2}")

# 写法三：列表推导式
count3 = sum([1 for s in data if is_pass(s)])
print(f"  列表推导式          : {count3}")

# 写法四：手动过滤后取长度
count4 = len([s for s in data if is_pass(s)])
print(f"  列表推导式 + len()  : {count4}")

print()
print("  四种写法结果一样，选你读得懂的那种。")

print()
print("=" * 60)
print("【6】另一个常见用法：生成器不只是产出 1")
print("=" * 60)
print(f"  所有分数的和          : {sum(s for s in data)}")
print(f"  所有及格的分数之和     : {sum(s for s in data if s >= 60)}")
print(f"  所有不及格的分数之和   : {sum(s for s in data if not is_pass(s))}")
print(f"  及格分数的个数         : {sum(1 for s in data if is_pass(s))}")
print("  → 产出 1 就是'计数'，产出 s 就是'求和'")
