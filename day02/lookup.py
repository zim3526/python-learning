scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 60}
name = input("请输入要查询的姓名：")
if name in scores:
    print(f"{name}的成绩是{scores[name]}")
else:
    print("查无此人")
