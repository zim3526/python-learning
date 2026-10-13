height = float(input("请问你的身高是（米）："))
weight = float(input("请问你的体重是（公斤）："))
bmi = weight/(height*height)

if bmi<18.5:
    print(f"你的BMI是{bmi:.2f}偏瘦")
elif bmi<24:
    print(f"你的BMI是{bmi:.2f}正常")
elif bmi<28:
    print(f"你的BMI是{bmi:.2f}偏胖")
else:
    print(f"你的BMI是{bmi:.2f}肥胖")