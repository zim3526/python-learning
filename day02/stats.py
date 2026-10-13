scores = [59, 60, 61, 100, 0]
print(f"成绩列表：{scores}")
print(f"总人数：{len(scores)}")
num = 0
for i in scores:
    num += i

print(f"总分：{num}")
ave = num/len(scores)
print(f"平均分：{ave:.2f}")
big = scores[0]
small = scores[0]
num2 = 0
for s in scores:
    if big < s:  
        big = s
    if small > s:
        small = s
    if s >= 60:
        num2 += 1
print(f"最高分：{big}")
print(f"最低分：{small}")
print(f"及格人数：{num2}")

