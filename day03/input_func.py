def get_number(prompt,low,high):
    while True:
        try:
            num = int(input(prompt))
            if low <= num <= high:
                return num
            print(f"请输入{low}到{high}之间的数字")
        except ValueError:
            print("请输入数字")

age = get_number("请输入年龄：", 0, 120)
score = get_number("请输入分数：", 0, 100)
count = get_number("请输入人数：", 1, 50)

print(f"年龄 {age}，分数 {score}，人数 {count}")