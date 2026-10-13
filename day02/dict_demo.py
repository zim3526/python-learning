dict = {"张三": 80, "李四": 90, "王五": 70, "赵六": 60}
print(dict["张三"])
dict["吴七"] = 50
print(dict)
dict["张三"] = 85
for n,s in dict.items():
    print(f"{n}：{s}")
print(dict["钱八"])
