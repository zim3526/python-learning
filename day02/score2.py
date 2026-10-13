score = int(input("输入分数："))
while score<0 or score>100:
    print("分数必须在0到100之间，请重新输入")
    score = int(input("输入分数："))
if score >= 90:
    print("优秀")
elif score >=80:
    print("良好")
elif score >=60:
    print("及格")
else:
    print("不及格")